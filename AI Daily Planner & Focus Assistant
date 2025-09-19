from datetime import datetime
from textblob import TextBlob
import json
import os

TASK_FILE = "tasks.json"

# Load tasks from file
def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as file:
            tasks = json.load(file)
            for task in tasks:
                if "completed" not in task:
                    task["completed"] = False
            return tasks
    return []

# Save tasks to file
def save_tasks(tasks):
    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# Convert priority string to numeric value for sorting
def get_priority_value(priority):
    return {"High": 1, "Medium": 2, "Low": 3}.get(priority, 4)

# Add a new task
def add_task():
    task_name = input("\n📝 Enter your task: ")
    due_date = input("📅 Enter due date (YYYY-MM-DD): ")

    polarity = TextBlob(task_name).sentiment.polarity
    if polarity > 0.2:
        priority = "High"
    elif polarity > -0.2:
        priority = "Medium"
    else:
        priority = "Low"

    task = {
        "task": task_name,
        "due": due_date,
        "priority": priority,
        "completed": False
    }

    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    print("✅ Task added successfully!")

# Show all tasks
def show_tasks():
    tasks = load_tasks()
    if not tasks:
        print("\n📭 No tasks found.")
        return

    tasks.sort(key=lambda x: (x["completed"], get_priority_value(x["priority"])))

    print("\n📋 Your Task List:\n")
    for i, task in enumerate(tasks, 1):
        status = "✅ Completed" if task["completed"] else "🕒 Pending"
        due_date = datetime.strptime(task["due"], "%Y-%m-%d").date()
        today = datetime.today().date()
        deadline_status = "⚠️ Overdue" if due_date < today and not task["completed"] else ""
        print(f"{i}. {task['task']} | Due: {task['due']} | Priority: {task['priority']} | {status} {deadline_status}")
    print(f"\n📌 Total Tasks: {len(tasks)} | ✅ Completed: {sum(t['completed'] for t in tasks)} | 🕒 Pending: {sum(not t['completed'] for t in tasks)}")

# Mark a task as completed
def mark_task_complete():
    tasks = load_tasks()
    if not tasks:
        print("\n📭 No tasks to mark as complete.")
        return

    show_tasks()
    try:
        task_no = int(input("\n✔️ Enter the task number to mark as complete: "))
        if 1 <= task_no <= len(tasks):
            tasks[task_no - 1]["completed"] = True
            save_tasks(tasks)
            print("🎉 Task marked as completed!")
        else:
            print("⚠️ Invalid task number.")
    except ValueError:
        print("⚠️ Please enter a valid number.")

# Generate focus plan using Pomodoro style
def generate_focus_plan():
    tasks = [t for t in load_tasks() if not t["completed"]]
    if not tasks:
        print("\n🛌 No pending tasks to plan.")
        return

    tasks.sort(key=lambda x: get_priority_value(x["priority"]))

    print("\n🧠 Suggested Focus Plan (Pomodoro Style):\n")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. 🔹 Focus: {task['task']} (25 mins)")
        print(f"   🔸 Break: Relax (5 mins)\n")

# Main menu
def main():
    while True:
        print("\n===== 🗓️ AI DAILY PLANNER & FOCUS ASSISTANT =====")
        print("1. ➕ Add Task")
        print("2. 📋 Show Tasks")
        print("3. ✅ Mark Task as Complete")
        print("4. ⏳ Generate Focus Plan")
        print("5. ❌ Exit")

        choice = input("Choose an option (1-5): ")

        if choice == "1":
            add_task()
        elif choice == "2":
            show_tasks()
        elif choice == "3":
            mark_task_complete()
        elif choice == "4":
            generate_focus_plan()
        elif choice == "5":
            print("👋 Goodbye! Stay focused and productive!")
            break
        else:
            print("⚠️ Invalid option. Try again.")

if __name__ == "__main__":
    main()
