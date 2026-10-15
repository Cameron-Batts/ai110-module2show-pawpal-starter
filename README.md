# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Features

- Add multiple pets, each with their own tasks
- Schedule tasks with a time, duration, priority, and repeat setting (once, daily, or weekly)
- Sorts tasks by date and time so the schedule is always in order
- Filters tasks by pet name or by done and not done
- Recurring tasks: completing a daily or weekly task automatically creates the next one
- Conflict warnings when two tasks are scheduled at the same time
- Streamlit app that keeps your pets and tasks while you use it

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Implementation Summary

PawPal+ has four classes in pawpal_system.py. Task and Pet are dataclasses. A Task stores one activity (description, time, frequency, due date, duration, priority, and whether it is done). A Pet stores its name, species, and a list of tasks, and add_task() also saves the pet's name on the task. An Owner stores a list of pets, and get_all_tasks() collects every pet's tasks into one list. The Scheduler takes an Owner and reads from get_all_tasks(), so it works across all pets. The Scheduler can return today's tasks, sort them by time, filter them by pet or completion status, create the next task when a daily or weekly task is completed, and warn about tasks scheduled at the same time. main.py is a demo script that shows all of this with two pets, and tests/test_pawpal.py has 9 pytest tests.

## 🖥️ Sample Output

```
Today's Schedule (sorted by time)
--------------------------------------------
[ ] 08:00  Morning walk (Mochi, 30 min) [high] 2026-10-14
[ ] 08:00  Grooming (Luna, 15 min) [low] 2026-10-14
[ ] 09:00  Feeding (Luna, 10 min) [high] 2026-10-14
[ ] 12:30  Medication (Mochi, 5 min) [high] 2026-10-14
[ ] 18:00  Evening walk (Mochi, 30 min) [medium] 2026-10-14

Conflict check
--------------------------------------------
Warning: 2 tasks at 08:00 on 2026-10-14: Morning walk (Mochi), Grooming (Luna)
```

## 🧪 Testing PawPal+

Run the tests with:

```bash
python -m pytest
```

The test suite has 9 tests in `tests/test_pawpal.py`. They cover:

- Task completion changes the task status
- Adding a task to a pet increases its task count
- Sorting returns tasks in chronological order
- Completing a daily task creates a new task for the next day
- Completing a one time task does not create a new task
- Conflict detection flags two tasks at the same time (and does not flag different times)
- Edge cases: a pet with no tasks gives an empty schedule, and tasks due on other days are left out of today's schedule

Latest result: 9 passed.

Confidence level: 4 out of 5 stars. The core logic (sorting, recurrence, conflicts) is tested and passes. I took off one star because conflict detection only checks exact matching times, not overlapping durations, and the Streamlit app itself has not been tested automatically.

## 📐 Smarter Scheduling


PawPal+ goes beyond a basic task list with a few algorithms in the `Scheduler` class.

| Feature | Method | Notes |
|---|---|---|
| Sort by time | `sort_by_time` | Orders tasks by due date, then by "HH:MM" time, using a lambda key. |
| Filter tasks | `filter_tasks` | Filters by pet name, completion status, or both. Pet name is not case sensitive. |
| Recurring tasks | `mark_task_complete` and `next_occurrence` | Completing a daily or weekly task creates a new copy due the next day or 7 days later. One time tasks do not repeat. |
| Conflict detection | `detect_conflicts` | Returns a warning for any date and time with more than one pending task, across all pets. It does not crash, it just reports. |

Conflict detection only checks for the exact same date and time. It does not check if durations overlap.

## 📸 Demo Walkthrough

1. Run `streamlit run app.py` and open the link it prints.
2. Type a pet name (like Mochi), pick a species, and click **Add pet**.
3. Under **Schedule a task**, pick the pet, type a description, choose a time, duration, priority, and how often it repeats, then click **Add task**. Add a few tasks, including two at the same time.
4. The **All tasks** table shows everything sorted by date and time.
5. Click **Generate schedule** to see today's tasks in order. If two tasks share the same time, a yellow warning shows which ones.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
