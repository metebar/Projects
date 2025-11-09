import tkinter as tk
import pygame
import os
import mysql.connector
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from mutagen.mp3 import MP3
import time


# Global variables
playlist = []  # List to store the selected MP3 files
current_song_index = 0  # Index of the currently playing song
song_listbox = None  # Global variable to hold the song listbox
logged_in_user = None  # Global variable to store the logged-in username
current_playlist = None  # Global variable to store the current playlist name
playlists_listbox = None  # Global variable to hold the playlists listbox
playlists_window = None  # Global variable to hold the playlists window
seek_position = None  # Define seek_position as a global variable
seek_in_progress= False #Flag to check if seek in progress
current_position = 0 #Position of the song for the progress bar
last_update_time = time.time() #global variable for the time
song_changed  = False #Flag to check if song is changed



# Function to initialize the pygame mixer
def init_mixer():
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.5)  # Set the volume (0.0 to 1.0)

        

# Function to load and play an MP3 file
def play_music(file_path):
    global seek_in_progress
    global seek_position

    # Check if a seek position is available
    if seek_in_progress:
        seek_position = pygame.mixer.music.get_pos() // 1000  # Convert milliseconds to seconds
    else:
        seek_position = pygame.mixer.music.get_pos() // 1000 if pygame.mixer.music.get_busy() else None

    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    update_song_label(os.path.basename(file_path))  # Update the song label with the file name





# Function to pause the currently playing music
def pause_music():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
 

# Function to resume the paused music
def resume_music():
    pygame.mixer.music.unpause()



# Function to stop the currently playing music
def stop_music():
    pygame.mixer.music.stop()
    update_song_label("")  # Clear the song label when music stops

# Function to handle the "Next" button click event
def next_song():
    global song_changed
    global current_song_index
    current_song_index = (current_song_index + 1) % len(playlist)  # Move to the next song (loop back to the beginning if at the end)
    play_music(playlist[current_song_index])
    song_changed = True

# Function to handle the "Previous" button click event
def previous_song():
    global song_changed

    global current_song_index
    current_song_index = (current_song_index - 1) % len(playlist)  # Move to the previous song (loop back to the end if at the beginning)
    play_music(playlist[current_song_index])
    song_changed = True


# Function to handle the volume slider change event
def change_volume(value):
    volume = float(value) / 100  # Convert the slider value to a volume value (0.0 to 1.0)
    pygame.mixer.music.set_volume(volume)

# Function to update the currently playing song label
def update_song_label(song_name):
    song_label.config(text="Currently playing: " + song_name)

# Function to handle the button click event
def add_song():
    file_path = filedialog.askopenfilename(title="Select MP3 File", filetypes=(("MP3 Files", "*.mp3"), ("All Files", "*.*")))
    if file_path:
        try:
            # Establish a connection to the MySQL database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123123123",
                database="music"
            )

            # Create a cursor object to execute SQL queries
            cursor = connection.cursor()

            # Execute the query to insert the song path into the database
            cursor.execute("INSERT INTO songs (song_path) VALUES (%s)", (file_path,))

            # Commit the transaction
            connection.commit()

            # Close the cursor and connection
            cursor.close()
            connection.close()

            # Update the playlist and song listbox
            playlist.append(file_path)
            song_name = os.path.basename(file_path)
            song_listbox.insert(tk.END, song_name)

        except mysql.connector.Error as error:
            print("Error while adding song to database:", error)
# Function to handle the button click event
def remove_song():
    selected_index = song_listbox.curselection()
    if selected_index:
        selected_song_index = int(selected_index[0])
        selected_song_path = playlist[selected_song_index]  # Get the selected song path from the playlist
        del playlist[selected_song_index]  # Remove the selected song from the playlist
        song_listbox.delete(selected_index)  # Remove the selected song from the listbox
        
        try:
            # Establish a connection to the MySQL database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123123123",
                database="music"
            )

            # Create a cursor object to execute SQL queries
            cursor = connection.cursor()

            # Execute the query to delete the song from the database
            cursor.execute("DELETE FROM songs WHERE song_path = %s", (selected_song_path,))

            # Commit the transaction
            connection.commit()

            # Close the cursor and connection
            cursor.close()
            connection.close()

        except mysql.connector.Error as error:
            print("Error while deleting song from database:", error)

# Function to fetch songs from MySQL database
def fetch_songs_from_database():
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123123123",
            database="music"
        )

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Execute the query to fetch songs from the database
        cursor.execute("SELECT song_path FROM songs")

        # Fetch all rows returned by the query
        rows = cursor.fetchall()

        # Add the songs to the playlist
        for row in rows:
            playlist.append(row[0])  # Assuming the song path is in the first column (index 0)

        # Close the cursor and connection
        cursor.close()
        connection.close()

    except mysql.connector.Error as error:
        print("Error while fetching songs from database:", error)

# Function to handle song selection from the listbox
def play_selected_song(event=None):
    global song_changed
    selected_index = song_listbox.curselection()
    if selected_index:
        selected_song_index = int(selected_index[0])
        global current_song_index
        current_song_index = selected_song_index
        play_music(playlist[current_song_index])
        song_changed = True



def seek_music(event):
    global seek_in_progress
    global seek_position
    global current_position

    if  not pygame.mixer.music.get_busy():
        messagebox.showerror("Error", "Music isn't playing.")
        return

    song_path = playlist[current_song_index]
    audio = MP3(song_path)
    song_duration = audio.info.length  # Get the song duration in seconds
    seek_position = int(event.x / progress_bar.winfo_width() * song_duration)  # Calculate the seek position in seconds

    # Set the seek_in_progress flag to True
    seek_in_progress = True


    pygame.mixer.music.pause()  # Pause the currently playing music
    pygame.mixer.music.set_pos(seek_position)  # Set the position of the currently playing music
    pygame.mixer.music.unpause()  # Unpause the music to resume playback

    # Update the progress bar immediately after seeking
    update_progress_bar()


def update_progress_bar():
    global last_update_time
    global seek_in_progress
    global seek_position
    global current_position
    global song_changed
    global progress_percentage


    if pygame.mixer.music.get_busy():
        if seek_in_progress:  # Check if a seek position is provided
            current_position = seek_position   # Use seek position
            seek_in_progress = False

        if song_changed:
            current_position = 0
            song_changed = False

        else:
            
            time_elapsed = time.time() - last_update_time
            current_position += time_elapsed 
            last_update_time = time.time()

 
        # Get the duration of the current song in seconds
        song_path = playlist[current_song_index]
        audio = MP3(song_path)
        song_duration = audio.info.length
        

        # Calculate the progress percentage
        progress_percentage = (current_position / song_duration) * 100

        # Update the progress bar value
        progress_bar['value'] = progress_percentage

        #If music is over play next song
        if progress_percentage >= 100:
            next_song()



    # Schedule the next update after a short delay
    window.after(100, update_progress_bar)
    


# Function to handle the login button click event
def login():
    login_window = tk.Toplevel()
    login_window.title("Login")

    username_label = tk.Label(login_window, text="Username:")
    username_label.pack(pady=10)

    username_entry = tk.Entry(login_window)
    username_entry.pack()

    password_label = tk.Label(login_window, text="Password:")
    password_label.pack()

    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    def authenticate_user():
        global logged_in_user
        username = username_entry.get()
        password = password_entry.get()

        # Check if the username and password are valid (you can replace this with your authentication logic)
        try:
            # Establish a connection to the MySQL database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123123123",
                database="music"
            )

            # Create a cursor object to execute SQL queries
            cursor = connection.cursor()

            # Execute the query to fetch user data from the database
            cursor.execute("SELECT username, password FROM users WHERE username=%s", (username,))

            # Fetch the row returned by the query
            row = cursor.fetchone()

            if row is not None and row[1] == password:
                logged_in_user = row[0]  # Set the logged-in username
                login_window.destroy()
                update_username_label()
                
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")

            # Close the cursor and connection
            cursor.close()
            connection.close()

        except mysql.connector.Error as error:
            print("Error while authenticating user:", error)

    login_button = tk.Button(login_window, text="Login", command=authenticate_user)
    login_button.pack(pady=10)


def register_user():
    # Retrieve user input from entry fields
    username = username_entry.get()
    password = password_entry.get()
    email = email_entry.get()

    # Connect to the database
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123123123',
        database='music'
    )
    cursor = conn.cursor()

    # Create the users table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (username VARCHAR(255), password VARCHAR(255), email VARCHAR(255))''')

    # Insert user information into the users table
    query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
    values = (username, password, email)
    cursor.execute(query, values)
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    # Destroy the registration window
    registration_window.destroy()

    # Display a success message
    messagebox.showinfo("Success","User registered successfully.")

# Function to open the registration window
def open_registration_window():
    global registration_window, username_entry, password_entry, email_entry
    registration_window = tk.Toplevel(window)

    # Create the entry fields for username, password, and email in the registration window
    username_label = tk.Label(registration_window, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(registration_window)
    username_entry.pack()

    password_label = tk.Label(registration_window, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(registration_window, show="*")
    password_entry.pack()

    email_label = tk.Label(registration_window, text="Email:")
    email_label.pack()
    email_entry = tk.Entry(registration_window)
    email_entry.pack()

    # Create the register button and associate it with the register_user function
    register_button = tk.Button(registration_window, text="Register", command=register_user)
    register_button.pack(pady=10)




# Function to update the username label on the main page
def update_username_label():
    username_label.config(text="Logged in as: " + logged_in_user)


# Create the main GUI window
window = tk.Tk()
window.title("Groove Master")

# Create the buttons, volume slider, and currently playing song label
button_frame = tk.Frame(window)
button_frame.grid(row=1, column=0, pady=10)

progress_bar_frame= tk.Frame(window)
progress_bar_frame.grid(row=0, column=0, columnspan=1, pady=10)

progress_bar = ttk.Progressbar(progress_bar_frame, orient=tk.HORIZONTAL, length=200, mode='determinate')
progress_bar.grid(row=0, column=1, pady=10)

play_button = tk.Button(button_frame, text="Play", command=play_selected_song)
play_button.grid(row=1, column=0, pady=10)

pause_button = tk.Button(button_frame, text="Pause", command=pause_music)
pause_button.grid(row=1, column=1, pady=10)

resume_button = tk.Button(button_frame, text="Resume", command=resume_music)
resume_button.grid(row=1, column=2, pady=10)

stop_button = tk.Button(button_frame, text="Stop", command=stop_music)
stop_button.grid(row=1, column=3, pady=10)

previous_button = tk.Button(progress_bar_frame, text="Previous", command=previous_song)
previous_button.grid(row=0, column=0, pady=10,padx=5)

next_button = tk.Button(progress_bar_frame, text="Next", command=next_song)
next_button.grid(row=0, column=2, pady=10,padx=5)

volume_frame = tk.Frame(window)
volume_frame.grid(row=2, column=0,columnspan=4)


volume_slider = tk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=change_volume)
volume_slider.grid(row=0, column=1)

song_label = tk.Label(window, text="Currently playing: ")
song_label.grid(row=4, column=0, columnspan=2, pady=10)


#Frame for add and remove buttons
add_remove_button_frame=tk.Frame(window)
add_remove_button_frame.grid(row=5, column=0, pady=10)

# Create the add song button
add_button = tk.Button(add_remove_button_frame, text="Add song", command=add_song)
add_button.grid(row=0, column=0,)

# Create the remove song button
remove_button = tk.Button(add_remove_button_frame, text="Remove Song", command=remove_song)
remove_button.grid(row=0, column=1)

# Create the song listbox
song_listbox = tk.Listbox(window, width=50)
song_listbox.grid(row=6, column=0, columnspan=2, pady=10)

# Fetch songs from the MySQL database
fetch_songs_from_database()

# Add songs to the listbox
for song_path in playlist:
    song_name = os.path.basename(song_path)
    song_listbox.insert(tk.END, song_name)

# Bind double-click event on the listbox to play the selected song
song_listbox.bind("<Double-Button-1>", play_selected_song)
# Bind the seek_music function to the progress bar click event
progress_bar.bind("<Button-1>", seek_music)

login_button_frame=tk.Frame(window)
login_button_frame.grid(row=7, column=0, pady=10)


# Create the login button
login_button = tk.Button(login_button_frame, text="Login", command=login)
login_button.grid(row=7, column=0, pady=10)

register_button = tk.Button(login_button_frame,text="Register",command=open_registration_window)
register_button.grid(row=7, column=1,pady=10)

# Create the username label
username_label = tk.Label(window, text="Logged in as: ")
username_label.grid(row=8, column=0, pady=10)
# Initialize the pygame mixer
init_mixer()

update_progress_bar()

# Start the GUI event loop
window.mainloop()