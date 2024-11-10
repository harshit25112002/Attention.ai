import streamlit as st
import sqlite3
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
from datetime import datetime

# Define the database file
DB_FILE = "preferences.db"

# Database setup functions
def create_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS preferences (
                        user_id TEXT PRIMARY KEY,
                        city TEXT,
                        available_time TEXT,
                        budget TEXT,
                        interests TEXT,
                        starting_point TEXT
                    )''')
    conn.commit()
    conn.close()

def get_preferences(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM preferences WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def save_preferences(user_id, city, available_time, budget, interests, starting_point):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''REPLACE INTO preferences (user_id, city, available_time, budget, interests, starting_point)
                      VALUES (?, ?, ?, ?, ?, ?)''', (user_id, city, available_time, budget, interests, starting_point))
    conn.commit()
    conn.close()

# Generate itinerary based on user inputs
def generate_itinerary(city, available_time, budget, interests, starting_point):
    time_parts = available_time.split("-")
    start_time = time_parts[0].strip() if len(time_parts) == 2 else "10:00 AM"
    end_time = time_parts[1].strip() if len(time_parts) == 2 else "4:00 PM"
    
    itinerary = f"""
    **City**: {city}
    **Available Time**: {start_time} - {end_time}
    **Budget**: {budget}
    **Interests**: {interests.capitalize()}
    **Starting Point**: {starting_point.capitalize()}
    
    **Suggested Itinerary**:
    
    **Morning**: Start your day at {starting_point} around {start_time}. Since you're interested in {interests}, begin with a quick exploration of nearby sites or a local attraction in {city}.

    **Late Morning to Lunch**: Head towards a popular {interests} spot. If you're into food, try a well-reviewed local cafe. For culture, a museum or historical site would be ideal.

    **Afternoon**: Visit a must-see attraction in {city} aligned with your interests.

    **Late Afternoon to Evening**: As you wrap up, consider a final stop at a scenic area or shopping district before heading back.
    """
    return itinerary

# Streamlit App with Chatbot Interface
def run_app():
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Personalized Tour Plan Bot 🌎</h1>", unsafe_allow_html=True)
    
    create_db()  # Initialize the database

    # Sidebar for user ID
    st.sidebar.markdown("<h2 style='color: #4CAF50;'>Welcome!</h2>", unsafe_allow_html=True)
    user_id = st.sidebar.text_input("Enter your User ID:")
    
    if user_id:
        st.markdown(f"<div style='color: #4CAF50;'>Hello, User {user_id}!</div>", unsafe_allow_html=True)
        previous_preferences = get_preferences(user_id)
        
        # Chatbot-like interaction
        if previous_preferences:
            st.markdown(f"<div style='color: #FF5733;'>🤖 Bot:</div> Welcome back! Last time, you were interested in {previous_preferences[4]} in {previous_preferences[2]}.", unsafe_allow_html=True)
        else:
            st.markdown("<div style='color: #FF5733;'>🤖 Bot:</div> Hello! Let's plan your trip.", unsafe_allow_html=True)

        # Collect user preferences
        city = st.text_input("Which city are you visiting?")
        available_time = st.text_input("How much time do you have for the trip (e.g., 10am - 4pm)?")
        budget = st.text_input("What is your budget for the day?")
        interests = st.text_input("What are your interests? (culture, adventure, food, shopping, etc.):")
        starting_point = st.text_input("Where will you start from (hotel, first attraction)?")
        
        if st.button("Save Preferences and Get Itinerary"):
            if city and available_time and budget and interests and starting_point:
                save_preferences(user_id, city, available_time, budget, interests, starting_point)
                
                # Generate and display the itinerary
                itinerary = generate_itinerary(city, available_time, budget, interests, starting_point)
                
                st.markdown("<div style='color: #FF5733;'>🤖 Bot:</div> Here's your personalized itinerary:", unsafe_allow_html=True)
                st.markdown(f"<div style='background-color: #FFF8DC; padding: 10px; border-radius: 5px;'>{itinerary}</div>", unsafe_allow_html=True)
            else:
                st.error("Please fill in all fields.")
    else:
        st.error("Please enter a user ID in the sidebar.")

if __name__ == "__main__":
    run_app()
