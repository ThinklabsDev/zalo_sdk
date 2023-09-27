"""
 @author tranvien98
 @email tranvanvien98bg@gmail.com
 @create date 2023-09-27 10:19:59
"""
import urllib
import requests
import datetime

from zalo_sdk import urls_patterns

from zalo_sdk import zalo_oa_exception


class BaseClient():
    def __init__(self, access_token, refresh_token, app_id, secret_key):
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._app_id = app_id
        self._secret_key = secret_key
        self._timeout = 15
        self._expire_at = 0

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, token):
        self._access_token = token

    @property
    def refresh_token(self):
        return self.access_token

    @refresh_token.setter
    def refresh_token(self, token):
        self._refresh_token = token

    def create_request_header(self, method: str, extra_headers: dict = None) -> dict:
        if extra_headers is None:
            extra_headers = {}
        if method == "POST":
            headers = {
                "Content-Type": "application/json",
                "access_token": self._access_token,
                **extra_headers
            }

        elif method == "GET":
            headers = {
                "access_token": self._access_token,
                **extra_headers
            }
        else:
            raise ValueError(f"Unknown method: {method}")
        return headers

    def send_request(self, method: str, url: str, body: dict = None, headers: dict = None, params: dict = None, ):
        """
        Send a request to Zalo, adding required tokens

        Params:
        :method: Either POST or GET
        :url: The Zalo endpoints to send the request
        :params: GET params to send with GET method
        :body: The body of POST request. If it is set in GET request, the body
               will be converted to JSON string and set the data param.
        :headers: Other HTTP headers to set with this request
        """
        if headers is None:
            headers = {}
        if params is None:
            params = {}
        if body is None:
            body = {}
        if self.is_access_token_expired():
            self.refresh_acccess_token()
        if method == "POST":
            responses = requests.post(
                url=url, params=params, headers=headers, json=body, timeout=self._timeout)
        elif method == "GET":
            responses = requests.get(
                url=url, params=params, headers=headers, timeout=self._timeout)
        else:
            raise ValueError(f"Unknown method: {method}")
        return responses

    def check_http_error(self, response: requests.Response):
        if response.status_code != 200:
            raise ValueError(
                f"HTTP Error {response.status_code}: {response.text}")

    def check_zalo_oa_error(self, response):
        if "error" in response and response["error"] != 0:
            if "message" in response:
                if response["error"] == -216 and "expired" in response["message"]:
                    raise zalo_oa_exception.ZaloOAAuthTokenExpiredException(
                        response["error"], response["message"])
                raise zalo_oa_exception.ZaloOAException(
                    response["error"], response["message"])
            raise zalo_oa_exception.ZaloOAException(response["error"])

    def request_authoriation_code_url(self, callback_url, code_challenge=None, state=None):
        """
        Get the URL to request the authorization code.

        Official Documentation:
        https://developers.zalo.me/docs/official-account/bat-dau/xac-thuc-va-uy-quyen-cho-ung-dung-new
        """
        parsed_url = urllib.parse.urlparse(urls_patterns.URL_AUTHOR_PERMISSION)
        params = {
            'app_id': self._app_id,
            'redirect_uri': callback_url,
        }
        if code_challenge is not None:
            params['code_challenge'] = code_challenge
        if state is not None:
            params['state'] = state

        auth_url = parsed_url._replace(query=urllib.parse.urlencode(params))
        return auth_url.geturl()

    def is_access_token_expired(self):
        return self._expire_at != 0 and self._expire_at < datetime.datetime.utcnow().timestamp()

    def check_and_set_token(self, zalo_response):
        # if 'refresh_token' not in zalo_response:
        #     raise zalo_sdk.ZaloException(-1,
        #                                  "'refresh_token' not found in the response")
        # if 'access_token' not in zalo_response:
        #     raise zalo_sdk.ZaloException(-1,
        #                                  "'access_token' not found in the response")

        expire_in = int(zalo_response.get("expires_in", 0))
        expire_at = datetime.datetime.now()+datetime.timedelta(seconds=expire_in)
        self._refresh_token = zalo_response['refresh_token']
        self._access_token = zalo_response['access_token']
        self._expire_at = int(expire_at.timestamp())

    def get_access_token_from_authorization_code(self, authorization_code: str, code_verifier: str):
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'secret_key': self._secret_key
        }
        body = {
            'code': authorization_code,
            'app_id': self._app_id,
            'grant_type': 'authorization_code',
            'code_verifier': code_verifier
        }

        response = requests.post(
            urls_patterns.URL_GET_ACCESS_TOKEN, data=body, headers=headers, timeout=self._timeout)
        self.check_http_error(response)
        zalo_response = response.json()
        self.check_zalo_oa_error(zalo_response)
        self.check_and_set_token(zalo_response)
        return self._access_token, self._refresh_token, self._expire_at

    def refresh_acccess_token(self):
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'secret_key': self._secret_key
        }
        body = {
            'refresh_token': self._refresh_token,
            'app_id': self._app_id,
            'grant_type': 'refresh_token'
        }

        response = requests.post(
            urls_patterns.URL_GET_ACCESS_TOKEN, data=body, headers=headers, timeout=self._timeout)
        self.check_http_error(response)
        zalo_response = response.json()
        self.check_zalo_oa_error(zalo_response)
        self.check_and_set_token(zalo_response)
        return self._access_token, self._refresh_token, self._expire_at
