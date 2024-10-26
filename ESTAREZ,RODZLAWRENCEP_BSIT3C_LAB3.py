MAX_UNITS = 16

COST_PER_UNIT = 100

COURSES = {
    1: 'Bachelor of Science in Information Technology (BSIT)',
    2: 'Bachelor of Science in Geodetic Engineering (BSGE)',
    3: 'Bachelor of Science in Agricultural and Biosystems Engineering (BSABEn)',
    4: 'Bachelor of Science in Food Technology (BSFT)'
}

EARS = {1: 'First Year'}
SEMESTERS = {1: 'First Semester'}

subjects = {
    1: { #first year Subject
        'First Year': { 
            'First Semester': {
                1: {'subject_name': 'Introduction to IT', 'units': 3},
                2: {'subject_name': 'Programming 1', 'units': 3},
                3: {'subject_name': 'Data Structures', 'units': 3},
                4: {'subject_name': 'Web Development', 'units': 3},
                5: {'subject_name': 'Physical Education 1', 'units': 2}
            }
        }
    },
    2: {
        'First Year': {
            'First Semester': {
                1: {'subject_name': 'Basic Surveying', 'units': 3},
                2: {'subject_name': 'Geodesy', 'units': 3},
                3: {'subject_name': 'Engineering Drawing', 'units': 3},
                4: {'subject_name': 'Calculus 1', 'units': 3},
                5: {'subject_name': 'Physical Education 1', 'units': 2}
            }
        }
    },
    3: {
        'First Year': {
            'First Semester': {
                1: {'subject_name': 'Agricultural Science', 'units': 3},
                2: {'subject_name': 'Soil Science', 'units': 3},
                3: {'subject_name': 'Biology 1', 'units': 3},
                4: {'subject_name': 'Chemistry 1', 'units': 3},
                5: {'subject_name': 'Physical Education 1', 'units': 2}
            }
        }
    },
    4: {
        'First Year': {
            'First Semester': {
                1: {'subject_name': 'Food Science Fundamentals', 'units': 3},
                2: {'subject_name': 'Nutrition', 'units': 3},
                3: {'subject_name': 'Food Microbiology', 'units': 3},
                4: {'subject_name': 'Food Chemistry', 'units': 3},
                5: {'subject_name': 'Physical Education 1', 'units': 2}
            }
        }
    }
}

students = {}

def get_yes_no_input(prompt):
    while True:
        response = input(prompt).strip().upper()
        if response in ['Y', 'N']:
            return response
        print("Invalid input. Please enter 'Y' or 'N'.")

def get_int_input(prompt, valid_range):
    while True:
        try:
            choice = int(input(prompt))
            if choice in valid_range:
                return choice
            print(f"Please select a valid option: {valid_range}")
        except ValueError:
            print("Invalid input. Please enter a number.")

def display_courses():
    print("Available Courses:")
    for key, value in COURSES.items():
        print(f"{key}: {value}")

def select_subjects(subjects, existing_units):
    selected_subjects = []
    print("Available Subjects:")
    for idx, subject in enumerate(subjects.values(), start=1):
        print(f"{idx}: {subject['subject_name']} ({subject['units']} units)")
    
    while True:
        subject_choice = get_int_input("Select the subject number (0 to finish): ", range(0, len(subjects) + 1))
        if subject_choice == 0:
            break
        selected_subject = subjects[subject_choice]
        if existing_units + selected_subject['units'] > MAX_UNITS:
            print("Adding this subject exceeds the maximum units. Please select a different subject.")
        else:
            selected_subjects.append(selected_subject)
            existing_units += selected_subject['units']
    
    return selected_subjects

def enroll_student():
    student_name = input("Enter student name: ").strip()
    student_id = input("Enter student ID: ").strip()
    student_age = input("Enter student age: ").strip()

    if not student_age.isdigit():
        print("Invalid age. Enrollment cancelled.")
        return
    
    student_age = int(student_age)
    student_address = input("Enter student address: ").strip()

    print("Demographic Information")
    print(f"Name: {student_name}")
    print(f"ID: {student_id}")
    print(f"Age: {student_age}")
    print(f"Address: {student_address}")
    print("------------------------------------------------------")

    display_courses()  # Display courses 
    selected_course_choice = get_int_input("Select the course number: ", valid_range=COURSES.keys())
    selected_course = COURSES[selected_course_choice]
    course_subjects = subjects[selected_course_choice]['First Year']['First Semester']
    selected_subjects = select_subjects(course_subjects, existing_units=0)

    total_units = sum(subject['units'] for subject in selected_subjects)
    total_units = enroll_additional_subjects(selected_course_choice, total_units, selected_subjects)
    total_fee = total_units * COST_PER_UNIT

    if get_yes_no_input(f"Do you want to enroll {student_name}? (Y/N): ") == 'Y':
        students[student_name] = {
            'id': student_id,
            'age': student_age,
            'address': student_address,
            'course': selected_course,
            'subjects': selected_subjects,
            'total_units': total_units,
            'total_fee': total_fee
        }
        print_certificate_of_registration(student_name, student_age, student_address, selected_course, selected_subjects, total_units, total_fee)
    else:
        print("Enrollment cancelled.")

def enroll_additional_subjects(course_choice, total_units, selected_subjects):
    while total_units < MAX_UNITS:
        additional_choice = get_yes_no_input("Do you want to enroll in more subjects? (Y/N): ")
        if additional_choice == 'N':
            break
        other_courses = [key for key in COURSES.keys() if key != course_choice]
        new_course_choice = get_int_input("Select another course from the available options: ", valid_range=other_courses)
        new_subjects = subjects[new_course_choice]['First Year']['First Semester']
        selected_additional_subjects = select_subjects(new_subjects, existing_units=total_units)
        selected_subjects.extend(selected_additional_subjects)
        total_units = sum(subject['units'] for subject in selected_subjects)

        if total_units >= MAX_UNITS:
            print("You have reached the maximum units (16 units). No more subjects can be added.")
            break
    
    return total_units

def print_certificate_of_registration(student_name, student_age, student_address, course, subjects, total_units, total_fee):
    print("\n--- Certificate of Registration (COR) ---")
    print(f"Student Name: {student_name}")
    print(f"ID: {students[student_name]['id']}")
    print(f"Age: {student_age}")
    print(f"Address: {student_address}")
    print(f"Course: {course}")
    print("\nEnrolled Subjects:")
    for subject in subjects:
        print(f"- {subject['subject_name']} ({subject['units']} units)")
    
    print(f"\nTotal Units: {total_units}")
    print(f"Total Fee: ₱{total_fee:,.2f}")
    print("--------------------------------------------------------------")

def main():
    while True:
        print("1. Enroll Student")
        print("2. Exit")
        choice = get_int_input("Select an option: ", [1, 2])
        if choice == 1:
            enroll_student()
        elif choice == 2:
            print("Exiting the program. Goodbye!")
            break

main()