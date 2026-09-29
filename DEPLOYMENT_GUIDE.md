# TravelGo — Step-by-Step AWS Deployment & Setup Guide

This guide walks you through the entire end-to-end process of setting up and deploying **TravelGo** on AWS for your **AWS Cloud Practitioner** project.

---

## 🏗️ Architecture Overview

```text
                        +----------------------+
                        |     User Browser     |
                        | (HTML/CSS/JavaScript)|
                        +----------+-----------+
                                   |
                                   | HTTP Port 80 / 5000
                                   v
                        +----------------------+
                        |     AWS EC2 (Linux)  |
                        |   Flask Application  |
                        +----------+-----------+
                                   |
                                   | (EC2 IAM Role)
                        +----------+----------+
                        |                     |
                        v                     v
               +----------------+    +----------------+
               |  AWS DynamoDB  |    |    AWS SNS     |
               |  Users Table   |    | Notifications  |
               | Bookings Table |    +-------+--------+
               +----------------+            |
                                             v
                                        User Email
```

---

## Step 1: Local Setup and Verification

1. **Activate Virtual Environment & Install Dependencies**:
   ```bash
   python -m venv venv
   # On Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   # On Mac/Linux:
   source venv/bin/activate

   pip install -r requirements.txt
   ```

2. **Run Application Locally**:
   ```bash
   python app.py
   ```
   Open `http://127.0.0.1:5000` in your web browser.

> [!NOTE]
> The application includes a smart **Local Store Fallback** (`USE_LOCAL_MOCK_DB=auto`), meaning it works seamlessly offline for testing even if AWS credentials are not yet configured!

---

## Step 2: AWS DynamoDB Setup

You need **two tables** in DynamoDB:

### Table 1: `travelgo-users`
- **Table Name**: `travelgo-users`
- **Partition Key (PK)**: `email` (Type: `String`)
- **Table class**: DynamoDB Standard
- **Read/Write Capacity**: On-demand (Pay per request)

### Table 2: `travelgo-bookings`
- **Table Name**: `travelgo-bookings`
- **Partition Key (PK)**: `booking_id` (Type: `String`)
- **Table class**: DynamoDB Standard
- **Read/Write Capacity**: On-demand (Pay per request)

*(Optional Automated Way)*:
If you have AWS CLI / credentials configured locally, simply run:
```bash
python scripts/setup_aws_resources.py --region us-east-1 --email your_email@example.com
```

---

## Step 3: Amazon SNS Setup

1. Go to the **Amazon SNS Console** -> **Topics** -> **Create topic**.
2. **Type**: `Standard`.
3. **Name**: `travelgo-booking-notifications`.
4. Click **Create topic** and copy the **Topic ARN** (e.g. `arn:aws:sns:us-east-1:123456789012:travelgo-booking-notifications`).
5. Click **Create subscription**:
   - **Protocol**: `Email`
   - **Endpoint**: Enter your email address.
6. Check your inbox and click **"Confirm subscription"** in the AWS email.

---

## Step 4: IAM Role for EC2

Create an IAM Role so EC2 can communicate with DynamoDB and SNS without hardcoding any access keys!

1. Go to **IAM Console** -> **Roles** -> **Create role**.
2. **Trusted entity type**: `AWS service` -> Select `EC2`.
3. **Permissions policies**:
   - Attach `AmazonDynamoDBFullAccess` (or custom policy for `travelgo-users` & `travelgo-bookings`).
   - Attach `AmazonSNSFullAccess` (or custom policy for `travelgo-booking-notifications`).
4. **Role name**: `TravelGo-EC2-Role`.
5. Click **Create role**.

---

## Step 5: Launch EC2 Instance

1. Go to **EC2 Console** -> **Launch Instances**.
2. **Name**: `TravelGo-Server`.
3. **AMI**: `Amazon Linux 2023 AMI` or `Ubuntu 22.04 LTS`.
4. **Instance Type**: `t2.micro` or `t3.micro` (Free Tier eligible).
5. **Key pair**: Create or choose an existing `.pem` key pair for SSH access.
6. **Network settings (Security Group)**:
   - Allow **SSH** (Port 22) from `Anywhere` or `My IP`.
   - Allow **HTTP** (Port 80) from `Anywhere (0.0.0.0/0)`.
   - Allow **Custom TCP** (Port 5000) from `Anywhere (0.0.0.0/0)`.
7. **Advanced Details**:
   - Under **IAM instance profile**, select `TravelGo-EC2-Role`.
8. Click **Launch Instance**.

---

## Step 6: Deploy TravelGo on EC2

1. **Connect to your EC2 instance via SSH**:
   ```bash
   ssh -i your-key.pem ec2-user@<EC2-PUBLIC-IP>
   ```

2. **Clone the repository**:
   ```bash
   git clone https://github.com/SohamMohite09/AWS-Practitioner.git TravelGo
   cd TravelGo
   ```

3. **Configure `.env` file**:
   ```bash
   cp .env.example .env
   nano .env
   ```
   Set:
   ```ini
   FLASK_SECRET_KEY=your-production-secret-key
   AWS_REGION=us-east-1
   DYNAMODB_USERS_TABLE=travelgo-users
   DYNAMODB_BOOKINGS_TABLE=travelgo-bookings
   SNS_TOPIC_ARN=arn:aws:sns:us-east-1:xxxxxx:travelgo-booking-notifications
   USE_LOCAL_MOCK_DB=False
   ```

4. **Run the Automated Setup Script**:
   ```bash
   chmod +x deploy/ec2_setup.sh
   ./deploy/ec2_setup.sh
   ```

5. **Verify the Application**:
   Open your browser and navigate to:
   `http://<EC2-PUBLIC-IP>` or `http://<EC2-PUBLIC-IP>:5000`

---

## Step 7: Testing the Complete Workflow

1. **Register**: Create an account with a new email and password.
2. **Login**: Sign in with registered credentials.
3. **Search**: Search for Buses, Trains, Flights, or Hotels.
4. **Seat Selection**: Pick a seat on the interactive seat layout.
5. **Confirm Booking**: Complete the reservation.
6. **Check SNS Email**: Look for the real-time booking confirmation email in your inbox.
7. **Dashboard**: View your reservation, login count, and status in the dashboard.
8. **Cancel**: Cancel the reservation and verify the cancellation SNS notification.
