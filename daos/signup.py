"""
This is the database access object that focuses on all queries regarding the sign up page of this web app
@Author: Angel G. Carrillo Laguna
@git: AngelGCL
@date_of_creation: September 29, 2019
"""

from config.dbconfig import pg_config
import psycopg2
import datetime as datetime

class signupDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['dbname'],
                                                                    pg_config['user'],
                                                                    pg_config['passwd'],
                                                                    pg_config['host']
                                                                    )
        self.conn = psycopg2._connect(connection_url)

#===================================================Professors=====================================#
    #does not include the user id because it could be null
    # will be used to find the professor's information if it exists already in the database
    # will return prior information of the professor in the data base if it exists*#
    def getProfessorPreData(self, email):
        cursor = self.conn.cursor()
        query = "select profid, firstname, lastname, acadpos, depid from Professor where upremail = %s;"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        return result

    def getAllDepts(self):
        cursor = self.conn.cursor()
        query = "select depname from Department;"
        cursor.execute(query,)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getDepartmentby(self, depid):
        cursor = self.conn.cursor()
        query = "select depname from Department where depid = %s;"
        cursor.execute(query, (depid,))
        result = cursor.fetchone()
        return result

    def getDepidbyDepname(self, depname):
        cursor = self.conn.cursor()
        query = "select depid from Department where depname = %s;"
        cursor.execute(query, (depname,))
        result = cursor.fetchone()
        return result

    def getActivities(self, profid):
        cursor = self.conn.cursor()
        query = "select activity.actid, activity.actname, activity.ongoing, activity.fundrange, activity.actdate, activity.description from activity inner join leads on activity.actid = leads.actid inner join professor on leads.profid = professor.profid where professor.profid = %s;"
        cursor.execute(query, (profid,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    #used to create new users in database and return userId to connect to profile
    def insertUser(self, json):
        email = json['email']
        password = json['password']
        cursor = self.conn.cursor()
        query = "insert into Users(email, password) values (%s, %s) returning userid;"
        cursor.execute(query, (email, password,))
        self.conn.commit()
        userid = cursor.fetchone()
        return userid

    #TO-DO: Falta que guarde la direccion del CV y de la foto
    # Creara un usuario nuevo y conectara el usuario a un nuevo profile de profesor
    # Returns userId for frontend to keep user logged in*#
    def insertProfessor(self, json):
        email = json['email']
        password = json['password']
        date = datetime.datetime.utcnow()
        utype = '1'
        cursor = self.conn.cursor()
        query = "insert into Users(email, password, dateupdated, usertype) values (%s, %s, %s, %s) returning userId;"
        cursor.execute(query, (email, password, date, utype,))
        self.conn.commit()
        uId = cursor.fetchone()
        if not uId:
            return uId
        else:
            fname = json['firstname']
            lname = json['lastname']
            position = json['acadpos']
            department = json['department']
            date = datetime.datetime.utcnow()
            description = json['description']
            hidden = False
            userid = uId
            depid = self.getDepidbyDepname(department)
            if len(description) > 0:
                query = "insert into Professor(firstname, lastname, acadpos, depid, userid, datecreated, dateupdated, description, hiddenprofile) values (%s, %s, %s, %s, %s, %s, %s, %s, %s) returning profid;"
                cursor.execute(query, (fname, lname, position, depid, userid, date, date, description, hidden,))
            else:
                query = "insert into Professor(firstname, lastname, acadpos, depid, userid, datecreated, dateupdated, hiddenprofile) values (%s, %s, %s, %s, %s, %s, %s, %s) returning profid;"
                cursor.execute(query, (fname, lname, position, depid, userid, date, date, hidden))
            profid = cursor.fetchone()
            tags = json['tags']
            if len(tags) > 0:
                for tag in tags:
                    self.tagProf(profid, tag['title'])
            activities = json['activities']
            if len(activities) > 0:
                for activity in activities:
                    actid = self.insertActivity(activity)
                    self.leadAct(profid, actid)
            self.conn.commit()
            return userid

    def updateProfessor(self, json):
        email = json['email']
        password = json['password']
        date = datetime.datetime.utcnow()
        utype = '1'
        cursor = self.conn.cursor()
        query = "insert into Users(email, password, dateupdated, usertype) values (%s, %s, %s, %s) returning userId;"
        cursor.execute(query, (email, password, date, utype,))
        self.conn.commit()
        uId = cursor.fetchone()
        if not uId:
            return uId
        else:
            query = "select profid from Professor where firstname = %s and lastname = %s;"
            fname = json['firstname']
            lname = json['lastname']
            profid = cursor.execute(query, (fname, lname,))
            position = json['acadpos']
            department = json['department']
            description = json['description']
            userid = uId
            depid = self.getDepidbyDepname(department)
            date = datetime.datetime.utcnow()
            hidden = False
            if len(description) > 0:
                query = "update Professor set firstname = %s, lastname = %s, acadpos = %s, depid = %s, userid = %s, dateupdated = %s, description = %s, hiddenprofile = %s where profid = %s;"
                cursor.execute(query, (fname, lname, position, depid, userid, date, description, hidden, profid,))
            else:
                query = "update Professor set firstname = %s, lastname = %s, acadpos = %s, depid = %s, userid = %s, dateupdated = %s, hiddenprofile = %s where profid = %s;"
                cursor.execute(query, (fname, lname, position, depid, userid, date, hidden, profid,))
            tags = json['tags']
            if len(tags) > 0:
                for tag in tags:
                    self.tagProf(profid, tag['title'])
            activities = json['activities']
            if len(activities) > 0:
                for activity in activities:
                    actid = self.insertActivity(activity)
                    self.leadAct(profid, actid)
            self.conn.commit()
            return userid

    #Crea nuevas actividades desde sign up
    def insertActivity(self, activity):
        actname = activity['actname']
        # active = json['active']
        fundrange = activity['fundrange']
        description = activity['description']
        actdate = activity['actdate']
        ongoing = activity['ongoing']
        date = datetime.datetime.utcnow()
        cursor = self.conn.cursor()
        query = "insert into Activity(actname, fundrange, datecreated, dateupdated, description, actdate, ongoing) values (%s, %s, %s, %s, %s, %s, %s) returning actid;"
        cursor.execute(query, (actname, fundrange, date, date, description, actdate, ongoing,))
        result = cursor.fetchone()
        self.conn.commit()
        return result

    def leadAct(self, profid, actid):
        cursor = self.conn.cursor()
        query = "insert into Leads(profid, actid) values (%s, %s);"
        cursor.execute(query, (profid, actid,))
        self.conn.commit()
    #===================================================Companies======================================#
    #TO-DO: crear funcion para crear cuenta y profile de compa~ia
    def getAllComps(self):
        cursor = self.conn.cursor()
        query = "select comname from Company;"
        cursor.execute(query,)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insertEmployee(self, json):
        email = json['email']
        password = json['password']
        date = datetime.datetime.utcnow()
        utype = '2'
        cursor = self.conn.cursor()
        query = "insert into Users(email, password, dateupdated, usertype) values (%s, %s, %s, %s) returning userId;"
        cursor.execute(query, (email, password, date, utype,))
        self.conn.commit()
        userid = cursor.fetchone()
        if not userid:
            return userid
        else:
            firstname = json['firstname']
            lastname = json['lastname']
            empposition = json['position']
            comname = json['compname']
            query = "select comid from company where comname = %s;"
            cursor.execute(query, (comname,))
            comid = cursor.fetchone()
            if not comid:
                query = "insert into Company(comname) values (%s) returning comid;"
                cursor.execute(query, (comname,))
                comid = cursor.fetchone()
            date = datetime.datetime.utcnow()
            query = "insert into Employee(firstname, lastname, empposition, comid, userid, datecreated, dateupdated) values (%s, %s, %s, %s, %s, %s, %s) returning empid;"
            cursor.execute(query, (firstname, lastname, empposition, comid, userid, date, date,))
            empid = cursor.fetchone()
            tags = json['tags']
            if len(tags) > 0:
                for tag in tags:
                    self.tagEmp(empid, tag['title'])
            self.conn.commit()
            return userid

    #TO-DO: Crear funcion para get company pre data*#
    def companyPreData(self, comname):
        cursor = self.conn.cursor()
        query = "select comid, comname from Company where comname = %s;"
        cursor.execute(query, comname,)
        result = cursor.fetchone()
        return result

    def createTags(self, tag):
        cursor = self.conn.cursor()
        query = "select tagid from Tag where tagname = %s;"
        cursor.execute(query, (tag,))
        result = cursor.fetchone()
        if not result:
            query = "insert into Tag(tagname) values (%s) returning tagid;"
            cursor.execute(query, (tag,))
            result = cursor.fetchone()
            self.conn.commit()
        return result

    def tagProf(self, profid, tag):
        cursor = self.conn.cursor()
        tagid = self.createTags(tag)
        query = "insert into experiencedin(tagid, profid) values (%s, %s) returning tagid;"
        cursor.execute(query, (tagid, profid,))
        result = cursor.fetchone()
        self.conn.commit()
        return result

    def tagEmp(self, empid, tag):
        cursor = self.conn.cursor()
        tagid = self.createTags(tag)
        query = "insert into interestedin(tagid, empid) values (%s, %s) returning tagid;"
        cursor.execute(query, (tagid, empid,))
        result = cursor.fetchone()
        self.conn.commit()
        return result

    #TO-DO: Arreglar attributes en db que deben ser not null
