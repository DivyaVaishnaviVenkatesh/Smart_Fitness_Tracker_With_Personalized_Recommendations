import streamlit as st
from streamlit_option_menu import option_menu
import json
import pandas as pd
from test import *
from Custom_Diet import *
from PIL import Image
import sqlite3
import matplotlib.pyplot as plt 
from db_operations import get_all_contact_messages, get_all_diets, get_all_medicines, get_all_workouts, insert_contact_message

# Function to initialize the database and create the required tables
def init_db():
    # Connect to SQLite database (this will create the db if it doesn't exist)
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS user_data')
    # Create user_data table
    cursor.execute('''
         CREATE TABLE IF NOT EXISTS user_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
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
            username TEXT,
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
        username TEXT,
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
            username TEXT,
            name TEXT,
            description TEXT,
            level TEXT,
            duration INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progress_tracker (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            weight REAL,
            calories_burned REAL,
            diet TEXT,
            workout TEXT,
            progress TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Database initialized and tables created successfully!")

# Call the init_db function to initialize the database
init_db()

# Function to insert user data into the user_data table
def insert_user_data(username, age, level, workout_plan):
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO user_data (username, age, level, workout_plan)
            VALUES (?, ?, ?, ?)
        ''', (username, age, level, workout_plan))
        conn.commit()
        print(f"Inserted user data: Username={username}, Age={age}, Level={level}, Workout Plan={workout_plan}")
    except sqlite3.Error as e:
        print(f"Error inserting user data: {e}")
    finally:
        conn.close()

# Function to insert workout data into the workouts table
def insert_workout_data(username, name, description, level, duration):
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO workouts (username, name, description, level, duration)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, name, description, level, duration))
        conn.commit()
        print(f"Inserted workout data: Username={username}, Name={name}, Description={description}, Level={level}, Duration={duration}")
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
def fetch_user_data(username):
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_data WHERE username = ?', (username,))
    data = cursor.fetchall()
    conn.close()
    return data

def fetch_workouts(username):
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM workouts WHERE username = ?', (username,))
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
    workouts = fetch_workouts(st.session_state.username)
    for workout in workouts:
        st.write(f"Workout Name: {workout[2]}")
        st.write(f"Description: {workout[3]}")
        st.write(f"Level: {workout[4]}")
        st.write(f"Duration: {workout[5]} minutes")
        st.write("---")

# Page Basic info
st.set_page_config(
    page_title='Smart Fitness Tracker with Personalized Recommendations',
    page_icon='Fitness_bloom.png'
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Side bar initialization and creation
with st.sidebar:
  if st.session_state.logged_in:
    selected = option_menu(
       
        menu_title="SFTPR",
        options=[
            "Home", "Diet", "Workout Suggestion", "Medicine Recommender", 
            "Progress Tracker", 
            "Health Tips", "Contact", "Settings"
        ],
        icons=[
            "house", "flower3", "wrench", "clipboard2-x", 
            "bar-chart", "trophy", "people", 
            "heart-pulse", "envelope", "gear"
        ],
        menu_icon="cast",
        default_index=0
    )
    if st.session_state.username:
            st.markdown(f"### Hello, **{st.session_state.username}** 👋")
    else:
            st.markdown("### Hello, Guest 👋 (Please login!)")
    if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.user_id = None
                st.success("Logged out successfully!")
                st.experimental_rerun()
  else:
            selected = "Login"



def register_user(username, password):
    """Register a new user."""
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (username, password)
            VALUES (?, ?)
        ''', (username, password))
        conn.commit()
        st.success("Registration successful! Please log in.")
        st.session_state.show_signup = False  # Redirect to login after registration
    except sqlite3.IntegrityError:
        st.error("Username already exists. Please choose a different username.")
    except Exception as e:
        st.error(f"Error during registration: {e}")
    finally:
        conn.close()

def login_user(username, password):
    """Authenticate a user."""
    conn = sqlite3.connect('fitness.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id FROM users WHERE username = ? AND password = ?
    ''', (username, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        st.session_state.user_id = user[0]
        st.session_state.username = username  # Store username in session state
        st.session_state.logged_in = True
        st.success(f"🎉 Logged in as **{username}**")
        st.experimental_rerun()
    else:
        st.error("❌ Invalid username or password.")

# Login Page
def login_page():
    # Ensure session state variables do not persist unwanted values
    if "login_username" in st.session_state:
        del st.session_state["login_username"]

    st.markdown("<h2 style='text-align: center; color: #4CAF50;'>Login</h2>", unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("👤 Username", placeholder="Enter your username", key="username_input")  
        password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")  

        if st.form_submit_button("Login", use_container_width=True):
            user = login_user(username, password)
            if user:
                st.session_state.user_id = user[0]
                st.session_state.username = username
                st.session_state.logged_in = True
                st.success(f"🎉 Logged in as **{username}**")
                st.experimental_rerun()
            else:
                st.error("❌ Invalid username or password.")

    if st.button("Don't have an account? Sign Up"):
        st.session_state.show_signup = True
        st.experimental_rerun()

def signup_page():
    st.markdown("<h2 style='text-align: center; color: #FF5733;'>Sign Up</h2>", unsafe_allow_html=True)
    with st.form("register_form"):
        new_username = st.text_input("👤 Choose a Username", key="register_username")
        new_password = st.text_input("🔑 Password", type="password", key="register_password")
        confirm_password = st.text_input("🔄 Confirm Password", type="password", key="confirm_password")

        if st.form_submit_button("Register", use_container_width=True):
            if new_password == confirm_password:
                register_user(new_username, new_password)
            else:
                st.error("❌ Passwords do not match.")

    if st.button("Already have an account? Login"):
        st.session_state.show_signup = False
        st.experimental_rerun()


if not st.session_state.logged_in:
    if st.session_state.show_signup:
        signup_page()
    else:
        login_page()
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

    # Fetch user data using the username from session state
    
    

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


def progress_tracker():
    st.title("🏋️ Track Your Progress")
    st.write("Log your workouts and health journey.")

    # User input fields
    username = st.text_input("Enter Your Username")
    weight = st.number_input("Enter Your Current Weight (kg)", min_value=30.0, max_value=200.0)
    calories = st.number_input("Calories Burned Today", min_value=0)
    diet = st.text_area("Describe Your Diet")
    workout = st.text_area("Describe Your Workout")
    progress = st.text_area("Your Overall Progress Notes")

    if st.button("Save Progress"):
        if username:
            conn = sqlite3.connect('fitness.db')
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO progress_tracker (username, weight, calories_burned, diet, workout, progress)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, weight, calories, diet, workout, progress))
            conn.commit()
            conn.close()
            st.success("✅ Progress saved successfully!")
        else:
            st.warning("⚠️ Please enter a username.")

    # Fetch and visualize data
    st.subheader("📊 Your Progress Overview")
    conn = sqlite3.connect('fitness.db')
    df = pd.read_sql("SELECT * FROM progress_tracker WHERE username = ?", conn, params=(username,))
    conn.close()

    if not df.empty:
        st.write("### Recent Entries")
        st.dataframe(df)

        # Weight Progress Chart
        st.write("### 📉 Weight Progress Over Time")
        fig, ax = plt.subplots()
        ax.plot(df['timestamp'], df['weight'], marker='o', linestyle='-')
        ax.set_xlabel("Date")
        ax.set_ylabel("Weight (kg)")
        ax.set_title("Weight Progress")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Calories Burned Chart
        st.write("### 🔥 Calories Burned Over Time")
        fig, ax = plt.subplots()
        ax.bar(df['timestamp'], df['calories_burned'], color='orange')
        ax.set_xlabel("Date")
        ax.set_ylabel("Calories Burned")
        ax.set_title("Calories Burned Progress")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.info("ℹ️ No progress data found. Start logging your progress!")

if selected == "Progress Tracker":
    progress_tracker()


# Set initial theme to Dark
if "theme" not in st.session_state:
    st.session_state.theme = "dark"  # Default to dark mode


def apply_theme():
    """Applies the selected theme using CSS injection."""
    if st.session_state.theme == "dark":
        dark_theme = """
        <style>
            body, .stApp { background-color: #0E1117; color: #FFFFFF; }
            
            /* Text and headings */
            h1, h2, h3, h4, h5, h6, p, div, span, label { color: #FFFFFF; }
            
            
            /* Input fields */
            .stTextInput>div>div>input, .stTextArea>div>div>textarea { 
                color: #FFFFFF; 
                background-color: #1E1E1E; 
                border: 1px solid #333333;
            }

            /* Select boxes */
            .stSelectbox>div>div>select, .stRadio>div>div>label { 
                color: #FFFFFF; 
                background-color: #1E1E1E; 
            }
            
            /* Buttons */
            .stButton>button { 
                color: #FFFFFF; 
                background-color: #4CAF50; 
                border: 1px solid #4CAF50; 
            }
            
            /* Dataframes */
            .stDataFrame { color: #FFFFFF; background-color: #1E1E1E; }
        </style>
        """
        st.markdown(dark_theme, unsafe_allow_html=True)
    
    else:
        light_theme = """
    <style>
    body, .stApp { background-color: #FFFFFF; color: #000000; }
    
    /* Text and headings */
    h1, h2, h3, h4, h5, h6, p, div, span, label { color: #000000 !important; }
    
    /* Input fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { 
        color: #000000 !important; 
        background-color: #F0F2F6 !important; 
        border: 1px solid #CCCCCC !important;
    }
    
    /* Select boxes & Radio buttons */
    .stSelectbox>div>div>select, .stRadio>div>div>label { 
        color: #FFFFFF !important; 
        background-color: #F0F2F6 !important; 
    }

    /* Fix for dropdown options */
    .stSelectbox>div>div>select option {
        color: #FFFFFF !important;
        background-color: #FFFFFF !important;
    }

    /* Buttons */
    .stButton>button { 
        color: #FFFFFF !important; 
        background-color: #4CAF50 !important; 
        border: 1px solid #4CAF50 !important; 
    }
    
    /* Dataframes */
    .stDataFrame { color: #000000 !important; background-color: #F0F2F6 !important; }
   </style>

        """
        st.markdown(light_theme, unsafe_allow_html=True)
        
def settings():
    st.title("Settings")

    # Theme Selection Dropdown
    theme = st.selectbox("Choose Theme", ["Dark", "Light"], index=0 if st.session_state.theme == "dark" else 1)

    # Update theme state
    st.session_state.theme = "light" if theme == "Light" else "dark"

    # Apply selected theme
    apply_theme()
    st.success(f"Theme set to {theme} mode!")

# Apply theme at startup
apply_theme()


if selected == "Settings":
    settings()

# Custom CSS for Improved Styling
st.markdown("""
    <style>
        .tip-box {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 2px 4px 10px rgba(0, 0, 0, 0.1);
            font-size: 20px;
            text-align: center;
            color: #333;
            font-weight: bold;
            margin: 20px auto;
            width: 80%;
        }

        .btn-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 15px;
        }

        .btn {
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s ease, box-shadow 0.3s ease;
        }

        .btn:hover {
            transform: scale(1.05);
            box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);
        }

        .btn-wrapper {
            display: flex;
            justify-content: center;
            margin-top: 15px;
        }
    </style>
""", unsafe_allow_html=True)

def health_tips():
    st.title("💡 Daily Health Tips")

    tips = [
        "💧 **Stay Hydrated:** Drink at least 2 liters of water daily.",
        "🏋️ **Stay Active:** Exercise at least 30 minutes every day.",
        "🥦 **Eat Right:** Include fiber, protein, and healthy fats in your diet.",
        "😴 **Get Enough Sleep:** Aim for 7-9 hours of sleep for better health.",
        "👀 **Reduce Screen Time:** Take short breaks to rest your eyes.",
        "🧘 **Practice Mindfulness:** Deep breathing helps reduce stress.",
        "🪑 **Improve Posture:** Sit upright to avoid back pain.",
        "🚫🍭 **Limit Sugar Intake:** Too much sugar can lead to health issues."
    ]

    if "tip_index" not in st.session_state:
        st.session_state.tip_index = 0

    # Display current tip inside a styled box
    st.markdown(
        f'<div style="background-color: {"#1E1E1E" if st.session_state.theme == "dark" else "#F0F2F6"}; '
        f'padding: 20px; border-radius: 10px; color: {"#FFFFFF" if st.session_state.theme == "dark" else "#000000"};'
        f'">{tips[st.session_state.tip_index]}</div>',
        unsafe_allow_html=True
    )

    # Centered navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        btn_prev, btn_next = st.columns([1, 1])

        with btn_prev:
            if st.button("⬅ Previous", key="prev_btn"):
                st.session_state.tip_index = (st.session_state.tip_index - 1) % len(tips)
        
        with btn_next:
            if st.button("Next ➡", key="next_btn"):
                st.session_state.tip_index = (st.session_state.tip_index + 1) % len(tips)

if selected == "Health Tips":
    health_tips()




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

    age = st.selectbox('Age', ['Select', 'Less than 18', '18 to 49', '49 to 60', 'Above 60'])
    duration = st.radio('Workout Duration:', ['Less frequently', 'Moderate', 'More Frequently'])
    level = st.selectbox('Select your level:', ['Select', 'beginner', 'intermediate', 'advanced'])
    button = st.button('Recommend Workout')

    if button:
        if level == 'Select':
            st.warning('Insertion error!! Re-check the input fields')
        else:
            nums = 1  # Initialize counter for days
            workout_plan = generate_workout(level)

            # Define days of the week explicitly
            days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            workout_data = []  # List to store workout details for visualization

            for day in days_of_week:
                if day == "Sunday":
                    st.markdown(
                        f"""
                        <h4>Your Workout Plan for Day {nums}: {day}</h4>
                        <div class="sundays">
                            <p style="color:#7FFF00; font-style:italic; font-family:cursive;">Take rest and go for a light walk in the park.</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    workout_data.append({"Day": day, "Workout Count": 0})  # No workouts on Sunday
                else:
                    exercises = exercise_by_level[level].get(day, ["No workout assigned"])
                    exercise_str = ", ".join(exercises)
                    insert_workout_data(st.session_state.username, f"Day {nums} Workout ({day})", exercise_str, level, 30)

                    st.markdown(
                        f"""
                        <h4>Your Workout Plan for Day {nums}: {day}</h4>
                        <div class="workout">
                            <div class="workout-info">
                                <p style="color:#7FFF00; font-style:italic; font-family:cursive;">Workout: {exercise_str}</p>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    workout_data.append({"Day": day, "Workout Count": len(exercises)})

                nums += 1  # Increment day counter

            # Insert user workout details into the user_data table
            insert_user_data(st.session_state.username, age, level, str(workout_plan))

            # Convert data to Pandas DataFrame
            df = pd.DataFrame(workout_data)

            # Create a bar chart for workout distribution
            st.subheader("📊 Workout Distribution Over the Week")
            fig = px.bar(df, x="Day", y="Workout Count", title="Number of Workouts per Day",
                         labels={"Workout Count": "Number of Exercises"},
                         color="Workout Count", height=400)
            st.plotly_chart(fig)


# For Medicine Recommender
if selected == 'Medicine Recommender':
    main_1()

# For custom food recommendations
if selected == 'Diet':    
    diet()