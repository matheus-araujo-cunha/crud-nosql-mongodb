from app.controllers import (delete, insert_post, retrieve, retrieve_by_id,
                             update)


def post_route(app):
    
    @app.get("/posts")
    def read_posts():
        return retrieve()

    @app.get("/posts/<int:id>")
    def read_post_by_id(id):
        return retrieve_by_id(id)

    @app.post("/posts")    
    def create_post():
        return insert_post()

    @app.delete("/posts/<int:id>")
    def delete_post(id):
        return delete(id)

    @app.patch("/posts/<int:id>")
    def update_post(id):
        return update(id)