"""
SMART STUDENT MANAGEMENT SYSTEM - FINAL FIXED VERSION
"""

import csv
import os
import json
import copy

FILE = "students.csv"

# ================= CSV FILE CREATION =================
if not os.path.exists(FILE):
    with open(FILE, "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow(["Name", "Math", "Science", "English"])
        writer.writerow(["Aman", 80, 75, 90])
        writer.writerow(["Riya", 40, 35, 50])
        writer.writerow(["Kabir", 95, 85, 88])
        writer.writerow(["Sneha", 70, 72, 68])
        writer.writerow(["Raj", 55, 60, 58])

    print("students.csv created with sample data\n")


# ================= LOGIN SYSTEM =================
def login():
    USER = "admin"
    PASSWORD = "python"
    attempts = 0

    while attempts < 3:
        u = input("Username: ")
        p = input("Password: ")

        if u == USER and p == PASSWORD:
            print("\nLogin Successful!\n")
            return True
        else:
            print("Invalid Credentials\n")
            attempts += 1

    print("Account Locked!")
    return False


# ================= READ STUDENTS =================
def read_students():
    students = {}

    with open(FILE) as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            name = row[0]
            marks = list(map(int, row[1:]))
            students[name] = marks

    return students


# ================= ADD STUDENT =================
def add_students():
    name = input("Student Name: ")
    math = int(input("Math Marks: "))
    science = int(input("Science Marks: "))
    english = int(input("English Marks: "))

    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, math, science, english])

    print("Student Added Successfully!\n")


# ================= CALCULATE AVERAGES =================
def calculate_averages(students):
    averages = {}

    for name, marks in students.items():
        avg = sum(marks) / len(marks)
        averages[name] = avg

    return averages


# ================= ASSIGN GRADES =================
def assign_grades(averages):

    def grade(avg):
        if avg >= 80:
            return "A"
        elif avg >= 60:
            return "B"
        elif avg >= 40:
            return "C"
        else:
            return "D"

    return dict(zip(
        averages.keys(),
        map(grade, averages.values())
    ))


# ================= SHOW REPORT =================
def show_report():
    students = read_students()

    if not students:
        print("No Data Found!\n")
        return

    backup_students = copy.deepcopy(students)

    averages = calculate_averages(students)
    grades = assign_grades(averages)

    passed = [name for name, avg in averages.items() if avg >= 40]
    toppers = list(filter(lambda x: averages[x] >= 85, averages))

    ranking = sorted(
        averages.items(),
        key=lambda x: x[1],
        reverse=True
    )

    print("\n========== STUDENT REPORT ==========")

    for name in students:
        print(f"{name} | Avg: {averages[name]:.2f} | Grade: {grades[name]}")

    print("\nPassed Students:", passed)
    print("Top Performers:", toppers)

    print("\n--- Ranking ---")
    for i, (name, avg) in enumerate(ranking, start=1):
        print(f"{i}. {name} - {avg:.2f}")

    report = {
        "students": students,
        "averages": averages,
        "grades": grades,
        "passed": passed,
        "toppers": toppers,
        "ranking": ranking
    }

    with open("report.json", "w") as f:
        json.dump(report, f, indent=4)

    print("\nReport exported to report.json\n")


# ================= MENU =================
def menu():
    while True:
        print("1. Add Student")
        print("2. Show Report")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_students()
        elif choice == "2":
            show_report()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid Choice\n")


# ================= MAIN =================
if login():
    menu()