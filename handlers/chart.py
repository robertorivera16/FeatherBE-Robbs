from flask import jsonify
from daos.chart import ChartDAO


class ChartHandler:

    # Helper method to build dictionary
    def usersAccountPerMonthToDict(self, rows):
        result = {}
        result['date'] = rows[0]
        result['qty'] = rows[1]
        return result

    def usersAccountsByDepartmentsToDict(self, rows):
        result = {}
        result['department'] = rows[0]
        result['qty'] = rows[1]
        return result


    def getCreatedUsersAccountsPerMonth(self): #Last 12 month
        dao = ChartDAO()
        data = dao.getCreatedUsersAccountsPerMonth()

        if not data:
            return jsonify(Error='No users found'), 404

        mapped_result = []
        for row in data:
            mapped_result.append(self.usersAccountPerMonthToDict(row))

        return jsonify(mapped_result)

    def getUpdatedUsersAccountsPerMonth(self):
        dao = ChartDAO()
        data = dao.getUpdatedUsersAccountsPerMonth()

        if not data:
            return jsonify(Error='No users found'), 404

        mapped_result = []
        for row in data:
            mapped_result.append(self.usersAccountPerMonthToDict(row))

        return jsonify(mapped_result)

    def getCreatedProfessorsProfilesPerMonth(self):
        dao = ChartDAO()
        data = dao.getCreatedProfessorsProfilesPerMonth()

        if not data:
            return jsonify(Error='No professors found'), 404

        mapped_result = []
        for row in data:
            mapped_result.append(self.usersAccountPerMonthToDict(row))

        return jsonify(mapped_result)

    def getUpdatedProfessorsProfilesPerMonth(self):
        dao = ChartDAO()
        data = dao.getUpdatedProfessorsProfilesPerMonth()

        if not data:
            return jsonify(Error='No professors found'), 404

        mapped_result = []
        for row in data:
            mapped_result.append(self.usersAccountPerMonthToDict(row))

        return jsonify(mapped_result)

    def getUsersAccountsByDepartments(self):
        dao = ChartDAO()
        data = dao.getUsersAccountsByDepartments()

        if not data:
            return jsonify(Error='No users found'), 404

        mapped_result = []
        for row in data:
            mapped_result.append(self.usersAccountsByDepartmentsToDict(row))

        return jsonify(mapped_result)

    def getUsersAccountsByCompanies(self):
        dao = ChartDAO()
        data = dao.getUsersAccountsByCompanies()

        if not data:
            return jsonify(Error='No users found'), 404

        mapped_result = []
        for row in data:
            mapped_result.append(self.usersAccountsByDepartmentsToDict(row))

        return jsonify(mapped_result)
