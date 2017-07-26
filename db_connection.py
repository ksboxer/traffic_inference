import mySQLdb

def connect():
	MySQLdb.connect(host="216.165.70.11",    # your host, usually localhost
                     user="root",         # your username
                     passwd="1234",  # your password
                     db="IoT_testing")        # name of the data base