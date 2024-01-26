import sqlite3

## Connect to SQlite
connection=sqlite3.connect("student.db")

# Create a cursor object to insert record,create table
cursor=connection.cursor()

### Creating a table
table_info="""
"`  Create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),
SECTION VARCHAR(25),MARKS INT);

"""
cursor.execute(table_info)

### Inserting Values
cursor.execute("INSERT INTO STUDENT VALUES ('Alice', 'Machine Learning', 'B', 75)")
cursor.execute("INSERT INTO STUDENT VALUES ('Bob', 'Web Development', 'C', 92)")
cursor.execute("INSERT INTO STUDENT VALUES ('Charlie', 'DEVOPS', 'B', 88)")
cursor.execute("INSERT INTO STUDENT VALUES ('David', 'Machine Learning', 'A', 95)")
cursor.execute("INSERT INTO STUDENT VALUES ('Eva', 'Web Development', 'A', 80)")
cursor.execute("INSERT INTO STUDENT VALUES ('Frank', 'Data Scienc?-    e', 'C', 78)")
cursor.execute("INSERT INTO STUDENT VALUES ('Grace', 'Web Development', 'A', 89)")
cursor.execute("INSERT INTO STUDENT VALUES ('Helen', 'Machine Learning', 'B', 94)")
cursor.execute("INSERT INTO STUDENT VALUES ('Isaac', 'Data Science', 'B', 85)")
cursor.execute("INSERT INTO STUDENT VALUES ('Jack', 'DEVOPS', 'C', 70)")

### Displaying values
print("The isnerted records are")
data=cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)

## Commit your changes int he databse
connection.commit()
connection.close()