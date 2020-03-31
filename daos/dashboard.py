"""
This is the database access object that focuses on all queries regarding the sign up page of this web app
@Author: Angel G. Carrillo Laguna
@git: AngelGCL
@date_of_creation: September 29, 2019
"""

from config.dbconfig import pg_config
import psycopg2

class DashboardDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['dbname'],
                                                                    pg_config['user'],
                                                                    pg_config['passwd'],
                                                                    pg_config['host']
                                                                    )
        self.conn = psycopg2._connect(connection_url)

    # Return a list of activities ordered by department. 
    def getActivitiesByDepartment(self):
        cursor = self.conn.cursor()

        query = """ SELECT DISTINCT a.actid, a.actname, d.dname
                    FROM activity a
                    INNER JOIN leads l
                        on a.actid = l.actid
                    INNER JOIN professor p
                        on p.profid = l.profid
                    INNER JOIN  department d
                        on d.depid = p.depid
                    ORDER BY d.dname
                """
        try:
            cursor.execute(query)
        except psycopg2.Error as e:
            return

        result = []

        for row in cursor:
            result.append(row)
        return result





#===================================================Professors=====================================#
    #does not include the user id because it could be null
    # will be used to find the professor's information if it exists already in the database
    # will return prior information of the professor in the data base if it exists*#
    def getProfessorPreData(self, firstname, lastname):
        cursor = self.conn.cursor()
        query = "select profid, firstname, lastname, acadpos, depid from Professor where firstname = %s and lastname = %s;"
        cursor.execute(query, firstname, lastname)
        result = cursor.fetchone()
        return result

    #used to create new users in database and return userId to connect to profile
    def insertUser(self, json):
        email = json['email']
        password = json['password']
        cursor = self.conn.cursor()
        query = "insert into Users(email, password) values (%s, %s) returning userId;"
        cursor.execute(query, (email, password,))
        self.conn.commit()
        uId = cursor.fetchone()
        return uId

    #TO-DO: Falta que guarde la direccion del CV y de la foto
    # Creara un usuario nuevo y conectara el usuario a un nuevo profile de profesor
    # Returns userId for frontend to keep user logged in*#
    def insertProfessor(self, json):
        email = json['email']
        password = json['password']
        cursor = self.conn.cursor()
        query = "insert into Users(email, password) values (%s, %s) returning userId;"
        cursor.execute(query, (email, password,))
        self.conn.commit()
        uId = cursor.fetchone()
        if not uId:
            return uId
        else:
            fname = json['firstName']
            lname = json['lastName']
            position = json['acadPos']
            department = json['depid']
            userId = uId
            query = "insert into Professor(firstName, lastName, acadpos, depid, userId) values (%s, %s, %s, %s, %s);"
            cursor.execute(query, (fname, lname, position, department, userId,))
            self.conn.commit()
            return userId

    #Crea nuevas actividades desde sign up
    def insertActivity(self, json):
        actname = json['actname']
        type = json['type']
        active = json['active']
        fundrange = json['fundrange']
        fundinterest = json['fundinterest']
        cursor = self.conn.cursor()
        query = "insert into Activity(actname, type, active, fundrange, fundinterest) values (%s, %s, %s, %s, %s) returning *;"
        cursor.execute(query, (actname, type, active, fundrange, fundinterest))
        self.conn.commit()
        result = cursor.fetchone()
        return result

    #===================================================Companies======================================#
    #TO-DO: crear funcion para crear cuenta y profile de compa~ia
    def insertCompany(self, json):
        email = json['email']
        password = json['password']
        cursor = self.conn.cursor()
        query = "insert into Users(email, password) values (%s, %s) returning userId;"
        cursor.execute(query, (email, password,))
        self.conn.commit()
        uId = cursor.fetchone()
        if not uId:
            return uId
        else:
            companyName = json['cname']
            personName = json['cpname']
            userId = uId
            query = "insert into Companies(cname, cpname, userId) values (%s, %s, %s);"
            cursor.execute(query, (companyName, personName, userId,))
            self.conn.commit()
            return userId

    #TO-DO: Crear funcion para get company pre data*#
    def companyPreData(self, cname):
        cursor = self.conn.cursor()
        query = "select cid, cname from Companies where cname = %s;"
        cursor.execute(query, cname)
        result = cursor.fetchone()
        return result

    #TO-DO: Arreglar attributes en db que deben ser not null