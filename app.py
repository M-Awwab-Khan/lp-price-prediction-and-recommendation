from customtkinter import *
from PIL import Image
from contants import *
import sqlite3

set_appearance_mode("light")

class App:
    def __init__(self):


        # Creating master window
        self.root = CTk()
        self.root.geometry("1280x720")

        self.create_account_page()

        self.root.mainloop()

    def create_account_page(self):


        # loading required images
        email_icon_image = Image.open('images/email.png')
        password_icon_image = Image.open('images/padlock.png')
        name_icon_image = Image.open('images/user.png')

        # Making icons
        email_icon = CTkImage(dark_image=email_icon_image, light_image=email_icon_image, size=(16,16))
        password_icon = CTkImage(dark_image=password_icon_image, light_image=password_icon_image, size=(15,15))
        name_icon = CTkImage(dark_image=name_icon_image, light_image=name_icon_image, size=(17,17))


        # Master frame
        self.account_frame = CTkFrame(master=self.root, fg_color=THEME_COlOR)
        self.account_frame.pack(fill="both", expand=True)

        # TabView to hold login elements
        self.account_tab = CTkTabview(self.account_frame, height=400, width=300, fg_color='white', segmented_button_fg_color=WHITE, segmented_button_selected_color=THEME_COlOR, segmented_button_unselected_color=GRAY, text_color=WHITE)
        self.account_tab.place(in_=self.account_frame, anchor='c', relx=.5, rely=.5)
        self.account_tab.pack_propagate(0)

        self.account_tab.add("Sign in")  # add tab at the end
        self.account_tab.add("Create your account")  # add tab at the end

        # Welcome label and headline
        welcome_subtitle='Enter your details and hit sign in to access the main application'
        CTkLabel(self.account_tab.tab('Sign in'), text='Welcome', text_color = BLACK, fg_color = 'transparent', font=('Arial', 30, 'bold')).pack(pady=(30, 0))
        CTkLabel(self.account_tab.tab('Sign in'), text=welcome_subtitle, text_color = GRAY, fg_color = 'transparent', font=('Arial', 15), wraplength=250).pack(pady=(10, 20))
        self.signin_error = CTkLabel(self.account_tab.tab('Sign in'), width=200, corner_radius = 5, text_color = ERROR, fg_color = '#ffbfba', font=('Arial', 13))
        self.signin_error.pack()
        self.signin_error.lower()
        #email field
        CTkLabel(master=self.account_tab.tab('Sign in'), text="  Email:", text_color=THEME_COlOR, anchor="w", justify="left", font=("Arial Bold", 14), image=email_icon, compound="left").pack(anchor="w", pady=(10, 0), padx=(25, 0))
        self.login_email = CTkEntry(self.account_tab.tab('Sign in'), height=40)
        self.login_email.pack(pady=(0, 10), padx=25, fill='x')

        # password field
        CTkLabel(master=self.account_tab.tab('Sign in'), text="  Password:", text_color=THEME_COlOR, anchor="w", justify="left", font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", padx=(25, 0))
        self.login_password = CTkEntry(self.account_tab.tab('Sign in'), height=40, show="*")
        self.login_password.pack(pady=(0, 10), padx=25, fill='x')

        # Sign in button
        CTkButton(self.account_tab.tab('Sign in'), text="Sign in", command=lambda email=self.login_email, password=self.login_password: self.login(email, password), height=30, width=100, corner_radius=20, fg_color=THEME_COlOR).pack(pady=30)


        # Sign up form
        # Welcome and Greetings
        CTkLabel(self.account_tab.tab('Create your account'), text='Create Account', text_color = BLACK, fg_color = 'transparent', font=('Arial', 30, 'bold')).pack(pady=(30, 0))
        signup_subtitle="Let's create your awesome account, then you'll be able to use LPPRS"
        CTkLabel(self.account_tab.tab('Create your account'), text=signup_subtitle, text_color = GRAY, fg_color = 'transparent', font=('Arial', 15), wraplength=250).pack(pady=(10, 20))
        self.signup_error = CTkLabel(self.account_tab.tab('Sign in'), width=200, corner_radius = 5, text_color = ERROR, fg_color = '#ffbfba', font=('Arial', 13))
        self.signup_error.pack()
        self.signup_error.lower()
        # Full Name
        CTkLabel(master=self.account_tab.tab('Create your account'), text="  Name:", text_color=THEME_COlOR, anchor="w", justify="left", font=("Arial Bold", 14), image=name_icon, compound="left").pack(anchor="w", pady=(10, 0), padx=(25, 0))
        self.name = CTkEntry(self.account_tab.tab('Create your account'), height=40)
        self.name.pack(pady=(0, 10), padx=25, fill='x')

        #email field
        CTkLabel(master=self.account_tab.tab('Create your account'), text="  Email:", text_color=THEME_COlOR, anchor="w", justify="left", font=("Arial Bold", 14), image=email_icon, compound="left").pack(anchor="w", pady=(10, 0), padx=(25, 0))
        self.signup_email = CTkEntry(self.account_tab.tab('Create your account'), height=40)
        self.signup_email.pack(pady=(0, 10), padx=25, fill='x')

        # password field
        CTkLabel(master=self.account_tab.tab('Create your account'), text="  Password:", text_color=THEME_COlOR, anchor="w", justify="left", font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", padx=(25, 0))
        self.signup_password = CTkEntry(self.account_tab.tab('Create your account'), height=40, show="*")
        self.signup_password.pack(pady=(0, 10), padx=25, fill='x')

        # Sign up button
        CTkButton(self.account_tab.tab('Create your account'), text="Create Account", command=lambda email=self.signup_email, password=self.signup_password, name=self.name: self.signup(name, email, password), height=30, width=100, corner_radius=20, fg_color=THEME_COlOR).pack(pady=30)

    def dashboard_page(self):
        self.dashboard_frame = CTkFrame(master=self.root, fg_color=THEME_COlOR)
        self.dashboard_frame.pack(fill="both", expand=True)
        CTkLabel(self.dashboard_frame, text='Welcome Awwab', text_color = BLACK, fg_color = 'transparent', font=('Arial', 30, 'bold')).pack(pady=(30, 0))


    def login(self, email, password):
        data = {
            "email": email.get(),
            "password": password.get()
        }
        if data['email'] != 'awwab':
            self.signin_error.config(text='Incorrect email or password')
            self.signin_error.lift()
        else:
            self.account_frame.pack_forget()
            self.dashboard_page()

    def signup(self, name, email, password):
        con = sqlite3.connect("accounts.db")
        data = {
            "name": name.get(),
            "email": email.get(),
            "password": password.get()
        }

        print(name.get(), email.get(), password.get())

if __name__ == '__main__':
    app = App()