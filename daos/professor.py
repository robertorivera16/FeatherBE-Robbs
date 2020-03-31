from config.dbconfig import pg_config
import psycopg2
import datetime

class ProfessorDAO:


    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['dbname'],
                                                                    pg_config['user'],
                                                                    pg_config['passwd'],
                                                                    pg_config['host']
                                                                    )
        self.conn = psycopg2._connect(connection_url)

    def getDepartments(self):
        cursor = self.conn.cursor()
        query = "select * from department order by depname asc"
        cursor.execute(query)
        depts = []
        for row in cursor:
            depts.append(row)
        return depts

    def getProfessorDataByProfid(self, profid):
        cursor = self.conn.cursor()
        query = "select firstname, lastname, acadpos from professor where profid = %s;"
        cursor.execute(query, (profid,))
        result = cursor.fetchone()
        return result

    def getProfessorDataByUserid(self, userid):
        cursor = self.conn.cursor()
        query = "select firstname, lastname, acadpos, dateupdated from professor where userid = %s;"
        cursor.execute(query, (userid,))
        result = cursor.fetchone()
        return result

    def getProfessorEmailByUserid(self, userid):
        cursor = self.conn.cursor()
        query = """ SELECT u.email
                        FROM users u 
                    INNER JOIN professor p 
                        on p.userid = u.userid
                    WHERE p.userid = %s;"""
        cursor.execute(query, (userid,))
        result = cursor.fetchone()
        return result

    def getProfessorTagsByProfid(self, profid):
        cursor = self.conn.cursor()
        query = """ SELECT t.tagname, t.tagid
                        FROM tag t 
                    INNER JOIN experiencedin e
                        on e.tagid = t.tagid
                    INNER JOIN professor p
                        on p.profid = e.profid
                    WHERE e.profid = %s"""
        cursor.execute(query, (profid,))
        tags = []
        for row in cursor:
            tags.append(row[0])
        return tags

    def getProfessorTagsByUserid(self, userid):
        cursor = self.conn.cursor()
        query = """ SELECT t.tagname, t.tagid
                        FROM tag t 
                    INNER JOIN experiencedin e
                        on e.tagid = t.tagid
                    INNER JOIN professor p
                        on p.profid = e.profid
                    WHERE p.userid = %s"""
        cursor.execute(query, (userid,))
        tags = []
        for row in cursor:
            tags.append(row)
        return tags

    def getProfessorActivitiesByProfid(self, profid):
        cursor = self.conn.cursor()
        query = """ SELECT a.actname
                        FROM activity a
                    INNER JOIN leads l
                        on l.actid = a.actid
                    WHERE l.profid = %s;"""
        cursor.execute(query, (profid,))
        activities = []
        for row in cursor:
            activities.append(row)
        return activities

    def getProfessorActivitiesByUserid(self, userid):
        cursor = self.conn.cursor()
        query = """ SELECT a.actid, a.actname, a.ongoing, a.fundrange, a.description, a.actdate 
                        FROM activity a
                    INNER JOIN leads l
                        on l.actid = a.actid
                    INNER JOIN professor p
                        on p.profid = l.profid
                    WHERE p.userid = %s;"""
        cursor.execute(query, (userid,))
        activities = []
        for row in cursor:
            activities.append(row)
        return activities

    def getProfessorDepartmentNameByProfid(self, profid):
        cursor = self.conn.cursor()
        query = """ SELECT d.depname 
                        FROM department d
                    INNER JOIN professor p
                        on d.depid = p.depid
                    WHERE p.profid = %s"""
        cursor.execute(query, (profid,))
        department = cursor.fetchone()
        return department

    def getProfessorDepartmentNameByUserid(self, userid):
        cursor = self.conn.cursor()
        query = """ SELECT d.depname 
                        FROM department d
                    INNER JOIN professor p
                        on d.depid = p.depid
                    WHERE p.userid = %s;"""
        cursor.execute(query, (userid,))
        department = cursor.fetchone()
        if department is None:
            return None
        else:
            return department

    def insertActivity(self, activity):
        actname = activity['actname']
        ongoing = activity['ongoing']
        fundrange = activity['fundrange']
        description = activity['description']
        actdate = activity['actdate']
        date = datetime.datetime.utcnow()
        cursor = self.conn.cursor()
        query = "insert into Activity(actname, fundrange, datecreated, dateupdated, description, actdate, ongoing) values (%s, %s, %s, %s, %s, %s, %s) returning actid;"
        cursor.execute(query, (actname, fundrange, date, date, description, actdate, ongoing,))
        result = cursor.fetchone()
        self.conn.commit()
        return result

    def leadAct(self, userid, actid):
        cursor = self.conn.cursor()
        query = "select profid from professor where userid = %s;"
        cursor.execute(query, (userid,))
        profid = cursor.fetchone()
        query = "insert into Leads(profid, actid) values (%s, %s);"
        cursor.execute(query, (profid, actid,))
        self.conn.commit()

    def updateActivity(self, actid, activity):
        cursor = self.conn.cursor()
        actname = activity['actname']
        fundrange = activity['fundrange']
        date = datetime.datetime.utcnow()
        description = activity['description']
        actdate = activity['actdate']
        ongoing = activity['ongoing']
        query = "update Activity set actname = %s, fundrange = %s, dateupdated = %s, description = %s, actdate = %s, ongoing = %s where actid = %s returning actid;"
        cursor.execute(query, (actname, fundrange, date, description, actdate, ongoing, actid,))
        result = cursor.fetchone()
        self.conn.commit()
        return result

    def deleteActivity(self, userid, actid):
        cursor = self.conn.cursor()
        query = "select profid from professor where userid = %s;"
        cursor.execute(query, (userid,))
        profid = cursor.fetchone()
        query = "delete from Leads where actid = %s and profid = %s;"
        cursor.execute(query, (actid, profid,))
        self.conn.commit()


    def setProfessorDataByUserid(self, userid, json):
        cursor = self.conn.cursor()
        query = """ UPDATE professor  
                        SET firstname = %s, lastname = %s, email = %s, description = %s, acadpos = %s, externallink = %s, dateupdated = %s
                        WHERE userid = %s
                        RETURNING dateupdated;"""
        firstname = json['firstname']
        lastname = json['lastname']
        email = json['email']
        description = json['description']
        acadpos = json['position']
        externallink = json['externallink']

        cursor.execute(query, (firstname, lastname, email, description, acadpos,externallink, datetime.datetime.utcnow(), userid))
        result = cursor.fetchone()
        return result