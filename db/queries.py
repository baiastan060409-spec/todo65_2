create_tasks_table = """
   CREATE TABLE IF NOT EXISTS tasks (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   task TEXT NOT NULL
   )
"""


#CREATE
insert_task = 'INSERT INTO tasks (tasks) VALUES (?)'

#READ
select_tasks = "SELECT id, task FROM tasks"

#UPDATE
update_task = 'UPDATE tasks SET task = ? WHERE id = ?'

#DELETE
delete-task = 'DELETE FROM tasks WHERE id = ?'