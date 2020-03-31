from config.dbconfig import pg_config
import psycopg2
from datetime import datetime

class EmployeeDAO:


    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['dbname'],
                                                                    pg_config['user'],
                                                                    pg_config['passwd'],
                                                                    pg_config['host']
                                                                    )
        self.conn = psycopg2._connect(connection_url)

    def getEmployeeDataByEmpid(self, empid):
        cursor = self.conn.cursor()
        query = "select firstname, lastname, empposition from employee where empid = %s;"
        cursor.execute(query, empid)
        result = cursor.fetchone()
        return result

    def getEmployeeEmailByUserid(self, userid):
        cursor = self.conn.cursor()
        query = """ SELECT u.email
                        FROM users u 
                    INNER JOIN employee e 
                        on e.userid = u.userid
                    WHERE e.userid = %s;"""
        cursor.execute(query, (userid,))
        result = cursor.fetchone()
        return result

    def getEmployeeDataByUserid(self, userid):
        cursor = self.conn.cursor()
        query = "select firstname, lastname, empposition, dateupdated from employee where userid = %s;"
        cursor.execute(query, (userid,))
        result = cursor.fetchone()
        return result

    def getEmployeeTagsByEmpid(self, empid):
        cursor = self.conn.cursor()
        query = """ SELECT t.tagname
                        FROM tag t 
                    INNER JOIN interestedin i
                        on i.tagid = t.tagid
                    WHERE i.empid = %s"""
        cursor.execute(query, empid)
        tags = []
        for row in cursor:
            tags.append(row[0])
        return tags

    def getEmployeeTagsByUserid(self, userid):
        cursor = self.conn.cursor()
        query = """ SELECT t.tagname, t.tagid
                        FROM tag t 
                    INNER JOIN interestedin i
                        on i.tagid = t.tagid
                    INNER JOIN employee e
                        on e.empid = i.empid
                    WHERE e.userid = %s"""
        cursor.execute(query, (userid,))
        tags = []
        for row in cursor:
            tags.append(row)
        return tags

    def getEmployeeActivitiesByEmpid(self, empid):
        cursor = self.conn.cursor()
        query = """ SELECT a.actid, a.actname, a.ongoing, a.fundrange, a.description, a.actdate 
                        FROM activity a
                    INNER JOIN sponsors s
                        on s.actid = a.actid
                    WHERE s.empid = %s"""
        cursor.execute(query, empid)
        activities = []
        for row in cursor:
            activities.append(row[0])
        return activities

    def getEmployeeActivitiesByUserid(self, userid):
        cursor = self.conn.cursor()
        query = """ SELECT a.actid, a.actname, a.ongoing, a.fundrange, a.description, a.actdate 
                        FROM activity a
                    INNER JOIN sponsors s
                        on s.actid = a.actid
                    INNER JOIN employee e
                        on e.empid = s.empid
                    WHERE e.userid = %s"""
        cursor.execute(query, (userid,))
        activities = []
        for row in cursor:
            activities.append(row)
        return activities

    def getEmployeeCompanyNameByEmpid(self, empid):
        cursor = self.conn.cursor()
        query = """ SELECT c.comname 
                        FROM company c
                    INNER JOIN employee e
                        on c.comid = e.comid
                    WHERE e.empid = %s"""
        cursor.execute(query, (empid,))
        company = cursor.fetchone()
        return company

    def getEmployeeCompanyNameByUserid(self, userid):
        cursor = self.conn.cursor()
        query = """ SELECT c.comname 
                        FROM company c
                    INNER JOIN employee e
                        on c.comid = e.comid
                    WHERE e.userid = %s"""
        cursor.execute(query, (userid,))
        company = cursor.fetchone()
        return company[0]

    def setEmployeeDataByUserid(self, userid, json):
        cursor = self.conn.cursor()
        query = """ UPDATE employee  
                    SET firstname = %s, lastname = %s, empposition = %s, dateupdated = %s
                    WHERE userid = %s
                    RETURNING firstname;"""

        firstname = json['firstname']
        lastname = json['lastname']
        email = json['email']
        empposition = json['position']

        cursor.execute(query, (firstname,lastname, empposition, datetime.utcnow(), userid,))
        result = cursor.fetchone()
        return result
