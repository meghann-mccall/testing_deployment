from flask_app.config.mysqlconnection import connectToMySQL
import datetime
from flask import flash, session
from flask_app.models import user, comment

class Post:
    DB = "CodingDojo_Wall_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.creator = None
        self.comments = None

    @classmethod
    def save(cls, data ):
        query = """
            INSERT INTO posts ( content, created_at, updated_at, users_id ) 
            VALUES ( %(content)s, now(), now(), %(users_id)s  );
            """
        result = connectToMySQL(cls.DB).query_db( query, data )
        return result

    @classmethod
    def get_all_posts(cls):
        query = "SELECT * from posts JOIN users WHERE posts.users_id = users.id"
        results = connectToMySQL(cls.DB).query_db(query)
        postlist = []
        for single_post in results:
            this_post = cls(single_post)
            this_post_creator = {
                "id": single_post['users.id'],
                "first_name": single_post['first_name'],
                "last_name": single_post['last_name'],
                "email": single_post['email'],
                "password": single_post['password'],
                "created_at": single_post['users.created_at'],
                "updated_at": single_post['users.updated_at']
            }
            author = user.User(this_post_creator)
            this_post.creator = author
            this_post_id = {
                "id": single_post['id']
            }
            comments = comment.Comment.get_all_comments(this_post_id)
            this_post.comments = comments
            postlist.append(this_post) 
        return postlist
    
    @classmethod
    def delete(cls, id):
        query = """DELETE FROM posts
            WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query,{"id": id})

    @staticmethod
    def validate_post(post):
        is_valid = True 
        if len(post['post']) < 1:
            flash("* Content cannot be blank.", 'post')
            is_valid = False
        return is_valid