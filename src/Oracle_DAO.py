import cx_Oracle
import os

class OracleDao:
    def __init__(self, ips, ports, ids, pws):
        os.environ['NLS_LANG'] = ".AL32UTF8"
        dsns = cx_Oracle.makedsn(ips, ports, "xe")
        self.conn = cx_Oracle.connect(ids, pws, dsns)
        self.cursor = self.conn.cursor()
    
    def __del__(self):
        self.cursor.close()
        self.conn.close()
        
    def CreateTable(self): 
        drop_sql = """
        BEGIN
            EXECUTE IMMEDIATE 'DROP TABLE videos';
        EXCEPTION
            WHEN OTHERS THEN
                IF SQLCODE != -942 THEN
                    RAISE;
                END IF;
        END;
        """
        self.cursor.execute(drop_sql)
        
        create_sql = ("""
            CREATE TABLE videos(
                link VARCHAR2(50),
                time VARCHAR2(10),
                title VARCHAR2(50),
                views VARCHAR2(10),
                origin VARCHAR2(10)
                ) 
        """)
        self.cursor.execute(create_sql)
        create_seq = """CREATE SEQUENCE videos_seq START WITH 1 INCREMENT BY 1 MINVALUE 1 MAXVALUE 99999999"""
        self.cursor.execute(create_seq)

    def insertVideo(self, tableName, link, time, title, view, origin):
        insert_sql = """
            INSERT INTO video_%s (link, time, title, view, origin) values('%s', '%s', '%s', '%s', '%s');
        """%(tableName, link, time, title, view, origin)
        self.cursor.execute(insert_sql)
        self.conn.commit()

    def searchVideo(self):
        "테이블 명으로 파일을 나누고 검색한다"
        search_sql = 'SELECT *  FROM all_tables'
            
        
        self.cursor.execute(search_sql)
        return self.cursor.fetchall()
        
    def deleteVideo(self, tableName):
        "테이블을 지운다"
        delete_sql = """
            DROP TABLE video_%s;
        """%(tableName)
        self.cursor.execute(delete_sql)
        self.conn.commit()

if __name__ == '__main__':
    ip = '192.168.0.12'
    port = '1521'
    id = 'bitai'
    pw = 'bitai'
    g_OracleDao = OracleDao(ips=ip, ports=port, ids=id, pws=pw)
    # g_OracleDao.searchVideo()
    g_OracleDao.CreateTable()