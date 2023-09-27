from zalo_sdk.oa.client import Client
from zalo_sdk.oa.zalo_message import ZaloRecipient, ZaloMessageBody

from . import ZaloSendMessage


class ZaloSendRequestBody(ZaloSendMessage):

    def test_send_text_message_body(self):
        recipient = ZaloRecipient(user_id=self.user_id)
        message_body = ZaloMessageBody(text="Hello, world!")

        client = Client(self.app_id, self.secret_key,
                        self.access_token, self.refresh_token)

        # Call the send_message function and assert the response
        generated_body = client.create_request_body(
            recipient=recipient, body=message_body)

        expected_body = {
            "recipient": {
                "user_id": self.user_id
            },
            "message": {
                "text": "Hello, world!"
            }
        }

        self.assertEqual(generated_body, expected_body)

    def test_send_long_text_message_body(self):
        recipient = ZaloRecipient(user_id=self.user_id)
        message_body = ZaloMessageBody(text="""
            Hello 👋,

            Welcome to our store! 🛍️

            We have a special promotion going on right now! 🎉

            📣 Don't miss out on these amazing deals:
            1. 50% OFF on all items 🎁
            2. Buy 2, Get 1 Free 🎈
            3. Free Shipping on orders over $50 🚚

            🔥 Hurry up and shop now before the offer ends!

            💬 Need help or have any questions? Feel free to reach out to our customer support team. 
			We're here to assist you 24/7.

            📞 Call us at +1 (800) 123-4567 or send us a message through our website.

            Thank you for choosing us. We hope you have a wonderful shopping experience!

            Best regards,
            Your Store Team 🛒

            """
                                       )

        client = Client(self.app_id, self.secret_key,
                        self.access_token, self.refresh_token)

        # Call the send_message function and assert the response
        generated_body = client.create_request_body(
            recipient=recipient, body=message_body)

        expected_body = {
            "recipient": {
                "user_id": self.user_id
            },
            "message": {
                "text":
                """
            Hello 👋,

            Welcome to our store! 🛍️

            We have a special promotion going on right now! 🎉

            📣 Don't miss out on these amazing deals:
            1. 50% OFF on all items 🎁
            2. Buy 2, Get 1 Free 🎈
            3. Free Shipping on orders over $50 🚚

            🔥 Hurry up and shop now before the offer ends!

            💬 Need help or have any questions? Feel free to reach out to our customer support team. 
			We're here to assist you 24/7.

            📞 Call us at +1 (800) 123-4567 or send us a message through our website.

            Thank you for choosing us. We hope you have a wonderful shopping experience!

            Best regards,
            Your Store Team 🛒

            """
            }
        }
        self.assertEqual(generated_body, expected_body)
