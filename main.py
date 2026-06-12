import flet as ft
import sqlite3

def main(page: ft.Page):
    def delete_last_task_db():
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM tasks ORDER BY id DESC LIMIT 1")
        last_task = cursor.fetchone()
        if last_task:
            cursor.execute("DELETE FROM tasks WHERE id = ?", (last_task[0],))
            conn.commit()
            deleted = True
        else:
            deleted = False
        conn.close()
        return deleted

    task_list = ft.Column()

    def delete_click(e):
        result = delete_last_task_db()
        if result:
            if len(task_list.controls) > 0:
                task_list.controls.pop()
                page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("История пуста!"))
            page.snack_bar.open = True
            page.update()

    page.add(
        ft.ElevatedButton("Удалить последнее", on_click=delete_click),
        task_list
    )

ft.app(target=main)