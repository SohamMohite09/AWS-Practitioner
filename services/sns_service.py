"""
Amazon Simple Notification Service (SNS) Service
Handles real-time email notifications for Booking Confirmations and Cancellations.
"""

import logging
from config import Config

logger = logging.getLogger(__name__)

class SNSService:
    def __init__(self):
        self.region = Config.AWS_REGION
        self.topic_arn = Config.SNS_TOPIC_ARN
        self.sns_client = None
        self._init_sns()

    def _init_sns(self):
        """Initialize boto3 SNS client."""
        if self.topic_arn:
            try:
                import boto3
                self.sns_client = boto3.client("sns", region_name=self.region)
                logger.info("SNS client initialized for topic: %s", self.topic_arn)
            except Exception as e:
                logger.warning("Could not initialize boto3 SNS client: %s", e)
                self.sns_client = None

    def send_booking_confirmation(self, booking):
        """
        Publishes a formatted booking confirmation message to the SNS topic.
        """
        subject = f"✈️ TravelGo Booking Confirmed — #{booking.get('booking_id')}"
        message = (
            f"Hello {booking.get('email')},\n\n"
            f"Your TravelGo reservation has been successfully confirmed!\n\n"
            f"--------------------------------------------------\n"
            f"Booking ID:        {booking.get('booking_id')}\n"
            f"Service Type:      {booking.get('type', '').upper()}\n"
            f"Details:           {booking.get('details', 'N/A')}\n"
            f"Route / Location:  {booking.get('source')} -> {booking.get('destination')}\n"
            f"Travel Date:       {booking.get('date')}\n"
            f"Seat / Room:       {booking.get('seat')}\n"
            f"Total Amount:      ₹{booking.get('price')}\n"
            f"Payment Method:    {booking.get('payment_method')}\n"
            f"Payment Ref:       {booking.get('payment_reference')}\n"
            f"Status:            {booking.get('status', 'CONFIRMED')}\n"
            f"--------------------------------------------------\n\n"
            f"Thank you for choosing TravelGo!\n"
            f"Have a safe and comfortable journey.\n\n"
            f"— The TravelGo Team (Powered by AWS)"
        )
        return self._publish(subject, message)

    def send_cancellation_notification(self, booking):
        """
        Publishes a cancellation notification to the SNS topic.
        """
        subject = f"❌ TravelGo Booking Cancelled — #{booking.get('booking_id')}"
        message = (
            f"Hello {booking.get('email')},\n\n"
            f"This is to inform you that your booking #{booking.get('booking_id')} has been successfully cancelled.\n\n"
            f"--------------------------------------------------\n"
            f"Booking ID:        {booking.get('booking_id')}\n"
            f"Service Type:      {booking.get('type', '').upper()}\n"
            f"Details:           {booking.get('details')}\n"
            f"Amount Refundable: ₹{booking.get('price')}\n"
            f"Status:            CANCELLED\n"
            f"--------------------------------------------------\n\n"
            f"If you did not request this cancellation, please contact support.\n\n"
            f"— The TravelGo Team (Powered by AWS)"
        )
        return self._publish(subject, message)

    def _publish(self, subject, message):
        """Internal helper to publish a message via SNS."""
        if not self.topic_arn or not self.sns_client:
            logger.info("[SNS SIMULATION] Subject: %s\nMessage: %s", subject, message)
            return True, "Simulated (SNS Topic ARN not configured or running in local mode)"

        try:
            response = self.sns_client.publish(
                TopicArn=self.topic_arn,
                Subject=subject[:100],  # AWS SNS subjects have a 100 character limit
                Message=message
            )
            message_id = response.get("MessageId")
            logger.info("SNS published successfully. MessageId: %s", message_id)
            return True, message_id
        except Exception as e:
            logger.error("Failed to publish SNS message: %s", e)
            return False, str(e)

# Singleton SNS instance
sns_service = SNSService()
