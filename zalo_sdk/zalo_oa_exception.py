
"""
 @author tranvien98
 @email tranvanvien98bg@gmail.com
 @create date 2023-09-27 09:54:13
"""

from zalo_sdk.zalo_exception import ZaloException


class ZaloOAException(ZaloException):
    """
    Zalo Official Account specific exception.

    Official document for the error codes:
    https://developers.zalo.me/docs/official-account/phu-luc/ma-loi
    """
    ERROR_CODE_TO_STR = {
        0: "Success",
        -32: "Your application reached limit call api",
        -201: "	<data_field> is invalid!",
        -204: "Offical Account is disable",
        -205: "Offical Account is not exist",
        -209: "Not supported this api",
        -210: "Parameter exceeds allowable limit",
        -211: "Out of quota",
        -212: "App has not registed this api",
        -213: "	User has not followed OA",
        -214: "Article is being processed",
        -216: "Access token is invalid",
        -217: "User has blocked invitation from OA",
        -218: "Out of quota receive",
        -221: "The OA needs to be verified to use this feature",
        -224: "The OA needs to upgrade OA Tier Package to use this feature",
        -227: "User is banned or has been inactive for more than 45 days",
        -230: "user has not interacted with the OA in the past 7 days",
        -232: "user has not interacted with the OA",
        -233: "Message type is invalid or not support",
        -234: "This message cannot be sent at night (10:00PM - 6:00AM)",
        -235: "This API does not support this type of OA",
        -240: "MessageV2 API has been shut down, please switch to MessageV3",
        -320: "Your app needs to connect with Zalo Cloud Account to use paid features",
        -321: "Zalo Cloud Account associated with this app is out of money or unable to be charged"
    }

    def __init__(self, code, custom_message=None):
        super(ZaloOAException).__init__(code, custom_message)
        self._msg = f"Zalo OA error ({self._code}) [{self.err_code_to_str()}]"
        if custom_message is not None:
            self._msg += f": {custom_message}"

    def err_code_to_str(self) -> str:
        if self._code in ZaloOAException.ERROR_CODE_TO_STR:
            return ZaloOAException.ERROR_CODE_TO_STR[self._code]

        return "Unknown error"


class ZaloOAAuthTokenExpiredException(ZaloOAException):
    """
    Auth token expired expcetion. When we get this exception, we should
    refresh the auth token to get a new one.
    """
