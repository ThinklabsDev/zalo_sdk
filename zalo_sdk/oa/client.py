"""
 @author tranvien98
 @email tranvanvien98bg@gmail.com
 @create date 2023-09-27 11:55:15
"""
from zalo_sdk.base_client import BaseClient
from zalo_sdk.oa.zalo_message import ZaloMessage
from zalo_sdk import urls_patterns


class Client(BaseClient):
    def __init__(self, app_id, secret_key, access_token="", refresh_token=""):
        super().__init__(app_id=app_id, secret_key=secret_key,
                         access_token=access_token, refresh_token=refresh_token)

    def create_request_body(self, recipient, body=None, action=None):
        msg_obj = ZaloMessage(
            recipient=recipient,
            message_body=body,
            action=action
        )
        return msg_obj.to_dict()

    def send_message(self, recipient, body=None, action=None, category="consultant"):
        if category == "consultant":
            url = urls_patterns.URL_SEND_MESSAGE_CONSULTANT
        else:
            raise ValueError("Invalid message category provided.")

        msg_header = self.create_request_header(method="POST")
        msg_body = self.create_request_body(recipient, body, action)

        response = self.send_request(
            method="POST", url=url, body=msg_body, headers=msg_header)
        return self._validate_zalo_response(response)

    def get_free_response_quota(self, message_id):
        headers = self.create_request_header(method="POST")
        body = {
            "message_id": message_id
        }
        response = self.send_request(
            method="POST", url=urls_patterns.URL_GET_FREE_RESPONSE_QUOTA, body=body, headers=headers)
        return self._validate_zalo_response(response)

    def get_profile(self, user_id):
        headers = self.create_request_header(method="GET")
        params = {
            "user_id": user_id
        }
        response = self.send_request(
            method="GET", url=urls_patterns.URL_GET_PROFILE, body=params, headers=headers
        )
        return self._validate_zalo_response(response)

    def _validate_zalo_response(self, response):
        self.check_http_error(response)
        zalo_response = response.json()
        self.check_zalo_oa_error(zalo_response)
        return zalo_response
