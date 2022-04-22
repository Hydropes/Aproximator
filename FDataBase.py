import sqlite3


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur =db.cursor()

    def getMenu(self):
        sql = """SELECT * FROM mainmenu"""
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()

            if res:
                li = []
                for el in res:
                    li.append(dict(el))
                return li

        except:
            print("Database error")
        return []
    def addUser(self,  name, email, hpsw):
        try:
            print(f'name = {name}, email = {email}, pas = {hpsw}')
            self.__cur.execute(f'SELECT COUNT() as `count` FROM users WHERE email LIKE {email}')
            res = self.__cur.fetchone()
            print(f'res={res}')
            if res['count']>0:
                print('Already have this user')
                return False
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?)", (name, email, hpsw))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Error for add to database', str(e))
            return False
        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute(f'SELECT * FROM users WHERE id = {user_id} LIMIT 1')
            res = self.__cur.fetchone()
            if not res:
                print('Cannot find such user')
                return False
            return res
        except sqlite3.Error as e:
            print('Error for get user from database'+ str(e))
        return False
    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f'SELECT * FROM users WHERE email = {email} LIMIT 1')
            res =self.__cur.fetchone()
            print(res)
            if not res:
                print('Cannot get data from DB')
                return False
            return res
        except sqlite3.Error as e:
            print('Error for get user from database'+ str(e))
        return False