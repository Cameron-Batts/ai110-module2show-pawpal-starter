import datetime

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A pet care planner that keeps your pets' routines organized.")

# Streamlit reruns this whole file on every click, so the Owner has to live in
# session_state. Only create it the first time, then reuse it.
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")
owner: Owner = st.session_state.owner

owner.name = st.text_input("Owner name", value="Jordan", key="owner_name")

st.divider()

# --- Add a pet ---------------------------------------------------------------
st.subheader("Add a pet")
with st.form("add_pet_form", clear_on_submit=True):
    new_pet_name = st.text_input("Pet name")
    new_pet_species = st.selectbox("Species", ["dog", "cat", "other"])
    add_pet_clicked = st.form_submit_button("Add pet")

if add_pet_clicked:
    name = new_pet_name.strip()
    existing = [p.name.lower() for p in owner.pets]
    if not name:
        st.warning("Please enter a pet name.")
    elif name.lower() in existing:
        st.warning(f"You already have a pet named {name}.")
    else:
        owner.add_pet(Pet(name, new_pet_species))
        st.success(f"Added {name} the {new_pet_species}.")

if owner.pets:
    st.write("Your pets: " + ", ".join(f"{p.name} ({p.species})" for p in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Add a task --------------------------------------------------------------
st.subheader("Schedule a task")
if owner.pets:
    with st.form("add_task_form"):
        pet_choice = st.selectbox("Pet", [p.name for p in owner.pets])
        description = st.text_input("Task description", value="Morning walk")
        col1, col2 = st.columns(2)
        with col1:
            task_time = st.time_input("Time", value=datetime.time(8, 0))
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        with col2:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)
            frequency = st.selectbox("Repeats", ["once", "daily", "weekly"])
        add_task_clicked = st.form_submit_button("Add task")

    if add_task_clicked:
        if not description.strip():
            st.warning("Please enter a task description.")
        else:
            pet = next(p for p in owner.pets if p.name == pet_choice)
            pet.add_task(
                Task(
                    description=description.strip(),
                    time=task_time.strftime("%H:%M"),
                    frequency=frequency,
                    duration_minutes=int(duration),
                    priority=priority,
                )
            )
            st.success(f"Added '{description.strip()}' for {pet.name}.")
else:
    st.info("Add a pet first, then you can schedule tasks for it.")


def task_rows(tasks):
    """Turn Task objects into simple rows for st.table."""
    return [
        {
            "Time": t.time,
            "Pet": t.pet_name,
            "Task": t.description,
            "Duration (min)": t.duration_minutes,
            "Priority": t.priority,
            "Repeats": t.frequency,
            "Done": "yes" if t.completed else "no",
        }
        for t in tasks
    ]


scheduler = Scheduler(owner)

all_tasks = scheduler.sort_by_time(owner.get_all_tasks())
if all_tasks:
    st.write("All tasks (sorted by date and time):")
    st.table(task_rows(all_tasks))

st.divider()

# --- Build the schedule ------------------------------------------------------
st.subheader("Today's schedule")
if st.button("Generate schedule"):
    schedule = scheduler.sort_by_time(scheduler.get_todays_schedule())
    if schedule:
        st.success(f"{len(schedule)} task(s) scheduled for today.")
        st.table(task_rows(schedule))
    else:
        st.info("Nothing is scheduled for today yet.")

    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            st.warning(warning)
    elif schedule:
        st.success("No scheduling conflicts found.")