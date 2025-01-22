from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from tabulate import tabulate
import json


class Task(ABC):
    
    id=0

    def __init__(self,name,deadline,status,priority,color):
        Task.id += 1  
        self.id = Task.id
        self.name=name
        self.deadline=datetime.strptime(deadline, '%Y-%m-%d')
        self.status=status
        self.priority=priority
        self.color=color

    @abstractmethod
    def task_type(self):
        pass

    @staticmethod
    def days_to_accomplish_task():
        pass

    def __str__(self):
        return (f"Task ID: {self.id}, Name: {self.name}, Deadline: {self.deadline}, "
                f"Status: {self.status}, Priority: {self.priority}, Color: {self.color}")

    
class PersonalTask(Task):

    def __init__(self,name,deadline,status,):
        super().__init__(name,deadline,status,priority="Low",color="Blue")

    def task_type(self):
        return "Personal Task"

class WorkTask(Task):
    
    def __init__(self,name,deadline,status,):
        super().__init__(name,deadline,status,priority="High",color="Red")

    def task_type(self):
        return "Work Task"


class TaskManagement:
    def __init__(self):
        self.tasks = []
        self.load_tasks_from_json()

    def add_task(self,task):
        if task not in self.tasks:
            self.tasks.append(task)
            print("Task added successfully!")
            self.save_tasks_to_json()

    def display_tasks(self):
        if not self.tasks:
            print("No tasks available.")
            return
       
        headers = ["ID", "Name", "Deadline", "Status", "Priority", "Color"]
        table = [
            [task.id, task.name, task.deadline.strftime('%Y-%m-%d'), task.status, task.priority, task.color]
            for task in self.tasks  
                ]
        
        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

    def save_tasks_to_json(self):
        tasks_data = [
            {"id": task.id, "name": task.name, "deadline": task.deadline.strftime('%Y-%m-%d'),
             "status": task.status, "priority": task.priority, "color": task.color}
            for task in self.tasks
        ]
        with open('tasks.json', 'w', encoding='utf-8') as file:
            json.dump(tasks_data, file, ensure_ascii=False, indent=4)
        print("Tasks saved to JSON.")

    def load_tasks_from_json(self):
        try:
            with open('tasks.json', 'r', encoding='utf-8') as file:
                tasks_data = json.load(file)
                for task_data in tasks_data:
                    task_type = "personal" if task_data["priority"] == "Low" else "work"
                    task = TaskScheduling.create_task(task_type, task_data["name"], task_data["deadline"], task_data["status"])
                    if task:
                        task.id = task_data["id"]  
                        task.priority = task_data["priority"]
                        task.color = task_data["color"]
                        self.tasks.append(task)
                print("Tasks loaded from JSON.")
        except FileNotFoundError:
            print("No existing tasks found, starting fresh.")

class TaskEditing():
    
    @staticmethod
    def set_task_status(task, new_status,task_manager):
        task.status = new_status
        task_manager.save_tasks_to_json()

    @staticmethod
    def set_task_priority(task, new_priority,task_manager):
        task.priority = new_priority
        task_manager.save_tasks_to_json()

    @staticmethod
    def set_task_deadline(task, new_deadline,task_manager):
        task.deadline = datetime.strptime(new_deadline, '%Y-%m-%d')
        task_manager.save_tasks_to_json()



class TaskTracking():
    def __init__(self, task_manager):
        self.task_manager = task_manager
    
    @staticmethod
    def get_task_status(task):
        return task.status

    @staticmethod
    def get_task_deadline(task):
        return task.deadline

    @staticmethod
    def get_task_color(task):
        return task.color

    def get_task_by_id(self, task_id):
        for task in self.task_manager.tasks:
            if task.id == task_id:
                return task
        return None



class TaskScheduling():
    SPECIAL_KEYWORDS = {
        "today": datetime.now().date(),
        "tomorrow": (datetime.now() + timedelta(days=1)).date(),
        "next week": (datetime.now() + timedelta(weeks=1)).date()
    }

    @staticmethod
    def create_task(task_type, name, deadline_keyword, status):
        if deadline_keyword in TaskScheduling.SPECIAL_KEYWORDS:
            deadline = TaskScheduling.SPECIAL_KEYWORDS[deadline_keyword].strftime('%Y-%m-%d')
        else:
            deadline = deadline_keyword  # Assume the user provided a valid date

        if task_type.lower() == "personal":
            return PersonalTask(name, deadline, status)
        elif task_type.lower() == "work":
            return WorkTask(name, deadline, status)
        else:
            print("Invalid task type!")
            return None



if __name__ == "__main__":
    task_manager = TaskManagement()
    task_tracking=TaskTracking(task_manager)

    def menu():
        while True:
            print("\n1) Add Task \n2) Display Tasks \n3) Edit Task \n0) Exit")
            try:
                choice = int(input("\nPlease select the operation you want to perform: "))
                if choice == 0:
                    print("Exiting program. Goodbye!")
                    break
                elif choice == 1:
                    name = input("Enter task name: ")
                    deadline = input("Enter deadline (YYYY-MM-DD or keyword like 'today', 'tomorrow','next week'): ").strip().lower()
                    status = input("Enter status (e.g., In Progress, Completed): ")
                    task_type = input("Enter task type (Personal/Work): ").strip().lower()

                    task = TaskScheduling.create_task(task_type, name, deadline, status)
                    if task:
                        task_manager.add_task(task)
                elif choice == 2:
                    task_manager.display_tasks()
                elif choice == 3:
                    task_id = int(input("Enter the Task ID to edit: "))
                    task = task_tracking.get_task_by_id(task_id)

                    if task:
                        print("1) Change Status \n2) Change Priority \n3) Change Deadline")
                        edit_choice = int(input("Select an edit operation: "))
                        if edit_choice == 1:
                            new_status = input("Enter new status: ")
                            TaskEditing.set_task_status(task, new_status,task_manager)
                        elif edit_choice == 2:
                            new_priority = input("Enter new priority: ")
                            TaskEditing.set_task_priority(task, new_priority,task_manager)
                        elif edit_choice == 3:
                            new_deadline = input("Enter new deadline (YYYY-MM-DD): ")
                            TaskEditing.set_task_deadline(task, new_deadline,task_manager)
                        print("Task updated successfully!")
                    else:
                        print("Task not found.")
                else:
                    print("Invalid choice, try again!")
            except ValueError:
                print("Please enter a valid number!")

    menu()
