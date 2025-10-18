# Data Model Overview

## Core Entities

### User
- `id` (UUID)
- `role` (enum: trainee, trainer, admin)
- `email`, `password_hash`, `mfa_enabled`
- `first_name`, `last_name`, `date_of_birth`, `gender`
- `created_at`, `updated_at`, `last_login`
- Relationships:
  - One-to-one with **TraineeProfile** or **TrainerProfile** depending on role.
  - Many invoices via **Invoice**.

### TraineeProfile
- `user_id` (FK to User)
- `goal` (enum: strength, hypertrophy, endurance, weight_loss, maintenance)
- `height_cm`, `weight_kg`, `body_fat_pct`
- `resting_heart_rate`, `training_days_per_week`
- `primary_trainer_id`
- `wearable_connections` (JSONB metadata)
- Relationships:
  - Many **WorkoutPlanAssignments**, **WorkoutSession**, **NutritionLog**, **BodyMeasurement**, **MessageThread**.

### TrainerProfile
- `user_id`
- `certifications`, `bio`
- `hourly_rate`
- Relationships:
  - Many trainees, workout plans, nutrition plans, invoices.

### Workout
- Master catalog entry.
- `id`, `name`, `category` (strength, hypertrophy, cardio, mobility)
- `primary_muscle_group`, `secondary_muscle_groups[]`
- `equipment`
- `youtube_url`
- `default_sets`, `default_reps`, `tempo`, `rest_interval_sec`
- `created_by` (trainer/admin)

### WorkoutPlan & Assignment
- **WorkoutPlan**: template with metadata (`goal`, `experience_level`, `duration_weeks`).
- **WorkoutPlanAssignment**: join between trainee and plan with start/end dates.
- **WorkoutDay**: nested entity describing day-level schedule.
- **WorkoutBlock**: set of exercises, recommended sets/reps, effort guidance.

### WorkoutSession
- Logs trainee execution.
- `id`, `trainee_id`, `workout_id`, `date`, `perceived_exertion` (1-5).
- `sets` array with `{set_number, reps_target, reps_completed, weight_kg, distance_m, duration_sec}`.
- `personal_record` flag and value.
- `notes`.

### BodyMeasurement
- `id`, `trainee_id`, `recorded_at`.
- Metrics: `weight_kg`, `body_fat_pct`, `waist_cm`, `hip_cm`, `chest_cm`, `thigh_cm`, `bicep_cm`, `progress_photo_url`.

### NutritionPlan
- Macro targets (protein_g, carbs_g, fat_g, fiber_g), calorie target, hydration target.
- `adjustment_rules` (JSONB for training/rest day logic).

### NutritionLog
- `id`, `trainee_id`, `date`.
- `meals[]` containing foods with macros and calories.
- `total_calories`, `total_protein`, `total_carbs`, `total_fats`, `total_fiber`.
- `energy_expenditure` from workouts/wearables.

### WearableMetric
- `id`, `trainee_id`, `source` (Apple, Garmin, etc.), `metric_type` (heart_rate, hrv, steps, sleep, calorie_burn).
- `recorded_at`, `value`, `metadata`.

### MessageThread & Message
- `thread_id`, `participant_ids[]`.
- Messages include `sender_id`, `content`, `attachments`, `created_at`, `read_at`.

### Invoice & Payment
- **Invoice**: `id`, `issuer_id` (trainer/admin), `recipient_id`, `amount`, `currency`, `status`, `due_date`, `line_items[]`, `notes`.
- **Payment**: `id`, `invoice_id`, `processor`, `transaction_id`, `amount`, `paid_at`, `status`, `receipt_url`.

## Derived Views & Analytics
- **ReadinessScore** table storing daily aggregates (HRV trends, sleep quality, training load).
- **ComplianceMetrics** view summarizing completion rates of workouts and nutrition adherence.
- **RevenueDashboard** materialized view for admin finance monitoring.

## Data Governance
- Soft deletes for critical entities to preserve audit trails.
- Audit logs capturing before/after snapshots for plan changes and billing updates.
- GDPR-friendly data export and deletion workflows per user.
