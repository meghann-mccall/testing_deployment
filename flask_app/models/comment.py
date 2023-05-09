from flask_app.config.mysqlconnection import connectToMySQL
import datetime
from flask import flash, session
from flask_app.models import user

class Comment:
    DB = "CodingDojo_Wall_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.posts_id = data['posts_id']
        self.creator = None

    @classmethod
    def save(cls, data ):
        query = """
                INSERT INTO comments ( content , created_at, updated_at, users_id, posts_id ) 
                VALUES ( %(content)s , now(), now(), %(users_id)s, %(posts_id)s );
                """
        result = connectToMySQL(cls.DB).query_db( query, data )
        return result
    
    @classmethod
    def get_all_comments(cls, data):
        query = """
            SELECT * from comments 
            JOIN users ON comments.users_id = users.id 
            WHERE posts_id = %(id)s         
            """
        results = connectToMySQL(cls.DB).query_db(query, data)
        commentslist = []
        for single_comment in results:
            this_comment = cls(single_comment)
            this_comment_creator = {
                "id": single_comment['users.id'],
                "first_name": single_comment['first_name'],
                "last_name": single_comment['last_name'],
                "email": single_comment['email'],
                "password": single_comment['password'],
                "created_at": single_comment['users.created_at'],
                "updated_at": single_comment['users.updated_at']
            }
            author = user.User(this_comment_creator)
            this_comment.creator = author
            commentslist.append(this_comment) 
        return commentslist

    # @classmethod
    # def get_all(cls):
    #     query = "SELECT * FROM cookie_users;"
    #     results = connectToMySQL(cls.DB).query_db(query)
    #     userlist = []
    #     for user in results:
    #         userlist.append( cls(user) )
    #     return userlist
    
    # @classmethod
    # def get_one(cls, id):
    #     query = "SELECT * FROM cookie_users WHERE id = %(id)s;"
    #     results = connectToMySQL(cls.DB).query_db(query, {'id': id})
    #     return cls(results[0])
    

    
    # @classmethod
    # def update(cls,data):
    #     query = """UPDATE cookie_users 
    #             SET name=%(name)s,cookie_type=%(cookie_type)s,num_of_boxes=%(num_of_boxes)s, updated_at=now()
    #             WHERE id = %(id)s;"""
    #     return connectToMySQL(cls.DB).query_db(query,data)
    
    # @classmethod
    # def delete(cls, id):
    #     query = """DELETE FROM cookie_users
    #         WHERE id = %(id)s;"""
    #     return connectToMySQL(cls.DB).query_db(query,{"id": id})
    
    # @classmethod
    # def get_user_by_email(cls,data):
    #     query = "SELECT * FROM users WHERE email = %(email)s;"
    #     result = connectToMySQL(cls.DB).query_db(query,data)
    #     if len(result) < 1:
    #         return False
    #     return cls(result[0])

    # @staticmethod
    # def validate_comment(comment):
    #     is_valid = True 
    #     if len(comment['content']) < 1:
    #         flash("Content cannot be blank.", 'comment')
    #         is_valid = False
    #     return is_valid