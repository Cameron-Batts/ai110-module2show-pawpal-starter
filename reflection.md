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

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

I used Claude in a chat to work through the project one step at a time. I asked it to suggest the classes and their attributes, create the Mermaid UML diagram, write the class skeleton with dataclasses, fill in the methods, write main.py, and draft the first tests. The most helpful prompts were the ones where I gave it the exact classes and attributes I wanted, because that got me a usable diagram and skeleton the first time.

---

**b. Judgment and verification**

I checked the AI's work by running it instead of trusting it. When I committed pawpal_system.py, my import check failed with an ImportError and the commit showed 0 insertions, which told me the file had been saved empty. I fixed it and committed again. I also ran main.py and pytest after each change to make sure the output matched what I expected, like the 2 passing tests. So far I have accepted the AI's suggestions, including adding pet_name to Task after its design review.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
