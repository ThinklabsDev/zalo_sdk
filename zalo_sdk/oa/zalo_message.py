"""
 @author tranvien98
 @email tranvanvien98bg@gmail.com
 @create date 2023-09-27 15:36:59
"""
import enum


class ZaloMessage:
    def __init__(self, recipient=None, message_body=None, action=None):
        """
        Parameters:
        recipients (ZaloRecipient): Recipients of the message
        message_body (ZaloMessageBody): Message body
        action (ZaloAction): send an action (e.g. emoji react)
        """
        self.msg = {}
        self.msg["recipient"] = recipient
        self.msg["message"] = message_body
        self.msg["sender_action"] = action

    def to_dict(self) -> dict:
        return {k: v.to_dict() for k, v in dict(filter(lambda pair: pair[1] is not None, self.msg.items())).items()}


class ZaloPayloadType(enum.Enum):
    file = enum.auto()
    template = enum.auto()


class ZaloTemplateType(enum.Enum):
    media = enum.auto()
    list = enum.auto()
    request_user_info = enum.auto()


class ZaloAttachment:
    def __init__(self, payload_type: str, payload: dict = None):
        self.payload_type = payload_type
        self.payload = payload

    def toDict(self) -> dict:
        return {
            "type": self.payload_type,
            "payload": self.payload
        }


class ZaloMessageBody:
    def __init__(self, text: str = None, attachment: ZaloAttachment = None, quote_message_id: str = None):
        self.body = {}
        self.body["text"] = text
        self.body["attachment"] = attachment
        self.body["quote_message_id"] = quote_message_id

    def to_dict(self) -> dict:
        return {k: v if isinstance(v, str) else v.to_dict() for k, v in dict(filter(lambda pair: pair[1] is not None, self.body.items())).items()}


class ZaloRecipient:
    def __init__(self, message_id=None, user_id=None, target=None):
        """
        Define a list of recipients. If more than one param is provided, only one is used.
        The priority order is
        """
        self.user_id = user_id
        self.message_id = message_id
        self.target = target

    def to_dict(self) -> dict:
        """
        Convert the object to dict. If there is more than one parameter set, only
        one parameter is use. The priority is
        message_id > user_id > target
        """

        if self.message_id is not None:
            return {"message_id": self.message_id}
        if self.user_id is not None:
            return {"user_id": self.user_id}
        if self.target is not None:
            return {"target": self.target}
        return {}
