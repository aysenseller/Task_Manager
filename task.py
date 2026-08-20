class Task:

    def __init__(self,title,completed,date,priority,due_date, id):
        self.title = title
        self.completed = completed
        self.date = date
        self.priority = priority
        self.due_date = due_date
        self.id = id
    def __str__(self):
        if self.completed:
            return f"[{self.id}][X] {self.title} - {self.priority} - Created: {self.date} - Due: {self.due_date}"
        else:
            return f"[{self.id}][ ] {self.title} - {self.priority} - Created: {self.date} - Due: {self.due_date}"
    def to_dict(self):
        return {
            "title" : self.title,
            "completed" : self.completed,
            "date" : self.date,
            "priority" : self.priority,
            "due_date" : self.due_date,
            "id" : self.id
        }
