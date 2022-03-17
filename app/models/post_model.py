from os import getenv
import pymongo

from app.services import (create_post_id, current_time, found_post_id,
                          validate_invalid_keys, validate_keys,
                          validate_type_values)

HOST_ADRESS = getenv("HOST_ADRESS")
client = pymongo.MongoClient(HOST_ADRESS)
DATABASE = getenv("DATABASE")

class Post:
    db = client[DATABASE]

    def __init__(self,**kwargs) -> None:
        validate_keys(**kwargs)

        self.title = kwargs["title"]
        self.author = kwargs["author"]
        self.tags = kwargs["tags"]
        self.content = kwargs["content"]
        self._id = create_post_id()
        self.update_at = current_time()
        self.created_at = current_time()

    @classmethod
    def get_posts(cls):
        posts_list = list(cls.db.posts.find())
        return posts_list

    @classmethod
    def get_post_by_id(cls,post_id):
        found_post_id(post_id)
        post = cls.db.posts.find_one({"_id":post_id})
        return post

    

    def create_post(self):
        new_post = self.__dict__
        self.db.posts.insert_one(new_post)
        return new_post
    


    @classmethod
    def remove_post(cls,post_id):
        found_post_id(post_id)
        post_deleted = cls.db.posts.find_one_and_delete({"_id":post_id})
        return post_deleted

    @classmethod
    def patch_post(cls,post_id,data):
        validate_invalid_keys(**data)
        validate_type_values(**data)
        found_post_id(post_id)
        data["update_at"] = current_time()
        post = cls.db.posts.find_one_and_update({"_id":post_id},{"$set":data},return_document=True)
        return post


