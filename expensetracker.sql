DROP DATABASE IF EXISTS expensetracker;
CREATE DATABASE IF NOT EXISTS expensetracker;
USE expensetracker;

DROP TABLE IF EXISTS user,
                     friend,
                     groupe,
                     expense, 
                     user_group, 
                     pays;

CREATE TABLE user (
  userid INT(4) AUTO_INCREMENT,
  username VARCHAR(31) NOT NULL,
  email VARCHAR(31) NOT NULL,
  CONSTRAINT user_userid_pk PRIMARY KEY (userid),
  CONSTRAINT user_username_u UNIQUE (username),
  CONSTRAINT user_email_u UNIQUE (email)
);

CREATE TABLE friend (
  userida INT(4),
  useridb INT(4),
  CONSTRAINT user_userida_fk FOREIGN KEY (userida) REFERENCES user(userid),
  CONSTRAINT user_useridb_fk FOREIGN KEY (useridb) REFERENCES user(userid)
);

CREATE TABLE groupe (
  groupid INT(4) AUTO_INCREMENT,
  groupname VARCHAR(31) NOT NULL,
  CONSTRAINT groupe_groupid_pk PRIMARY KEY (groupid)
);

CREATE TABLE expense (
  expenseid INT(4) AUTO_INCREMENT,
  expensename VARCHAR(31) NOT NULL,
  amount INT(6) NOT NULL,
  userid INT(4) NOT NULL,
  groupid INT(4) NOT NULL,
  expensedate DATE NOT NULL,
  CONSTRAINT expense_expenseid_pk PRIMARY KEY (expenseid),
  CONSTRAINT expense_userid_fk FOREIGN KEY (userid) REFERENCES user(userid),
  CONSTRAINT expense_groupid_fk FOREIGN KEY (groupid) REFERENCES groupe(groupid)
);

CREATE TABLE user_group (
  userid INT(4) NOT NULL,
  groupid INT(4) NOT NULL,
  CONSTRAINT usergroup_user_fk FOREIGN KEY (userid) REFERENCES user(userid),
  CONSTRAINT usergroup_group_fk FOREIGN KEY (groupid) REFERENCES groupe(groupid)
);

CREATE TABLE pays (
  expenseid INT(4) NOT NULL,
  userid INT(4) NOT NULL,
  payed INT(6) NOT NULL,
  total INT(6) NOT NULL,
  CONSTRAINT pays_expenseid_fk FOREIGN KEY (expenseid) REFERENCES expense(expenseid),
  CONSTRAINT pays_userid_fk FOREIGN KEY (userid) REFERENCES user(userid)
);