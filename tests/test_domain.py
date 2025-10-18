from iron_oak import (
    AdminProfile,
    Invoice,
    MacroTarget,
    Message,
    NutritionEntry,
    NutritionTracker,
    TraineeProfile,
    TrainerProfile,
    WorkoutCategory,
    WorkoutDefinition,
    WorkoutSet,
    WorkoutTracker,
)


def create_sample_trainee(trainee_id: str = "trainee-1"):
    tracker = WorkoutTracker()
    tracker.register_workout(
        WorkoutDefinition(
            name="Back Squat",
            muscle_group="legs",
            category=WorkoutCategory.STRENGTH,
            suggested_sets=4,
            suggested_reps=8,
            youtube_url="https://youtube.com/example",
        )
    )
    tracker.register_workout(
        WorkoutDefinition(
            name="Rowing",
            muscle_group="full body",
            category=WorkoutCategory.CARDIO,
            suggested_sets=1,
            suggested_reps=10,
            youtube_url="https://youtube.com/example-row",
        )
    )
    nutrition = NutritionTracker(target=MacroTarget(calories=2400, protein=150, carbs=250, fats=70))
    return TraineeProfile(
        trainee_id=trainee_id,
        name="Alex",
        height_cm=180,
        weight_kg=82,
        resting_heart_rate=65,
        workout_days_per_week=4,
        tracker=tracker,
        nutrition=nutrition,
    )


def test_workout_logging_and_pr():
    trainee = create_sample_trainee()
    session = trainee.tracker.record_session(
        "Back Squat",
        [
            WorkoutSet(reps=8, weight=135, effort=6),
            WorkoutSet(reps=8, weight=140, effort=7),
            WorkoutSet(reps=6, weight=150, effort=8),
        ],
    )
    assert session.total_volume() == (8 * 135) + (8 * 140) + (6 * 150)
    assert trainee.tracker.personal_record("back squat") == 150
    recommendation = trainee.tracker.recommend_rest("back squat", activity_level="moderate")
    assert "rest" in recommendation.lower() or "balanced" in recommendation.lower()


def test_nutrition_analytics_and_insights():
    trainee = create_sample_trainee()
    trainee.nutrition.log_entry(NutritionEntry(calories_in=2500, calories_out=400, protein=160, carbs=260, fats=70))
    trainee.nutrition.log_entry(NutritionEntry(calories_in=2300, calories_out=500, protein=150, carbs=240, fats=65))
    totals = trainee.nutrition.totals()
    assert totals["net_calories"] == (2500 + 2300) - (400 + 500)
    balance = trainee.nutrition.macro_balance()
    assert balance is not None
    insights = trainee.nutrition.optimization_insights(bmi=trainee.bmi(), resting_hr=trainee.resting_heart_rate, workout_days=trainee.workout_days_per_week)
    assert "calories" in insights and "cardio" in insights and "protein" in insights


def test_trainer_can_manage_plans_and_billing():
    trainee = create_sample_trainee()
    trainer = TrainerProfile(trainer_id="trainer-1", name="Jordan")
    trainer.assign_trainee(trainee)
    trainer.update_workout_plan(trainee.trainee_id, "back squat", suggested_sets=5, suggested_reps=5)
    updated = trainee.tracker.get_workout("back squat")
    assert updated.suggested_sets == 5 and updated.suggested_reps == 5

    trainer.update_macro_plan(trainee.trainee_id, calories=2200, protein=180, carbs=200, fats=70)
    assert trainee.nutrition.target.calories == 2200
    assert trainee.nutrition.target.protein == 180

    message = trainer.send_message(trainee.trainee_id, "Great progress!")
    assert isinstance(message, Message)
    assert trainer.inbox[-1].body == "Great progress!"

    invoice = Invoice(invoice_id="inv-1", trainee_id=trainee.trainee_id, trainer_id=trainer.trainer_id, amount=120.0, description="Monthly coaching")
    trainer.issue_invoice(invoice)
    assert trainer.invoices["inv-1"].amount == 120.0


def test_admin_reporting():
    admin = AdminProfile(admin_id="admin")
    trainer = TrainerProfile(trainer_id="trainer-1", name="Jordan")
    trainee_a = create_sample_trainee("trainee-a")
    trainee_b = create_sample_trainee("trainee-b")
    trainer.assign_trainee(trainee_a)
    trainer.assign_trainee(trainee_b)
    admin.register_trainer(trainer)

    invoice_a = Invoice(invoice_id="inv-a", trainee_id="trainee-a", trainer_id="trainer-1", amount=200.0, description="Training")
    invoice_b = Invoice(invoice_id="inv-b", trainee_id="trainee-b", trainer_id="trainer-1", amount=180.0, description="Nutrition")
    trainer.issue_invoice(invoice_a)
    trainer.issue_invoice(invoice_b)
    invoice_b.mark_paid()

    trainees = admin.list_all_trainees()
    assert {trainee.trainee_id for trainee in trainees} == {"trainee-a", "trainee-b"}
    report = admin.billing_report()
    assert report["total_invoiced"] == 380.0
    assert report["total_paid"] == 180.0
