"""Demo script: build an owner with two pets and print today's schedule."""

from pawpal_system import Owner, Pet, Task, Scheduler


def print_schedule(owner: Owner, tasks: list) -> None:
    """Print a readable schedule for the given tasks."""
    print(f"Today's Schedule for {owner.name}")
    print("-" * 44)
    if not tasks:
        print("No tasks scheduled for today.")
        return
    for task in tasks:
        status = "x" if task.completed else " "
        print(
            f"[{status}] {task.time}  {task.description} "
            f"({task.pet_name}, {task.duration_minutes} min) "
            f"[{task.priority}]"
        )


def main() -> None:
    owner = Owner("Jordan")

    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)

    mochi.add_task(Task("Morning walk", "08:00", duration_minutes=30, priority="high"))
    luna.add_task(Task("Feeding", "09:00", duration_minutes=10, priority="high"))
    mochi.add_task(Task("Medication", "12:30", duration_minutes=5, priority="high"))
    luna.add_task(Task("Play time", "18:00", duration_minutes=20, priority="low"))

    scheduler = Scheduler(owner)
    print_schedule(owner, scheduler.get_todays_schedule())


if __name__ == "__main__":
    main()