import sqlite3

# Step 1: Create database and table
conn = sqlite3.connect(":memory:")  # in-memory database
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE students (
    roll_no INTEGER,
    name TEXT,
    gpa REAL,
    department TEXT,
    year INTEGER
)
""")

# Step 2: Insert sample data
students_data = [
    (101, "Alice", 9.1, "CSE", 3),
    (102, "Bob", 7.8, "ECE", 2),
    (103, "Charlie", 8.5, "MECH", 4),
    (104, "David", 9.3, "CSE", 3),
    (105, "Eva", 8.0, "EEE", 2),
    (106, "Frank", 7.5, "CIVIL", 1),
    (107, "Grace", 9.2, "CSE", 4),
    (108, "Hannah", 8.7, "IT", 3),
    (109, "Ian", 8.9, "CSE", 2),
    (110, "Jane", 7.2, "ECE", 1)
]
cursor.executemany("INSERT INTO students VALUES (?, ?, ?, ?, ?)", students_data)
conn.commit()

# Step 3: Function to convert natural language to SQL
def nl_to_sql(query):
    query = query.lower()

    if "all students" in query:
        return "SELECT * FROM students"
    elif "gpa > 8" in query:
        return "SELECT * FROM students WHERE gpa > 8"
    elif "cse students" in query:
        return "SELECT * FROM students WHERE department = 'CSE'"
    elif "final year" in query:
        return "SELECT * FROM students WHERE year = 4"
    elif "2nd year" in query:
        return "SELECT * FROM students WHERE year = 2"
    else:
        return None

# Step 4: Main Chat Loop
print("🤖 AI Chat to SQL System")
print("You can ask like:")
print(" - Show all students")
print(" - Show CSE students")
print(" - Show students with GPA > 8")
print(" - Show 3rd year students")
print(" - Show final year students")
print(" - Show highest GPA student")
print("Type 'exit' to quit.")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    sql_query = nl_to_sql(user_input)

    if sql_query:
        print(f"🔹 SQL Query: {sql_query}")
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        # Print table header
        print("\nRoll_No | Name     | GPA  | Department | Year")
        print("------------------------------------------------")
        for row in rows:
            print(f"{row[0]:<7} | {row[1]:<8} | {row[2]:<4} | {row[3]:<10} | {row[4]}")
        print()
    else:
        print("❌ Sorry, I couldn’t understand that request.\n")
