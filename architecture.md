# TravelGo — Architecture

## 1. High-Level Architecture

```text
                         +----------------------+
                         |      User Browser    |
                         | HTML/CSS/JS          |
                         +----------+-----------+
                                    |
                                    | HTTP/HTTPS
                                    v
                         +----------------------+
                         |      AWS EC2         |
                         |  Flask Application   |
                         +----------+-----------+
                                    |
                         +----------+----------+
                         |                     |
                         v                     v
                +----------------+    +----------------+
                |   DynamoDB     |    |      SNS       |
                | Users          |    | Notifications  |
                | Bookings       |    +-------+--------+
                +----------------+            |
                                              v
                                            Email
```

## 2. Application Layers

### Presentation Layer
Technology:
- HTML
- CSS
- JavaScript
- Jinja2/Flask templates

Responsibilities:
- forms
- navigation
- search UI
- seat selection UI
- hotel filters
- booking summaries
- dashboard
- cancellation UI

### Application Layer

Flask routes/controllers handle:
- authentication requests
- searches
- booking requests
- cancellation requests
- dashboard requests

Business logic should not be unnecessarily embedded inside templates.

### Data/Cloud Layer

Use boto3 to communicate with:
- DynamoDB
- SNS

The AWS access mechanism should depend on the environment:
- local development: configured AWS credentials/profile if permitted
- EC2: IAM instance role

Never hard-code access keys.

## 3. DynamoDB Model

The SkillWallet specification defines two primary entities.

### Users Table

Partition key:
```text
email (String)
```

Attributes:
```text
email
name
password
logins
```

### Bookings Table

Partition key:
```text
booking_id (String)
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

The logical relationship is:

```text
Users
  |
  | 1
  |
  | many
  v
Bookings
```

A booking belongs to one user through `email`.

## 4. Booking Flow

```text
User
 |
 | Search
 v
Flask
 |
 | Display options
 v
User selects option
 |
 | Submit booking
 v
Flask validation
 |
 +----> Generate booking_id
 |
 +----> Save booking in DynamoDB
 |
 +----> Publish SNS notification
 |
 v
Booking confirmation
```

Important ordering:
- A booking should not be reported as successfully confirmed until persistence succeeds.
- Notification failure should be handled separately from database persistence and should not silently create duplicate bookings.

## 5. Cancellation Flow

```text
User Dashboard
      |
      | Cancel
      v
Flask
      |
      | Validate ownership/eligibility
      v
DynamoDB
      |
      | Update cancellation state
      v
SNS
      |
      v
Email notification
```

## 6. Authentication Flow

```text
Registration
    |
    v
Validate input
    |
    v
Hash password
    |
    v
DynamoDB Users
```

```text
Login
  |
  v
Find user by email
  |
  v
Verify password hash
  |
  v
Create Flask session
  |
  v
Protected application
```

## 7. Recommended Flask Structure

```text
TravelGo/
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── routes/
│   ├── auth.py
│   ├── travel.py
│   ├── booking.py
│   └── dashboard.py
│
├── services/
│   ├── dynamodb_service.py
│   ├── sns_service.py
│   └── booking_service.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── search.html
│   ├── booking.html
│   ├── confirmation.html
│   └── dashboard.html
│
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

This is a recommended structure, not a requirement to over-engineer the project. A smaller structure is acceptable if it remains clean.

## 8. AWS Architecture by Phase

### Development
```text
Local PC
  |
  v
Flask
  |
  +--> DynamoDB
  +--> SNS
```

### Deployment
```text
Internet
   |
   v
EC2 Security Group
   |
   v
Flask Application
   |
   +--> DynamoDB
   |
   +--> SNS
```

### IAM

EC2 should receive an IAM role containing only the permissions needed by the application.

Avoid attaching broad administrator permissions to the application role.

## 9. Architectural Principles

- Keep Flask responsible for web/application behavior.
- Keep AWS calls in service/data-access functions rather than scattering boto3 calls everywhere.
- Keep credentials out of source code.
- Keep the data model aligned with the supplied specification.
- Avoid adding infrastructure that the project does not require.
- Prefer deterministic, testable booking operations.
