# TravelGo — Implementation Phases

This document converts the SkillWallet project flow into an execution plan for Claude Code.

## Phase 0 — Repository Preparation

### Goal
Create a safe development baseline.

Tasks:
- inspect repository
- initialize/verify Git
- create `.gitignore`
- create Python virtual environment
- create `requirements.txt`
- create basic Flask application
- create README
- verify Flask runs locally

Deliverable:
```text
Browser -> Local Flask application
```

Commit:
```text
chore: initialize TravelGo project
```

---

# Epic 1 — Backend Development and Application Setup

Source requirement:
- Develop backend using Flask
- Integrate AWS services using boto3

### Tasks

1. Build Flask application.
2. Create base template/layout.
3. Create initial routes.
4. Create configuration layer.
5. Add boto3 dependency.
6. Create AWS service abstraction.
7. Prepare DynamoDB/SNS integration points.
8. Add registration/login foundation.
9. Verify local application.

### Acceptance Test

```text
Start Flask
   ↓
Open browser
   ↓
Home page loads
   ↓
Navigation works
```

---

# Epic 2 — AWS Account Setup

### Goal
Use the provided AWS environment.

IMPORTANT:
The supplied specification says a temporary AWS account will be provided through Troven.

Do not create a personal AWS account.

Tasks:
- log into provided AWS console
- identify region
- verify access
- record required non-secret configuration

Do not create resources that belong to later Epics unless necessary.

---

# Epic 3 — DynamoDB Database Creation and Setup

### Goal
Create persistent storage.

### Users table

Primary key:
```text
email
```

Attributes:
```text
email
name
password
logins
```

### Bookings table

Primary key:
```text
booking_id
```

Attributes:
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

### Tasks

1. Create Users table.
2. Create Bookings table.
3. Verify table availability.
4. Implement boto3 access.
5. Implement user creation.
6. Implement user lookup.
7. Implement booking creation.
8. Implement booking retrieval.
9. Implement booking ownership filtering.
10. Test CRUD operations needed by the application.

### Acceptance Test

```text
Register
  ↓
DynamoDB Users

Create booking
  ↓
DynamoDB Bookings

Dashboard
  ↓
Retrieve user's bookings
```

---

# Epic 4 — SNS Notification Setup

### Goal
Send real-time email notifications.

Tasks:
1. Create SNS topic for booking notifications.
2. Configure email subscription.
3. Confirm subscription where required by AWS.
4. Implement boto3 SNS publishing.
5. Trigger notification after successful booking.
6. Trigger notification after successful cancellation.
7. Test notification behavior.

### Important

Database persistence must succeed before reporting the booking as successful.

Do not send a successful-booking notification for a failed database write.

---

# Epic 5 — IAM Role Setup

### Goal
Give EC2 controlled access to AWS resources.

Tasks:
1. Create IAM role for EC2.
2. Attach policies required for:
   - DynamoDB operations used by TravelGo
   - SNS publishing used by TravelGo
3. Attach the role to EC2.

Prefer least privilege.

Do not use AdministratorAccess for the application merely for convenience.

---

# Epic 6 — EC2 Instance Setup

### Goal
Prepare the server.

Tasks:
1. Launch EC2 using the provided AWS environment.
2. Select appropriate instance configuration.
3. Configure security group.
4. Allow HTTP access.
5. Allow SSH access only as needed.
6. Connect to the instance.
7. Install required runtime dependencies.
8. Verify Python/Flask environment.

---

# Epic 7 — Deployment Using EC2

### Goal
Run TravelGo on EC2.

Tasks:
1. Upload/clone project files.
2. Install dependencies.
3. Configure environment variables.
4. Verify IAM role access.
5. Verify DynamoDB access.
6. Verify SNS access.
7. Run Flask application.
8. Use an appropriate production server configuration where required.
9. Verify external browser access.

### Target

```text
Internet
   ↓
EC2
   ↓
Flask
   ├── DynamoDB
   └── SNS
```

---

# Epic 8 — Testing and Deployment

### Functional Tests

Test:
- registration
- login
- logout
- search
- bus booking
- train booking
- flight booking
- hotel booking
- seat selection
- hotel filtering
- dashboard
- booking history
- cancellation
- SNS confirmation
- SNS cancellation

### Security Tests

Verify:
- unauthenticated users cannot access protected pages
- users cannot cancel another user's booking
- passwords are hashed
- credentials are not committed
- AWS permissions are appropriate

### Deployment Tests

Verify:
- EC2 application starts
- Flask pages load
- DynamoDB operations work
- SNS operations work
- application remains functional after restart

---

# Final Phase — Documentation and Conclusion

Prepare:
- architecture explanation
- database explanation
- AWS service explanation
- screenshots
- testing evidence
- deployment evidence
- conclusion

The final explanation should be understandable enough for an academic demonstration/viva.

## Recommended Git Milestones

```text
1. chore: initialize TravelGo project
2. feat: add Flask application structure
3. feat: add authentication
4. feat: integrate DynamoDB
5. feat: add travel and hotel booking workflows
6. feat: add user dashboard and cancellation
7. feat: integrate SNS notifications
8. chore: configure IAM deployment
9. chore: deploy TravelGo to EC2
10. test: verify end-to-end TravelGo workflows
11. docs: finalize project documentation
```
