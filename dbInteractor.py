import mysql.connector
import json
# import json_util

"""# my_db_connection = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="123570123570",
#   port = 3306, # for Mamp users
#   database='classicmodels'
# )


# cursor = my_db_connection.cursor()
# cursor.execute("select database();")

# print(my_db_connection.get_server_info())
# print(cursor.fetchone())

# res = cursor.execute("select * from customers limit 5")

# print(cursor.fetchone())

# # cursor.close()
# my_db_connection.close()"""


class Text:
    connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123570123570",
            port = 3306, # for Mamp users
            database='major_project'
        )
    
    @classmethod
    def start_connection(cls):
        if not Text.connection.is_connected():
            Text.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123570123570",
                port = 3306, # for Mamp users
                database='major_project'
                )
    
    @classmethod
    def close_connection(cls):
        if Text.connection.is_connected():
            Text.connection.close()
    
    
    @staticmethod
    def get_json(cursor, query):
        cursor.execute(query) 
        result = cursor.fetchall()
        
        row_headers=[x[0] for x in cursor.description] 
        
        json_data=[]
        for result in result:
            json_data.append(dict(zip(row_headers,result)))
        
        
        # print(json.dumps(json_data))
        
        return json.loads(json.dumps(json_data, default=str))
    
    
    @classmethod
    def find_by_text_id(cls, text_id):
        # print("HERE\n\n\n")
        if not Text.connection.is_connected():
            Text.start_connection()
        
        cursor = Text.connection.cursor()
        cursor.execute("select database();")
        cursor.fetchone()
        
        query = f"SELECT * FROM text_ where text_id={text_id};"
        
        
        return Text.get_json(cursor, query)
    
    @classmethod
    def get_max_id(cls):
        # print("HERE\n\n\n")
        if not Text.connection.is_connected():
            Text.start_connection()
        
        cursor = Text.connection.cursor()
        cursor.execute("select database();")
        cursor.fetchone()
        
        query = f"SELECT MAX(text_id) FROM text_;"
        
        
        
        return Text.get_json(cursor, query)

    
    @classmethod
    def add_text(cls, text):
        if not Text.connection.is_connected():
            Text.start_connection()
        
        cursor = Text.connection.cursor()
        cursor.execute("select database();")
        cursor.fetchone()
        
        query = f"INSERT INTO text_ (text_) VALUES ('{text}');"
        # print(query)
        
        cursor.execute(query) 
        Text.connection.commit()
        

    @classmethod
    def get_all(cls):
        if not Text.connection.is_connected():
            Text.start_connection()
        
        cursor = Text.connection.cursor()
        cursor.execute("select database();")
        cursor.fetchone()
        
        query = f"SELECT * FROM text_;"
        
        
        return Text.get_json(cursor, query)

class Summary:
    connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123570123570",
            port = 3306, # for Mamp users
            database='major_project'
        )
    
    @classmethod
    def start_connection(cls):
        if not Summary.connection.is_connected():
            Summary.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123570123570",
                port = 3306, # for Mamp users
                database='major_project'
                )
    
    @classmethod
    def close_connection(cls):
        if Summary.connection.is_connected():
            Summary.connection.close()
    
    
    @staticmethod
    def get_json(cursor, query):
        cursor.execute(query) 
        result = cursor.fetchall()
        
        row_headers=[x[0] for x in cursor.description] 
        
        json_data=[]
        for result in result:
            json_data.append(dict(zip(row_headers,result)))
        
        
        # print(json.dumps(json_data))
        
        return json.loads(json.dumps(json_data, default=str))
    
    
    @classmethod
    def find_by_text_id(cls, summarization_id):
        # print("HERE\n\n\n")
        if not Summary.connection.is_connected():
            Summary.start_connection()
        
        cursor = Summary.connection.cursor()
        cursor.execute("select database();")
        cursor.fetchone()
        
        query = f"SELECT * FROM summarization where summarization_id={summarization_id};"
        
        
        return Summary.get_json(cursor, query)

    
    @classmethod
    def add_summary(cls, summary, compression_ratio, text_id):
        if not Summary.connection.is_connected():
            Summary.start_connection()
        
        cursor = Summary.connection.cursor()
        cursor.execute("select database();")
        cursor.fetchone()
        
        query = f"INSERT INTO summarization (summary, compression_ratio, text_id) VALUES ('{summary}', '{compression_ratio}', '{text_id}');"
        
        # print(query)
        # print(query)
        # print("\n\n\n\n\n")
        
        cursor.execute(query) 
        Summary.connection.commit()
        

    @classmethod
    def get_all(cls):
        if not Summary.connection.is_connected():
            Summary.start_connection()
        
        cursor = Summary.connection.cursor()
        cursor.execute("select database();")
        cursor.fetchone()
        
        query = f"SELECT * FROM summarization;"
        
        
        return Summary.get_json(cursor, query)
    
    @classmethod
    def get_by_Id(cls, id_, id_of):
        if not Summary.connection.is_connected():
            Summary.start_connection()
        
        cursor = Summary.connection.cursor()
        cursor.execute("select database();")
        cursor.fetchone()
        
        if id_of == "text_id":
            query = f"SELECT * FROM summarization where text_id='{id_}';"
        else:
            query = f"SELECT * FROM summarization where summarization_id='{id_}';"
            
        print(query)
        return Summary.get_json(cursor, query)


        

# a = text.find_by_text_id(1)
# print(a.email)        
