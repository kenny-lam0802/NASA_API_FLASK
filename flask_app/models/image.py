from flask_app.config.mysqlconnection import connectToMySQL

class Image:
    DB = 'nasa_images_schema'
    def __init__(self, data):
        self.id = data ["id"]
        self.date = data ["date"]
        self.description = data ["description"]
        self.image_link = data ["image_link"]
        self.created_at = data ["created_at"]
        self.updated_at = data ["updated_at"]
        
    @classmethod
    def save_image(cls, data):
        query = """
        INSERT INTO favorites (date, description, image_link)
        VALUES
        (%(date)s, %(description)s, %(image_link)s);
        """
        return connectToMySQL(cls.DB).query_db(query,data)
    
    @classmethod
    def select_by_date(cls, data):
        query = "SELECT * from favorites WHERE date = %(date)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            return cls(results[0])
        