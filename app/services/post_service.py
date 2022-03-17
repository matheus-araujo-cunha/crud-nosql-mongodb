from datetime import datetime as dt
import pymongo
from os import getenv
from app.exceptions import IdNotFoundError,InvalidKeysError,MissingKeyError,TypeValueError
 

DATABASE = getenv("DATABASE")
HOST_ADRESS = getenv("HOST_ADRESS")

client = pymongo.MongoClient(HOST_ADRESS)
db = client[DATABASE]

EXPECTED_KEYS = ["title","author","content","tags"]

TYPES_VALUES = {"title":str,"author":str,"content":str,"tags":list}

def get_posts():
    return list(db.posts.find())

def found_post_id(id:int):
    posts_list = get_posts()

    id_list = [post["_id"] for post in posts_list]

    if id not in id_list:
        raise IdNotFoundError(id)
    

def current_time():
    return dt.now()

def validate_type_values(**post_dict):
    posts_items = list(post_dict.items())

    wrong_field = []

    for key,value in list(posts_items):
        correct_type_name = TYPES_VALUES[key].__name__
        if not type(value) is TYPES_VALUES[key]:
            wrong_field.append({key:f"Value type must be a {correct_type_name}"})

    if wrong_field:
        raise TypeValueError(wrong_field)            

def validate_keys(**post_dict):
    validate_missing_keys(post_dict)
    validate_invalid_keys(**post_dict)
    validate_type_values(**post_dict)

def validate_invalid_keys(**post_dict:dict):
    post_keys = list_keys(post_dict)
    invalid_keys = [key for key in post_keys if key not in EXPECTED_KEYS]

    if invalid_keys:
        raise InvalidKeysError(EXPECTED_KEYS + invalid_keys,EXPECTED_KEYS)

def validate_missing_keys(post_dict:dict):
    post_keys = list_keys(post_dict)
    missing_keys = [key for key in EXPECTED_KEYS if key not in post_keys]

    if missing_keys:
        raise MissingKeyError(missing_keys,EXPECTED_KEYS)


def list_keys(dictionary:dict):
    return list(dictionary.keys())


def create_post_id():
        posts_list = get_posts()

        if posts_list:
            last_post = posts_list[-1]["_id"]
            return last_post + 1
            
        return 1    