from psycopg2 import connect
# from clcrypto import *

class BaseModel:
    __db_con = None
    @staticmethod
    def connect(
            username = "postgres",
            passwd = "coderslab",
            hostname = "127.0.0.1",
            db_name = "workshop_2_db"
        ):
        if BaseModel.__db_con == None:
            BaseModel.__db_con = connect(user=username, password=passwd, host=hostname, database=db_name)
            BaseModel.__db_con.autocommit = True
        return BaseModel.__db_con
    @staticmethod
    def disconnect():
        if BaseModel.__db_con != None:
            BaseModel.__db_con.close()
            BaseModel.__db_con = None
    @staticmethod
    def cursor():
        if BaseModel.__db_con == None:
            BaseModel.connect()
        return BaseModel.__db_con.cursor()

class User(BaseModel):
    __id = None
    username = None
    __hashed_password = None
    email = None
    def __init__(self):
        self.__id = -1
        self.username = ""
        self.__hashed_password = ""
        self.email = ""

    def __str__(self):
        return '{}<{}>'.format(self.username,self.email)

    def delete(self):
        sql = "DELETE FROM Users WHERE id=%s"
        User.cursor().execute(sql, (self.__id, ))
        self.__id = -1
        return True

    def save(self):
        if self.__id == -1:
            sql = """INSERT INTO Users(username, email, hashed_password)
                     VALUES(%s, %s, %s) RETURNING id"""
            values = (self.username, self.email, self.__hashed_password)
            cur = User.cursor()
            cur.execute(sql, values)
            self.__id = cur.fetchone()[0]  # albo cursor.fetchone()['id']
            return True
        else:
            pass
        return False

    @staticmethod
    def load_user_by_id(user_id):
        sql = "SELECT id, username, email, hashed_password FROM users WHERE id=%s"
        cursor = User.cursor()
        cursor.execute(sql, (user_id, ))  # (user_id, ) - bo tworzymy krotkę
        data = cursor.fetchone()
        if data:
            loaded_user = User()
            loaded_user.__id = data[0]
            loaded_user.username = data[1]
            loaded_user.email = data[2]
            loaded_user.__hashed_password = data[3]
            return loaded_user
        else:
            return None

    @staticmethod
    def create_storage():
        sql = '''
            CREATE TABLE Users(
                id SERIAL,
                username VARCHAR(64),
                hashed_password VARCHAR(128),
                email VARCHAR(128),
                PRIMARY KEY(id)
            );
        '''
        cur = User.cursor()
        cur.execute(sql)
        cur.close()
        return True

class Message(BaseModel):
    pass
