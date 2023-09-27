## Luồng hoạt động màn trò chuyện
### 1 Lấy các đoạn hội thoại


Khi bắt đầu vào

Khung số 1 sẽ gọi api Message>get all conversation: {{host}}/{{route_api}}/chatbot/65027a8dde6f97a2dddf50ef/conversations

65027a8dde6f97a2dddf50ef: id_chatbot

để lấy tất cả đoạn hội thoại
Hiển thị thông tin name_conversation

### 2 Chat

Bắt đầu chat sẽ gọi websocket ws://{host}/socket/chatbot/65027a8dde6f97a2dddf50ef

Gửi request dạng json

{
    "type": "question",
    "token": "",
    "is_conversation_exists": false,
    "id_conversation": "",
    "text": "Thời tiết hôm nay như thế "
}

trong đó is_conversation_exists: true khi đoạn hội thoại đã tồn tại
id_conversation: cho trường hợp đoạn hội thoại đã tồn tại

+ response đầu tiên sẽ là: 
{
    "sender": "system",
    "text": "",
    "type": "conversation_information",
    "id_conversation": "64f05d57827d9a05f51c8590"
}
Khi nhận thông tin này sẽ refresh lại bảng 1 ở hình đầu tiên để lấy thông tin cuộc hội thoại mới

+ Các response tiếp theo là câu trả lời

{
    "sender": "bot",
    "text": "T",
    "type": "stream",
    "is_end": false
}

đoạn chat kết thúc khi giá trị is_end là true

{
    "sender": "bot",
    "text": "T\u00f4i kh\u00f4ng bi\u1ebft \u0111\u1ecba \u0111i\u1ec3m c\u1ee7a b\u1ea1n n\u00ean kh\u00f4ng th\u1ec3 cung c\u1ea5p th\u00f4ng tin v\u1ec1 th\u1eddi ti\u1ebft h\u00f4m nay. B\u1ea1n c\u00f3 th\u1ec3 cho t\u00f4i bi\u1ebft \u0111\u1ecba \u0111i\u1ec3m c\u1ee7a b\u1ea1n \u0111\u1ec3 t\u00f4i c\u00f3 th\u1ec3 cung c\u1ea5p th\u00f4ng tin ch\u00ednh x\u00e1c h\u01a1n kh\u00f4ng?",
    "type": "stream",
    "is_end": true
}

### 3 Chat với đoạn hội thoại đã có sẵn:
Sử dụng api get one conversation khi người dùng click vào 1 đoạn hội thoại

{{host}}/{{route_api}}/conversations/650bf21afbe4545ab2dc961a

Lệnh chat tương tự như trên
