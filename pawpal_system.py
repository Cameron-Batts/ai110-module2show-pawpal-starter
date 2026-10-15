"""PawPal+ logic layer: Task, Pet, Owner, and Scheduler."""

from dataclasses import dataclass, field, replace
from datetime import date, timedelta
from typing import Dict, List, Optional, Tuple


@dataclass
class Task:
    """A single pet care activity."""

    description: str
    time: str  # "HH:MM" in 24 hour format
    frequency: str = "once"  # "once", "daily", or "weekly"
    due_date: date = field(default_factory=date.today)
    duration_minutes: int = 15
    priority: str = "medium"  # "low", "medium", or "high"
    completed: bool = False
    pet_name: str = ""  # filled in by Pet.add_task

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def next_occurrence(self) -> Optional["Task"]:
        """Return a fresh copy due on the next occurrence, or None if it does not repeat."""
        if self.frequency == "daily":
            days = 1
        elif self.frequency == "weekly":
            days = 7
        else:
            return None
        return replace(self, due_date=self.due_date + timedelta(days=days), completed=False)


@dataclass
class Pet:
    """A pet and the tasks that belong to it."""

    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet and record the pet's name on it."""
        task.pet_name = self.name
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks


class Owner:
    """A person who owns one or more pets."""

    def __init__(self, name: str):
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return every task from every pet in one list."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """The brain: organizes tasks across all of an owner's pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def get_todays_schedule(self) -> List[Task]:
        """Return all tasks due today across every pet."""
        today = date.today()
        return [t for t in self.owner.get_all_tasks() if t.due_date == today]

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks in chronological order (due date first, then HH:MM time)."""
        return sorted(tasks, key=lambda t: (t.due_date, t.time))

    def filter_tasks(
        self, pet_name: Optional[str] = None, completed: Optional[bool] = None
    ) -> List[Task]:
        """Return tasks filtered by pet name and/or completion status."""
        tasks = self.owner.get_all_tasks()
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet_name.lower() == pet_name.lower()]
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        return tasks

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Mark a task done; if it repeats, add the next one to the same pet and return it."""
        if task.completed:
            return None
        task.mark_complete()
        next_task = task.next_occurrence()
        if next_task is None:
            return None
        for pet in self.owner.pets:
            if pet.name == task.pet_name:
                pet.add_task(next_task)
                return next_task
        return None

    def detect_conflicts(self) -> List[str]:
        """Return a warning for every date and time that has more than one pending task."""
        slots: Dict[Tuple[date, str], List[Task]] = {}
        for task in self.owner.get_all_tasks():
            if not task.completed:
                slots.setdefault((task.due_date, task.time), []).append(task)

        warnings: List[str] = []
        for (due, time_str), tasks in sorted(slots.items()):
            if len(tasks) > 1:
                names = ", ".join(f"{t.description} ({t.pet_name})" for t in tasks)
                warnings.append(f"Warning: {len(tasks)} tasks at {time_str} on {due}: {names}")
        return warnings