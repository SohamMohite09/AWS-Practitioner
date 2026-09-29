"""
AWS Resource Provisioning Script
Automatically creates required DynamoDB tables and SNS topic for TravelGo.
Usage: python scripts/setup_aws_resources.py [--region us-east-1] [--email your_email@example.com]
"""

import sys
import argparse
import boto3
from botocore.exceptions import ClientError

def create_dynamodb_tables(dynamodb, region):
    print(f"\n[1/3] Setting up DynamoDB Tables in {region}...")

    # 1. Users Table (PK: email)
    users_table_name = "travelgo-users"
    try:
        table = dynamodb.create_table(
            TableName=users_table_name,
            KeySchema=[{"AttributeName": "email", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "email", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST"
        )
        print(f"  ⏳ Creating table '{users_table_name}'...")
        table.wait_until_exists()
        print(f"  ✅ Table '{users_table_name}' created successfully (PK: email [String]).")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            print(f"  ℹ️ Table '{users_table_name}' already exists.")
        else:
            print(f"  ❌ Error creating '{users_table_name}': {e}")

    # 2. Bookings Table (PK: booking_id)
    bookings_table_name = "travelgo-bookings"
    try:
        table = dynamodb.create_table(
            TableName=bookings_table_name,
            KeySchema=[{"AttributeName": "booking_id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "booking_id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST"
        )
        print(f"  ⏳ Creating table '{bookings_table_name}'...")
        table.wait_until_exists()
        print(f"  ✅ Table '{bookings_table_name}' created successfully (PK: booking_id [String]).")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            print(f"  ℹ️ Table '{bookings_table_name}' already exists.")
        else:
            print(f"  ❌ Error creating '{bookings_table_name}': {e}")

def create_sns_topic(sns_client, subscribe_email=None):
    print("\n[2/3] Setting up Amazon SNS Topic...")
    topic_name = "travelgo-booking-notifications"
    try:
        response = sns_client.create_topic(Name=topic_name)
        topic_arn = response.get("TopicArn")
        print(f"  ✅ SNS Topic created: {topic_arn}")

        if subscribe_email:
            print(f"  📬 Subscribing email '{subscribe_email}' to SNS notifications...")
            sub_resp = sns_client.subscribe(
                TopicArn=topic_arn,
                Protocol="email",
                Endpoint=subscribe_email
            )
            print(f"  ✅ Subscription request sent! Please check '{subscribe_email}' and click Confirm.")
        
        return topic_arn
    except ClientError as e:
        print(f"  ❌ Error creating SNS topic: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Provision TravelGo AWS Resources")
    parser.add_argument("--region", default="us-east-1", help="AWS Region (default: us-east-1)")
    parser.add_argument("--email", default=None, help="Email address to receive booking SNS notifications")
    args = parser.parse_args()

    print("=" * 60)
    print("🚀 TravelGo AWS Resource Provisioning (AWS Practitioner)")
    print("=" * 60)

    try:
        dynamodb = boto3.resource("dynamodb", region_name=args.region)
        sns_client = boto3.client("sns", region_name=args.region)
    except Exception as e:
        print(f"❌ Failed to initialize boto3 clients: {e}")
        print("Please ensure AWS credentials or IAM role are configured.")
        sys.exit(1)

    create_dynamodb_tables(dynamodb, args.region)
    topic_arn = create_sns_topic(sns_client, args.email)

    print("\n[3/3] Configuration Summary:")
    print("=" * 60)
    print(f"AWS_REGION={args.region}")
    print("DYNAMODB_USERS_TABLE=travelgo-users")
    print("DYNAMODB_BOOKINGS_TABLE=travelgo-bookings")
    if topic_arn:
        print(f"SNS_TOPIC_ARN={topic_arn}")
    print("USE_LOCAL_MOCK_DB=False")
    print("=" * 60)
    print("✅ AWS Resources are ready for TravelGo deployment!\n")

if __name__ == "__main__":
    main()
