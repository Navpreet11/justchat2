import streamlit as st
import sqlite3
from datetime import*
from PIL import Image
from io import BytesIO
from datetime import datetime
import time


im = Image.open("logo.png")
st.set_page_config(
    page_title="JustChat",
    page_icon=im
   
)

st.markdown("<center><img src=https://img.icons8.com/color/400/chat--v1.png;alt=centered image; height=200; width=200> </center>",unsafe_allow_html=True)
#2196F3
#1565c0
label=("<h1 style='font-family:arial;color:#2196F3;text-align:center'>JustChat</h1>")
st.markdown(label,unsafe_allow_html=True)



streamlitstyle = """
			<style>
			body,[class*="css"]{background-image: url("https://img.freepik.com/premium-photo/photo-smooth-gradient-background-square-gradient-2-colors-from-top-bottom-gradient-colorful_873925-69842.jpg");
                        background-attachment: fixed;
                        background-size:cover
			
			
                       
			
			
                        }
			</style>
			"""



st.markdown(streamlitstyle, unsafe_allow_html=True)

















def displaychat(message):
    
    st.markdown(
        """
        <div style="background-color: lightgreen; padding: 10px; border-radius: 5px;">
            <span style="color: #555; font-weight: bold;"></span>
            <span style="color: #555;">{}</span>
        </div>
        """.format(message),
        unsafe_allow_html=True
    )



def displayright(message):
    st.markdown(
        """
        <div style="background-color: lightblue; padding: 10px; border-radius: 5px; float: right; text-align: right;">
            <span style="color: #333; font-weight: bold;"></span>
            <span style="color: #555;">{}</span>
        </div>
        """.format(message),
        unsafe_allow_html=True
    )




def setdark():
    """
    Apply dark theme to Streamlit app
    """
    dark_theme = """
    <style>
    /* Set page background color */
    body {
        color: #2196F3;
        background-color: #1E1E1E;
    }

    /* Set header and footer background color */
    .css-1o2jlnu.e1nhwh5g0 {
        background-color: #333333;
    }

    /* Set text color */
    .css-2trqyj {
        color: #2196F3;
    }
    </style>
    """
    st.markdown(dark_theme, unsafe_allow_html=True)

setdark()








hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)



conn = sqlite3.connect('chatdatanew1.db')
cursor = conn.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
""")
conn.commit()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT NOT NULL,
        recipient TEXT NOT NULL,
        message TEXT NOT NULL,
        picture BLOB,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()


def main():
   
    if not is_user_logged_in():
        login()
    else:
        chat_app()


def is_user_logged_in():
    return st.session_state.get('username') is not None




def login():
    st.header("Log In")
    

    username = st.text_input("",placeholder="Please enter your username", key="login_username")
    password = st.text_input("",placeholder="Please enter your password", type="password", key="login_password")

    if st.button("Log In"):
        if authenticate_user(username, password):
            set_user_logged_in(username)
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")
    st.write("___")
  
    st.subheader("Don't have an account yet?")
    if st.button("Create One Now "):
        st.session_state.show_signup_form = True

    if st.session_state.get('show_signup_form'):
        signup()


def signup():
    st.header("Sign Up")

    new_username = st.text_input("",placeholder="Please enter your new username", key="signup_username")
    new_password = st.text_input("",placeholder="Please enter your new password", type="password", key="signup_password")
    submit_button = st.button("Sign Up")

    if submit_button:
        create_account(new_username, new_password)

def authenticate_user(username, password):
    query = "SELECT username FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    return result is not None


def create_account(username, password):
    query = "INSERT INTO users (username, password) VALUES (?, ?)"
    try:
        cursor.execute(query, (username, password))
        conn.commit()
        st.success("User created successfully!")
        
    except sqlite3.IntegrityError:
        st.error("Username already exists")


def set_user_logged_in(username):
    st.session_state.username = username


def chat_app():
   
  
    st.header(f"You are logged in as: {st.session_state.username}")

    st.write("___")
    st.subheader("Choose a person to send message or see message")

   
    cursor.execute("SELECT username FROM users WHERE username != ?", (st.session_state.username,))
    recipients = [row[0] for row in cursor.fetchall()]

    recipient = st.selectbox("", recipients, key="recipient")
    st.write("____")
    st.subheader("Enter your message  you want to send to"+" "  +str(recipient))

    message = st.text_input("",placeholder="Enter the Message you want to send to"+" "  +str(recipient), key="message")

    #expa=st.expander("Send a picture to" +" "  +recipient)
    #with expa:
         #picture = st.file_uploader("select a picture", type=['jpg', 'jpeg', 'png'], key="picture")

    if st.button("Send message ➡️"):#and picture
         if message:
            insert_query = "INSERT INTO messages (sender, recipient, message) VALUES (?, ?, ?)"
            cursor.execute(insert_query, (st.session_state.username, recipient, message ))
            conn.commit()
            st.success("Message sent successfully")
            #st.session_state.is_button_clicked = True
        
        
        

    st.write("___")
    #st.subheader("Chat History")
    #chat_history = get_chat_history(st.session_state.username)
    if recipient:
        st.header(f" Your Chat History with {recipient}")
        query = "SELECT sender, message , timestamp FROM messages WHERE (sender = ? AND recipient = ?) OR (sender = ? AND recipient = ?) ORDER BY timestamp"
        cursor.execute(query, (st.session_state.username, recipient,recipient, st.session_state.username))
        chat_history = cursor.fetchall()
        for chat in chat_history:
             sender= chat[0]
             message = chat[1]
             timestamp = chat[2]
             #image_path = chat[2]

             
             if sender == st.session_state.username:
                 st.write("___")
                 displaychat(f"You: {message}")
                 st.success(f"sended on : {timestamp}")
            # delete_key = f"delete_{chat[0]}"
            # if st.button("Delete this message 🗑",key=delete_key):
               #  delete_message(chat[0])
                # st.warning("Message deleted successfully!")
             else:
                 st.write("___")
                 displayright(f"{sender}: {message} ")
                 st.info(f"received on : {timestamp}")
             #if image_path:
                 #st.image(image_path, use_column_width=True)

        
   



def send_message(sender, receiver, message,picture):
    query = "INSERT INTO messages (sender, receiver, message,picture) VALUES (?, ?, ?, ?)"#picture
    cursor.execute(query, (sender, receiver, message,picture.read() if picture else None ))
    conn.commit()
def delete_message(message_id):
    query = "DELETE FROM messages WHERE id = ?"
    cursor.execute(query, (message_id,))
 
    conn.commit()


def get_chat_history(username):
    query = "SELECT id, sender, receiver, message , picture FROM messages WHERE sender = ? OR receiver = ? ORDER BY timestamp"
    
    cursor.execute(query, (username, username))
    chat_history = cursor.fetchall()
    
    return chat_history


if __name__ == "__main__":
    main()
    cursor.close()
    conn.close()
