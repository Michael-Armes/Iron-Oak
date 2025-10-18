"""Account management, messaging, and billing models."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List

from .nutrition import NutritionTracker
from .workouts import WorkoutTracker


@dataclass
class Message:
    sender_id: str
    recipient_id: str
    body: str
    sent_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Invoice:
    invoice_id: str
    trainee_id: str
    trainer_id: str
    amount: float
    description: str
    issued_at: datetime = field(default_factory=datetime.utcnow)
    paid: bool = False

    def mark_paid(self) -> None:
        self.paid = True


@dataclass
class TraineeProfile:
    trainee_id: str
    name: str
    height_cm: float
    weight_kg: float
    resting_heart_rate: int
    workout_days_per_week: int
    tracker: WorkoutTracker
    nutrition: NutritionTracker
    wearable_metrics: Dict[str, float] = field(default_factory=dict)

    def bmi(self) -> float:
        height_m = self.height_cm / 100
        if height_m == 0:
            return 0.0
        return self.weight_kg / (height_m ** 2)

    def update_weight(self, weight_kg: float) -> None:
        self.weight_kg = weight_kg

    def update_wearable(self, metric: str, value: float) -> None:
        self.wearable_metrics[metric] = value


@dataclass
class TrainerProfile:
    trainer_id: str
    name: str
    trainees: Dict[str, TraineeProfile] = field(default_factory=dict)
    inbox: List[Message] = field(default_factory=list)
    invoices: Dict[str, Invoice] = field(default_factory=dict)

    def assign_trainee(self, trainee: TraineeProfile) -> None:
        self.trainees[trainee.trainee_id] = trainee

    def update_workout_plan(self, trainee_id: str, definition_name: str, suggested_sets: int, suggested_reps: int) -> None:
        trainee = self.trainees[trainee_id]
        definition = trainee.tracker.get_workout(definition_name)
        updated = type(definition)(
            name=definition.name,
            muscle_group=definition.muscle_group,
            category=definition.category,
            suggested_sets=suggested_sets,
            suggested_reps=suggested_reps,
            youtube_url=definition.youtube_url,
        )
        trainee.tracker.register_workout(updated)

    def update_macro_plan(self, trainee_id: str, calories: int, protein: int, carbs: int, fats: int) -> None:
        trainee = self.trainees[trainee_id]
        trainee.nutrition.target = type(trainee.nutrition.target)(
            calories=calories,
            protein=protein,
            carbs=carbs,
            fats=fats,
        )

    def send_message(self, trainee_id: str, body: str) -> Message:
        message = Message(sender_id=self.trainer_id, recipient_id=trainee_id, body=body)
        self.inbox.append(message)
        return message

    def issue_invoice(self, invoice: Invoice) -> None:
        self.invoices[invoice.invoice_id] = invoice


@dataclass
class AdminProfile:
    admin_id: str
    trainers: Dict[str, TrainerProfile] = field(default_factory=dict)

    def register_trainer(self, trainer: TrainerProfile) -> None:
        self.trainers[trainer.trainer_id] = trainer

    def list_all_trainees(self) -> List[TraineeProfile]:
        trainees: List[TraineeProfile] = []
        for trainer in self.trainers.values():
            trainees.extend(trainer.trainees.values())
        return trainees

    def billing_report(self) -> Dict[str, float]:
        total_invoiced = 0.0
        total_paid = 0.0
        for trainer in self.trainers.values():
            for invoice in trainer.invoices.values():
                total_invoiced += invoice.amount
                if invoice.paid:
                    total_paid += invoice.amount
        return {"total_invoiced": total_invoiced, "total_paid": total_paid}
