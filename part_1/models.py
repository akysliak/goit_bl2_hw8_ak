import certifi

from bson import json_util
from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE

#connect(db="hw", host="mongodb://localhost:27017")

connect(
    db="web16_mod08",
    host="mongodb+srv://akysliak:O9aLSLc69X4QZ7nj@cluster0.qz6jqg4.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=certifi.where()
)

class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=15))
    quote = StringField()
    meta = {"collection": "quotes"}

    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args, **kwargs)
        data["author"] = self.author.fullname
        return json_util.dumps(data, ensure_ascii=False)