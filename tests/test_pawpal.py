from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def make_owner():
    """Helper: an owner with one pet named Mochi."""
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog")
    owner.add_pet(mochi)
    return owner, mochi


def test_mark_complete_changes_status():
    task = Task("Walk", "08:00")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Mochi", "dog")
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task("Walk", "08:00"))
    assert len(pet.get_tasks()) == 1


def test_sort_by_time_returns_chronological_order():
    owner, mochi = make_owner()
    mochi.add_task(Task("Evening walk", "18:00"))
    mochi.add_task(Task("Breakfast", "07:30"))
    mochi.add_task(Task("Lunch", "12:00"))
    scheduler = Scheduler(owner)

    times = [t.time for t in scheduler.sort_by_time(owner.get_all_tasks())]
    assert times == ["07:30", "12:00", "18:00"]


def test_daily_task_creates_next_day_task_when_completed():
    owner, mochi = make_owner()
    task = Task("Feeding", "09:00", frequency="daily")
    mochi.add_task(task)
    scheduler = Scheduler(owner)

    new_task = scheduler.mark_task_complete(task)

    assert task.completed is True
    assert new_task is not None
    assert new_task.due_date == task.due_date + timedelta(days=1)
    assert new_task.completed is False
    assert new_task in mochi.get_tasks()


def test_one_time_task_does_not_repeat():
    owner, mochi = make_owner()
    task = Task("Vet visit", "10:00", frequency="once")
    mochi.add_task(task)

    assert Scheduler(owner).mark_task_complete(task) is None
    assert len(mochi.get_tasks()) == 1


def test_conflict_detection_flags_same_time():
    owner, mochi = make_owner()
    luna = Pet("Luna", "cat")
    owner.add_pet(luna)
    mochi.add_task(Task("Walk", "08:00"))
    luna.add_task(Task("Grooming", "08:00"))

    warnings = Scheduler(owner).detect_conflicts()

    assert len(warnings) == 1
    assert "08:00" in warnings[0]


def test_no_conflict_when_times_differ():
    owner, mochi = make_owner()
    mochi.add_task(Task("Walk", "08:00"))
    mochi.add_task(Task("Feeding", "09:00"))

    assert Scheduler(owner).detect_conflicts() == []


def test_pet_with_no_tasks_gives_empty_schedule():
    owner, _ = make_owner()
    scheduler = Scheduler(owner)

    assert scheduler.get_todays_schedule() == []
    assert scheduler.detect_conflicts() == []


def test_todays_schedule_ignores_other_dates():
    owner, mochi = make_owner()
    mochi.add_task(Task("Walk", "08:00"))
    mochi.add_task(Task("Tomorrow walk", "08:00", due_date=date.today() + timedelta(days=1)))

    schedule = Scheduler(owner).get_todays_schedule()

    assert [t.description for t in schedule] == ["Walk"]