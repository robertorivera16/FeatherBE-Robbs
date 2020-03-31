from flask import jsonify
from daos.employee import EmployeeDAO

class EmployeeHandler:

    # Helper method to build dictionary
    def employeeDataToDict(self, rows, email,  company, tags, activities):
        result = {}
        result['firstname'] = rows[0]
        result['lastname'] = rows[1]
        result['empposition'] = rows[2]
        result['dateupdated'] = rows[3]
        result['email'] = email[0]
        result['company'] = company
        result['tags'] = tags
        result['activities'] = activities
        return result

    def activityToDict(self, row):
        result = {}
        result['actid'] = row[0]
        result['actname'] = row[1]
        result['ongoing'] = row[2]
        result['fundrange'] = row[3]
        result['description'] = row[4]
        result['actdate'] = row[5]
        return result

    def tagToDict(self, row):
        result = {}
        result['tagname'] = row[0]
        result['tagid'] = row[1]
        return result

    def useridToDict(self, row):
        result = {}
        result['dateupdated'] = row[0]
        return result

    def getEmployeeDataByEmpid(self, empid):
        dao = EmployeeDAO()
        data = dao.getEmployeeDataByEmpid(empid)

        if not data:
            return jsonify(Error='Employee not found'), 404

        tags = dao.getEmployeeTagsByEmpid(empid)
        activities = dao.getEmployeeActivitiesByEmpid(empid)
        company = dao.getEmployeeCompanyNameByEmpid(empid)

        mapped_result = self.employeeDataToDict(data, company, tags, activities)
        return jsonify(mapped_result)

    def getEmployeeDataByUserid(self, userid):
        dao = EmployeeDAO()
        data = dao.getEmployeeDataByUserid(userid)

        if not data:
            return data

        tags = dao.getEmployeeTagsByUserid(userid)
        email = dao.getEmployeeEmailByUserid(userid);
        activities = dao.getEmployeeActivitiesByUserid(userid)
        trans = []
        tags_dict = []
        for act in activities:
            trans.append(self.activityToDict(act))
        for tag in tags:
            tags_dict.append(self.tagToDict(tag))
        company = dao.getEmployeeCompanyNameByUserid(userid)

        mapped_result = self.employeeDataToDict(data, email, company, tags_dict, trans)
        return jsonify(mapped_result)

    def setEmployeeDataByUserid(self, userid, json):
        dao = EmployeeDAO()
        data = dao.setEmployeeDataByUserid(userid, json)
        if not data:
            return None
        result = self.useridToDict(data)
        return jsonify(result)
