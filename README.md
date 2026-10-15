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

PawPal+ has four classes in pawpal_system.py. Task and Pet are dataclasses. A Task stores one activity (description, time, frequency, due date, duration, priority, and whether it is done). A Pet stores its name, species, and a list of tasks, and add_task() also saves the pet's name on the task. An Owner stores a list of pets, and get_all_tasks() collects every pet's tasks into one list. The Scheduler takes an Owner and reads from get_all_tasks(), so it works across all pets. Right now it can return the tasks due today. Sorting, filtering, and conflict checks are planned for Phase 4. main.py is a demo script that builds an owner with two pets and prints today's schedule, and tests/test_pawpal.py has the first two pytest tests.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
Today's Schedule for Jordan
--------------------------------------------
[ ] 08:00  Morning walk (Mochi, 30 min) [high]
[ ] 12:30  Medication (Mochi, 5 min) [high]
[ ] 09:00  Feeding (Luna, 10 min) [high]
[ ] 18:00  Play time (Luna, 20 min) [low]
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

PawPal+ goes beyond a basic task list with a few algorithms in the `Scheduler` class.

| Feature | Method | Notes |
|---|---|---|
| Sort by time | `sort_by_time` | Orders tasks by due date, then by "HH:MM" time, using a lambda key. |
| Filter tasks | `filter_tasks` | Filters by pet name, completion status, or both. Pet name is not case sensitive. |
| Recurring tasks | `mark_task_complete` and `next_occurrence` | Completing a daily or weekly task creates a new copy due the next day or 7 days later. One time tasks do not repeat. |
| Conflict detection | `detect_conflicts` | Returns a warning for any date and time with more than one pending task, across all pets. It does not crash, it just reports. |

Conflict detection only checks for the exact same date and time. It does not check if durations overlap.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
