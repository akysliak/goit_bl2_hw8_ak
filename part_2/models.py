from mongoengine import *
import certifi

connect(
    db="web16_mod08_task2",
    host="mongodb+srv://akysliak:O9aLSLc69X4QZ7nj@cluster0.qz6jqg4.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=certifi.where()
)


class Contact(Document):
    fullname = StringField(max_length=150)
    email = StringField(max_length=50)
    message_sent = BooleanField(default=False)
