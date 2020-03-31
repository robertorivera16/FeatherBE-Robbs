from config.dbconfig import pg_config
import psycopg2

class signinDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['dbname'],
                                                                    pg_config['user'],
                                                                    pg_config['passwd'],
                                                                    pg_config['host']
                                                                    )
        self.conn = psycopg2._connect(connection_url)


    def getUserData(self, email, password):
        cursor = self.conn.cursor()
        query = "select userid, usertype from users where email = %s and password = %s;"
        cursor.execute(query, (email, password))
        result = cursor.fetchone()
        return result

    def getUserType(self, userid):
        cursor = self.conn.cursor()
        query = "select usertype from users where userid = %s;"
        cursor.execute(query, userid)
        result = cursor.fetchone()
        return result