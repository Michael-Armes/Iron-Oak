# Functional Requirements

## User Roles
- **Trainee** – Fitness app user focusing on training and nutrition adherence.
- **Trainer** – Professional coach who manages trainees' plans, communicates, and handles billing.
- **Administrator** – Organization staff with full control over accounts, compliance, and financial operations.

## Trainee Experience
1. **Onboarding & Profile**
   - Capture goals (strength, hypertrophy, endurance, weight loss), preferred training days, rest heart rate, body measurements, and wearable device connections.
   - Calculate BMI and recommended caloric intake based on biometrics.
2. **Workout Management**
   - Workout library with filtering by muscle group, movement pattern, equipment, and training focus (strength, hypertrophy, endurance, mobility, cardio).
   - For each workout:
     - Suggested sets, reps, tempo, rest intervals, and intensity guidelines.
     - Editable input fields for actual sets/reps/weight/time/distance.
     - Personal record tracking per exercise and session history.
     - Effort perception slider (1–5).
     - Embedded or linked demonstration video (YouTube).
     - Targeted muscle groups and training intent (cardio vs muscle growth, etc.).
   - Automated recommendations for rest days or alternative cardio sessions based on weekly load, recovery, and goals.
3. **Progress Tracking**
   - Body measurement logs (weight, body fat %, circumference, photos) with historical charts.
   - Wearable data ingestion (heart rate, steps, sleep, HRV) with analytics.
   - Dashboard summarizing training adherence, PR streaks, and readiness indicators.
4. **Nutrition Tracking**
   - Daily calorie intake logging via barcode scanning/manual entry, with macro breakdown (protein, carbs, fats, fiber).
   - Calorie expenditure estimation from workouts and wearables.
   - Macro and calorie targets generated from BMI, resting heart rate, goals, and weekly workout schedule.
   - Optimization insights (e.g., adjust carbs on training days).
5. **Communication**
   - Secure messaging with assigned trainer.
   - Push/email reminders for workouts, nutrition, and scheduled check-ins.
6. **Billing**
   - View invoices, payment history, and subscription status.

## Trainer Experience
1. **Client Management**
   - Dashboard listing trainees with compliance, readiness, and risk indicators.
   - Ability to view/edit trainee profiles, goals, and wearable data summaries.
2. **Programming Tools**
   - Create and assign workout plans, adjust sets/reps, customize effort guidance, and attach new video links.
   - Modify nutrition plans and macro targets; push updates to trainee dashboards.
   - Schedule rest days, deload weeks, and cardio recommendations.
3. **Analytics & Reporting**
   - Review trainee progress: body composition trends, PRs, training load vs recovery, calorie balance.
   - Export reports or share summaries with trainees.
4. **Communication**
   - Two-way messaging, group broadcasts, and ability to tag workouts or meals for feedback.
5. **Billing Management**
   - Generate invoices, track payment status, apply discounts, and log services rendered.

## Administrator Capabilities
1. **Account Management**
   - CRUD for all users, role assignments, and permissions.
   - Monitor authentication logs and enforce security policies (MFA, password resets).
2. **Operational Oversight**
   - Access to all dashboards with read/write privileges.
   - System configuration: workout template libraries, macro calculation defaults, wearable API credentials.
3. **Billing & Compliance**
   - Oversee invoices, payments, refunds, and revenue reporting.
   - Manage integrations with payment gateways and accounting software.
   - Audit trails for trainer interactions and data changes.

## Non-Functional Requirements
- **Security**: Role-based access control, encrypted data at rest/in transit, HIPAA-compliant data handling where applicable.
- **Scalability**: Support thousands of concurrent trainees, real-time syncing with multiple wearable platforms.
- **Availability**: Target 99.5% uptime with regional redundancy.
- **Performance**: Workout and nutrition dashboards should load within 2 seconds under normal load.
- **Privacy**: Trainees control data sharing with trainers; consent management for wearable integrations.
- **Extensibility**: Modular architecture to add new wearable providers, workout content, or nutrition databases.
