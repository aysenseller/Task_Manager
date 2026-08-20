from task import Task
from task_manager_class import TaskManager
import json


def test_task_creation():

    task = Task(
        "Python",
        False,
        "2026-08-19",
        "High",
        "2026-08-25",
        1
    )

    assert task.title == "Python"


def test_task_is_not_completed():

    task = Task(
        "Python",
        False,
        "2026-08-19",
        "High",
        "2026-08-25",
        1
    )

    assert task.completed == False


def test_add_task(monkeypatch):

    manager = TaskManager()

    inputs = iter([
        "Python çalış",
        "High",
        "2026-08-25"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    manager.add_task()

    assert len(manager.tasks) == 1
    assert manager.tasks[0].title == "Python çalış"
    assert manager.tasks[0].priority == "High"
    assert manager.tasks[0].due_date == "2026-08-25"
    assert manager.tasks[0].completed == False
    assert manager.tasks[0].id == 1


def test_complete_task(monkeypatch):

    manager = TaskManager()

    task = Task(
        "Python",
        False,
        "2026-08-19",
        "High",
        "2026-08-25",
        1
    )

    manager.tasks.append(task)

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "1"
    )

    manager.complete_task()

    assert manager.tasks[0].completed == True


def test_delete_task(monkeypatch):

    manager = TaskManager()

    task = Task(
        "Python",
        False,
        "2026-08-19",
        "High",
        "2026-08-25",
        1
    )

    manager.tasks.append(task)

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "1"
    )

    manager.delete_task()

    assert len(manager.tasks) == 0


# ---------------- EDIT TASK ----------------


def test_edit_title(monkeypatch):

    manager = TaskManager()

    task = Task(
        "Python",
        False,
        "2026-08-19",
        "High",
        "2026-08-25",
        1
    )

    manager.tasks.append(task)

    inputs = iter([
        "1",
        "1",
        "Java"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    manager.edit_task()

    assert manager.tasks[0].title == "Java"


def test_edit_priority(monkeypatch):

    manager = TaskManager()

    task = Task(
        "Python",
        False,
        "2026-08-19",
        "High",
        "2026-08-25",
        1
    )

    manager.tasks.append(task)

    inputs = iter([
        "1",
        "2",
        "Low"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    manager.edit_task()

    assert manager.tasks[0].priority == "Low"


def test_edit_due_date(monkeypatch):

    manager = TaskManager()

    task = Task(
        "Python",
        False,
        "2026-08-19",
        "High",
        "2026-08-25",
        1
    )

    manager.tasks.append(task)

    inputs = iter([
        "1",
        "4",
        "2026-09-01"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs)
    )

    manager.edit_task()

    assert manager.tasks[0].due_date == "2026-09-01"


# ---------------- SEARCH ----------------


def test_search_by_id():

    manager = TaskManager()

    task = Task(
        "Python",
        False,
        "2026-08-19",
        "High",
        "2026-08-25",
        1
    )

    manager.tasks.append(task)

    found_task = None

    for task in manager.tasks:
        if task.id == 1:
            found_task = task

    assert found_task is not None
    assert found_task.title == "Python"


# ---------------- FILTER ----------------


def test_filter_by_priority():

    manager = TaskManager()

    task1 = Task(
        "Python",
        False,
        "2026-08-19",
        "High",
        "2026-08-25",
        1
    )

    task2 = Task(
        "Java",
        False,
        "2026-08-19",
        "Low",
        "2026-08-30",
        2
    )

    manager.tasks.append(task1)
    manager.tasks.append(task2)

    high_tasks = [
        task for task in manager.tasks
        if task.priority == "High"
    ]

    assert len(high_tasks) == 1
    assert high_tasks[0].title == "Python"


# ---------------- SORT ----------------


def test_sort_by_due_date():

    manager = TaskManager()

    task1 = Task(
        "Python",
        False,
        "2026-08-19",
        "High",
        "2026-08-30",
        1
    )

    task2 = Task(
        "Java",
        False,
        "2026-08-19",
        "Low",
        "2026-08-25",
        2
    )

    manager.tasks.append(task1)
    manager.tasks.append(task2)

    sorted_tasks = sorted(
        manager.tasks,
        key=lambda task: task.due_date
    )

    assert sorted_tasks[0].title == "Java"
    assert sorted_tasks[1].title == "Python"


# ---------------- DELETE COMPLETED ----------------


def test_delete_completed_tasks():

    manager = TaskManager()

    task1 = Task(
        "Python",
        True,
        "2026-08-19",
        "High",
        "2026-08-25",
        1
    )

    task2 = Task(
        "Java",
        False,
        "2026-08-19",
        "Low",
        "2026-08-30",
        2
    )

    manager.tasks.append(task1)
    manager.tasks.append(task2)

    manager.delete_completed_tasks()

    assert len(manager.tasks) == 1
    assert manager.tasks[0].title == "Java"

def test_save_tasks(monkeypatch, tmp_path):

    manager = TaskManager()

    task = Task(
        "Python",
        False,
        "2026-08-19",
        "High",
        "2026-08-25",
        1
    )

    manager.tasks.append(task)

    file_path = tmp_path / "tasks.json"

    monkeypatch.chdir(tmp_path)

    manager.save_tasks()

    assert file_path.exists()

def test_load_tasks(monkeypatch, tmp_path):

    manager = TaskManager()

    file_path = tmp_path / "tasks.json"

    task_data = [
        {
            "title": "Python",
            "completed": False,
            "date": "2026-08-19",
            "priority": "High",
            "due_date": "2026-08-25",
            "id": 1
        }
    ]

    with open(file_path, "w") as file:
        json.dump(task_data, file)

    monkeypatch.chdir(tmp_path)

    manager.load_tasks()

    assert len(manager.tasks) == 1
    assert manager.tasks[0].title == "Python"
    assert manager.tasks[0].priority == "High"
    assert manager.tasks[0].due_date == "2026-08-25"
    assert manager.tasks[0].id == 1

def test_complete_task_invalid_id(monkeypatch):

    manager = TaskManager()

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "999"
    )

    manager.complete_task()

    assert len(manager.tasks) == 0

    
