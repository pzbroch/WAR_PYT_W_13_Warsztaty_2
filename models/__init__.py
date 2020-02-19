


# /* DATABASE messaging */
#
# CREATE DATABASE messaging;
#
# CREATE TABLE users(
#     id SERIAL,
#     username VARCHAR(64) UNIQUE,
#     hashed_password VARCHAR(128),
#     PRIMARY KEY(id)
# );
#
# CREATE TABLE messages(
#     id SERIAL,
#     from_id INT REFERENCES users(id),
#     to_id INT REFERENCES users(id),
#     text VARCHAR(255),
#     creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     PRIMARY KEY(id)
# );



from psycopg2 import connect
from models.clcrypto import *



class BaseModel:
    __cnx = None

    @staticmethod
    def connect(username='postgres', passwd='coderslab', hostname='127.0.0.1', db_name='messaging'):
        if BaseModel.__cnx == None:
            BaseModel.__cnx = connect(user=username, password=passwd, host=hostname, database=db_name)
            BaseModel.__cnx.autocommit = True
        return BaseModel.__cnx

    @staticmethod
    def disconnect():
        if BaseModel.__cnx != None:
            BaseModel.__cnx.close()
            BaseModel.__cnx = None

    @staticmethod
    def cursor():
        if BaseModel.__cnx == None:
            BaseModel.connect()
        return BaseModel.__cnx.cursor()



class User(BaseModel):
    __id = None
    username = None
    __hashed_password = None

    def __init__(self):
        self.__id = -1
        self.username = ''
        self.__hashed_password = ''

    def __str__(self):
        return self.username

    @property
    def id(self):
        return self.__id

    def set_password(self,password):
        if len(password) > 7:
            self.__hashed_password = password_hash(password)
        else:
            raise Exception('Password too short!')

    def password_check(self,password):
        return check_password(password,self.__hashed_password)

    def delete(self):
        sql = 'DELETE FROM users WHERE id=%s'
        User.cursor().execute(sql, (self.__id, ))
        self.__id = -1
        return True

    def save(self):
        if self.__id == -1:
            sql = 'INSERT INTO users(username, hashed_password) VALUES(%s, %s) RETURNING id;'
            values = (self.username, self.__hashed_password)
            cursor = User.cursor()
            cursor.execute(sql, values)
            self.__id = cursor.fetchone()[0]
            return True
        else:
            sql = 'UPDATE users SET username=%s, hashed_password=%s WHERE id=%s;'
            values = (self.username, self.__hashed_password, self.__id)
            cursor = User.cursor()
            cursor.execute(sql, values)
            return True
        return False

    @staticmethod
    def load_by_(column,value):
        sql = 'SELECT id, username, hashed_password FROM users WHERE {} = %s;'.format(column)
        cursor = User.cursor()
        cursor.execute(sql, (value,))
        data = cursor.fetchone()
        if data:
            loaded_user = User()
            loaded_user.__id = data[0]
            loaded_user.username = data[1]
            loaded_user.__hashed_password = data[2]
            return loaded_user
        else:
            return None

    @staticmethod
    def load_all():
        sql = 'SELECT id, username, hashed_password FROM users;'
        cursor = User.cursor()
        cursor.execute(sql)
        outUsers = []
        for row in cursor:
            loaded_user = User()
            loaded_user.__id = row[0]
            loaded_user.username = row[1]
            loaded_user.__hashed_password = row[2]
            outUsers.append(loaded_user)
        return outUsers

    @staticmethod
    def create_storage():
        sql = '''
            CREATE TABLE users(
                id SERIAL,
                username VARCHAR(64) UNIQUE,
                hashed_password VARCHAR(128),
                PRIMARY KEY(id)
            );
        '''
        cursor = User.cursor()
        cursor.execute(sql)
        cursor.close()
        return True



class Message(BaseModel):
    __id = None
    from_id = None
    to_id = None
    text = None
    creation_date = None

    def __init__(self):
        self.__id = -1
        self.from_id = -1
        self.to_id = -1
        self.text = ''

    def __str__(self):
        return self.text

    def save(self):
        if self.__id == -1:
            sql = 'INSERT INTO messages(from_id, to_id, text) VALUES(%s, %s, %s) RETURNING id;'
            values = (self.from_id, self.to_id, self.text)
            cursor = Message.cursor()
            cursor.execute(sql, values)
            self.__id = cursor.fetchone()[0]
            return True
        raise Exception('Existing message cannot be modified!')

    @staticmethod
    def load_by_(column,value):
        sql = 'SELECT id, from_id, to_id, text, creation_date FROM messages WHERE {} = %s ORDER BY creation_date DESC;'.format(column)
        cursor = Message.cursor()
        cursor.execute(sql, (value,))
        outMessages = []
        for row in cursor:
            loaded_message = Message()
            loaded_message.__id = row[0]
            loaded_message.from_id = row[1]
            loaded_message.to_id = row[2]
            loaded_message.text = row[3]
            loaded_message.creation_date = row[4]
            outMessages.append(loaded_message)
        return outMessages

    @staticmethod
    def load_all():
        sql = 'SELECT id, from_id, to_id, text, creation_date FROM messages;'
        cursor = Message.cursor()
        cursor.execute(sql)
        outMessages = []
        for row in cursor:
            loaded_message = Message()
            loaded_message.__id = row[0]
            loaded_message.from_id = row[1]
            loaded_message.to_id = row[2]
            loaded_message.text = row[3]
            loaded_message.creation_date = row[4]
            outMessages.append(loaded_message)
        return outMessages

    @staticmethod
    def create_storage():
        sql = '''
            CREATE TABLE messages(
                id SERIAL,
                from_id INT REFERENCES users(id),
                to_id INT REFERENCES users(id),
                text VARCHAR(255),
                creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(id)
            );
        '''
        cursor = Message.cursor()
        cursor.execute(sql)
        cursor.close()
        return True
