"""PawPal+ logic layer: Task, Pet, Owner, and Scheduler."""

from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional


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
        self.completed = True


@dataclass
class Pet:
    """A pet and the tasks that belong to it."""

    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        task.pet_name = self.name
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        return self.tasks


class Owner:
    """A person who owns one or more pets."""

    def __init__(self, name: str):
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """The brain: organizes tasks across all of an owner's pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def get_todays_schedule(self) -> List[Task]:
        today = date.today()
        return [t for t in self.owner.get_all_tasks() if t.due_date == today]

    # Phase 4 will fill these in.
    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        pass

    def filter_tasks(
        self, pet_name: Optional[str] = None, completed: Optional[bool] = None
    ) -> List[Task]:
        pass

    def detect_conflicts(self) -> List[str]:
        pass