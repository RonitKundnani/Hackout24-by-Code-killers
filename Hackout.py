import tkinter as tk
from tkinter import messagebox
import mysql.connector
from tkinter import filedialog
from PIL import Image, ImageTk

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ronit@2722",
    database="farmer"
)
cursor = conn.cursor()


# Function to open the sign-up window for consumers
def open_signup_consumer():
    home_window.withdraw()  # Hide the home window
    signup_consumer_window.deiconify()  # Show the consumer sign-up window

# Function to open the sign-up window for farmers
def open_signup_farmer():
    home_window.withdraw()  # Hide the home window
    signup_farmer_window.deiconify()  # Show the farmer sign-up window

# Function to open the sign-in window for consumers
def open_signin_consumer():
    home_window.withdraw()  # Hide the home window
    signin_consumer_window.deiconify()  # Show the consumer sign-in window

# Function to open the sign-in window for farmers
def open_signin_farmer():
    home_window.withdraw()  # Hide the home window
    signin_farmer_window.deiconify()  # Show the farmer sign-in window

# Function to open farmer main page
def open_farmer_home():
    signin_farmer_window.withdraw()
    farmer_home_window.deiconify()

# Function to open consumer main page
def open_consumer_home():
    signin_consumer_window.withdraw()
    consumer_home_window.deiconify()

# Function to sign up (for both consumer and farmer)
def signup(is_farmer):
    global username
    global password
    global phone
    global fullname
    global acres
    username = entry_signup_username.get()
    password = entry_signup_password.get()
    phone = int(entry_signup_phone.get())
    fullname = entry_signup_fullname.get()
    acres = entry_signup_acres.get() if is_farmer else None

    if username == "" or password == "":
        messagebox.showwarning("Invalid input", "Please enter both username and password")
        return

    # Check if the user already exists
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result:
        messagebox.showwarning("Error", "Username already exists")
    else:
        # Insert the new user into the database
        if is_farmer:
            cursor.execute("INSERT INTO users (username, password, fullname, phone, acres) VALUES (%s, %s, %s, %s, %s)", (username, password, fullname, phone, acres))
        else:
            cursor.execute("INSERT INTO consumer (username, password, fullname, phone) VALUES (%s, %s, %s, %s)", (username, password, fullname, phone))
        conn.commit()
        messagebox.showinfo("Success", "Account created successfully")
        entry_signup_username.delete(0, tk.END)
        entry_signup_password.delete(0, tk.END)
        if is_farmer:
            signup_farmer_window.withdraw()  # Hide the sign-up window
            signin_farmer_window.deiconify()  # Show the sign-in window
        else:
            signup_consumer_window.withdraw()  # Hide the sign-up window
            signin_consumer_window.deiconify()  # Show the sign-in window

# Function to sign in (for both consumer and farmer)
def signin(is_farmer):
    global username
    global password
    username = entry_signin_username.get()
    password = entry_signin_password.get()

    if username == "" or password == "":
        messagebox.showwarning("Invalid input", "Please enter both username and password")
        return

    # Check if the user exists and the password matches
    if is_farmer:
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    else:
        cursor.execute("SELECT * FROM consumer WHERE username = %s AND password = %s", (username, password))

    result = cursor.fetchone()

    if result:
        messagebox.showinfo("Success", "Login successful")
        if is_farmer:
            open_farmer_home()  # Redirect to farmer home page
        else:
            open_consumer_home()  # Redirect to consumer home page
    else:
        messagebox.showwarning("Error", "Incorrect username or password")

# Function to open consumer home page
def signin2(is_farmer=False):
    global username
    global password
    username = entry_signin_usernamec.get()
    password = entry_signin_passwordc.get()

    if username == "" or password == "":
        messagebox.showwarning("Invalid input", "Please enter both username and password")
        return

    cursor.execute("SELECT * FROM consumer WHERE username = %s AND password = %s", (username, password))
    result = cursor.fetchone()

    if result:
        messagebox.showinfo("Success", "Login successful")
        open_consumer_home()  # Redirect to consumer home page
    else:
        messagebox.showwarning("Error", "Incorrect username or password")

# Function to handle the profile button click



# def open_profile():
#     messagebox.showinfo("Profile", "Profile information goes here")

def open_profile(username, password):
    label_farmer_home.config(text="")
    form_frame = tk.Frame(farmer_home_window)
    form_frame.pack(pady=10)
    # Create and place the username label and entry
    label_username = tk.Label(form_frame, text="Username:", font=('Arial', 12, 'bold'), padx=10)
    label_username.pack(side='left')
    entry_username = tk.Entry(form_frame, font=('Arial', 12))
    entry_username.pack(side='left',padx=10)
    entry_username.insert(0, username)

    form_frame2 = tk.Frame(farmer_home_window)
    form_frame2.pack(pady=5)

    label_password = tk.Label(form_frame2, text="Password:", font=('Arial', 12, 'bold'), padx=10)
    label_password.pack(side='left')
    entry_password = tk.Entry(form_frame2, show="*", font=('Arial', 12))
    entry_password.pack(side='left', padx=10)
    entry_password.insert(0, password)



    form_frame3 = tk.Frame(farmer_home_window)
    form_frame3.pack(pady=5)

    label_fullname = tk.Label(form_frame3, text="fullname:", font=('Arial', 12, 'bold'), padx=10)
    label_fullname.pack(side='left')
    entry_fullname = tk.Entry(form_frame3, font=('Arial', 12))
    entry_fullname.pack(side='left', padx=10)
    #entry_fullname.insert(0, fullname)



    form_frame4 = tk.Frame(farmer_home_window)
    form_frame4.pack(pady=5)

    label_phone = tk.Label(form_frame4, text="phone:", font=('Arial', 12, 'bold'), padx=10)
    label_phone.pack(side='left')
    entry_phone = tk.Entry(form_frame4,font=('Arial', 12))
    entry_phone.pack(side='left', padx=10)
    #entry_phone.insert(0, phone)


    form_frame5 = tk.Frame(farmer_home_window)
    form_frame5.pack(pady=5)

    label_acres = tk.Label(form_frame5, text="acres:", font=('Arial', 12, 'bold'), padx=10)
    label_acres.pack(side='left')
    entry_acres = tk.Entry(form_frame5, font=('Arial', 12))
    entry_acres.pack(side='left', padx=10)
    #entry_acres.insert(0, acres)
    
    def upload_image():
        # Open file dialog to select an image file
        file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")])

        
        
        if file_path:
            # Open and display the image
            img = Image.open(file_path)
            img = img.resize((250, 250), Image.LANCZOS)  # Resize image to fit the window
            img = ImageTk.PhotoImage(img)

            label_image = tk.Label(farmer_home_window)
            label_image.pack(pady=10)

            # Update the label with the new image
            label_image.config(image=img)
            label_image.image = img  # Keep a reference to avoid garbage collection


    button_upload = tk.Button(farmer_home_window, text="Upload Your FarmerCertificate",font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white',command=upload_image)
    button_upload.pack(pady=10)   

    





# Function to handle the available deals button click
def open_available_deals():
    messagebox.showinfo("Available Deals", "Available deals information goes here")

# Function to handle the make deal button click
def open_make_deal():
    messagebox.showinfo("Make Deal", "Make a new deal information goes here")

# Function to handle the dealer's chat button click
def open_dealers_chat():
    messagebox.showinfo("Dealer's Chat", "Dealer's chat functionality goes here")

# Function to handle the support contact button click
def open_support_contact():
    messagebox.showinfo("Support Contact", "Support contact information goes here")

# Function to handle the log out button click
def logout():
    farmer_home_window.withdraw()  # Hide the farmer home window
    home_window.deiconify()  # Show the home window

# Set up a common style
def style_window(window, title):
    window.title(title)
    window.geometry("500x400")
    window.configure(bg="#2c3e50")
    window.resizable(True, True)

# Home Window setup
home_window = tk.Tk()
style_window(home_window, "Select User Type")

label_home_title = tk.Label(home_window, text="Select User Type", font=("Arial", 24, "bold"), fg="#ecf0f1", bg="#2c3e50")
label_home_title.pack(pady=20)

button_farmer = tk.Button(home_window, text="Farmer", font=("Arial", 18), bg="#3498db", fg="#ecf0f1", command=lambda: open_signin_farmer())
button_farmer.pack(pady=10)

button_consumer = tk.Button(home_window, text="Consumer", font=("Arial", 18), bg="#1abc9c", fg="#ecf0f1", command=lambda: open_signin_consumer())
button_consumer.pack(pady=10)

# Sign-In Window for Farmers setup
signin_farmer_window = tk.Toplevel(home_window)
style_window(signin_farmer_window, "Sign In (Farmer)")
signin_farmer_window.withdraw()  # Hide the sign-in window initially

label_signin_title_farmer = tk.Label(signin_farmer_window, text="Farmer Sign In", font=("Arial", 40, "bold"), fg="#ecf0f1", bg="#2c3e50")
label_signin_title_farmer.pack(pady=10)

label_signin_username_farmer = tk.Label(signin_farmer_window, text="Username", font=("Arial", 24), fg="#ecf0f1", bg="#2c3e50")
label_signin_username_farmer.pack(pady=7)
entry_signin_username = tk.Entry(signin_farmer_window, font=("Arial", 18))
entry_signin_username.pack(pady=5)

label_signin_password_farmer = tk.Label(signin_farmer_window, text="Password", font=("Arial", 24), fg="#ecf0f1", bg="#2c3e50")
label_signin_password_farmer.pack(pady=5)
entry_signin_password = tk.Entry(signin_farmer_window, show="*", font=("Arial", 18))
entry_signin_password.pack(pady=5)

button_signin_farmer = tk.Button(signin_farmer_window, text="Sign In", font=("Arial", 16), bg="#3498db", fg="#ecf0f1", padx="2", command=lambda: signin(is_farmer=True))
button_signin_farmer.pack(pady=10)

button_goto_signup_farmer = tk.Button(signin_farmer_window, text="Sign Up", font=("Arial", 16), bg="#1abc9c", fg="#ecf0f1", command=open_signup_farmer)
button_goto_signup_farmer.pack(pady=5)

# Sign-Up Window for Farmers setup
signup_farmer_window = tk.Toplevel(home_window)
style_window(signup_farmer_window, "Sign Up (Farmer)")
signup_farmer_window.withdraw()  # Hide the sign-up window initially

label_signup_title_farmer = tk.Label(signup_farmer_window, text="Create Farmer Account", font=("Arial", 16, "bold"), fg="#ecf0f1", bg="#2c3e50")
label_signup_title_farmer.pack(pady=10)

label_signup_username_farmer = tk.Label(signup_farmer_window, text="Username", font=("Arial", 12), fg="#ecf0f1", bg="#2c3e50")
label_signup_username_farmer.pack(pady=5)
entry_signup_username = tk.Entry(signup_farmer_window, font=("Arial", 12))
entry_signup_username.pack(pady=5)

label_signup_fullname_farmer = tk.Label(signup_farmer_window, text="Full Name", font=("Arial", 12), fg="#ecf0f1", bg="#2c3e50")
label_signup_fullname_farmer.pack(pady=5)
entry_signup_fullname = tk.Entry(signup_farmer_window, font=("Arial", 12))
entry_signup_fullname.pack(pady=5)

label_signup_phone_farmer = tk.Label(signup_farmer_window, text="Phone no", font=("Arial", 12), fg="#ecf0f1", bg="#2c3e50")
label_signup_phone_farmer.pack(pady=5)
entry_signup_phone = tk.Entry(signup_farmer_window, font=("Arial", 12))
entry_signup_phone.pack(pady=5)

label_signup_password_farmer = tk.Label(signup_farmer_window, text="Password", font=("Arial", 12), fg="#ecf0f1", bg="#2c3e50")
label_signup_password_farmer.pack(pady=5)
entry_signup_password = tk.Entry(signup_farmer_window, show="*", font=("Arial", 12))
entry_signup_password.pack(pady=5)

label_signup_acres_farmer = tk.Label(signup_farmer_window, text="Acres", font=("Arial", 12), fg="#ecf0f1", bg="#2c3e50")
label_signup_acres_farmer.pack(pady=5)
entry_signup_acres = tk.Entry(signup_farmer_window, font=("Arial", 12))
entry_signup_acres.pack(pady=5)

button_signup_farmer = tk.Button(signup_farmer_window, text="Sign Up", font=("Arial", 16), bg="#3498db", fg="#ecf0f1", command=lambda: signup(is_farmer=True))
button_signup_farmer.pack(pady=10)

# Sign-In Window for Consumers setup
signin_consumer_window = tk.Toplevel(home_window)
style_window(signin_consumer_window, "Sign In (Consumer)")
signin_consumer_window.withdraw()  # Hide the sign-in window initially

label_signin_title_consumer = tk.Label(signin_consumer_window, text="Consumer Sign In", font=("Arial", 40, "bold"), fg="#ecf0f1", bg="#2c3e50")
label_signin_title_consumer.pack(pady=10)

label_signin_username_consumer = tk.Label(signin_consumer_window, text="Username", font=("Arial", 24), fg="#ecf0f1", bg="#2c3e50")
label_signin_username_consumer.pack(pady=7)
entry_signin_usernamec = tk.Entry(signin_consumer_window, font=("Arial", 18))
entry_signin_usernamec.pack(pady=5)

label_signin_password_consumer = tk.Label(signin_consumer_window, text="Password", font=("Arial", 24), fg="#ecf0f1", bg="#2c3e50")
label_signin_password_consumer.pack(pady=5)
entry_signin_passwordc = tk.Entry(signin_consumer_window, show="*", font=("Arial", 18))
entry_signin_passwordc.pack(pady=5)

button_signin_consumer = tk.Button(signin_consumer_window, text="Sign In", font=("Arial", 16), bg="#3498db", fg="#ecf0f1", command=lambda: signin2())
button_signin_consumer.pack(pady=10)

button_goto_signup_consumer = tk.Button(signin_consumer_window, text="Sign Up", font=("Arial", 16), bg="#1abc9c", fg="#ecf0f1", command=open_signup_consumer)
button_goto_signup_consumer.pack(pady=5)

# Sign-Up Window for Consumers setup
signup_consumer_window = tk.Toplevel(home_window)
style_window(signup_consumer_window, "Sign Up (Consumer)")
signup_consumer_window.withdraw()  # Hide the sign-up window initially

label_signup_title_consumer = tk.Label(signup_consumer_window, text="Create Consumer Account", font=("Arial", 16, "bold"), fg="#ecf0f1", bg="#2c3e50")
label_signup_title_consumer.pack(pady=10)

label_signup_username_consumer = tk.Label(signup_consumer_window, text="Username", font=("Arial", 12), fg="#ecf0f1", bg="#2c3e50")
label_signup_username_consumer.pack(pady=5)
entry_signup_username = tk.Entry(signup_consumer_window, font=("Arial", 12))
entry_signup_username.pack(pady=5)

label_signup_fullname_consumer = tk.Label(signup_consumer_window, text="Full Name", font=("Arial", 12), fg="#ecf0f1", bg="#2c3e50")
label_signup_fullname_consumer.pack(pady=5)
entry_signup_fullname = tk.Entry(signup_consumer_window, font=("Arial", 12))
entry_signup_fullname.pack(pady=5)

label_signup_phone_consumer = tk.Label(signup_consumer_window, text="Phone no", font=("Arial", 12), fg="#ecf0f1", bg="#2c3e50")
label_signup_phone_consumer.pack(pady=5)
entry_signup_phone = tk.Entry(signup_consumer_window, font=("Arial", 12))
entry_signup_phone.pack(pady=5)

label_signup_password_consumer = tk.Label(signup_consumer_window, text="Password", font=("Arial", 12), fg="#ecf0f1", bg="#2c3e50")
label_signup_password_consumer.pack(pady=5)
entry_signup_password = tk.Entry(signup_consumer_window, show="*", font=("Arial", 12))
entry_signup_password.pack(pady=5)

button_signup_consumer = tk.Button(signup_consumer_window, text="Sign Up", font=("Arial", 16), bg="#3498db", fg="#ecf0f1", command=lambda: signup(is_farmer=False))
button_signup_consumer.pack(pady=10)

# Farmer Home Window setup
farmer_home_window = tk.Toplevel(home_window)
style_window(farmer_home_window, "Farmer Home")
farmer_home_window.withdraw()

# Frame for buttons
left_frame = tk.Frame(farmer_home_window, bg="#34495e", width=150)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

# Buttons on the left
button_profile = tk.Button(left_frame, text="Profile", font=("Arial", 14), bg="#3498db", fg="#ecf0f1", command=lambda: open_profile(username, password))
button_profile.pack(fill=tk.X, padx=10, pady=5)

button_available_deals = tk.Button(left_frame, text="Available Deals", font=("Arial", 14), bg="#3498db", fg="#ecf0f1", command=open_available_deals)
button_available_deals.pack(fill=tk.X, padx=10, pady=5)

button_make_deal = tk.Button(left_frame, text="Make Deal", font=("Arial", 14), bg="#3498db", fg="#ecf0f1", command=open_make_deal)
button_make_deal.pack(fill=tk.X, padx=10, pady=5)

button_dealers_chat = tk.Button(left_frame, text="Dealer's Chat", font=("Arial", 14), bg="#3498db", fg="#ecf0f1", command=open_dealers_chat)
button_dealers_chat.pack(fill=tk.X, padx=10, pady=5)

button_support_contact = tk.Button(left_frame, text="Support Contact", font=("Arial", 14), bg="#3498db", fg="#ecf0f1", command=open_support_contact)
button_support_contact.pack(fill=tk.X, padx=10, pady=5)

button_logout = tk.Button(left_frame, text="Log Out", font=("Arial", 14), bg="#e74c3c", fg="#ecf0f1", command=logout)
button_logout.pack(fill=tk.X, padx=10, pady=5)

# Label for Farmer Home content
label_farmer_home = tk.Label(farmer_home_window, text="Welcome Farmer", font=("Arial", 40, "bold"), fg="#ecf0f1", bg="#2c3e50")
label_farmer_home.pack(pady=100)

# Consumer Home Window setup
consumer_home_window = tk.Toplevel(home_window)
style_window(consumer_home_window, "Consumer Home")
consumer_home_window.withdraw()

label_consumer_home = tk.Label(consumer_home_window, text="Welcome Consumer", font=("Arial", 40, "bold"), fg="#ecf0f1", bg="#2c3e50")
label_consumer_home.pack(pady=100)

# Start the Tkinter loop
home_window.mainloop()

# Close the connection to the database when the application closes
cursor.close()
conn.close()
