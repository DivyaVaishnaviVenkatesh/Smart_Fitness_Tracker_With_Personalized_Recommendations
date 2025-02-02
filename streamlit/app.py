import streamlit as st
from streamlit_option_menu import option_menu
import json
import pandas as pd
from test import *
from Custom_Diet import *
from PIL import Image
import sqlite3
from db_operations import get_all_contact_messages, get_all_diets, get_all_medicines, get_all_workouts, insert_contact_message

# Function to initialize the database and create the required tables
def init_db():
    # Connect to SQLite database (this will create the db if it doesn't exist)
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()

    # Create user_data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            level TEXT,
            workout_plan TEXT
        )
    ''')

    # Create contact_messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('DROP TABLE IF EXISTS diets')

    # Create diets table with the updated schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            dosage TEXT,
            frequency TEXT,
            side_effects TEXT
        )
    ''')
    cursor.execute('DROP TABLE IF EXISTS medicines')
    # Create medicines table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        disease_name TEXT,
        medicine_name TEXT,
        dosage_form TEXT,
        strength TEXT,
        instructions TEXT
    )
''')

    # Create workouts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            level TEXT,
            duration INTEGER
        )
    ''')

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Database initialized and tables created successfully!")

# Call the init_db function to initialize the database
init_db()

# Function to insert user data into the user_data table
def insert_user_data(age, level, workout_plan):
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO user_data (age, level, workout_plan)
            VALUES (?, ?, ?)
        ''', (age, level, workout_plan))
        conn.commit()
        print(f"Inserted user data: Age={age}, Level={level}, Workout Plan={workout_plan}")
    except sqlite3.Error as e:
        print(f"Error inserting user data: {e}")
    finally:
        conn.close()

# Function to insert workout data into the workouts table
def insert_workout_data(name, description, level, duration):
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO workouts (name, description, level, duration)
            VALUES (?, ?, ?, ?)
        ''', (name, description, level, duration))
        conn.commit()
        print(f"Inserted workout data: Name={name}, Description={description}, Level={level}, Duration={duration}")
    except sqlite3.Error as e:
        print(f"Error inserting workout data: {e}")
    finally:
        conn.close()

# Function to insert contact message into the contact_messages table
def insert_contact_message(name, email, message):
    print(f"Debug - Inserting Contact Message: {name}, {email}, {message}")  # Debug
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO contact_messages (name, email, message)
            VALUES (?, ?, ?)
        ''', (name, email, message))
        conn.commit()
        print(f"Inserted contact message: Name={name}, Email={email}, Message={message}")
    except sqlite3.Error as e:
        print(f"Error inserting contact message: {e}")
    finally:
        conn.close()

# Function to fetch user data from the user_data table
def fetch_user_data():
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_data')
    data = cursor.fetchall()
    conn.close()
    return data

# Function to display contact messages
def display_contact_messages():
    messages = get_all_contact_messages()
    for message in messages:
        st.write(f"Name: {message[1]}")
        st.write(f"Email: {message[2]}")
        st.write(f"Message: {message[3]}")
        st.write(f"Date: {message[4]}")
        st.write("---")

# Function to display diets
def display_diets():
    diets = get_all_diets()
    for diet in diets:
        st.write(f"Diet Name: {diet[1]}")
        st.write(f"Description: {diet[2]}")
        st.write(f"Type: {diet[3]}")
        st.write(f"Calories: {diet[4]}")
        st.write("---")

# Function to display medicines
def display_medicines():
    medicines = get_all_medicines()
    for medicine in medicines:
        st.write(f"Medicine Name: {medicine[1]}")
        st.write(f"Dosage: {medicine[2]}")
        st.write(f"Frequency: {medicine[3]}")
        st.write(f"Side Effects: {medicine[4]}")
        st.write("---")

# Function to display workouts
def display_workouts():
    workouts = get_all_workouts()
    for workout in workouts:
        st.write(f"Workout Name: {workout[1]}")
        st.write(f"Description: {workout[2]}")
        st.write(f"Level: {workout[3]}")
        st.write(f"Duration: {workout[4]} minutes")
        st.write("---")


# Page Basic info
st.set_page_config(
    page_title='Smart Fitness Tracker with Personalized Recommendations',
    page_icon='Fitness_bloom.png'
)

# Side bar initialization and creation
with st.sidebar:
    selected = option_menu(
        menu_title='SFTPR',
        options=['Home', 'Diet', 'Workout Suggestion', 'Medicine Recommender', 'Contact'],
        icons=['house', 'flower3', 'wrench', 'clipboard2-x', 'envelope'],
    )

# Homepage
def homepage():
    st.title("Smart Fitness Tracker with Personalized Recommendations")
    words = '''
        <p style="font-style:italic; font-family:cursive;">
    Smart Fitness Tracker and Personalized Recommendations is an intelligent system that provides customized suggestions  
    for diet, medicine, and workout plans based on user data.
    </p>
    <p style="font-style:italic; font-family:cursive;">
    This machine learning-powered app uses collaborative and content-based filtering to generate personalized recommendations.
    </p>
    <p style="font-style:italic; font-family:cursive;">
    This is a prototype of the actual system, and we plan to introduce various enhancements in the future.
    </p>
    '''

    tech_stack = '''
        <ul>
            <li style="font-style:italic; font-family:cursive;">Dataset: CSV, JSON Files</li>
            <li style="font-style:italic; font-family:cursive;">Others libraries: Pandas, Numpy, Sklearn, Streamlit, Json</li>
            <li style="font-style:italic; font-family:cursive;">Programming: Python, Notebook</li>
            <li style="font-style:italic; font-family:cursive;">Visualization tools: Matplotlib, Plotly</li>
        </ul>
    '''
    
    image = Image.open('first.jpg')

    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown(words, unsafe_allow_html=True)
    with right_column:
        st.image(image, use_column_width=True)

    st.title('Dataset')
    st.subheader("User Data from Database:")
    data = fetch_user_data()
    for row in data:
        st.write(f"User {row[0]}: Age - {row[1]}, Level - {row[2]}, Workout Plan - {row[3]}")

    files = load_data()

    json_files = get_suggestion(files, 10)
    data_files = get_data(json_files)

    st.dataframe(data_files)

    st.title('Tech Stack')
    st.markdown(tech_stack, unsafe_allow_html=True)

if selected == 'Home':
    homepage()

# Defining CSS file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Loading CSS
local_css('style.css')

# Contact Form Frontend
def form():
    with st.container():
        st.write("---")
        st.header('Get In Touch With Me!')
        st.write('##')

        # Input fields for the contact form
        name = st.text_input('Your Full Name', key='name')
        email = st.text_input('Your Email ID', key='email')
        message = st.text_area('Your Message', key='message')

        # Submit button
        if st.button('Send'):
            # Check if all fields are filled
            if name and email and message:
                # Insert the contact message into the database
                insert_contact_message(name, email, message)
                st.success("Message sent successfully!")
            else:
                st.warning("Please fill in all fields before submitting.")
if selected == 'Contact':
    form()

# Exercise JSON Dataset
exercise_by_level ={
    'beginner':{
        'Monday':['20 Squats','10 Push-ups','10 Lunges Each leg','15 seconds Plank','30 Jumping Jacks'],
        'Tuesday':['20 Squats','10 Push-ups','10 Lunges Each leg','15 seconds Plank','30 Jumping Jacks'],
        'Wednesday':['15 minutes Walk','30 seconds Jump rope(2 reps)','20 seconds Cobra Stretch'],
        'Thursday':['25 Squats','12 Push-ups','12 Lunges Each leg','15 seconds Plank','30 Jumping Jacks'],
        'Friday':['25 Squats','12 Push-ups','12 Lunges Each leg','15 seconds Plank','30 Jumping Jacks'],
        'Saturday':['15 minutes Walk','30 seconds Jump rope(2 reps)','20 seconds Cobra Stretch']
    },
    'intermediate':{
        'Monday':['3 Set Squats(8-12 reps)','3 Set Leg Extension(8-12 reps)','3 Set Lunges(10 reps Each)','30 Seconds Skipping(2 reps)'],
        'Tuesday':['3 Set Bench Press(12 reps)','3 Set Dumb-bell incline press(8-12 reps)','3 Set Cable Crossovers(10-12 reps)','30 Seconds Boxing Skip(2 reps)'],
        'Wednesday':['3 Set Deadlifts(6-12 reps)','3 Set Barbell Curls(8-12 reps)','3 Set Incline Curls(8-12 reps)'],
        'Thursday':['3 Set Shoulder Press(8-10 reps)','3 Set Incline Lateral Raises(8-10 reps)','3 Set Sit-ups(10-12 reps)','2 Set Leg Raises(8-12 reps)'],
        'Friday':['10 minutes Brisk Walk','1 minute Skipping','Breathing Exercises'],
        'Saturday':['10 minutes Brisk Walk','1 minute Skipping','Breathing Exercises']
    },
    'advanced':{
        'Monday':['5 Set Squats(8-12 reps)','5 Set Leg Extension(8-12 reps)','5 Set Lunges(10 reps Each)','60 Seconds Skipping(2 reps)'],
        'Tuesday':['5 Set Bench Press(12 reps)','5 Set Dumb-bell incline press(8-12 reps)','5 Set Cable Crossovers(10-12 reps)','60 Seconds Boxing Skip(2 reps)'],
        'Wednesday':['5 Set Deadlifts(6-12 reps)','5 Set Barbell Curls(8-12 reps)','5 Set Incline Curls(8-12 reps)'],
        'Thursday':['5 Set Shoulder Press(8-10 reps)','5 Set Incline Lateral Raises(8-10 reps)','5 Set Sit-ups(10-12 reps)','4 Set Leg Raises(8-12 reps)'],
        'Friday':['20 minutes Brisk Walk','2 minute Boxing Skip','Breathing Exercises'],
        'Saturday':['25 minutes Brisk Walk','1 minute Skipping','Breathing Exercises']
    }
}

def generate_workout(level):
    # Return the workout plan for the selected level
    return exercise_by_level[level]

# For Workout Suggestion
if selected == 'Workout Suggestion':
    st.title('Personalized Workout Recommender')

    age = st.selectbox('Age',['Select','Less than 18','18 to 49', '49 to 60','Above 60'])

    options = ['Less frequently','Moderate','More Frequently']

    duration = st.radio('Workout Duration:', options)

    level = st.selectbox('Select your level:',['Select','beginner','intermediate','advanced'])

    button = st.button('Recommend Workout')

    if button:
        nums = 1

        if level == 'Select':
            st.warning('Insertion error!! Re-check the input fields')

        else:
            workout_plan = generate_workout(level)
            for day, exercises in exercise_by_level[level].items():
                exercise_str = ",".join(exercises)
               
                # Insert workout data into the workouts table
                insert_workout_data(f"Day {nums} Workout", exercise_str, level, 30)  # Assuming 30 minutes duration

                # Display workout plan
                st.markdown(
                    f"""
                    <h4>Your Workout Plan For Day {nums}</h4>
                    <div class="workout">
                        <div class="workout-info">
                            <p style="color:#7FFF00; font-style:italic; font-family:cursive;">Day:{day}</p>
                            <p style="color:#7FFF00; font-style:italic; font-family:cursive;">Workout:{exercise_str}</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                nums += 1

            st.markdown(
                f"""
                <h4> Your Workout Plan for Day {nums}</h4>
                <div class="sundays">
                    <p style="color:#7FFF00; font-style:italic; font-family:cursive;">Take rest at Sundays and do a little walk in the park</p>
                </div>
                """,
                unsafe_allow_html=True)

            # Insert user data into the user_data table
            insert_user_data(age, level, str(workout_plan))

# For Medicine Recommender
if selected == 'Medicine Recommender':
    main_1()

# For custom food recommendations
if selected == 'Diet':    
    diet()