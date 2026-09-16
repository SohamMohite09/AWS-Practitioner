# TravelGo — Product Requirements Document

## 1. Project Overview

TravelGo is a full-stack, cloud-based travel booking platform for reserving buses, trains, flights, and hotels through a unified interface.

The application uses:
- Flask for the backend
- HTML/CSS/JavaScript and Flask templates for the web interface
- AWS DynamoDB for persistent user and booking data
- AWS SNS for booking/cancellation email notifications
- AWS EC2 for deployment
- boto3 for AWS integration
- IAM for controlled AWS permissions

The project is being implemented according to the SkillWallet AWS Cloud Practitioner project specification.

## 2. Primary Goal

Build a functional demonstration of a unified travel booking platform that supports:
1. User registration and login
2. Travel/accommodation search
3. Bus, train, flight, and hotel booking workflows
4. Dynamic seat selection for transportation
5. Hotel filtering
6. Booking summaries
7. Centralized cancellation
8. User travel history/dashboard
9. SNS-based booking notifications
10. Deployment of the Flask application on EC2

## 3. Important Project Constraints

- Do NOT create a personal AWS account.
- The SkillWallet material states that a temporary AWS account will be provided through Troven.
- Do NOT create AWS resources until the relevant project phase explicitly requires them.
- Keep AWS configuration externalized; never hard-code credentials.
- Prefer a simple, understandable implementation suitable for an academic project.
- Do not introduce unnecessary frameworks or services.
- Do not replace DynamoDB with SQL databases.
- Do not replace Flask with another backend framework.
- Do not add real-world travel-provider APIs unless explicitly requested.
- Sample/mock travel inventory is acceptable unless the project instructions later require a real API.

## 4. Target Users

### Traveler
A traveler should be able to:
- register
- log in
- search available travel/accommodation options
- select a transportation seat where applicable
- select/filter hotels
- make a booking
- view booking details
- receive notifications
- cancel eligible bookings
- view booking history

### Administrator/Service Provider

SNS may also notify an administrator or service provider about transactions where required. This does not require a separate admin dashboard unless explicitly requested.

## 5. Core Data Model

The provided project specification defines two primary entities.

### Users

Primary key:
- `email`

Attributes:
- `email`
- `name`
- `password`
- `logins`

The password must be stored securely as a password hash, not as plaintext.

### Bookings

Primary key:
- `booking_id`

Attributes:
- `booking_id`
- `email`
- `type`
- `source`
- `destination`
- `date`
- `seat`
- `details`
- `price`
- `payment_method`
- `payment_reference`

`email` associates a booking with its user.

## 6. Functional Requirements

### Authentication
- Registration page
- Login page
- Logout
- Session-based authentication
- Protected dashboard/booking routes
- Password hashing

### Search
Support search/filtering for:
- Bus
- Train
- Flight
- Hotel

Transportation search should support at minimum:
- source
- destination
- date

Hotel search/filtering should support the project requirements, including categories such as:
- budget
- luxury

### Booking
- Display selected travel/hotel details
- Allow required seat selection for transportation
- Collect booking/payment-method information as required by the project
- Generate a unique booking ID
- Store the booking in DynamoDB
- Show a booking confirmation/summary

### Cancellation
- Show eligible bookings
- Allow cancellation
- Update booking status/record consistently
- Trigger notification after successful cancellation

### Dashboard
Display:
- upcoming bookings
- past bookings
- booking type
- date
- price
- booking details
- cancellation option where applicable

### Notifications
After a successful booking:
1. Persist the booking.
2. Trigger SNS.
3. SNS sends the configured email notification.

After a successful cancellation:
1. Persist the cancellation state.
2. Trigger the appropriate SNS notification.

## 7. Non-Functional Requirements

### Security
- Never commit AWS credentials.
- Use IAM roles on EC2.
- Use environment variables/configuration for non-secret settings.
- Hash passwords.
- Validate user input.
- Use secure session configuration where appropriate.

### Maintainability
- Separate routes, services, AWS/database access, templates, and static assets where practical.
- Keep functions small and understandable.
- Add comments only where they clarify non-obvious logic.
- Prefer readable code over clever abstractions.

### Cloud
The target deployment architecture is:
Browser -> EC2 -> Flask -> DynamoDB/SNS

## 8. Acceptance Criteria

The project is acceptable when:
- A user can register and log in.
- User data is stored in DynamoDB.
- A logged-in user can search supported travel/hotel inventory.
- A user can create a booking.
- Booking data is stored in DynamoDB.
- A booking confirmation is displayed.
- SNS notification is triggered after successful booking when SNS is configured.
- A user can view booking history.
- A user can cancel an eligible booking.
- Cancellation state is persisted.
- SNS notification is triggered after successful cancellation when SNS is configured.
- Flask can be deployed and run on EC2.
- EC2 can access DynamoDB/SNS through an appropriate IAM role.

## 9. Definition of Done

A feature is not considered complete merely because code was written.

For each feature:
1. Implement it.
2. Run the application.
3. Test the relevant workflow.
4. Fix errors.
5. Verify data/state changes.
6. Review security implications.
7. Update documentation if needed.
8. Commit the working change to Git.

