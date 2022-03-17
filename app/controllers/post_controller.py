from http import HTTPStatus

from flask import jsonify, request

from app.exceptions import (IdNotFoundError, InvalidKeysError, MissingKeyError,
                            TypeValueError)
from app.models import Post


def retrieve():
    posts_list = Post.get_posts()
    return jsonify(posts_list),HTTPStatus.OK

def retrieve_by_id(id:int):
    try:
        post = Post.get_post_by_id(id)
    except IdNotFoundError as error:
        return {"error": error.message},error.status_code     

    return post,HTTPStatus.OK

def insert_post():
    data = request.get_json()

    try:
        post = Post(**data)
        post.create_post()
    except MissingKeyError as error:
        return {
            "error":error.message,
            "keys_expected":error.expected_keys,
            "keys_missing":error.missing_keys
            },error.status_code
    except InvalidKeysError as error:
        return {
            "error":error.message,
            "keys_expected":error.expected_keys,
            "keys_received":error.invalid_keys
            },error.status_code
    except TypeValueError as error:
        return {"wrong fields":error.wrong_field},error.status_code            

    return post.__dict__,HTTPStatus.CREATED    

def delete(id:int):
    try:
        post_deleted = Post.remove_post(id)
    except IdNotFoundError as error:
        return {"error":error.message},error.status_code

    return post_deleted,HTTPStatus.OK

def update(id:int):
    data = request.get_json()
    try:
        post_updated = Post.patch_post(id,data)   
    except IdNotFoundError as error:
        return {"error":error.message},error.status_code
    except InvalidKeysError as error:
        return {
            "error":error.message,
            "keys_expected":error.expected_keys,
            "keys_received":error.invalid_keys
            },error.status_code       
    except TypeValueError as error:
        return {"wrong fields":error.wrong_field},error.status_code   
    
    return post_updated,HTTPStatus.OK