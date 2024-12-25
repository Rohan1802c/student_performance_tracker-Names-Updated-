import matplotlib.pyplot as plt
import sqlite3

def fetch_data(db_file, query, params=()):
    """Fetch data from the SQLite database based on the provided query."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(query, params)
    data = cursor.fetchall()
    conn.close()
    return data


def plot_student_performance(db_file, roll_no):
    """Bar chart: Compare marks across subjects for a specific student."""
    data = fetch_data(
        db_file,
        """
        SELECT Name, Physics_Final, Chemistry_Final, Maths_Final, Computer_Final
        FROM students
        WHERE RollNo = ?
        """,
        (roll_no,)
    )

    if not data:
        print(f"No student found with Roll No: {roll_no}")
        return

    name, physics, chemistry, maths, computer = data[0]
    marks = [physics, chemistry, maths, computer]
    subjects = ['Physics', 'Chemistry', 'Maths', 'Computer']

    plt.bar(subjects, marks, color=['blue', 'green', 'orange', 'red'])
    plt.title(f'Marks Comparison for {name} (Roll No: {roll_no})')
    plt.xlabel('Subjects')
    plt.ylabel('Marks')
    plt.ylim(0, 100)
    plt.show()


def student_progress_across_tests(db_file, roll_no):
    """Line graph: Track a student's progress across tests in all subjects."""
    data = fetch_data(
        db_file,
        """
        SELECT Name, Physics_Test1, Physics_Test2, Physics_Test3, Chemistry_Test1,
               Chemistry_Test2, Chemistry_Test3, Maths_Test1, Maths_Test2, Maths_Test3,
               Computer_Test1, Computer_Test2, Computer_Test3
        FROM students
        WHERE RollNo = ?
        """,
        (roll_no,)
    )

    if not data:
        print(f"No student found with Roll No: {roll_no}")
        return

    name, *marks = data[0]
    tests = ['Test1', 'Test2', 'Test3']
    subjects = ['Physics', 'Chemistry', 'Maths', 'Computer']

    plt.figure(figsize=(10, 6))
    for i, subject in enumerate(subjects):
        plt.plot(tests, marks[i*3:(i+1)*3], marker='o', label=subject)

    plt.title(f'Test Performance Trend for {name} (Roll No: {roll_no})')
    plt.xlabel('Tests')
    plt.ylabel('Marks')
    plt.legend()
    plt.grid()
    plt.ylim(0, 50)
    plt.show()


def subject_top_5_students(db_file, subject):
    """Bar chart: Top 5 students in a specific subject."""
    data = fetch_data(
        db_file,
        f"""
        SELECT Name, {subject}_Final
        FROM students
        ORDER BY {subject}_Final DESC
        LIMIT 5
        """
    )
    if not data:
        print(f"No data available for the subject: {subject}")
        return

    names = [row[0] for row in data]
    marks = [row[1] for row in data]

    plt.bar(names, marks, color='gold')
    plt.title(f'Top 5 Students in {subject}')
    plt.xlabel('Students')
    plt.ylabel('Marks')
    plt.ylim(0, 100)
    plt.show()


def subject_pass_fail_ratio(db_file, subject):
    """Pie chart: Pass/Fail ratio for a specific subject."""
    pass_count = fetch_data(db_file, f"SELECT COUNT(*) FROM students WHERE {subject}_Final >= 40")[0][0]
    fail_count = fetch_data(db_file, f"SELECT COUNT(*) FROM students WHERE {subject}_Final < 40")[0][0]

    labels = ['Pass', 'Fail']
    values = [pass_count, fail_count]
    colors = ['green', 'red']

    plt.pie(values, labels=labels, autopct=lambda p: f'{p:.1f}%', startangle=90, colors=colors)
    plt.title(f'Pass/Fail Ratio in {subject}')
    plt.show()


def subject_trend_average_tests(db_file, subject):
    """Line graph: Average marks in tests over time for a subject."""
    data = fetch_data(
        db_file,
        f"""
        SELECT AVG({subject}_Test1), AVG({subject}_Test2), AVG({subject}_Test3)
        FROM students
        """
    )

    if not data:
        print(f"No data available for the subject: {subject}")
        return

    averages = list(data[0])
    tests = ['Test1', 'Test2', 'Test3']

    plt.plot(tests, averages, marker='o', color='blue')
    plt.title(f'Average Test Performance Trend in {subject}')
    plt.xlabel('Tests')
    plt.ylabel('Average Marks')
    plt.ylim(0, 50)
    plt.grid()
    plt.show()


def overall_class_performance(db_file):
    """Bar chart: Average marks for the entire class across all subjects."""
    data = fetch_data(
        db_file,
        """
        SELECT AVG(Physics_Final), AVG(Chemistry_Final), AVG(Maths_Final), AVG(Computer_Final)
        FROM students
        """
    )

    if not data:
        print("No data available for class performance.")
        return

    averages = list(data[0])
    subjects = ['Physics', 'Chemistry', 'Maths', 'Computer']

    plt.bar(subjects, averages, color=['blue', 'green', 'orange', 'red'])
    plt.title('Overall Class Performance Across Subjects')
    plt.xlabel('Subjects')
    plt.ylabel('Average Marks')
    plt.ylim(0, 100)
    plt.show()


def subject_distribution(db_file):
    """Boxplot: Distribution of marks for all students in each subject."""
    data = fetch_data(
        db_file,
        """
        SELECT Physics_Final, Chemistry_Final, Maths_Final, Computer_Final
        FROM students
        """
    )

    if not data:
        print("No data available for distribution analysis.")
        return

    subjects = ['Physics', 'Chemistry', 'Maths', 'Computer']
    plt.boxplot(list(zip(*data)), labels=subjects, patch_artist=True)
    plt.title('Subject-Wise Distribution of Marks')
    plt.ylabel('Marks')
    plt.ylim(0, 100)
    plt.grid()
    plt.show()


def overall_test_trend(db_file):
    """Line graph: Average marks across all tests for all subjects."""
    data = fetch_data(
        db_file,
        """
        SELECT AVG(Physics_Test1), AVG(Physics_Test2), AVG(Physics_Test3),
               AVG(Chemistry_Test1), AVG(Chemistry_Test2), AVG(Chemistry_Test3),
               AVG(Maths_Test1), AVG(Maths_Test2), AVG(Maths_Test3),
               AVG(Computer_Test1), AVG(Computer_Test2), AVG(Computer_Test3)
        FROM students
        """
    )

    if not data:
        print("No data available for overall test trend.")
        return

    averages = list(data[0])
    tests = ['Test1', 'Test2', 'Test3']
    subjects = ['Physics', 'Chemistry', 'Maths', 'Computer']

    plt.figure(figsize=(10, 6))
    for i, subject in enumerate(subjects):
        plt.plot(tests, averages[i*3:(i+1)*3], marker='o', label=subject)

    plt.title('Overall Class Test Trends')
    plt.xlabel('Tests')
    plt.ylabel('Average Marks')
    plt.legend()
    plt.grid()
    plt.ylim(0, 50)
    plt.show()


def visualization_menu(db_file):
    """Display visualization options and generate selected graph."""
    while True:
        print("\nVisualization Options:")
        print("1. Student performance comparison across subjects")
        print("2. Student progress across tests in all subjects")
        print("3. Top 5 students in a specific subject")
        print("4. Subject pass/fail ratio")
        print("5. Subject average marks across tests")
        print("6. Overall class performance across subjects")
        print("7. Subject-wise distribution of marks")
        print("8. Overall test trends")
        print("9. Exit")

        choice = input("Enter your choice: ")
        
        if choice == '1':
            roll_no = input("Enter Roll Number: ")
            plot_student_performance(db_file, roll_no)
        elif choice == '2':
            roll_no = input("Enter Roll Number: ")
            student_progress_across_tests(db_file, roll_no)
        elif choice == '3':
            subject = input("Enter Subject (Physics, Chemistry, Maths, Computer): ").capitalize()
            subject_top_5_students(db_file, subject)
        elif choice == '4':
            subject = input("Enter Subject (Physics, Chemistry, Maths, Computer): ").capitalize()
            subject_pass_fail_ratio(db_file, subject)
        elif choice == '5':
            subject = input("Enter Subject (Physics, Chemistry, Maths, Computer): ").capitalize()
            subject_trend_average_tests(db_file, subject)
        elif choice == '6':
            overall_class_performance(db_file)
        elif choice == '7':
            subject_distribution(db_file)
        elif choice == '8':
            overall_test_trend(db_file)
        elif choice == '9':
            print("Exiting visualization menu.")
            break
        else:
            print("Invalid choice. Please try again.")
