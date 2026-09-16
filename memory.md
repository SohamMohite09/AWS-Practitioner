# TravelGo — Claude Code Project Memory

This file is the persistent working memory for the TravelGo repository.

Claude Code should read this file before continuing substantial work and update it when important project state changes.

## 1. Project Identity

Project:
TravelGo — A Cloud-Powered Real-Time Travel Booking Platform Using AWS

Academic/project context:
AWS Cloud Practitioner / SkillWallet project.

## 2. Technology Stack

Backend:
- Python
- Flask

AWS:
- EC2
- DynamoDB
- SNS
- IAM

AWS SDK:
- boto3

Frontend:
- HTML
- CSS
- JavaScript
- Flask/Jinja templates

Version control:
- Git

## 3. Required AWS Services

```text
EC2      -> hosts Flask application
DynamoDB -> stores users and bookings
SNS      -> sends booking/cancellation notifications
IAM      -> controls EC2 AWS permissions
```

## 4. Current Architecture

```text
Browser
   |
   v
Flask on EC2
   |
   +--> DynamoDB
   |
   +--> SNS
```

## 5. Database Contract

### Users

PK:
```text
email
```

Fields:
```text
email
name
password
logins
```

### Bookings

PK:
```text
booking_id
```

Fields:
```text
booking_id
email
type
source
destination
date
seat
details
price
payment_method
payment_reference
```

Relationship:
```text
One User -> Many Bookings
```

## 6. Project Requirements

Core workflows:
- registration
- login
- logout
- travel search
- hotel filtering
- seat selection
- booking
- confirmation
- dashboard
- cancellation
- SNS notification

## 7. AWS Account Constraint

IMPORTANT:

The supplied SkillWallet specification says the material is for understanding only and instructs the learner not to create an AWS account because a temporary account will be provided through Troven.

Never create a personal AWS account as part of this project.

## 8. Current Phase

Update this section after each completed phase.

Current phase:
```text
Phase 0 — Repository Preparation
```

Current status:
```text
Not started / update this after work begins
```

## 9. Completed Work

Update this list chronologically.

```text
- Project specification reviewed
- Project documentation files created
```

## 10. Active Work

Write the current task here.

```text
No active implementation task recorded yet.
```

## 11. Known Decisions

- Use Flask.
- Use boto3 for AWS integration.
- Use DynamoDB rather than a relational database.
- Use SNS for notifications.
- Deploy Flask on EC2.
- Keep the implementation simple enough for academic explanation.
- Do not create unnecessary external travel API integrations unless explicitly required.

## 12. Known Assumptions

- Travel inventory can initially be represented by application/sample data unless later SkillWallet instructions explicitly require a real travel-provider API.
- Payment fields are part of the specified booking schema; a real payment gateway is not specified in the supplied material.
- The provided ER description specifies Users and Bookings as the primary data entities.

## 13. Environment Variables

Document variable NAMES here, never actual secret values.

Example:

```text
FLASK_SECRET_KEY=
AWS_REGION=
DYNAMODB_USERS_TABLE=
DYNAMODB_BOOKINGS_TABLE=
SNS_TOPIC_ARN=
```

Never place real credentials in this file.

## 14. Important Security Notes

- Passwords must be hashed.
- AWS credentials must never be committed.
- `.env` should be ignored by Git.
- EC2 should use an IAM role.
- Booking ownership must be checked server-side.
- Client-side email/user IDs must not be trusted for authorization.

## 15. Testing Checklist

```text
[ ] Flask starts locally
[ ] Registration works
[ ] Login works
[ ] Logout works
[ ] DynamoDB Users works
[ ] Travel search works
[ ] Hotel filtering works
[ ] Seat selection works
[ ] Booking creation works
[ ] Booking appears in dashboard
[ ] Cancellation works
[ ] SNS booking notification works
[ ] SNS cancellation notification works
[ ] IAM permissions work
[ ] EC2 deployment works
[ ] Application accessible remotely
```

## 16. How Claude Should Update This File

When a major task is completed:
1. update Current Phase
2. update Current Status
3. add completed work
4. record important architecture/schema decisions
5. record unresolved issues
6. update testing checklist

Do not put credentials, tokens, passwords, or private keys into this file.

## 17. Handoff Rule

If Claude Code starts a new session:
1. read `prd.md`
2. read `architecture.md`
3. read `rules.md`
4. read `phases.md`
5. read `design.md`
6. read `memory.md`
7. inspect the current Git status
8. inspect the current repository before making changes

Then continue from the recorded current phase instead of rebuilding existing work.
