import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd

db_config = {
    'host': 'localhost',      
    'user': 'demotester',     
    'password': 'DaisyPixelJax!', 
    'database': 'MiddleSchoolDB' 
}

def connect_start():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Connected to the database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None
    
def select_query(query, values=None):
    connection = connect_start()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(query, values)
            result = cursor.fetchall()
            print("Query executed succeusfully")
            return result
        except Error as e:
            print(f"Error running query: {e}")
        finally:
            cursor.close()
            connection_end(connection)

def insert_query(query, values):
    connection = connect_start()
    if connection:
        cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
        st.success("Should insert correctly")

    except Error as e:
        st.error(f"Error: Running query: {e}")
    finally:
        cursor.close()
        connection_end(connection)
    

    
def connection_end(connection):
    if connection.is_connected():
        connection.close()
        print("Connection has been closed")


def main():
    st.title("Middle School Database")
    students = select_query("SELECT * FROM Students")
    fauclty = select_query("SELECT * FROM Faculty")
    roles = select_query("SELECT * FROM Roles")
    class_code = select_query("SELECT * FROM ClassCode")

    if students:
        column_labels = ['Student ID', 'First Name', 'Last Name', 'DOB','Grade','Guardian First','Guardian Last','Guardian Number', 'Guardian Email', 'Address']
        org_students = pd.DataFrame(students, columns=column_labels)


        st.subheader("Student Data")
        st.dataframe(org_students)

    if fauclty:
        column_labels = ["Faculty ID", "Faculty First", "Faculty Last", "Faculty Code",'Email', "Phone", "Class Subject"]
        org_faculty = pd.DataFrame(fauclty, columns=column_labels)

        st.subheader("Faculty Data")
        st.dataframe(org_faculty)

        if roles:
            with st.expander("Faculty Codes"):
                st.dataframe(roles)
        if class_code:
            with st.expander("Class Codes"):
                st.dataframe(class_code)

    tab1,tab2,tab3,tab4 = st.tabs(["Insert Data", "Delete Data", "Modify Data", "Test4"])

    with tab1:
        with st.form(key = 'create_form'):
            st.subheader("This is Tab1!")

            tb1,tb2,tb3 = st.tabs(["Students", "Faculty", "Enrollment"])
            
            with tb1:
                text =  st.text_input("Student's First Name")
                text1 = st.text_input("Student's Last Name")
                text2 = st.text_input("Date of Birth:  (Example: 1998-04-04) ")
                text3 = st.text_input("Grade")
                text4 = st.text_input("Guardian First Name")
                text5 = st.text_input("Guardian Last Name")
                text7 = st.text_input("Guardian Email")
                text6 = st.text_input("Guardian's Phone")
                text8 = st.text_input("Address")
                st.text("")
                st.text("")
                submit_students = st.form_submit_button("Submit")
                if submit_students:
                    if not text or not text1 or not text2 or not text3 or not text4 or not text5 or not text6 or not text7:
                        st.error("Please fill out all fields.")
                    else: 
                        new_data = """INSERT INTO Students (student_fname, student_lname, student_dob, grade, guardian_fname,
                                guardian_lname, guardian_number, guardian_email,guardian_address)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        new_submit = (text, text1, text2, text3, text4, text5, text6, text7, text8)

                        tester = insert_query(new_data, new_submit)
           
            with tb2:
                text = st.text_input("First Name")
                text1 = st.text_input("Last Name")
                text2 = st.text_input("Faculty Code")
                text3 = st.text_input("Email")
                text4 = st.text_input("Phone Number")
                text5 = st.text_input("class_code")

                submit_faculty = st.form_submit_button("New Faculty")
                if submit_faculty:
                    if not text or not text1 or not text2 or not text3 or not text4:
                        st.error("Please fill out all fields")
                    else:
                        if not text5 or text5 == 'Null' or text5 == 'null':
                            text5 = None
                        new_data = """INSERT INTO Faculty(faculty_fname, faculty_lname, faculty_code, 
                        faculty_email, faculty_phone, class_code)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                        new_submit = (text, text1, text2, text3, text4, text5)
                        tester = insert_query(new_data, new_submit)


            with tb3:
                rooms = select_query("SELECT * FROM Room")
                column_labels = ["Room ID","Room Number", "Floor", "Class Code"]
                org_rooms = pd.DataFrame(rooms, columns=column_labels)
                with st.expander("Rooms"):
                    st.dataframe(org_rooms)
                text = st.text_input("Student ID")
                text1 = st.text_input("Class Code")
                text2 = st.text_input("Room Number")
                text3 = st.text_input("Faculty ID")
                
                submit_enroll = st.form_submit_button("New Enroll")
                if submit_enroll:
                    if not text or not text1 or not text2 or not text3:
                        st.error("Please fill out all fields")
                    else:
                        new_data = """INSERT INTO Enroll(student_id, class_code, room_number, faculty_id)
                        VALUES (%s, %s, %s, %s)
                    """
                        new_submit = (text, text1, text2, text3)
                        tester = insert_query(new_data, new_submit)

    with tab2:
        with st.form(key = 'deleteForm'):
            st.subheader("this is tab2")
            delete, delete2, delete3 = st.tabs(["Student", "Faculty","Enrollment"])
            with delete:
                deleter = st.text_input("Enter Student ID:")
                submit = st.form_submit_button("Delete")
                if submit:
                    query = "DELETE FROM Students where student_id = %s"
                    insert_query(query, (deleter,))
            with delete2:
                deleter = st.text_input("Enter Faculty ID:")
                submit = st.form_submit_button("Delete.")
                if submit:
                    query = "DELETE FROM Faculty where faculty_id = %s"
                    insert_query(query, (deleter,))
            with delete3:
                deleter = st.text_input("Enter Enrollment ID:")
                submit = st.form_submit_button("Delete:")
                if submit:
                    query = "DELETE FROM Enroll where enrollment_id = %s"
                    insert_query(query, (deleter,))

    with tab3:
        with st.form(key ='modifyform'):
            mod1, mod2, mod3 = st.tabs(["Students", "Faculty", "Enrollment"])
            with mod1:
                studentID = st.text_input("Enter Student ID")
                try:
                    studentID = int(studentID)
                except:
                    st.error("Student ID must a number")
                choice = st.text_input("Enter: First Name, Last Name, DOB, Grade, Guardian First, Guardian Last, Guardian Number, Guardian Email, Address")
                choice = choice.lower().strip()
                change = st.text_input("Enter New Data:")
                submit = st.form_submit_button("Modify")
                if submit:
                    if choice == "first name":
                        choice = 'student_fname'
                    elif choice == 'last name':
                        choice = 'student_lname'
                    elif choice == 'dob':
                        choice = 'student_dob'
                    elif choice == 'grade':
                        choice = 'grade'
                    elif choice == 'guardian first':
                        choice = 'guardian_fname'
                    elif choice == 'guardian last':
                        choice = 'guardian_lname'
                    elif choice == 'guardian number':
                        choice = 'guardian_number'
                    elif choice == 'guardian email':
                        choice = 'guardian_email'
                    elif choice == 'address':
                        choice = 'guardian_address'
                    else:
                       st.error("Not a Valid input")
                       choice = None
                    if choice:
                        update = """
                        UPDATE Students
                        SET {} = %s
                        WHERE student_id = %s
                    """.format(choice)
                        newValues = (change, studentID)
                        insert_query(update,newValues)
            with mod2:
                facultyID = st.text_input("Enter Faculty ID")
                try:
                    facultyID = int(facultyID)
                except:
                    st.error("Faculty ID must a number")
                choice = st.text_input("Enter: First Name, Last Name, Faculty Code, Email, Phone, class code")
                choice = choice.lower().strip()
                change = st.text_input("Enter New Data :")
                submit = st.form_submit_button("Modify:")
                if submit:
                    if choice == "first name":
                        choice = 'faculty_fname'
                    elif choice == 'last name':
                        choice = 'faculty_lname'
                    elif choice == 'faculty code':
                        choice = 'faculty_code'
                    elif choice == 'email':
                        choice = 'faculty_email'
                    elif choice == 'phone':
                        choice = 'faculty_phone'
                    elif choice == 'class code':
                        choice = 'class_code'
                    else:
                       st.error("Not a Valid input")
                       choice = None
                    if choice:
                        update = """
                        UPDATE Faculty
                        SET {} = %s
                        WHERE faculty_id = %s
                    """.format(choice)
                        newValues = (change, facultyID)
                        insert_query(update,newValues)
            with mod3:
                enrollmentID = st.text_input("Enter Enrollment ID")
                try:
                    enrollmentID = int(enrollmentID)
                except:
                    st.error("Enrollment ID must a number")
                choice = st.text_input("Student ID, Class Code, Room Number, Faculty ID")
                choice = choice.lower().strip()
                change = st.text_input("Enter New Data  :")
                submit = st.form_submit_button("Modify.")
                if submit:
                    if choice == "student id":
                        choice = 'student_id'
                    elif choice == 'class code':
                        choice = 'class_code'
                    elif choice == 'room number':
                        choice = 'room_number'
                    elif choice == 'faculty id':
                        choice = 'faculty_id'
                    else:
                       st.error("Not a Valid input")
                       choice = None
                    if choice:
                        update = """
                        UPDATE Enroll
                        SET {} = %s
                        WHERE enrollment_id = %s
                    """.format(choice)
                        newValues = (change, enrollmentID)
                        insert_query(update,newValues)


                        

                    
            


if __name__ == "__main__":
    main()
