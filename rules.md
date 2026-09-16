# TravelGo — Claude Code Rules

These rules are mandatory for Claude Code while working on this repository.

## 1. Source of Truth

Primary project requirements come from the supplied SkillWallet TravelGo project specification.

Do not silently replace project requirements with a different architecture.

If the specification is ambiguous:
1. identify the ambiguity,
2. choose the simplest reasonable implementation,
3. document the assumption,
4. ask for approval when the decision could materially change the architecture.

## 2. AWS Safety

NEVER:
- create an AWS account
- request the user to enter payment information
- hard-code AWS access keys
- commit `.env` files containing credentials
- delete AWS resources without explicit approval
- create expensive AWS infrastructure unnecessarily

The project specification states that a temporary AWS account will be provided through Troven.

Before any AWS resource creation, clearly state:
- what resource will be created
- why it is needed
- expected cost/free-tier considerations if known
- what permissions are required

## 3. Credentials

Never write credentials into:
- Python source files
- HTML
- JavaScript
- Git history
- README files
- screenshots

Use environment/configuration mechanisms.

On EC2, prefer the assigned IAM instance role instead of static credentials.

## 4. Git Rules

Before major changes:
```bash
git status
git diff
```

After a coherent working feature:
```bash
git add .
git commit -m "descriptive message"
```

Do not create meaningless commits such as:
- update
- changes
- fix stuff

Use descriptive commits such as:
```text
feat: add DynamoDB user repository
feat: add booking workflow
feat: integrate SNS booking notifications
fix: prevent duplicate booking submission
```

Never force-push or rewrite Git history unless explicitly instructed.

## 5. Existing Code

Before modifying code:
1. inspect the repository
2. understand the current structure
3. search for existing implementations
4. reuse existing utilities when appropriate

Do not overwrite an existing feature simply because another implementation is easier.

## 6. Dependency Rules

Do not add a package unless it has a clear purpose.

Prefer:
- Flask
- boto3
- Werkzeug/Flask-supported security utilities
- python-dotenv if environment configuration needs it

Avoid adding large frameworks or libraries without justification.

After dependency changes:
- update `requirements.txt`
- verify installation
- test the application

## 7. Flask Rules

- Use application configuration rather than scattered constants.
- Protect authenticated routes.
- Validate incoming form data.
- Do not store plaintext passwords.
- Use appropriate HTTP methods.
- Do not trust client-provided user identity for booking ownership.
- Obtain the authenticated user's identity from the server-side session.
- Avoid exposing internal AWS errors directly to users.

## 8. DynamoDB Rules

The supplied model is:

### Users
```text
email = PK
name
password
logins
```

### Bookings
```text
booking_id = PK
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

Do not change primary keys casually.

When changing the schema:
- explain why
- check all dependent code
- update documentation
- test existing workflows

## 9. Booking Integrity

A booking must belong to the authenticated user.

For cancellation:
- verify the booking exists
- verify the booking belongs to the logged-in user
- verify it is cancellable
- update its state consistently

Do not trust:
```text
?email=someone@example.com
```
as proof of ownership.

## 10. SNS Rules

SNS should be triggered only after the relevant database operation succeeds.

Avoid duplicate notifications caused by repeated requests.

Keep SNS logic isolated in a service/helper.

## 11. Frontend Rules

- Keep UI responsive.
- Do not introduce a frontend framework unless explicitly required.
- Use accessible form labels and buttons.
- Give clear validation/error messages.
- Keep JavaScript focused on interactive behavior.
- Do not put AWS credentials or AWS SDK secrets in browser code.

## 12. Testing Rules

After implementing a feature, test:
- happy path
- invalid input
- unauthenticated access
- ownership/security checks
- database failure handling where practical

At minimum verify:
```text
Register -> Login -> Search -> Book -> Dashboard -> Cancel
```

## 13. Debugging Rules

When an error occurs:
1. reproduce it
2. inspect the traceback
3. identify the root cause
4. make the smallest appropriate fix
5. rerun the failing workflow
6. check for regressions

Do not repeatedly patch symptoms without identifying the root cause.

## 14. Code Style

Prefer simple, readable Python.

Do not generate unnecessary abstractions.

Do not create:
- unused classes
- unused services
- speculative APIs
- unnecessary design patterns

The project should remain understandable to a student who must explain it in a viva.

## 15. Documentation

Update documentation when:
- architecture changes
- AWS configuration changes
- environment variables change
- database schema changes
- deployment procedure changes

## 16. Agent Behavior

Before a large implementation:
- inspect
- plan
- explain
- implement in small steps
- test
- commit

Do not make large destructive changes in one operation.

When unsure, stop and explain the uncertainty rather than inventing requirements.
