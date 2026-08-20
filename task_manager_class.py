from datetime import date, timedelta
from task import Task
import json


class TaskManager:

    print ("Task Manager started!")
    
    def __init__(self):
        self.tasks = []
        self.next_id = 1
    # ---------------- ADD ----------------

    def add_task(self):
        task_input = input("Enter your task: ")

        while True:
            priority_input = input(
                "Enter task's priority (High/Medium/Low): "
            )

            if priority_input.lower() in ["high", "medium", "low"]:
                priority_input = priority_input.capitalize()
                break

            print("Invalid priority! Please enter High, Medium or Low.")

        today = str(date.today())

        while True:
            due_date = input(
                "Enter due date (YYYY-MM-DD): "
            )

            try:
                date.fromisoformat(due_date)
                break
            except ValueError:
                print("Invalid date! Please use YYYY-MM-DD.")

        task_id = self.next_id
        self.next_id += 1

        task = Task(
            task_input,
            False,
            today,
            priority_input,
            due_date,
            task_id
        )

        self.tasks.append(task)

        print("Task added successfully!")

    # ---------------- SHOW ----------------

    def show_tasks(self):
        if not self.tasks:
            print("No tasks found!")
            return

        for task in self.tasks:
            print(task)

    # ---------------- COMPLETE ----------------

    def complete_task(self):
        found = False

        try:
            task_id = int(
                input("Enter task ID to complete: ")
            )
        except ValueError:
            print("Please enter a valid number!")
            return

        for task in self.tasks:
            if task_id == task.id:

                if task.completed:
                    print("Task is already completed!")
                else:
                    task.completed = True
                    print("Task completed successfully!")

                found = True
                break

        if not found:
            print("Task ID not found!")

    # ---------------- DELETE ----------------

    def delete_task(self):
        found = False

        try:
            task_id = int(
                input("Enter task ID to delete: ")
            )
        except ValueError:
            print("Please enter a valid number!")
            return

        for task in self.tasks:
            if task_id == task.id:
                self.tasks.remove(task)

                print("Deleting process is successful!")

                found = True
                break

        if not found:
            print("Task ID not found!")

    # ---------------- EDIT ----------------

    def edit_task(self):
        found = False

        try:
            task_id = int(
                input("Enter task ID that you want to edit: ")
            )
        except ValueError:
            print("Please enter a valid number!")
            return

        for task in self.tasks:

            if task_id == task.id:

                print("1-Edit Title")
                print("2-Edit Priority")
                print("3-Edit Completed Status")
                print("4-Edit Due Date")

                choice = input("What do you want to edit? ")

                # TITLE
                if choice == "1":
                    new_title = input(
                        "Enter task's new name: "
                    )

                    task.title = new_title

                # PRIORITY
                elif choice == "2":

                    while True:
                        new_priority = input(
                            "Enter task's new priority: "
                        )

                        if new_priority.lower() in [
                            "high",
                            "medium",
                            "low"
                        ]:
                            new_priority = new_priority.capitalize()
                            break

                        print(
                            "Invalid priority! "
                            "Please enter High, Medium or Low."
                        )

                    task.priority = new_priority

                # COMPLETED
                elif choice == "3":

                    new_completed_status = input(
                        "Completed? (True/False): "
                    ).lower()

                    if new_completed_status == "true":
                        task.completed = True

                    elif new_completed_status == "false":
                        task.completed = False

                    else:
                        print(
                            "Invalid status! "
                            "Please enter True or False."
                        )
                        return

                # DUE DATE
                elif choice == "4":

                    while True:
                        new_due_date = input(
                            "Enter task's new due date "
                            "(YYYY-MM-DD): "
                        )

                        try:
                            date.fromisoformat(new_due_date)
                            break

                        except ValueError:
                            print(
                                "Invalid date! "
                                "Please use YYYY-MM-DD."
                            )

                    task.due_date = new_due_date

                else:
                    print("Invalid choice!")
                    return

                print("Task updated successfully!")

                found = True
                break

        if not found:
            print("Task ID not found!")

    # ---------------- STATISTICS ----------------

    def statistics(self):
        completed_count = 0
        high_count = 0
        medium_count = 0
        low_count = 0

        for task in self.tasks:

            if task.completed:
                completed_count += 1

            if task.priority == "High":
                high_count += 1

            elif task.priority == "Medium":
                medium_count += 1

            elif task.priority == "Low":
                low_count += 1

        print(f"Total Tasks: {len(self.tasks)}")
        print(f"Completed Tasks: {completed_count}")
        print(f"Pending Tasks: {len(self.tasks) - completed_count}")

        print(f"High Priority: {high_count}")
        print(f"Medium Priority: {medium_count}")
        print(f"Low Priority: {low_count}")

    # ---------------- COMPLETED ----------------

    def show_completed_tasks(self):
        found = False

        for task in self.tasks:
            if task.completed:
                print(task)
                found = True

        if not found:
            print("No completed tasks found!")

    # ---------------- PENDING ----------------

    def show_pending_tasks(self):
        found = False

        for task in self.tasks:
            if not task.completed:
                print(task)
                found = True

        if not found:
            print("No pending tasks found!")

    # ---------------- SEARCH ----------------

    def search_task(self):
        search_input = input(
            "Enter the name to search for: "
        )

        found = False

        for task in self.tasks:
            if search_input.lower() in task.title.lower():
                print(task)
                found = True

        if not found:
            print("No task that is searched found!")

    # ---------------- SEARCH BY ID ----------------

    def search_by_id(self):
        try:
            task_id = int(
                input("Enter task ID to search: ")
            )
        except ValueError:
            print("Please enter a valid number!")
            return

        for task in self.tasks:
            if task.id == task_id:
                print(task)
                return

        print("Task ID not found!")

    # ---------------- PRIORITY FILTER ----------------

    def filter_by_priority(self):
        found = False

        priority = input(
            "Enter the priority that you want to filter: "
        )

        for task in self.tasks:
            if task.priority.lower() == priority.lower():
                print(task)
                found = True

        if not found:
            print("No tasks found with this priority!")

    # ---------------- STATUS + PRIORITY FILTER ----------------

    def filter_tasks(self):
        found = False

        priority = input(
            "Enter priority (High/Medium/Low): "
        )

        status = input(
            "Enter status (Completed/Pending): "
        )

        for task in self.tasks:

            if (
                task.priority.lower() == priority.lower()
                and
                (
                    task.completed
                    if status.lower() == "completed"
                    else not task.completed
                )
            ):
                print(task)
                found = True

        if not found:
            print("No matching tasks found!")

    # ---------------- SORT PRIORITY ----------------

    def sort_by_priority(self):
        priority_order = {
            "High": 1,
            "Medium": 2,
            "Low": 3
        }

        sorted_tasks = sorted(
            self.tasks,
            key=lambda task: priority_order[task.priority]
        )

        for task in sorted_tasks:
            print(task)

    # ---------------- SORT TITLE ----------------

    def sort_by_title(self):
        sorted_tasks = sorted(
            self.tasks,
            key=lambda task: task.title.lower()
        )

        for task in sorted_tasks:
            print(task)

    # ---------------- SORT DUE DATE ----------------

    def sort_by_due_date(self):
        sorted_tasks = sorted(
            self.tasks,
            key=lambda task: date.fromisoformat(task.due_date)
        )

        for task in sorted_tasks:
            print(task)

    # ---------------- UPCOMING ----------------

    def upcoming_tasks(self):
        found = False
        today = date.today()

        for task in self.tasks:

            due_date = date.fromisoformat(task.due_date)
            difference = (due_date - today).days

            if 0 <= difference <= 7 and not task.completed:
                print(task)
                found = True

        if not found:
            print("No upcoming tasks found!")

    # ---------------- OVERDUE ----------------

    def show_overdue_tasks(self):
        found = False
        today = date.today()

        for task in self.tasks:

            due_date = date.fromisoformat(task.due_date)

            if due_date < today and not task.completed:
                print(task)
                found = True

        if not found:
            print("No overdue tasks found!")

    # ---------------- DELETE COMPLETED ----------------

    def delete_completed_tasks(self):
        remaining_tasks = []
        deleted = 0

        for task in self.tasks:

            if task.completed:
                deleted += 1
            else:
                remaining_tasks.append(task)

        self.tasks[:] = remaining_tasks

        if deleted == 0:
            print("No completed tasks found!")
        else:
            print(
                f"{deleted} completed task(s) deleted!"
            )

    def save_tasks(self):
        data = []
        for task in self.tasks:
            data.append(task.to_dict())

        with open("tasks.json", "w") as file:
            json.dump(data, file, indent=4)

        print("Tasks saved successfully!")

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                data = json.load(file)
            self.tasks = []
            for item in data:
                task = Task(
                    item["title"],
                    item["completed"],
                    item["date"],
                    item["priority"],
                    item["due_date"],
                    item["id"]
                )

                self.tasks.append(task)
            if self.tasks:
                self.next_id = max(task.id for task in self.tasks) + 1
            else:
                self.next_id = 1
        
            print("Tasks loaded successfully!")

        except FileNotFoundError:
                print("No saved tasks found!")

    def show_menu(self):

        print("\n========== TASK MANAGER ==========")
        print("1- Add Task")
        print("2- Show Tasks")
        print("3- Complete Task")
        print("4- Delete Task")
        print("5- Save Tasks")
        print("6- Load Tasks")
        print("7- Exit")
        print("8- Statistics")
        print("9- Edit Task")
        print("10- Show Completed Tasks")
        print("11- Show Pending Tasks")
        print("12- Search Task")
        print("13- Search Task By ID")
        print("14- Sort By Priority")
        print("15- Sort By Title")
        print("16- Sort By Due Date")
        print("17- Show Overdue Tasks")
        print("18- Show Upcoming Tasks")
        print("19- Filter By Priority")
        print("20- Filter By Priority And Status")
        print("21- Delete Completed Tasks")

    def process_choice(self,choice):
        if choice == "1":
            self.add_task()

        elif choice == "2":
            self.show_tasks()

        elif choice == "3":
            self.complete_task()

        elif choice == "4":
            self.delete_task()

        elif choice == "5":
            self.save_tasks()
            print("Tasks saved successfully!")

        elif choice == "6":
            self.load_tasks()
            print("Tasks loaded successfully!")

        elif choice == "8":
            self.statistics()

        elif choice == "9":
            self.edit_task()

        elif choice == "10":
            self.show_completed_tasks()

        elif choice == "11":
            self.show_pending_tasks()

        elif choice == "12":
            self.search_task()

        elif choice == "13":
            self.search_by_id()

        elif choice == "14":
            self.sort_by_priority()

        elif choice == "15":
            self.sort_by_title()

        elif choice == "16":
            self.sort_by_due_date()

        elif choice == "17":
            self.show_overdue_tasks()

        elif choice == "18":
            self.upcoming_tasks()

        elif choice == "19":
            self.filter_by_priority()

        elif choice == "20":
            self.filter_tasks()

        elif choice == "21":
            self.delete_completed_tasks()

        else:
            print("Invalid choice!")