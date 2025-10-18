# System Architecture

## Overview
Iron Oak will be delivered as a cloud-native platform composed of modular services with a shared identity and data layer. The ecosystem includes:
- **Mobile & Web Clients**: React Native mobile app and React web portal backed by a GraphQL API for rich data interactions, with offline caching for workout logging.
- **API Gateway & BFF**: A gateway that handles authentication, rate limiting, and request routing to backend services. A "Backend-for-Frontend" service adapts responses for trainee, trainer, and admin clients.
- **Microservices**:
  - **Workout Service**: Manages exercise catalog, workout templates, personalized plans, personal records, and effort metrics.
  - **Nutrition Service**: Handles food database, macro targets, meal logging, and caloric analytics.
  - **Analytics Service**: Aggregates wearable data, calculates readiness scores, recommends rest/cardio, and runs ML models for optimization suggestions.
  - **Messaging Service**: Provides real-time chat, notifications, and scheduled reminders.
  - **Billing Service**: Interfaces with payment processors (Stripe) for invoicing, subscriptions, refunds, and transaction tracking.
  - **Account Service**: Central user management, role provisioning, and audit logging.
- **Data Layer**: PostgreSQL for relational data, TimescaleDB extensions for time-series metrics, Redis for caching sessions and leaderboard data, and S3-compatible storage for progress photos.
- **Integrations**:
  - Wearable providers (Apple HealthKit, Google Fit, Garmin) via OAuth and webhook updates.
  - YouTube Data API for workout video metadata.
  - Third-party nutrition databases (e.g., USDA, FatSecret).
  - Payment gateway webhooks for billing reconciliation.

## Authentication & Authorization
- OAuth2 + OpenID Connect for user login; support for social sign-in and email/password.
- Multi-factor authentication for trainers and admins.
- Role-based access control enforced at the API Gateway and within services using policy-as-code (e.g., OPA).

## Data Flow Example
1. Trainee logs a workout in the mobile app.
2. BFF validates the request, enriches with user profile data, and forwards to the Workout Service.
3. Workout Service stores the session, updates personal records, and publishes events to a message bus (Kafka).
4. Analytics Service consumes the event, recalculates readiness, and triggers notifications if rest is recommended.
5. Trainer dashboard updates via GraphQL subscriptions and WebSocket channels.

## Observability & Ops
- Centralized logging (ELK stack), distributed tracing (OpenTelemetry + Jaeger), and metrics (Prometheus + Grafana).
- CI/CD pipelines with automated testing, schema migrations, and deployment via Kubernetes.
- Feature flagging (LaunchDarkly) for gradual rollout of new modules.

## Security Considerations
- Encrypt sensitive data with KMS-managed keys.
- Regular penetration testing and vulnerability scanning.
- Data retention policies for photos, biometrics, and payment info following compliance standards.
