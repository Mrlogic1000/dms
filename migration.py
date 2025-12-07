from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime, timedelta

DB_NAME = 'dms'

TABLES = {}
TABLES['devices'] = (
    "CREATE TABLE `devices` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(200) NOT NULL,"
    "  `model` varchar(200) NOT NULL,"
    "  `mac` varchar(200) NOT NULL,"
    "  `sn` varchar(200) ,"
    "  `purchase_date` varchar(200),"
    "  `status` varchar(200) ,"
    "  `device_type` varchar(200) ,"
    "  `manufacture` varchar(200) ,"
    "  `location` varchar(200) ,"
    "  `ip` varchar(200) ,"
    "  `create_at` varchar(200),"
    "  `update_at` varchar(200),"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['maintenances'] = (
    "CREATE TABLE `maintenances` ("
    "  `maintenance_id` char(4) NOT NULL,"
    "  `device_id` int NOT NULL,"
    "  `old_value` varchar(200),"
    "  `new_value` varchar(200),"
    "  `description` text NOT NULL,"
    "  `create_at` varchar(200),"
    "  PRIMARY KEY (`maintenance_id`), "
     "  CONSTRAINT `maintenance_ibfk_1` FOREIGN KEY (`device_id`) "
    "     REFERENCES `devices` (`id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

# TABLES['salaries'] = (
#     "CREATE TABLE `salaries` ("
#     "  `emp_no` int(11) NOT NULL,"
#     "  `salary` int(11) NOT NULL,"
#     "  `from_date` date NOT NULL,"
#     "  `to_date` date NOT NULL,"
#     "  PRIMARY KEY (`emp_no`,`from_date`), KEY `emp_no` (`emp_no`),"
#     "  CONSTRAINT `salaries_ibfk_1` FOREIGN KEY (`emp_no`) "
#     "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE"
#     ") ENGINE=InnoDB")

# TABLES['dept_emp'] = (
#     "CREATE TABLE `dept_emp` ("
#     "  `emp_no` int(11) NOT NULL,"
#     "  `dept_no` char(4) NOT NULL,"
#     "  `from_date` date NOT NULL,"
#     "  `to_date` date NOT NULL,"
#     "  PRIMARY KEY (`emp_no`,`dept_no`), KEY `emp_no` (`emp_no`),"
#     "  KEY `dept_no` (`dept_no`),"
#     "  CONSTRAINT `dept_emp_ibfk_1` FOREIGN KEY (`emp_no`) "
#     "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE,"
#     "  CONSTRAINT `dept_emp_ibfk_2` FOREIGN KEY (`dept_no`) "
#     "     REFERENCES `departments` (`dept_no`) ON DELETE CASCADE"
#     ") ENGINE=InnoDB")

# TABLES['dept_manager'] = (
#     "  CREATE TABLE `dept_manager` ("
#     "  `emp_no` int(11) NOT NULL,"
#     "  `dept_no` char(4) NOT NULL,"
#     "  `from_date` date NOT NULL,"
#     "  `to_date` date NOT NULL,"
#     "  PRIMARY KEY (`emp_no`,`dept_no`),"
#     "  KEY `emp_no` (`emp_no`),"
#     "  KEY `dept_no` (`dept_no`),"
#     "  CONSTRAINT `dept_manager_ibfk_1` FOREIGN KEY (`emp_no`) "
#     "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE,"
#     "  CONSTRAINT `dept_manager_ibfk_2` FOREIGN KEY (`dept_no`) "
#     "     REFERENCES `departments` (`dept_no`) ON DELETE CASCADE"
#     ") ENGINE=InnoDB")

# TABLES['titles'] = (
#     "CREATE TABLE `titles` ("
#     "  `emp_no` int(11) NOT NULL,"
#     "  `title` varchar(50) NOT NULL,"
#     "  `from_date` date NOT NULL,"
#     "  `to_date` date DEFAULT NULL,"
#     "  PRIMARY KEY (`emp_no`,`title`,`from_date`), KEY `emp_no` (`emp_no`),"
#     "  CONSTRAINT `titles_ibfk_1` FOREIGN KEY (`emp_no`)"
#     "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE"
#     ") ENGINE=InnoDB")

cnx = mysql.connector.connect(user='root', password='Key@a1b2',
                              host='127.0.0.1',
                              )

# cnx = mysql.connector.connect(user='root')
cursor = cnx.cursor()


def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)


for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")




menu = ['name','model','mac','sn','purchase_date','status','device_type','manufacture','location','ip','create_at','update_at']
dic = {
    'name':'Router',
    'model':'cr8377474',
    'mac':'A1:B2:C3:D4:E5:F6',
    'sn':'sieuurpwe7494',
    'purchase_date':'9999 1 1',
    'status':'Active',
    'device_type':'Router',
    'manufacture':'Mikrotik',
    'location':'GTI',
    'ip':'172.3.100.1',
    'create_at':date(9999, 1, 1),
    'update_at':'9999 1 1',
    }

tomorrow = datetime.now().date() + timedelta(days=1)
columns = ",".join(dic.keys())
placeholders = ', '.join(['%s'] * len(dic))
# data_dic = f'({", ".join(dic.values())})'
# print(data_dic)

add_device = ("INSERT INTO devices "
               f"({columns}) "               
               f"VALUES ({placeholders})"
               )
print(add_device)

# data_device = ('Geert', 'Vanderkelen', tomorrow, 'M', date(1977, 6, 14))
cursor.execute(add_device, tuple(dic.values()))
device_no = cursor.lastrowid
print(device_no)

# add_salary = ("INSERT INTO salaries "
#               "(emp_no, salary, from_date, to_date) "
#               "VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)")


# Insert new employee


# Insert salary information
# data_salary = {
#   'emp_no': emp_no,
#   'salary': 50000,
#   'from_date': tomorrow,
#   'to_date': date(9999, 1, 1),
# }
# cursor.execute(add_salary, data_salary)

# Make sure data is committed to the database
cnx.commit()

cursor.close()
cnx.close()


class Migration:
    def __init__(self,db_name,user,password,host):
        self.DB_NAME = db_name
        self.cnx = mysql.connector.connect(user, password,host)
        self.cursor = self.cnx.cursor()
    
    def create_database(self):
        try:
            self.cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.DB_NAME))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
    def select_db(self):
        try:
            self.cursor.execute("USE {}".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Database {} does not exists.".format(DB_NAME))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                create_database(cursor)
                print("Database {} created successfully.".format(DB_NAME))
                cnx.database = DB_NAME
            else:
                print(err)
                exit(1)

    def create_table(self,TABLES):
        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                self.cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")

