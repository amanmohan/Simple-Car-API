import sqlite3
conn = sqlite3.connect('tesla.db')


print "Opened database successfully";


cursor = conn.execute("SELECT id, name, address, salary  from COMPANY")
for row in cursor:
	print row
conn.close()