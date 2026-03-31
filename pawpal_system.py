from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import uuid


@dataclass
class Task:
    """Dataclass representing a pet task"""
    task_name: str
    duration: int  # in minutes
    priority: int  # 1-3, where 1 is highest
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))  # Auto-generated unique ID
    prefered_time: Optional[str] = None  # "morning" or "afternoon"
    frequency: str = "daily"    # "daily", "weekly", or "monthly"
    completed: bool = False     # completion status
    
    def update(self, name: str = None, duration: int = None, priority: int = None, prefered_time: str = None, frequency: str = None) -> bool:
        """Update task details with validation
        
        Validates input before updating:
        - name: not empty string
        - duration: integer between 1-480 minutes
        - priority: integer between 1-3
        - prefered_time: "morning" or "afternoon" (optional, case-insensitive)
        - frequency: "daily", "weekly", or "monthly"
        
        Args:
            name: new task name
            duration: new duration in minutes
            priority: new priority level
            prefered_time: "morning" or "afternoon"
            frequency: "daily", "weekly", or "monthly"
            
        Returns:
            bool: True if all updates were successful, False if any validation failed
        """
        # Validate and update name
        if name is not None:
            if not isinstance(name, str) or not name:
                return False
            self.task_name = name
        
        # Validate and update duration
        if duration is not None:
            if not isinstance(duration, int) or duration <= 0 or duration > 480:
                return False
            self.duration = duration
        
        # Validate and update priority
        if priority is not None:
            if not isinstance(priority, int) or priority < 1 or priority > 3:
                return False
            self.priority = priority
        
        # Validate and update prefered_time (case-insensitive, only "morning" or "afternoon")
        if prefered_time is not None:
            prefered_time_lower = prefered_time.lower()
            if prefered_time_lower not in ["morning", "afternoon"]:
                return False
            self.prefered_time = prefered_time_lower
        
        # Validate and update frequency (only "daily", "weekly", "monthly")
        if frequency is not None:
            if not isinstance(frequency, str) or frequency.lower() not in ["daily", "weekly", "monthly"]:
                return False
            self.frequency = frequency.lower()
        
        return True


    def is_feasible(self, available_time: int) -> bool:
        """Check if task is feasible in a given available time
        
        Args:
            available_time (int): Available time in minutes (must be >= 0)
            
        Returns:
            bool: True if task duration fits in available time, False otherwise
            
        Raises:
            ValueError: If available_time is negative
        """
        if not isinstance(available_time, int) or available_time < 0:
            raise ValueError(f"Available time must be a non-negative integer, got {available_time}")
        
        return self.duration <= available_time
    
    def mark_complete(self) -> None:
        """Mark task as completed"""
        self.completed = True
    
    def __post_init__(self):
        """Post-initialization validation for Task dataclass"""
        # Validate task_name
        if not isinstance(self.task_name, str) or not self.task_name:
            raise ValueError("Task name cannot be empty")
        
        # Validate duration
        if not isinstance(self.duration, int) or self.duration <= 0 or self.duration > 480:
            raise ValueError(f"Invalid duration {self.duration}. Duration must be an integer between 1 and 480 minutes.")
        
        # Validate priority
        if not isinstance(self.priority, int) or self.priority < 1 or self.priority > 3:
            raise ValueError(f"Invalid priority {self.priority}. Priority must be an integer between 1 and 3.")
        
        # Validate prefered_time (case-insensitive, optional, only "morning" or "afternoon")
        if self.prefered_time is not None:
            if not isinstance(self.prefered_time, str) or not self.prefered_time:
                raise ValueError(f"Invalid prefered_time {self.prefered_time}. Must be a non-empty string.")
            prefered_time_lower = self.prefered_time.lower()
            if prefered_time_lower not in ["morning", "afternoon"]:
                raise ValueError(f"Invalid prefered_time '{self.prefered_time}'. Must be 'morning' or 'afternoon'.")
            self.prefered_time = prefered_time_lower
        
        # Validate frequency (only "daily", "weekly", or "monthly")
        if not isinstance(self.frequency, str) or not self.frequency:
            raise ValueError("Frequency cannot be empty")
        frequency_lower = self.frequency.lower()
        if frequency_lower not in ["daily", "weekly", "monthly"]:
            raise ValueError(f"Invalid frequency '{self.frequency}'. Must be 'daily', 'weekly', or 'monthly'.")
        self.frequency = frequency_lower


@dataclass
class Pet:
    """Dataclass representing a pet"""
    name: str
    pet_type: str
    age: int
    tasks: List[Task] = field(default_factory=list)
    
    def add_task(self, task: Task) -> None:
        """Add a task to the pet
        
        Args:
            task (Task): Task object to add
            
        Raises:
            TypeError: If task is not a Task instance
            ValueError: If a task with the same ID already exists
        """
        if not isinstance(task, Task):
            raise TypeError(f"Expected Task instance, got {type(task)}")
        
        # Check if task with same ID already exists
        if any(t.task_id == task.task_id for t in self.tasks):
            raise ValueError(f"Task with ID {task.task_id} already exists")
        
        self.tasks.append(task)
    
    def get_tasks(self) -> List[Task]:
        """Get all tasks for the pet
        
        Returns:
            List[Task]: List of all tasks for this pet
        """
        return list(self.tasks)
    
    def remove_task(self, task_id: str) -> bool:
        """Remove a task by task_id
        
        Args:
            task_id (str): ID of task to remove
            
        Returns:
            bool: True if task was removed, False if task not found
        """
        for i, task in enumerate(self.tasks):
            if task.task_id == task_id:
                self.tasks.pop(i)
                return True
        return False
    
    def get_total_duration(self) -> int:
        """Calculate total duration of all tasks
        
        Returns:
            int: Total duration in minutes of all tasks
        """
        return sum(task.duration for task in self.tasks)
    
    def __post_init__(self):
        """Post-initialization validation for Pet dataclass"""
        # Validate name
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("Pet name cannot be empty")
        
        # Validate pet_type
        if not isinstance(self.pet_type, str) or not self.pet_type:
            raise ValueError("Pet type cannot be empty")
        
        # Validate age
        if not isinstance(self.age, int) or self.age < 0:
            raise ValueError(f"Invalid age {self.age}. Age must be a non-negative integer.")


@dataclass
class Owner:
    """Dataclass representing a pet owner"""
    name: str
    available_time: int
    preferences: dict = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)
    
    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner
        
        Args:
            pet (Pet): Pet object to add
            
        Raises:
            TypeError: If pet is not a Pet instance
            ValueError: If a pet with the same name, type, and age already exists
        """
        if not isinstance(pet, Pet):
            raise TypeError(f"Expected Pet instance, got {type(pet)}")
        
        # Check if pet with same attributes (name, type, age) already exists
        for existing_pet in self.pets:
            if (existing_pet.name.lower() == pet.name.lower() and
                existing_pet.pet_type.lower() == pet.pet_type.lower() and
                existing_pet.age == pet.age):
                raise ValueError(
                    f"Pet '{pet.name}' ({pet.pet_type}, {pet.age} years old) already exists"
                )
        
        self.pets.append(pet)
    
    def get_pets(self) -> List[Pet]:
        """Get all pets owned
        
        Returns:
            List[Pet]: List of all pets owned by this owner
        """
        return list(self.pets)
    
    def set_availability(self, time: int) -> None:
        """Set available time for pet care
        
        Args:
            time (int): Available time in minutes (must be >= 0)
            
        Raises:
            ValueError: If time is negative
        """
        if not isinstance(time, int) or time < 0:
            raise ValueError(f"Available time must be a non-negative integer, got {time}")
        
        self.available_time = time
    
    def __post_init__(self):
        """Post-initialization validation for Owner dataclass"""
        # Validate name
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("Owner name cannot be empty")
        
        # Validate available_time
        if not isinstance(self.available_time, int) or self.available_time < 0:
            raise ValueError(f"Invalid available_time {self.available_time}. Must be a non-negative integer.")
        
        # Validate preferences is a dict
        if not isinstance(self.preferences, dict):
            raise ValueError("Invalid preferences format. Please provide a valid preference.")
        if "prefered_time" in self.preferences:
            if self.preferences["prefered_time"].lower() not in ["morning", "afternoon"]:
                raise ValueError("Invalid prefered_time in preferences. Must be 'morning' or 'afternoon'.")


class Scheduler:
    """Class for scheduling pet tasks"""
    
    def __init__(self, owner: Owner, pet: Pet, available_time: int):
        self.owner = owner
        self.pet = pet
        self.available_time = owner.available_time
        self.plan: List[Task] = []
    
    def filter_by_constraints(self) -> List[Task]:
        """Filter tasks based on constraints
        
        Only returns tasks that can fit in available time
        
        Returns:
            List[Task]: Tasks that are feasible given time constraints
        """
        feasible_tasks = []
        for task in self.pet.get_tasks():
            if task.is_feasible(self.available_time):
                feasible_tasks.append(task)
        return feasible_tasks
    
    def sort_by_priority(self, tasks: List[Task] = None) -> List[Task]:
        """Sort tasks by priority (highest priority first)
        
        Args:
            tasks (List[Task], optional): Tasks to sort. If None, uses filtered tasks.
                                         Priority 1 is highest, 3 is lowest.
        
        Returns:
            List[Task]: Tasks sorted by priority (ascending: 1 > 2 > 3)
        """
        if tasks is None:
            tasks = self.filter_by_constraints()
        
        return sorted(tasks, key=lambda t: t.priority)
    
    def generate_plan(self) -> List[Task]:
        """Generate a schedule plan for tasks
        
        Strategy:
        1. Filter tasks by feasibility constraints
        2. Sort by priority (highest first)
        3. Greedily add tasks until time runs out
        
        Returns:
            List[Task]: Ordered list of tasks that fit in available time
        """
        # Get feasible tasks sorted by priority
        sorted_tasks = self.sort_by_priority()
        
        # Greedily add tasks to plan until time runs out
        self.plan = []
        remaining_time = self.available_time
        
        for task in sorted_tasks:
            if task.duration <= remaining_time:
                self.plan.append(task)
                remaining_time -= task.duration
        
        return self.plan
    
    def explain_plan(self) -> str:
        """Provide explanation of the generated plan
        
        Returns:
            str: Formatted explanation of why tasks were chosen/excluded
        """
        explanation = f"Schedule Plan for {self.pet.name} ({self.pet.pet_type})\n"
        explanation += f"Available time: {self.available_time} minutes\n"
        explanation += "-" * 50 + "\n\n"
        
        if not self.plan:
            explanation += "⚠️  No tasks could be scheduled with available time.\n"
            all_tasks = self.pet.get_tasks()
            if all_tasks:
                explanation += "\nTasks that do NOT fit:\n"
                for task in all_tasks:
                    explanation += f"  • {task.task_name} ({task.duration} min, priority {task.priority}) - "
                    if task.duration > self.available_time:
                        explanation += f"exceeds available time ({task.duration} > {self.available_time})\n"
                    else:
                        explanation += "not selected\n"
            return explanation
        
        # Explain included tasks
        explanation += f"✅ Scheduled Tasks ({len(self.plan)}):\n"
        total_duration = 0
        for i, task in enumerate(self.plan, 1):
            explanation += f"  {i}. {task.task_name}\n"
            explanation += f"     Duration: {task.duration} min | Priority: {task.priority}\n"
            if task.prefered_time:
                explanation += f"     Preferred time: {task.prefered_time}\n"
            total_duration += task.duration
        
        explanation += f"\nTotal scheduled time: {total_duration} / {self.available_time} minutes\n"
        explanation += f"Remaining time: {self.available_time - total_duration} minutes\n"
        
        # Explain excluded tasks
        feasible_not_scheduled = [t for t in self.filter_by_constraints() if t not in self.plan]
        if feasible_not_scheduled:
            explanation += f"\n❌ Feasible but NOT scheduled ({len(feasible_not_scheduled)}):\n"
            for task in feasible_not_scheduled:
                explanation += f"  • {task.task_name} ({task.duration} min, priority {task.priority}) - "
                explanation += "lower priority than scheduled tasks\n"
        
        all_tasks = self.pet.get_tasks()
        infeasible = [t for t in all_tasks if not t.is_feasible(self.available_time)]
        if infeasible:
            explanation += f"\n⛔ Too long to fit ({len(infeasible)}):\n"
            for task in infeasible:
                explanation += f"  • {task.task_name} ({task.duration} min) - exceeds available time\n"
        
        return explanation
