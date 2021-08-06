from Manager import Manager


class DBManager(Manager):
    def __init__(self, DAO: object):
        self.dao = DAO()

    def connect(self, user, db, table):
        result_code = self.dao.connect(user, db, table)
        self.result_handler(result_code, 'connect')

    def update(self, sql: str):
        result_code = self.dao.update(sql)
        self.result_handler(result_code, 'update')

    def select(self, sql: str):
        result_code = self.dao.select(sql)
        self.result_handler(result_code, 'select')

    def insert(self, sql: str):
        result_code = self.dao.insert(sql)
        self.result_handler(result_code, 'insert')

    def delete(self, sql: str):
        result_code = self.dao.delete(sql)
        self.result_handler(result_code, 'delete')
