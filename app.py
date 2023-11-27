import redis
import pymysql
import json
from config import *

# @Singleton # Managed by Singleton Pattern
class DatabaseManager:
    __redis_connection = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=0, decode_responses=True)
    __sql_connection = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD, db=MYSQL_DB, charset="utf8")
    __sql_cursor = __sql_connection.cursor()
    
    __INJECTION_CHECK = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXZY0123456789"

    def findUserByUsername(self, username: str):
        try:
            for i in username:
                if i not in self.__INJECTION_CHECK:
                    raise Exception("Invalid Username | username = {}".format(username))

            result = self.__redis_connection.get(username)
            result = json.loads(result)
            
            result["returnCode"] = 1
            result["msg"] = "Data Loaded from Redis"

            return result
        except Exception as NoSQLError:
            try:
                self.__sql_cursor.execute("select * from {} where username = '{}'".format(MYSQL_TABLE, username))
                data = self.__sql_cursor.fetchall()[0]
                
                result = {
                    "sid": data[0],
                    "username": data[1],
                    "returnCode": 0,
                    "msg": "NoSQL Error : {}\nData Loaded from SQL".format(NoSQLError)
                }

                return result
            except Exception as SQLError:
                return {
                    "returnCode": -1,
                    "msg": "NoSQL Error : {}\nSQL Error : {}".format(NoSQLError, SQLError)
                }

    def syncDatabase(self, username):
        try:
            for i in username:
                if i not in self.__INJECTION_CHECK:
                    raise Exception("Invalid Username | username = {}".format(username))

            result = self.__redis_connection.get(username)
            result = json.loads(result)

            sql = "update {} set ".format(MYSQL_TABLE)
            for k, v in result.items(): 
                if type(v) == int:
                    sql += "{}={},",format(k, v)
                elif type(v) == str:
                    sql += "{}='{}',".format(k, v)
            sql = sql[:-1]
            sql += " where username = '{}'".format(username)

            self.__sql_cursor.execute(sql)
            self.__sql_connection.commit()

            return {
                "returnCode": 0,
                "msg": "Succeed Synchronization | username = {}".format(username)
            }
        except Exception as e:
            return {
                "returnCode": -1,
                "msg": "Failed Synchronization | error = {}".format(e)
            }


databaseManager = DatabaseManager()