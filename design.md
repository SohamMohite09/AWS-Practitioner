# TravelGo — UI/UX Design Specification

## 1. Design Objective

TravelGo should feel like a simple travel-booking website rather than an AWS administration interface.

The interface should prioritize:
- clarity
- simple navigation
- fast booking flow
- readable information
- responsive layout
- clear booking status

Do not over-design the application with unnecessary animations or complex frontend frameworks.

## 2. Main Navigation

Recommended navigation:

```text
TravelGo
-----------------------------------------------
Home | Bus | Train | Flight | Hotels | My Bookings | Login
```

For authenticated users:

```text
TravelGo
-----------------------------------------------
Home | Search | My Bookings | Profile | Logout
```

## 3. Home Page

Recommended structure:

```text
+---------------------------------------------+
|                   TravelGo                  |
|                                             |
|       Plan your journey with ease           |
|                                             |
| [Bus] [Train] [Flight] [Hotels]             |
|                                             |
| From: __________  To: __________             |
| Date: __________                             |
|                                             |
|               [ Search ]                    |
+---------------------------------------------+
```

## 4. Search Results

Each result should clearly show:

```text
Operator / Hotel Name
--------------------------------
Source -> Destination
Date
Departure / Arrival
Price
Availability
[Select]
```

For hotels:

```text
Hotel Name
--------------------------------
Location
Category: Budget / Luxury
Rating
Amenities
Price per night
[View / Book]
```

## 5. Transportation Seat Selection

For buses/trains/flights where seat selection is applicable:

```text
Select Your Seat

[01] [02] [03] [04]
[05] [06] [07] [08]
[09] [10] [11] [12]

Available
Selected
Unavailable

Selected seat: 06

[Continue]
```

Use JavaScript only for client-side interaction.

The server must still validate the booking request.

## 6. Hotel Filters

Recommended filters:

```text
Hotel Filters
---------------------
[ ] Budget
[ ] Luxury

Price:
[ minimum ] - [ maximum ]

[ Apply Filters ]
```

Do not rely exclusively on client-side filtering if the dataset is sensitive or large. The server should enforce important business rules.

## 7. Booking Page

Show a clear summary:

```text
Booking Summary
--------------------------------
Type: Flight
From: Hyderabad
To: Bangalore
Date: 20/09/2026
Seat: 12A
Details: Flight TG101
Price: ₹4250

Payment Method:
(o) UPI
( ) Card
( ) Other

[ Confirm Booking ]
```

For a real payment gateway, do not implement fake payment processing as if money was actually transferred unless explicitly required. The project can store the requested payment method/reference fields for demonstration.

## 8. Confirmation Page

```text
Booking Confirmed!

Booking ID: TG-XXXXXXXX

Your booking has been successfully recorded.

A notification has been sent to your registered email
when SNS is configured.

[View My Bookings]
[Back to Home]
```

## 9. Dashboard

Recommended sections:

```text
My Bookings

Upcoming
--------------------------------
Flight | Hyderabad -> Bangalore
20 Sep | ₹4250
Booking ID: TG12345
[View] [Cancel]

Past
--------------------------------
Hotel | Chennai
10 Aug | ₹2500
Booking ID: TG67890
Status: Completed
```

## 10. Cancellation

Cancellation should require a clear confirmation:

```text
Cancel Booking?

Booking ID: TG12345
Travel: Hyderabad -> Bangalore
Date: 20 Sep 2026
Price: ₹4250

[Keep Booking] [Confirm Cancellation]
```

After cancellation:

```text
Booking Cancelled

Your booking has been cancelled successfully.
A notification will be sent when SNS is configured.
```

## 11. Login Page

```text
Welcome Back

Email
[________________]

Password
[________________]

[ Login ]

Don't have an account?
[ Register ]
```

## 12. Registration Page

```text
Create Account

Name
[________________]

Email
[________________]

Password
[________________]

[ Register ]
```

## 13. Visual Guidelines

Use:
- consistent spacing
- readable typography
- clear buttons
- cards for travel/hotel results
- responsive layouts
- consistent status indicators

Avoid:
- excessive gradients
- excessive animations
- huge JavaScript bundles
- unnecessary UI libraries
- cluttered pages

## 14. Responsive Design

The application should work on:
- desktop
- tablet
- mobile

Use CSS flexbox/grid and responsive media queries.

## 15. Error States

Every important workflow should have clear errors.

Examples:
```text
Invalid email or password.
Please enter a source and destination.
No travel options found.
This seat is no longer available.
Booking could not be completed.
You are not authorized to cancel this booking.
Notification could not be sent.
```

Do not display raw Python tracebacks or AWS exception details to end users.

## 16. Accessibility

Use:
- `<label>` for form controls
- semantic buttons
- sufficient text contrast
- keyboard-friendly forms
- descriptive error messages

## 17. Design Principle

The UI should communicate the complete flow:

```text
Search
  ↓
Choose
  ↓
Review
  ↓
Book
  ↓
Confirm
  ↓
Manage
```
