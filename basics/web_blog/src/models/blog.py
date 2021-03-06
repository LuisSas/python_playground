import uuid
import datetime
from src.common.database import Database
from src.models.post import Post

class Blog(object):

    def __init__(self, author, title, description, _id=None):
        self.author = author
        self.title = title
        self.description = description
        self._id = uuid.uuid4().hex if _id is None else _id

    def new_post(self):
        title = input("Enter post title: ")
        content = input("Enter post content: ")
        date = input("Enter post date, or leave black for today (in format DDMMYYYY): ")
        if date == "":
            date = datetime.datetime.utcnow()
        else:
            date = datetime.datetime.strptime(date, "%d%m%Y")
        post = Post(blog_id=self._id,
                    title=title,
                    content=content,
                    author=self.author,
                    date_created=date)
        post.save_to_mongo()

    def get_posts(self):
        return Post.from_blog(self._id)

    def save_to_mongo(self):
        Database.insert(collection='blogs',
                        data=self.json())

    def json(self):
        return {
                "_id": self._id,
                "author": self.author,
                "title": self.title,
                "description": self.description
                }

    @classmethod
    def from_mongo(cls, id):
        blog_data = Database.find_one(collection="blogs",
                                    query={'_id': id})
        return cls(**blog_data)

