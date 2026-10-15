# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The three main things a user should be able to do are add a pet, schedule a task for that pet (like a walk, a feeding, medication, or a vet visit), and see today's tasks in order. I picked these because they cover the basic loop of the app: set up the pet, plan the care, then check what to do next.

I used four classes. Task holds one activity: what it is, the time, how often it repeats, the due date, how long it takes, the priority, and whether it is done. Pet holds the pet's name and species and its list of tasks. Owner holds the owner's name and a list of pets, and it has one method that returns every pet's tasks together. Scheduler takes an owner and does the thinking: sorting by time, filtering, finding conflicts, and building today's schedule. I kept the Scheduler separate so the other three classes only store data.

---

**b. Design changes**

My design changed after I reviewed the skeleton with AI. A Task did not know which pet it belonged to, so once get_all_tasks() put every pet's tasks in one list, the Scheduler could not filter by pet name or show which pet a task was for. I added a pet_name field to Task that gets filled in when a task is added to a pet. I also decided conflict checks should compare the due date along with the time.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

One tradeoff is that conflict detection only flags tasks that have the exact same date and time. It does not check if the durations overlap. For example, a 30 minute walk at 08:00 and a feeding at 08:15 would not get a warning even though they overlap. I kept it this way because it is simple and easy to test, and for a pet owner an exact match is the most obvious problem. If I had more time I would compare start time plus duration to catch real overlaps.

---

## 3. AI Collaboration

**a. How you used AI**

I used Claude in a chat to work through the project one step at a time. I asked it to suggest the classes and their attributes, create the Mermaid UML diagram, write the class skeleton with dataclasses, fill in the methods, write main.py, and draft the first tests. The most helpful prompts were the ones where I gave it the exact classes and attributes I wanted, because that got me a usable diagram and skeleton the first time.

---

**b. Judgment and verification**

I checked the AI's work by running it instead of trusting it. When I committed pawpal_system.py, my import check failed with an ImportError and the commit showed 0 insertions, which told me the file had been saved empty. I fixed it and committed again. I also ran main.py and pytest after each change to make sure the output matched what I expected, like the 2 passing tests. So far I have accepted the AI's suggestions, including adding pet_name to Task after its design review.
I also looked at a shorter version of detect_conflicts that used defaultdict and a list comprehension. It saved a couple of lines but the warning message was harder to read, so I kept my original version.

---

## 4. Testing and Verification

**a. What you tested**

I tested the main behaviors of the Scheduler and the Task and Pet classes. That includes marking a task complete, adding a task to a pet, sorting tasks by time, creating the next task when a daily task is completed, making sure a one time task does not repeat, and flagging two tasks at the same time as a conflict. I also tested edge cases like a pet with no tasks and tasks that are due on a different day. These matter because the whole app depends on the schedule being in the right order and not missing or repeating tasks by mistake.

**b. Confidence**

I am about a 4 out of 5 confident that the scheduler works. All 9 tests pass and they cover the main logic. I took off a point because conflict detection only checks for the exact same time and not overlapping durations, and I have not tested the Streamlit app automatically. If I had more time I would test tasks that overlap, invalid time strings like "25:99", two pets with the same name, and a weekly task that is completed more than once.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
