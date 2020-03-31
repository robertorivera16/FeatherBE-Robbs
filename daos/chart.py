from config.dbconfig import pg_config
import psycopg2

class ChartDAO:


    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s" % (pg_config['dbname'],
                                                                    pg_config['user'],
                                                                    pg_config['passwd'],
                                                                    pg_config['host']
                                                                    )
        self.conn = psycopg2._connect(connection_url)

    def getCreatedUsersAccountsPerMonth(self): #1
        cursor = self.conn.cursor()
        query = """ select to_char(datecreated, 'MM-YYYY') as idate,  
                           count(userid) 
                    from users as u 
                    where u.datecreated > (now() - INTERVAL '6 MONTH')
                    group by 1
                    order by 1 asc;"""
        cursor.execute(query)
        professors = []
        for row in cursor:
            professors.append(row)
        return professors

    def getUpdatedUsersAccountsPerMonth(self): #2
        cursor = self.conn.cursor()
        query = """ select to_char(dateupdated, 'MM-YYYY') as idate,  
                           count(userid) 
                    from users as u 
                    where u.dateupdated > (now() - INTERVAL '6 MONTH')
                    group by 1
                    order by 1 asc;"""
        cursor.execute(query)
        professors = []
        for row in cursor:
            professors.append(row)
        return professors

    def getCreatedProfessorsProfilesPerMonth(self): #3
        cursor = self.conn.cursor()
        query = """ select to_char(datecreated, 'MM-YYYY') as idate,  
                           count(profid) 
                    from professor as p 
                    where p.datecreated > (now() - INTERVAL '6 MONTH')
                    group by 1
                    order by 1 asc;"""
        cursor.execute(query)
        professors = []
        for row in cursor:
            professors.append(row)
        return professors

    def getUpdatedProfessorsProfilesPerMonth(self): #4
        cursor = self.conn.cursor()
        query = """ select to_char(dateupdated, 'MM-YYYY') as idate,  
                           count(userid) 
                    from professor as p 
                    where p.dateupdated > (now() - INTERVAL '6 MONTH')
                    group by 1
                    order by 1 asc;"""
        cursor.execute(query)
        professors = []
        for row in cursor:
            professors.append(row)
        return professors

    def getUsersAccountsByDepartments(self):
        cursor = self.conn.cursor()
        query = """ select d.depname, count(p.profid)
                    from professor as p 
                    INNER JOIN department AS d
                        on d.depid = p.depid
                    INNER JOIN users AS u
                        on p.userid = u.userid
                    GROUP BY d.depname
                    ORDER BY d.depname asc;"""
        cursor.execute(query)
        professors = []
        for row in cursor:
            professors.append(row)
        return professors

    def getUsersAccountsByCompanies(self):
        cursor = self.conn.cursor()
        query = """ select d.comname, count(p.empid)
                    from employee as p 
                    INNER JOIN company AS d
                        on d.comid = p.comid
                    INNER JOIN users AS u
                        on p.userid = u.userid
                    GROUP BY d.comname
                    ORDER BY d.comname asc;"""
        cursor.execute(query)
        professors = []
        for row in cursor:
            professors.append(row)
        return professors
