from customtkinter import *
from login import *
from PIL import Image
from contants import *

set_appearance_mode("light")

# Creating master window
app = CTk()
app.geometry("1280x720")

# loading required images
email_icon_image = Image.open('images/email.png')
password_icon_image = Image.open('images/padlock.png')

# Making icons
email_icon = CTkImage(dark_image=email_icon_image, light_image=email_icon_image, size=(16,16))
password_icon = CTkImage(dark_image=password_icon_image, light_image=password_icon_image, size=(15,15))

# Master frame
mframe = CTkFrame(master=app, fg_color=THEME_COlOR)
mframe.pack(fill="both", expand=True)

# TabView to hold login elements
login_container = CTkTabview(mframe, height=400, width=300, fg_color='white', segmented_button_fg_color=WHITE, segmented_button_selected_color=THEME_COlOR, segmented_button_unselected_color=GRAY, text_color=WHITE)
login_container.place(in_=mframe, anchor='c', relx=.5, rely=.5)
login_container.pack_propagate(0)

login_container.add("Sign in")  # add tab at the end
login_container.add("Create your account")  # add tab at the end

welcome_subtitle='Enter your details and hit sign in to access the main application'

# Welcome label and headline
CTkLabel(login_container.tab('Sign in'), text='Welcome', text_color = BLACK, fg_color = 'transparent', font=('Arial', 30, 'bold')).pack(pady=(30, 0))
CTkLabel(login_container.tab('Sign in'), text=welcome_subtitle, text_color = GRAY, fg_color = 'transparent', font=('Arial', 15), wraplength=250).pack(pady=(10, 20))

#email field
CTkLabel(master=login_container.tab('Sign in'), text="  Email:", text_color=THEME_COlOR, anchor="w", justify="left", font=("Arial Bold", 14), image=email_icon, compound="left").pack(anchor="w", pady=(10, 0), padx=(25, 0))
email = CTkEntry(login_container.tab('Sign in'), height=40)
email.pack(pady=(0, 10), padx=25, fill='x')

# password field
CTkLabel(master=login_container.tab('Sign in'), text="  Password:", text_color=THEME_COlOR, anchor="w", justify="left", font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", padx=(25, 0))
password = CTkEntry(login_container.tab('Sign in'), height=40, show="*")
password.pack(pady=(0, 10), padx=25, fill='x')

# Sign in button
CTkButton(login_container.tab('Sign in'), text="Sign in", command=lambda email=email, password=password: login(email, password), height=30, width=100, corner_radius=20, fg_color=THEME_COlOR).pack(pady=30)


app.mainloop()