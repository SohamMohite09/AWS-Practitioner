# ✈️ TravelGo — AWS Cloud Practitioner Project

**TravelGo** is a full-stack, cloud-powered travel and hotel booking web platform built with **Python (Flask)**, **AWS DynamoDB**, **Amazon SNS**, and deployed on **Amazon EC2** using **IAM roles**.

---

## 🌟 Key Features

- **Multi-Service Travel Hub**: Unified interface for booking **Buses**, **High-Speed Trains**, **Domestic Flights**, and **Hotels (Budget & Luxury)**.
- **Dynamic Seat Reservation**: Interactive seat picker map (01 to 24) with real-time selection feedback.
- **Serverless Cloud Persistence**: Built on **Amazon DynamoDB** with two main entities: `Users` (PK: `email`) and `Bookings` (PK: `booking_id`).
- **Real-Time SNS Email Alerts**: Automated email dispatch for successful bookings and cancellations via **Amazon SNS**.
- **Secure Architecture**: Password hashing with Werkzeug, server-side session management, and **AWS IAM instance profiles** on EC2 (zero hardcoded secrets).
- **Responsive UI/UX**: Clean, modern interface designed with vanilla CSS, accessible forms, and digital printable e-tickets / boarding passes.
- **Dual Offline / Online Mode**: Seamlessly works locally offline without AWS credentials, and automatically hooks into AWS services when deployed.

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| **Backend** | Python 3, Flask, Gunicorn |
| **Cloud Provider** | Amazon Web Services (AWS) |
| **Compute** | Amazon EC2 (Amazon Linux 2023 / Ubuntu) |
| **Database** | Amazon DynamoDB (NoSQL) |
| **Notifications** | Amazon SNS (Simple Notification Service) |
| **Security & Auth** | AWS IAM Roles, Werkzeug Password Hashing |
| **SDK** | AWS SDK for Python (`boto3`) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript, Jinja2 |

---

## 📊 Database Schema (DynamoDB)

### 1. Users Table (`travelgo-users`)
- **Partition Key**: `email` (String)
- **Attributes**: `email`, `name`, `password` (hashed), `logins` (number), `created_at`

### 2. Bookings Table (`travelgo-bookings`)
- **Partition Key**: `booking_id` (String, e.g. `TG-8A39F12B`)
- **Attributes**: `booking_id`, `email` (FK), `type` (bus/train/flight/hotel), `source`, `destination`, `date`, `seat`, `details`, `price`, `payment_method`, `payment_reference`, `status`, `created_at`

---

## 🚀 Quickstart (Local Development)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/SohamMohite09/AWS-Practitioner.git
   cd AWS-Practitioner
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\Activate.ps1
   # Linux / macOS:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**:
   ```bash
   cp .env.example .env
   ```

5. **Start Flask**:
   ```bash
   python app.py
   ```
   Open `http://127.0.0.1:5000` in your browser.

---

## ☁️ Deployment on AWS EC2

For complete step-by-step instructions on setting up DynamoDB tables, SNS topics, IAM Roles, Security Groups, and EC2, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md).

---

## 📄 License
MIT License. Built for AWS Cloud Practitioner Certification & Academic Demonstration.
