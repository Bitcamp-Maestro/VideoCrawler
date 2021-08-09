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
        
    def CreateTable(self, tableName): 
        """ 키워드를 테이블 명으로 지정해서 테이블을 생성한다."""
        drop_sql = """
        BEGIN
            EXECUTE IMMEDIATE 'DROP TABLE video_%s';
        EXCEPTION
            WHEN OTHERS THEN
                IF SQLCODE != -942 THEN
                    RAISE;
                END IF;
        END;
        """%(tableName)
        self.cursor.execute(drop_sql)
        
        create_sql = ("""
            CREATE TABLE video_%s(
                id NUMBER NOT NULL, 
                link VARCHAR2(50),
                time VARCHAR2(10),
                title VARCHAR2(50),
                views VARCHAR2(10),
                origin VARCHAR2(10)
                ) 
        """%(tableName))
        self.cursor.execute(create_sql)
        
        drop_seq = "DROP SEQUENCE video_seq_%s"%(tableName)
        self.cursor.execute(drop_seq)
        create_seq = """
            CREATE SEQUENCE video_seq_%s 
            START WITH 1 INCREMENT BY 1 MINVALUE 1 MAXVALUE 99999999"""%(tableName)
        self.cursor.execute(create_seq)

    def insertVideo(self, tableName, link, time, title, views, origin):
        """
        데이터 사입 함수 | tableName = 검색 키워드/
        link = 영상링크/time = 영상길이/title = 영상이름/
        views = 조회수/origin = 플랫폼이름
        """
        insert_sql = """
            INSERT INTO video_%s (id, link, time, title, views, origin) 
            values(video_seq_%s.NEXTVAL, '%s', '%s', '%s', '%s', '%s')
        """%(tableName, tableName, link, time, title, views, origin)
        self.cursor.execute(insert_sql)
        self.conn.commit()

    def searchVideo(self):
        """테이블 명으로 파일을 나누고 검색한다"""
        search_sql = "select object_name from user_objects where object_type = 'TABLE'"
            
        
        self.cursor.execute(search_sql)
        print(self.cursor.fetchall())
        return
        
    def deleteVideo(self, tableName):
        "테이블을 지운다"
        delete_sql = """
            DROP TABLE video_%s
        """%(tableName)
        self.cursor.execute(delete_sql)
        self.conn.commit()

# if __name__ == '__main__':
    # ip = '192.168.0.12'
    # port = '1521'
    # id = 'bitai'
    # pw = 'bitai'
    # tableName = "aaa"
    # g_OracleDao = OracleDao(ips=ip, ports=port, ids=id, pws=pw)
    # g_OracleDao.CreateTable(tableName=tableName)
    # g_OracleDao.insertVideo(tableName=tableName, link="링크", time="000", title="title", views="views", origin="origin")
    # g_OracleDao.deleteVideo(tableName=tableName)
    # g_OracleDao.searchVideo()