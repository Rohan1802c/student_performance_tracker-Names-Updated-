import sqlite3
import csv
import os
from visualization import visualization_menu

DB_FILE = "database.db"
CSV_FILE = "students.csv"

def csv_to_sqlite():
    """Convert CSV data to SQLite database."""
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)  # Remove existing database to recreate
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create table
    cursor.execute("""
    CREATE TABLE students (
        RollNo INTEGER PRIMARY KEY,
        Name TEXT,
        Physics_Test1 INTEGER, Physics_Test2 INTEGER, Physics_Test3 INTEGER, Physics_Final INTEGER,
        Chemistry_Test1 INTEGER, Chemistry_Test2 INTEGER, Chemistry_Test3 INTEGER, Chemistry_Final INTEGER,
        Maths_Test1 INTEGER, Maths_Test2 INTEGER, Maths_Test3 INTEGER, Maths_Final INTEGER,
        Computer_Test1 INTEGER, Computer_Test2 INTEGER, Computer_Test3 INTEGER, Computer_Final INTEGER
    )
    """)

    # Insert data from CSV
    with open(CSV_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
            INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                int(row['RollNo']), row['Name'],
                int(row['Physics_Test1']), int(row['Physics_Test2']), int(row['Physics_Test3']), int(row['Physics_Final']),
                int(row['Chemistry_Test1']), int(row['Chemistry_Test2']), int(row['Chemistry_Test3']), int(row['Chemistry_Final']),
                int(row['Maths_Test1']), int(row['Maths_Test2']), int(row['Maths_Test3']), int(row['Maths_Final']),
                int(row['Computer_Test1']), int(row['Computer_Test2']), int(row['Computer_Test3']), int(row['Computer_Final'])
            ))
    conn.commit()
    conn.close()
    print("CSV data successfully converted to SQLite database.")


def update_csv():
    """Update the CSV file to reflect the latest data in the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()

    # Write to CSV
    with open(CSV_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["RollNo", "Name", "Physics_Test1", "Physics_Test2", "Physics_Test3", "Physics_Final",
                         "Chemistry_Test1", "Chemistry_Test2", "Chemistry_Test3", "Chemistry_Final", "Maths_Test1",
                         "Maths_Test2", "Maths_Test3", "Maths_Final", "Computer_Test1", "Computer_Test2", "Computer_Test3",
                         "Computer_Final"])
        writer.writerows(rows)
    print("CSV file updated.")


def view_students():
    """Display all student records with original column names from the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Retrieve the column names from the SQLite database
    cursor.execute("PRAGMA table_info(students)")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]  # Extract column names from query result

    # Query all student records
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()

    # Print column names
    print(column_names)
    
    # Print student records
    for row in rows:
        print(row)


def search_student():
    """Search student by roll number or name and display column names."""
    search_term = input("Enter Roll Number or Name to search: ")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Retrieve the column names from the SQLite database
    cursor.execute("PRAGMA table_info(students)")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]  # Extract column names from query result

    # Query the students table for the search term
    cursor.execute("SELECT * FROM students WHERE RollNo = ? OR Name LIKE ?", (search_term, f"%{search_term}%"))
    rows = cursor.fetchall()
    conn.close()

    if rows:
        # Print column names
        print(column_names)

        # Print student records
        for row in rows:
            print(row)
    else:
        print("No records found.")



def update_student():
    """Update a student's record and the CSV file."""
    roll_no = input("Enter Roll Number of student to update: ")
    field = input("Enter field to update (e.g., Name, Physics_Test1): ")
    new_value = input("Enter new value: ")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE students SET {field} = ? WHERE RollNo = ?", (new_value, roll_no))
    conn.commit()
    conn.close()

    update_csv()  # Update CSV file after modifying the database
    print("Record updated successfully.")


def delete_student():
    """Delete a student's record and update the CSV file."""
    roll_no = input("Enter Roll Number of student to delete: ")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE RollNo = ?", (roll_no,))
    conn.commit()
    conn.close()

    update_csv()  # Update CSV file after deleting the record
    print("Record deleted successfully.")


def add_student():
    """Add a new student record to the database and CSV file."""
    roll_no = input("Enter Roll Number: ")
    name = input("Enter Name: ")
    physics_test1 = int(input("Enter Physics Test 1 score: "))
    physics_test2 = int(input("Enter Physics Test 2 score: "))
    physics_test3 = int(input("Enter Physics Test 3 score: "))
    physics_final = int(input("Enter Physics Final score: "))
    
    chemistry_test1 = int(input("Enter Chemistry Test 1 score: "))
    chemistry_test2 = int(input("Enter Chemistry Test 2 score: "))
    chemistry_test3 = int(input("Enter Chemistry Test 3 score: "))
    chemistry_final = int(input("Enter Chemistry Final score: "))
    
    maths_test1 = int(input("Enter Maths Test 1 score: "))
    maths_test2 = int(input("Enter Maths Test 2 score: "))
    maths_test3 = int(input("Enter Maths Test 3 score: "))
    maths_final = int(input("Enter Maths Final score: "))
    
    computer_test1 = int(input("Enter Computer Test 1 score: "))
    computer_test2 = int(input("Enter Computer Test 2 score: "))
    computer_test3 = int(input("Enter Computer Test 3 score: "))
    computer_final = int(input("Enter Computer Final score: "))

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO students (RollNo, Name, Physics_Test1, Physics_Test2, Physics_Test3, Physics_Final,
                          Chemistry_Test1, Chemistry_Test2, Chemistry_Test3, Chemistry_Final,
                          Maths_Test1, Maths_Test2, Maths_Test3, Maths_Final,
                          Computer_Test1, Computer_Test2, Computer_Test3, Computer_Final)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        roll_no, name, physics_test1, physics_test2, physics_test3, physics_final,
        chemistry_test1, chemistry_test2, chemistry_test3, chemistry_final,
        maths_test1, maths_test2, maths_test3, maths_final,
        computer_test1, computer_test2, computer_test3, computer_final
    ))
    conn.commit()
    conn.close()

    update_csv()  # Update CSV file after adding the new student
    print("New student added successfully.")


def main():
    csv_to_sqlite()
    while True:
        print("\nOptions:")
        print("1. View student records")
        print("2. Search student by roll number or name")
        print("3. Update student data")
        print("4. Delete student data")
        print("5. Add new student")
        print("6. Generate visualizations")
        print("7. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            view_students()
        elif choice == '2':
            search_student()
        elif choice == '3':
            update_student()
        elif choice == '4':
            delete_student()
        elif choice == '5':
            add_student()
        elif choice == '6':
            visualization_menu(DB_FILE)
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
