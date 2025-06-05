import mariadb
import sys


class MariaDBAPI:
    def __init__(self):
        self.userid = None
        self.connect()

    def connect(self):
        try:
            self.conn = mariadb.connect(
                user="root",
                password="ilikemarciee3",
                host="localhost",
                port=3306,
                database="expensetracker",
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        self.cursor = self.conn.cursor()

    def signIn(self, username):
        self.cursor.execute(
            "SELECT * FROM user WHERE username=?;", (username, ))
        result = self.cursor.fetchall()
        if len(result) == 0:
            return False
        else:
            self.userid = result[0][0]
            return True

    def signUp(self, username, email):
        self.cursor.execute(
            "SELECT * FROM user WHERE username=? OR email=?", (username, email,))
        result = self.cursor.fetchall()
        if len(result) == 0:
            self.cursor.execute(
                "INSERT INTO user (username, email) VALUES (?, ?)", (username, email))
            self.conn.commit()
            return True
        else:
            return False

    def cumulativeOwe(self):
        try:
            # select *,sum(total-payed) from pays where expenseid in (select expenseid from expense where userid=1) and userid!=1;
            self.cursor.execute(
                "SELECT COALESCE(SUM(total-payed), 0) FROM pays WHERE expenseid in (SELECT expenseid FROM expense WHERE userid=?) and userid!=?", (self.userid, self.userid))
            total = self.cursor.fetchall()
            return total[0][0]
        except:
            return 0

    def cumulativeDebt(self):
        try:
            self.cursor.execute(
                "SELECT COALESCE(SUM(total-payed), 0) FROM pays WHERE userid=?;", (self.userid,))
            total = self.cursor.fetchall()
            return total[0][0]
        except:
            return 0

    def getGroupDebts(self):
        # select g.groupid, g.groupname, sum(total-payed) from pays p join expense e join groupe g where p.expenseid=e.expenseid and e.groupid=g.groupid and p.expenseid in (select expenseid from expense where userid=3);
        try:
            self.cursor.execute(
                "SELECT g.groupid, g.groupname, SUM(total-payed) FROM pays p join expense e join groupe g where p.expenseid=e.expenseid and e.groupid=g.groupid and p.expenseid in (select expenseid from expense where userid=?) group by g.groupid;", (self.userid,))
            result = self.cursor.fetchall()
            return result
        except:
            return -1

    def getFriendDebts(self):
        #  select u.userid, u.username, sum(total-payed) from pays p join user u where p.userid=u.userid and expenseid in (select expenseid from expense where userid=1) and u.userid in (select a.useridb from friend a join friend b where a.userida=1 and (a.userida,a.useridb)=(b.useridb,b.userida)) group by u.userid;
        try:
            self.cursor.execute("SELECT u.userid, u.username, SUM(total-payed) FROM pays p JOIN user u WHERE p.userid=u.userid AND expenseid IN (SELECT expenseid FROM expense WHERE userid=?) AND u.userid IN (SELECT a.useridb FROM friend a JOIN friend b WHERE a.userida=? and (a.userida,a.useridb)=(b.useridb,b.userida)) GROUP BY u.userid;", (self.userid, self.userid))
            result = self.cursor.fetchall()
            return result
        except:
            return -1

    def getExpenseWithinMonth(self):
        # select expensename, amount, groupname, expensedate from expense natural join groupe g join user_group u where g.groupid=u.groupid and u.userid=1 and datediff(now(), expensedate)<=30;
        try:
            self.cursor.execute(
                "SELECT expensename, amount, groupname, expensedate FROM expense NATURAL JOIN groupe g JOIN user_group u WHERE g.groupid=u.groupid AND u.userid=? AND DATEDIFF(NOW(), expensedate) <= 30;", (self.userid,))
            result = self.cursor.fetchall()
            return result
        except:
            return -1

    def getExpenseByName(self, expensename):
        # select expensename, amount, expensedate from expense e join user_group ug where e.groupid=ug.groupid and expensename="mexpense" and ug.userid=1;
        try:
            self.cursor.execute(
                "SELECT expensename, amount, expensedate FROM expense e JOIN user_group ug WHERE e.groupid=ug.groupid AND expensename=? AND ug.userid=?;", (expensename, self.userid))
            result = self.cursor.fetchall()
            return result
        except:
            return -1

    def addFriend(self, username):
        try:
            self.cursor.execute(
                "SELECT * FROM user WHERE username=? AND userid!=?", (username, self.userid))
            result = self.cursor.fetchall()
            if len(result) == 0:
                return False
            else:
                self.cursor.execute(
                    "INSERT INTO friend VALUES (?,?)", (self.userid, result[0][0]))
                self.conn.commit()
                return True
        except:
            print("Error")
            return False

    def getFriendRequests(self):
        # SELECT b.userid, b.username FROM (SELECT userida as a, useridb as b FROM friend WHERE userida!=1 AND useridb=1 EXCEPT SELECT useridb as a, userida as b FROM friend WHERE userida=1 AND useridb!=1)a JOIN user b ON a.a=b.userid;
        self.cursor.execute("SELECT b.userid, b.username FROM (SELECT userida as a, useridb as b FROM friend WHERE userida!=? AND useridb=? EXCEPT SELECT useridb as a, userida as b FROM friend WHERE userida=? AND useridb!=?)a JOIN user b ON a.a=b.userid;",
                            (self.userid, self.userid, self.userid, self.userid))
        result = self.cursor.fetchall()
        return result

    def acceptFriendRequest(self, username):
        try:
            self.cursor.execute(
                "SELECT * FROM user WHERE username=? AND userid!=?", (username, self.userid))
            result = self.cursor.fetchall()
            if len(result) == 0:
                return False
            else:
                self.cursor.execute(
                    "INSERT INTO friend VALUES (?,?)", (self.userid, result[0][0]))
                self.conn.commit()
                return True
        except:
            print("Error")
            return False

    def deleteFriend(self, username):
        try:
            self.cursor.execute(
                "SELECT userid FROM user WHERE username=?", (username,))
            useridb = self.cursor.fetchall()
            if len(useridb) == 0:
                return False
            else:
                self.cursor.execute("DELETE FROM friend WHERE (userida=? AND useridb=?) OR (userida=? AND useridb=?)", (
                    self.userid, useridb[0][0], useridb[0][0], self.userid))
                self.conn.commit()
                return True
        except:
            print("Error")
            return False

    def getFriends(self):
        # SELECT b.userid, b.username FROM (SELECT userida as a, useridb as b FROM friend WHERE userida!=1 AND useridb=1 INTERSECT SELECT useridb as a, userida as b FROM friend WHERE userida=1 AND useridb!=1)a JOIN user b ON a.a=b.userid;
        # self.cursor.execute("SELECT b.userid, b.username FROM (SELECT userida as a, useridb as b FROM friend WHERE userida!=? AND useridb=? INTERSECT SELECT useridb as a, userida as b FROM friend WHERE userida=? AND useridb!=?)a JOIN user b ON a.a=b.userid;",
        #                     (self.userid, self.userid, self.userid, self.userid))
        #  select * from user where userid in (select a.useridb from friend a join friend b where a.userida=1 and (a.userida,a.useridb)=(b.useridb,b.userida));
        self.cursor.execute(
            "SELECT * FROM user WHERE userid IN (SELECT a.useridb from friend a join friend b WHERE a.userida=? AND (a.userida,a.useridb)=(b.useridb,b.userida));",  (self.userid,))
        result = self.cursor.fetchall()
        return result

    def getFriend(self, friendid):
        #  select expensename,username from expense e join user_group ug where e.groupid in (select groupid from user_group where userid=1) and ug.userid=2;
        self.cursor.execute(
            "SELECT expensename, expensedate FROM expense e JOIN user_group ug WHERE e.groupid IN (SELECT groupid FROM user_group WHERE userid=?) AND ug.userid=?;", (self.userid, friendid))
        result = self.cursor.fetchall()
        return result

    def createGroup(self, groupname):
        try:
            # INSERT INTO groupe (groupname) VALUES ("group1");
            self.cursor.execute(
                "INSERT INTO groupe (groupname) VALUES (?);", (groupname,))

            # INSERT INTO user_group VALUES (userid, groupid);
            groupid = self.cursor.lastrowid
            self.cursor.execute(
                "INSERT INTO user_group VALUES (?,?);", (self.userid, groupid))
            self.conn.commit()
            return True
        except:
            print(f"ERROR")
            return False

    def getMyGroups(self):
        # SELECT groupid, groupname FROM user NATURAL JOIN user_group NATURAL JOIN groupe WHERE userid=2;
        self.cursor.execute(
            "SELECT groupid, groupname FROM user NATURAL JOIN user_group NATURAL JOIN groupe WHERE userid=?;", (self.userid,))
        result = self.cursor.fetchall()
        return result

    def getGroup(self, groupid):
        # SELECT username FROM (SELECT * FROM user_group WHERE groupid=2)a NATURAL JOIN user;
        self.cursor.execute(
            "SELECT groupname FROM groupe WHERE groupid=?", (groupid,))
        result1 = self.cursor.fetchall()
        self.cursor.execute(
            "SELECT username FROM (SELECT * FROM user_group WHERE groupid=?)a NATURAL JOIN user;", (groupid,))
        result2 = self.cursor.fetchall()
        return result1, result2

    def addFriendToGroup(self, username, groupid):
        # INSERT INTO user_group VALUES ((SELECT userid FROM user WHERE username="jane"), 5)
        try:
            self.cursor.execute(
                "INSERT INTO user_group VALUES ((SELECT userid FROM user WHERE username=?), ?);", (username, groupid))
            self.conn.commit()
            return True
        except:
            return False

    def friendsNotInGroup(self, groupid):
        self.cursor.execute("SELECT username FROM (SELECT a as a FROM (SELECT userida as a, useridb as b FROM friend WHERE userida!=? AND useridb=? INTERSECT SELECT useridb as a, userida as b FROM friend WHERE userida=? AND useridb!=?)a EXCEPT SELECT userid as a FROM user_group WHERE groupid=?)b JOIN user ON b.a=user.userid;",  (self.userid, self.userid, self.userid, self.userid, groupid))
        result = self.cursor.fetchall()
        return result

    def createExpense(self, expensename, amount, groupid, date):
        try:
            self.cursor.execute("INSERT INTO expense (expensename, amount, userid, groupid, expensedate) VALUES (?,?,?,?,(SELECT STR_TO_DATE(?, '%M %d, %Y')))", (
                expensename, amount, self.userid, groupid, date))
            self.conn.commit()
            expenseid = self.cursor.lastrowid

            self.cursor.execute(
                "SELECT userid FROM user_group WHERE groupid=?", (groupid,))
            members = self.cursor.fetchall()
            numberOfMembers = len(members)

            for i in members:
                self.cursor.execute(
                    "INSERT INTO pays VALUES (?,?,?,?);", (expenseid, i[0], 0, amount/numberOfMembers))
                self.conn.commit()

            self.cursor.execute("UPDATE pays SET payed=? WHERE expenseid=? AND userid=?", (
                amount/numberOfMembers, expenseid, self.userid))
            self.conn.commit()
            return True

        except:
            print("ERROR")

    def getDebtsInGroup(self, groupid):
        self.cursor.execute("SELECT * FROM (SELECT e.userid,COALESCE(owed,0) as owed FROM (SELECT userid, SUM(owed) as owed FROM (SELECT userid, SUM(total-payed) as owed FROM pays WHERE expenseid IN (SELECT expenseid FROM expense WHERE groupid=? AND userid=?) GROUP BY userid UNION SELECT a.userid, SUM(payed-total) as owed FROM (SELECT * FROM expense WHERE groupid=? AND userid!=?)a JOIN (SELECT * FROM pays WHERE userid=?)b ON a.expenseid=b.expenseid GROUP BY userid)c GROUP BY userid)d RIGHT JOIN (SELECT userid FROM user_group WHERE groupid=?)e ON d.userid=e.userid)f NATURAL JOIN user;", (groupid, self.userid, groupid, self.userid, self.userid, groupid))
        result = self.cursor.fetchall()
        return result

    def getGroupName(self, groupid):
        self.cursor.execute(
            "SELECT groupname FROM groupe WHERE groupid=?", (groupid,))
        result = self.cursor.fetchall()
        return result

    def getGroupbySearch(self, groupname):
        # select * from groupe where groupname="marciee" and groupid in (select groupid from user_group where userid=1);
        self.cursor.execute(
            "SELECT * FROM groupe WHERE groupname=? AND groupid IN (SELECT groupid FROM user_group WHERE userid=?);", (groupname, self.userid))
        result = self.cursor.fetchall()
        return result

    def getFriendbySearch(self, username):
        #  select * from user where userid in (select useridb from friend where userida=1);
        self.cursor.execute(
            "SELECT * FROM user WHERE userid IN (SELECT useridb FROM friend WHERE userida=?) AND username=?;", (self.userid, username))
        result = self.cursor.fetchall()
        return result

    def getGroupId(self, groupname):
        self.cursor.execute(
            "SELECT groupid FROM groupe WHERE groupname=?", (groupname,))
        result = self.cursor.fetchall()
        return result

    def payMemberInGroup(self, amount, groupid, username):
        # UPDATE pays SET payed=payed+1 WHERE expenseid IN (SELECT expenseid FROM expense WHERE groupid=2) LIMIT 1;
        # SELECT expenseid FROM expense WHERE groupid=2 AND userid=?
        res = self.getUserId(username)
        usernameid = res[0][0]
        self.cursor.execute("UPDATE pays SET payed=payed+? WHERE expenseid IN (SELECT expenseid FROM expense WHERE groupid=? AND userid=?) AND userid=? LIMIT 1;",
                            (amount, groupid, usernameid, self.userid))
        self.conn.commit()
        return True

    def getUserId(self, username):
        self.cursor.execute(
            "SELECT userid FROM user WHERE username=?", (username,))
        result = self.cursor.fetchall()
        return result

    def getGroupExpenses(self, groupid):
        # SELECT expensename, amount, username FROM (SELECT * FROM expense WHERE groupid=2)a JOIN user b ON a.userid=b.userid ;
        self.cursor.execute(
            "SELECT expensename, amount, username FROM (SELECT * FROM expense WHERE groupid=?)a JOIN user b ON a.userid=b.userid;", (groupid,))
        result = self.cursor.fetchall()
        return result

    def deleteGroup(self, groupid):
        # check if group input by user exists
        self.cursor.execute(
            "SELECT * FROM groupe WHERE groupid=?;", (groupid,))
        result = self.cursor.fetchall()
        if (len(result) == 0):
            return False

        # delete according tuples in pays ( found at least one )
        try:
            self.cursor.execute(
                "DELETE FROM pays WHERE expenseid in (SELECT expenseid FROM expense WHERE groupid=?);", (groupid,))
            self.conn.commit()
            print("Deleting outstanding balance...")
            self.cursor.execute(
                "DELETE FROM expense WHERE groupid=?", (groupid,))
            self.conn.commit()
            print("Deleting expense records made with group...")
            self.cursor.execute(
                "DELETE FROM user_group WHERE groupid=?", (groupid,))
            self.conn.commit()
            print("Deleting group...")
            self.cursor.execute(
                "DELETE FROM groupe WHERE groupid=?;", (groupid,))
            self.conn.commit()
            return True

        except:
            print("No expenses recorded!")
            return True

    def deleteGroupExpense(self, expensename, groupid):
        self.cursor.execute(
            "SELECT * FROM groupe WHERE groupid=?;", (groupid,))
        result = self.cursor.fetchall()
        if (len(result) == 0):
            return False

        try:
            self.cursor.execute(
                "DELETE FROM pays WHERE expenseid in (SELECT expenseid FROM expense WHERE expensename=?);", (expensename,))
            self.conn.commit()
            print("Deleting outstanding balance...")
            self.cursor.execute(
                "DELETE FROM expense WHERE groupid=? AND expensename=?", (groupid, expensename))
            self.conn.commit()
            print("Deleting expense records made with group...")

        except:
            print("No expenses recorded!")
            return True
