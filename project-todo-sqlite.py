import sqlite3
import datetime

class Database:
    def __init__(self, path="todos.db"):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS todos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        self.connection.commit()

    # CREATE
    def add_to_db(self, todo):
        self.cursor.execute(
            "INSERT INTO todos(text, created_at) VALUES(?, ?)",
            (todo.text, todo.date.strftime("%Y-%m-%d %H:%M:%S"))
        )
        self.connection.commit()
        print("ToDo Added!\n")

    # UPDATE (by real DB id)
    def replace_todo_db(self, row_id, newTodo):
        self.cursor.execute(
            "UPDATE todos SET text=? WHERE id=?",
            (newTodo.text, row_id)
        )
        self.connection.commit()
        print("ToDo Replaced!\n")

    # DELETE (by real DB id)
    def delete_todo_db(self, row_id):
        self.cursor.execute("DELETE FROM todos WHERE id=?", (row_id,))
        self.connection.commit()
        print("ToDo Deleted!\n")

    # READ
    def show_todos(self):
        self.cursor.execute("SELECT id, text, created_at FROM todos ORDER BY id")
        return self.cursor.fetchall()

    def close(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()


class Manager:
    def __init__(self, database):
        self.database = database

    def add(self, todo):
        self.database.add_to_db(todo)

    def replace_todo(self, row_id, newTodo):
        self.database.replace_todo_db(row_id, newTodo)

    def delete_todo(self, row_id):
        self.database.delete_todo_db(row_id)

    def showAll(self):
        data = self.database.show_todos()
        if data:
            print("\n")
            for index, (row_id, text, created_at) in enumerate(data, 1):
                print(f"{'-' * 25} {index} {'-' * 25}")
                print(f"ID: {row_id}\nDate: {created_at}\nToDo: {text}")
                print("-" * 53)
        else:
            print("\nThere are not ToDos in the database!")

    # helper -> return real DB id from visible number
    def pick_row_id(self):
        data = self.database.show_todos()
        if not data:
            print("There are not ToDos in the database!")
            return None

        self.showAll()
        oldTodoNumber = input("Choose ToDo N from list to replace or delete: ").strip()
        if not oldTodoNumber.isdigit():
            print("Please enter the digit!")
            return None

        n = int(oldTodoNumber)
        if n < 1 or n > len(data):
            print(f"Please choose ToDo N between 1 - {len(data)} range!")
            return None

        row_id = data[n - 1][0]
        return row_id


class ToDo:
    def __init__(self, text):
        self.text = text
        self.date = datetime.datetime.now()

    def __str__(self):
        return f"Date: {self.date.strftime('%d/%m/%Y %H:%M')}\nToDo: {self.text}"


def todo_checker(manager):
    return manager.pick_row_id()


def menu():
    database = Database()
    manager = Manager(database)
    choice = None

    try:
        while choice != "q":
            print("ToDo List Menu:")
            print("a) Add Todo")
            print("r) Replace Todo")
            print("d) Delete Todo")
            print("s) Show all Todos")
            print("q) Quit")

            choice = input("Action: ").strip().lower()

            if choice == "a":
                text = input("ToDo: ").strip()
                if text:
                    todo = ToDo(text)
                    manager.add(todo)
                else:
                    print("Empty ToDo is not allowed.")

            elif choice == "r":
                row_id = todo_checker(manager)
                if row_id:
                    text = input("New ToDo: ").strip()
                    if text:
                        newTodo = ToDo(text)
                        manager.replace_todo(row_id, newTodo)
                    else:
                        print("Empty ToDo is not allowed.")

            elif choice == "d":
                row_id = todo_checker(manager)
                if row_id:
                    manager.delete_todo(row_id)

            elif choice == "s":
                manager.showAll()

            elif choice == "q":
                pass

            else:
                print("Unknown option.")

    finally:
        database.close()


menu()
