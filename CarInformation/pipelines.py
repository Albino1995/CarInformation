import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class CarinformationPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    """
    异步化插入数据库
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            password=settings["MYSQL_PASSWORD"],
            charset='utf8',
            # 返回字典表示的记录
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        # 实例化类
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 异步插入错误处理
        query.addErrorback(self.handle_error)

    def handle_error(self, failure):
        # 异步插入错误处理
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)
