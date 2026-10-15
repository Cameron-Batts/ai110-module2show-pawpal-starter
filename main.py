"""Demo script: sorting, filtering, recurring tasks, and conflict detection."""

from typing import List

from pawpal_system import Owner, Pet, Scheduler, Task


def print_tasks(title: str, tasks: List[Task]) -> None:
    """Print a titled, readable list of tasks."""
    print(title)
    print("-" * 44)
    if not tasks:
        print("(none)")
    for task in tasks:
        status = "x" if task.completed else " "
        print(
            f"[{status}] {task.time}  {task.description} "
            f"({task.pet_name}, {task.duration_minutes} min) "
            f"[{task.priority}] {task.due_date}"
        )
    print()


def main() -> None:
    owner = Owner("Jordan")

    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)

    # Tasks are added out of order on purpose.
    mochi.add_task(Task("Evening walk", "18:00", duration_minutes=30, priority="medium"))
    luna.add_task(Task("Feeding", "09:00", frequency="daily", duration_minutes=10, priority="high"))
    mochi.add_task(Task("Medication", "12:30", duration_minutes=5, priority="high"))
    mochi.add_task(Task("Morning walk", "08:00", frequency="daily", duration_minutes=30, priority="high"))
    luna.add_task(Task("Grooming", "08:00", duration_minutes=15, priority="low"))  # same time as the walk

    scheduler = Scheduler(owner)

    print_tasks("Today's Schedule (sorted by time)", scheduler.sort_by_time(scheduler.get_todays_schedule()))
    print_tasks("Mochi's tasks only", scheduler.sort_by_time(scheduler.filter_tasks(pet_name="Mochi")))

    print("Conflict check")
    print("-" * 44)
    for warning in scheduler.detect_conflicts() or ["No conflicts found."]:
        print(warning)
    print()

    # Completing a daily task creates tomorrow's copy.
    walk = next(t for t in mochi.tasks if t.description == "Morning walk")
    new_task = scheduler.mark_task_complete(walk)
    print("Marked 'Morning walk' complete")
    print("-" * 44)
    print(f"Next occurrence created for {new_task.due_date} at {new_task.time}\n")

    print_tasks("Pending tasks", scheduler.sort_by_time(scheduler.filter_tasks(completed=False)))
    print_tasks("Completed tasks", scheduler.filter_tasks(completed=True))


if __name__ == "__main__":
    main()