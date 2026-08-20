from task_manager_class import TaskManager
from file_manager import save_tasks, load_tasks


manager = TaskManager()


while True:

    manager.show_menu()

    choice = input("Enter your choice: ")

    if choice == "7":
        print("Goodbye!")
        break

    manager.process_choice(choice)

