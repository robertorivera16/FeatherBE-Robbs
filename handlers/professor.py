from flask import jsonify
from daos.professor import ProfessorDAO


class ProfessorHandler:

    # Helper method to build dictionary
    def professorDataToDict(self, rows, email, department, tags, activities, description):
        result = {}
        result['firstname'] = rows[0]
        result['lastname'] = rows[1]
        result['acadposition'] = rows[2]
        result['dateupdated'] = rows[3]
        result['department'] = department
        result['email'] = email[0]
        result['tags'] = tags
        result['activities'] = activities
        result['description'] = description
        return result

    def tagToDict(self, row):
        result = {}
        result['tagname'] = row[0]
        result['tagid'] = row[1]
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

    def deptsToDict(self, row):
        result = {}
        result['value'] = row[1]
        result['text'] = row[1]
        return result

    def useridToDict(self, row):
        result = {}
        result['dateupdated'] = row[0]
        return result

    def getDepartments(self):
        dao = ProfessorDAO()
        data = dao.getDepartments()
        if not data:
            return jsonify(Error='Employee not found'), 404
        dept_dict = []
        for dep in data:
            dept_dict.append(self.deptsToDict(dep))
        return jsonify(dept_dict)

    def getProfessorDataByProfid(self, profid):
        dao = ProfessorDAO()
        data = dao.getProfessorDataByProfid(profid)

        if not data:
            return jsonify(Error='Employee not found'), 404

        tags = dao.getProfessorTagsByProfid(profid)
        activities = dao.getProfessorActivitiesByProfid(profid)
        department = dao.getProfessorDepartmentNameByProfid(profid)

        mapped_result = self.professorDataToDict(data, department, tags, activities)
        return jsonify(mapped_result)

    def getProfessorDataByUserid(self, userid):
        dao = ProfessorDAO()
        data = dao.getProfessorDataByUserid(userid)

        if not data:
            return data
        email = dao.getProfessorEmailByUserid(userid);
        tags = dao.getProfessorTagsByUserid(userid)
        activities = dao.getProfessorActivitiesByUserid(userid)
        description = 'This description is a test.'
        trans = []
        tags_dict = []
        for act in activities:
            trans.append(self.activityToDict(act))
        for tag in tags:
            tags_dict.append(self.tagToDict(tag))
        department = dao.getProfessorDepartmentNameByUserid(userid)
        mapped_result = self.professorDataToDict(data, email, department, tags_dict, trans, description)
        return jsonify(mapped_result)

    def editActivity(self, json):
        dao = ProfessorDAO()
        action = json['action']
        if action == 'create':
            activity = json['activity']
            userid = json['userid']
            actid = dao.insertActivity(activity)
            dao.leadAct(userid, actid)
        if action == 'edit':
            actid = json['actid']
            activity = json['activity']
            dao.updateActivity(actid, activity)
        if action == 'delete':
            actid = json['actid']
            userid = json['userid']
            dao.deleteActivity(userid, actid)

    def setProfessorDataByUserid(self, userid, json):
        dao = ProfessorDAO()
        data = dao.setProfessorDataByUserid(userid, json)
        if not data:
            return None
        result = self.useridToDict(data)
        return jsonify(result)
