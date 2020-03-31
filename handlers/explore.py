from flask import jsonify
from daos.explore import ExploreDAO


class ExploreHandler:

    # Helper method to build dictionary
    def professorDataToDict(self, rows):
        result = {}
        result['id'] = rows[0]
        result['first_name'] = rows[1]
        result['last_name'] = rows[2]
        result['position'] = rows[3]
        result['department'] = rows[4]
        result['last_updated'] = rows[5]
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

    def employeeDataToDict(self, rows):
        result = {}
        result['id'] = rows[0]
        result['first_name'] = rows[1]
        result['last_name'] = rows[2]
        result['position'] = rows[3]
        result['company'] = rows[4]
        result['last_updated'] = rows[5]
        return result

    def tagToDict(self, row):
        result = {}
        result["id"] = row[0]
        result["tagname"] = row[1]
        return result

    def getAllProfessorsProfiles(self):
        dao = ExploreDAO()
        data = dao.getAllProfessorsProfiles()

        if not data:
            return jsonify(Error='No professors profiles found'), 404

        mapped_result = []
        for row in data:
            mapped_result.append(self.professorDataToDict(row))

        return jsonify(mapped_result)

    def getAllEmployeeProfiles(self):
        dao = ExploreDAO()
        data = dao.getAllEmployeeProfiles()

        if not data:
            return jsonify(Error="No employees profiles found"), 404

        mapped_result = []
        for row in data:
            mapped_result.append(self.employeeDataToDict(row))
        return jsonify(mapped_result)

    def getAllTags(self):
        dao = ExploreDAO()
        data = dao.getAllTags()

        if not data:
            return jsonify(Error="No tags found"), 404

        mapped_result = []
        for row in data:
            mapped_result.append(self.tagToDict(row))
        return jsonify(mapped_result)

    def searchProfessorsProfileQT(self, q, tagid):
        dao = ExploreDAO()
        data = dao.searchProfessorsProfileQT(q, tagid)

        if not data:
            return jsonify(Error="No professor profiles found"), 404

        mapped_result = []
        for row in data:
            mapped_result.append(self.employeeDataToDict(row))
        return jsonify(mapped_result)

    def searchProfessorsProfileT(self, tagid):
        dao = ExploreDAO()
        data = dao.searchProfessorsProfileT(tagid)

        if not data:
            return jsonify(Error="No professor profiles found"), 404

        mapped_result = []
        for row in data:
            mapped_result.append(self.employeeDataToDict(row))
        return jsonify(mapped_result)

    def searchProfessorsProfileQ(self, q):
        dao = ExploreDAO()
        data = dao.searchProfessorsProfileQ(q)

        if not data:
            return jsonify(Error="No professor profiles found"), 404

        mapped_result = []
        for row in data:
            mapped_result.append(self.employeeDataToDict(row))
        return jsonify(mapped_result)

    def searchEmployeeProfileQT(self, q, tagid):
        dao = ExploreDAO()
        data = dao.searchEmployeeProfileQT(q, tagid)

        if not data:
            return jsonify(Error="No employees profiles found"), 404

        mapped_result = []
        for row in data:
            mapped_result.append(self.employeeDataToDict(row))
        return jsonify(mapped_result)

    def searchEmployeeProfileT(self, tagid):
        dao = ExploreDAO()
        data = dao.searchEmployeeProfileT(tagid)

        if not data:
            return jsonify(Error="No employees profiles found"), 404

        mapped_result = []
        for row in data:
            mapped_result.append(self.employeeDataToDict(row))
        return jsonify(mapped_result)

    def searchEmployeeProfileQ(self, q):
        dao = ExploreDAO()
        data = dao.searchEmployeeProfileQ(q)

        if not data:
            return jsonify(Error="No employees profiles found"), 404

        mapped_result = []
        for row in data:
            mapped_result.append(self.employeeDataToDict(row))
        return jsonify(mapped_result)
