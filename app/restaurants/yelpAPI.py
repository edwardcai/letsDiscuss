'''API for interacting with the Yelp Academic Dataset from a SQL database'''
import MySQLdb
import yelpAPI

host = 'localhost'
user = 'root'
password = ''
db = 'yelp'



def loadComments(name, zipcode):
    

    conn = MySQLdb.connect(host, user, password, db, charset='utf8mb4')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM restaurants WHERE name = %s AND zipcode = %s", [name, zipcode])
    res = cursor.fetchone()
    if res is None:
        return []
    id = res[0] 
    cursor.execute("SELECT text, stars FROM reviews WHERE business_id = %s LIMIT 500", [id])
    return cursor.fetchall()


