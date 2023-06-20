import pymysql
 
# access database
db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     passwd='root',
                     db='prescriptxn',
                     charset='utf8')
 

cursor = db.cursor()


sql = """CREATE TABLE users(
        userID SMALLINT NOT NULL AUTO_INCREMENT,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        gender VARCHAR(10) NOT NULL,
        birthday DATE NOT NULL,
        address VARCHAR(100) NOT NULL,
        city VARCHAR(50) NOT NULL,
        province VARCHAR(50) NOT NULL,
        postal_code VARCHAR(20) NOT NULL,
        email VARCHAR(100) NOT NULL,
        PRIMARY KEY(userID)
         );"""


cursor.execute(sql)
 

cursor.execute("show tables") 
 




mycursor = db.cursor() 
mycursor.execute("SELECT * FROM users")
results = mycursor.fetchall()


db.commit()
mycursor.close()
cursor.close()
db.close()