import sqlite3

class DBManager:

    def __init__(self, dbName):
        self.dbName = dbName
        self.con = sqlite3.connect(self.dbName)
        self.cur = self.con.cursor()
        print("successfully connected")

    def select_data(self, region):
        self.cur.execute("SELECT * FROM path WHERE Region = '%s'" % region)
        self.con.commit()
        result = self.cur.fetchall()
        return result

    def close_db(self):
        self.con.commit()
        self.con.close()
        print("close db")


if __name__ == '__main__':
    print("DBManager")
    db = DBManager("./path.db")

    result = db.select_data("서울")
    #db.term_calculator(date.today().isoformat(), result[0][6])
    db.close_db()