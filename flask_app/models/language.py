from flask_app.config.mysqlconnection import connectToMySQL

class Language:
    schema = "login_registration_schema"

    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
    
    @classmethod
    def read_all(cls):
        query = "SELECT * FROM languages;"
        results = connectToMySQL(cls.schema).query_db(query)
        languages = []
        for result in results:
            languages.append(cls(result))
        return languages
    
    @classmethod
    def is_in_db(cls,data):
        query = "SELECT id FROM languages WHERE id=%(id)s;"
        results = connectToMySQL(cls.schema).query_db(query,data)
        return len(results) > 0
    
