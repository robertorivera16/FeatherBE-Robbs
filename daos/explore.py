from config.dbconfig import pg_config
import psycopg2

class ExploreDAO:


    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['dbname'],
                                                                    pg_config['user'],
                                                                    pg_config['passwd'],
                                                                    pg_config['host']
                                                                    )
        self.conn = psycopg2._connect(connection_url)

    def getAllProfessorsProfiles(self):
        cursor = self.conn.cursor()
        query = """ SELECT p.userid, p.firstname, p.lastname,p.acadpos, d.depname, p.dateupdated 
                    FROM professor AS p
                    INNER JOIN department AS d
                        on d.depid = p.depid
                    WHERE p.hiddenprofile = false;"""
        cursor.execute(query)
        professors = []
        for row in cursor:
            professors.append(row)
        return professors



    def getAllEmployeeProfiles(self):
        cursor = self.conn.cursor()
        query = """ SELECT e.userid, e.firstname, e.lastname, e.empposition,c.comname, e.dateupdated
                    FROM employee as e
                    INNER JOIN company as c
                        on e.comid = c.comid;
                    """
        cursor.execute(query)
        employees = []
        for row in cursor:
            employees.append(row)
        return employees

    def getAllTags(self):
        cursor = self.conn.cursor()
        query = """SELECT tagid, tagname
                   FROM tag;
                """
        cursor.execute(query)
        tags = []
        for row in cursor:
            tags.append(row)
        return tags

    def searchProfessorsProfileQT(self, q, tagid):
        cursor = self.conn.cursor()
        q = '%' + q + '%'
        query = """ SELECT p.userid, p.firstname, p.lastname,p.acadpos, d.depname, p.dateupdated 
                    FROM professor AS p
                    INNER JOIN department AS d
                        on d.depid = p.depid
                    INNER JOIN experiencedin AS e
                        on e.profid = p.profid
                    WHERE p.hiddenprofile = false AND e.tagid = %s AND (p.firstname ilike %s OR p.lastname ilike %s);"""
        cursor.execute(query, (tagid, q, q,))
        professors = []
        for row in cursor:
            professors.append(row)
        return professors

    def searchProfessorsProfileQ(self, q):
        cursor = self.conn.cursor()
        q = '%' + q + '%'
        query = """ SELECT p.userid, p.firstname, p.lastname,p.acadpos, d.depname, p.dateupdated 
                    FROM professor AS p
                    INNER JOIN department AS d
                        on d.depid = p.depid
                    WHERE p.hiddenprofile = false AND (p.firstname ilike %s OR p.lastname ilike %s);"""
        cursor.execute(query, (q, q,))
        professors = []
        for row in cursor:
            professors.append(row)
        return professors

    def searchProfessorsProfileT(self, tagid):
        cursor = self.conn.cursor()
        query = """ SELECT p.userid, p.firstname, p.lastname,p.acadpos, d.depname, p.dateupdated 
                    FROM professor AS p
                    INNER JOIN department AS d
                        on d.depid = p.depid
                    INNER JOIN experiencedin AS e
                        on e.profid = p.profid
                    WHERE p.hiddenprofile = false AND e.tagid = %s;"""
        cursor.execute(query, (tagid,))
        professors = []
        for row in cursor:
            professors.append(row)
        return professors

    def searchEmployeeProfileQT(self, q, tagid):
        cursor = self.conn.cursor()
        q = '%' + q + '%'
        query = """ SELECT e.userid, e.firstname, e.lastname, e.empposition,c.comname, e.dateupdated
                    FROM employee as e
                    INNER JOIN company as c
                        on e.comid = c.comid
                    INNER JOIN interestedin as i
                        on i.empid = e.empid
                    WHERE i.tagid = %s and (e.firstname ilike %s or e.lastname ilike %s);"""
        cursor.execute(query, (tagid, q, q))
        employees = []
        for row in cursor:
            employees.append(row)
        return employees

    def searchEmployeeProfileQ(self, q):
        cursor = self.conn.cursor()
        q = '%' + q + '%'
        query = """ SELECT e.userid, e.firstname, e.lastname, e.empposition,c.comname, e.dateupdated
                    FROM employee as e
                    INNER JOIN company as c
                        on e.comid = c.comid
                    INNER JOIN interestedin as i
                        on i.empid = e.empid
                    WHERE e.firstname ilike %s or e.lastname ilike %s;"""
        cursor.execute(query, ( q, q))
        employees = []
        for row in cursor:
            employees.append(row)
        return employees

    def searchEmployeeProfileT(self, tagid):
        cursor = self.conn.cursor()
        query = """ SELECT e.userid, e.firstname, e.lastname, e.empposition,c.comname, e.dateupdated
                    FROM employee as e
                    INNER JOIN company as c
                        on e.comid = c.comid
                    INNER JOIN interestedin as i
                        on i.empid = e.empid
                    WHERE i.tagid = %s;"""
        cursor.execute(query, (tagid,))
        employees = []
        for row in cursor:
            employees.append(row)
        return employees
