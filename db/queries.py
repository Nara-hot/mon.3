create_table ="""CREATE TABLE IF NOT EXISIS TASKS(
                 ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 TASK TEXT NOT NULL)"""


#CRUD - CREATE - READ - UPDATE - DELETE

# CREATE
insert_task ='INSERT INTO tasks (task) values(?)'

#READ
select_task = 'SELECT id, task FROM tasks'

#UPDATE
uptade_task = "UPDATE TASK SET task"
