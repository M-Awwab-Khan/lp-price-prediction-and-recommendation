from customtkinter import *
from PIL import Image
from contants import *
import sqlite3
import pickle
import pandas as pd
import numpy as np

pipe = pickle.load(open('pipe.pkl', 'rb'))
df = pd.read_csv('cleaned_data.csv')

set_appearance_mode("light")

class App:
    def __init__(self):


        # Creating master window
        self.root = CTk()
        self.root.geometry("1280x720")

        self.create_account_page()
        self.con = sqlite3.connect("database.db")
        self.cur = self.con.cursor()

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
        self.signin_error = CTkLabel(self.account_tab.tab('Sign in'), width=200, corner_radius = 5, text_color = ERROR, fg_color = ERROR_FG, font=('Arial', 13))
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
        self.signup_error = CTkLabel(self.account_tab.tab('Create your account'), width=150, corner_radius = 5, text_color = ERROR, fg_color = ERROR_FG, font=('Arial', 13))
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
        self.dashboard_frame.pack(fill=BOTH, expand=True)
        self.dashboard_frame.pack_propagate(0)
        my_frame = CTkScrollableFrame(master=self.dashboard_frame , width=450 , height=400 ,
        fg_color=WHITE,corner_radius=20)
        CTkLabel(master=my_frame, text="Enter Specifications", font=("Arial", 30, "bold")).pack(pady=(30, 0))
        my_frame.place(in_=self.dashboard_frame, anchor='c', relx=.5, rely=.5)
        frame1=CTkFrame(master=my_frame , width=300 , height=220, fg_color=WHITE)
        frame1.pack(pady=30, side=RIGHT,expand=True,fill=BOTH)
        frame2=CTkFrame(master=my_frame , width=300 , height=220, fg_color=WHITE)
        frame2.pack(pady=30, side=LEFT,expand=True,fill=BOTH)
        #Labels
        l1=CTkLabel(frame2, text="Enter Company Name", fg_color="transparent", font=("Arial", 15))
        l1.pack(padx=13, pady=10, anchor="w")
        l2=CTkLabel(frame2, text="Enter Type Name", fg_color="transparent", font=("Arial", 15))
        l2.pack(padx=13, pady=10, anchor="w")
        l2=CTkLabel(frame2, text="Enter Weight (kg)", fg_color="transparent", font=("Arial", 15))
        l2.pack(padx=13, pady=10, anchor="w")
        l3=CTkLabel(frame2, text="Enter RAM (GB)", fg_color="transparent", font=("Arial", 15))
        l3.pack(padx=13, pady=10, anchor="w")
        l4=CTkLabel(frame2, text="Enter GPU Name", fg_color="transparent", font=("Arial", 15))
        l4.pack(padx=13, pady=10, anchor="w")    
        l5=CTkLabel(frame2, text="Enter IPS", fg_color="transparent", font=("Arial", 15))
        l5.pack(padx=13, pady=10, anchor="w")
        l13=CTkLabel(frame2, text="Enter Touchscreen", fg_color="transparent", font=("Arial", 15))
        l13.pack(padx=13, pady=10, anchor="w")
        l6=CTkLabel(frame2, text="Enter Screen Size (inches)", fg_color="transparent", font=("Arial", 15))
        l6.pack(padx=13, pady=10, anchor="w")
        l7=CTkLabel(frame2, text="Enter Screen Resolution", fg_color="transparent", font=("Arial", 15))
        l7.pack(padx=13, pady=10, anchor="w")
        l8=CTkLabel(frame2, text="Enter Processor Speed (GHz)", fg_color="transparent", font=("Arial", 15))
        l8.pack(padx=13, pady=10, anchor="w")
        l9=CTkLabel(frame2, text="Enter HDD (GB)", fg_color="transparent", font=("Arial", 15))
        l9.pack(padx=13, pady=10, anchor="w")
        l10=CTkLabel(frame2, text="Enter SSD (GB)", fg_color="transparent", font=("Arial", 15))
        l10.pack(padx=13, pady=10, anchor="w")
        l11=CTkLabel(frame2, text="Enter CPU Name", fg_color="transparent", font=("Arial", 15))
        l11.pack(padx=13, pady=10, anchor="w")
        l12=CTkLabel(frame2, text="Enter Operating System", fg_color="transparent", font=("Arial", 15))
        l12.pack(padx=13, pady=10, anchor="w")
        #comboboxes
        self.brandname=CTkComboBox(master=frame1,values=list(df['Company'].unique()), dropdown_fg_color=WHITE, dropdown_hover_color =THEME_COlOR, button_color=THEME_COlOR, width=150, corner_radius=5)
        self.brandname.pack(pady=10,padx=10, fill='x', expand=True)
        self.typename=CTkComboBox(master=frame1,values=list(df['TypeName'].unique()), dropdown_fg_color=WHITE, dropdown_hover_color =THEME_COlOR, button_color=THEME_COlOR, width=150, corner_radius=5)
        self.typename.pack(pady=10,padx=10, fill='x', expand=True)
        self.weight=CTkEntry(master=frame1, height=30)
        self.weight.pack(pady=10,padx=10, fill='x', expand=True)
        self.ram=CTkComboBox(master=frame1,values=["2", "4","8", "12", "16", "24","32","64","128"], dropdown_fg_color=WHITE, dropdown_hover_color =THEME_COlOR, button_color=THEME_COlOR, width=150, corner_radius=5)
        self.ram.pack(pady=10,padx=10, fill='x', expand=True)
        self.gpu=CTkComboBox(master=frame1,values=list(df['Gpu'].unique()), dropdown_fg_color=WHITE, dropdown_hover_color =THEME_COlOR, button_color=THEME_COlOR, width=150, corner_radius=5)
        self.gpu.pack(pady=10,padx=10, fill='x', expand=True)
        self.ips=CTkComboBox(master=frame1,values=["Yes","No"], dropdown_fg_color=WHITE, dropdown_hover_color =THEME_COlOR, button_color=THEME_COlOR, width=150, corner_radius=5)
        self.ips.pack(pady=10,padx=10, fill='x', expand=True)
        self.touchscreen=CTkComboBox(master=frame1,values=["Yes","No"], dropdown_fg_color=WHITE, dropdown_hover_color =THEME_COlOR, button_color=THEME_COlOR, width=150, corner_radius=5)
        self.touchscreen.pack(pady=10,padx=10, fill='x', expand=True)
        self.screensize=CTkEntry(master=frame1, height=30)
        self.screensize.pack(pady=10,padx=10, fill='x', expand=True)
        self.resolution=CTkComboBox(master=frame1,values=['1920x1080','1366x768','1600x900','3840x2160','3200x1800','2880x1800','2560x1600','2560x1440','2304x1440'], dropdown_fg_color=WHITE, dropdown_hover_color =THEME_COlOR, button_color=THEME_COlOR, width=150, corner_radius=5)
        self.resolution.pack(pady=10,padx=10, fill='x', expand=True)
        self.ghz=CTkEntry(master=frame1, height=30)
        self.ghz.pack(pady=10,padx=10, fill='x', expand=True)
        self.hdd=CTkComboBox(master=frame1,values=["0","128","256","512","1024","2048"], dropdown_fg_color=WHITE, dropdown_hover_color =THEME_COlOR, button_color=THEME_COlOR, width=150, corner_radius=5)
        self.hdd.pack(pady=10,padx=10, fill='x', expand=True)
        self.ssd=CTkComboBox(master=frame1,values=['0','128','256','512', "1024"], dropdown_fg_color=WHITE, dropdown_hover_color =THEME_COlOR, button_color=THEME_COlOR, width=150, corner_radius=5)
        self.ssd.pack(pady=10,padx=10, fill='x', expand=True)
        self.cpu=CTkComboBox(master=frame1,values=list(df['CPU Name'].unique()), dropdown_fg_color=WHITE, dropdown_hover_color =THEME_COlOR, button_color=THEME_COlOR, width=150, corner_radius=5)
        self.cpu.pack(pady=10,padx=10, fill='x', expand=True)
        self.os=CTkComboBox(master=frame1,values=list(df['os'].unique()), dropdown_fg_color=WHITE, dropdown_hover_color =THEME_COlOR, button_color=THEME_COlOR, width=150, corner_radius=5)
        self.os.pack(pady=(10, 40),padx=10, fill='x', expand=True)

        #predict button
        CTkButton(my_frame, text="Predict", command=self.predict_price, height=40, width=150, corner_radius=20, fg_color=THEME_COlOR).place(in_=my_frame, anchor='s', relx=.5, rely=1)
        prediction_frame = CTkFrame(master=self.dashboard_frame , width=400 , height=50 ,
        fg_color=WHITE,corner_radius=20)
        prediction_frame.place(in_=self.dashboard_frame, anchor='s', relx=.5, rely=.97)
        self.price_label = CTkLabel(master=prediction_frame, text='The predicted price will display here', font=("Arial", 20))
        self.price_label.pack(pady=30, padx=30)

    def predict_price(self):
        brandname = self.brandname.get()
        typename = self.typename.get()
        ram = int(self.ram.get())
        gpu = self.gpu.get()
        weight = float(self.weight.get())
        cpu = self.cpu.get()
        ghz = float(self.ghz.get())
        hdd = int(self.hdd.get())
        ssd = int(self.ssd.get())
        os = self.os.get()
        screensize = float(self.screensize.get())
        x_res = int(self.resolution.get().split('x')[0])
        y_res = int(self.resolution.get().split('x')[1])
        ppi = (((x_res**2) + (y_res**2))**0.5) / screensize
        if self.touchscreen.get() == "Yes":
            touchscreen = 1
        else:
            touchscreen = 0
        if self.ips.get() == "Yes":
            ips = 1
        else:
            ips = 0

        input_array = np.array([brandname, typename, ram, gpu, weight, touchscreen, ips, ppi, cpu, ghz, hdd, ssd, os], dtype='object')
        input_array = input_array.reshape(1, 13)
        price = round(np.exp(pipe.predict(input_array)[0]))
        self.price_label.configure(text=f"The predicted price for this configuration is Rs. {price}")

    def login(self, email, password):
        data = {
            "email": email.get(),
            "password": password.get()
        }
        
        # res = self.cur.execute(f"SELECT * FROM accounts WHERE email='{data['email']}'")
        # results = res.fetchall()
        # print(results)
        # if len(results) != 0:
        #     if results[0][2] == data['password']:
        #         self.account_frame.pack_forget()
        #         self.dashboard_page()
        # else:
        #     self.signin_error.configure(text='Invalid email or password')
        #     self.signin_error.lift()
        self.account_frame.pack_forget()
        self.dashboard_page()

    def signup(self, name, email, password):
        data = {
            "name": str(name.get()),
            "email": str(email.get()),
            "password": str(password.get())
        }
        if data['name'] and data['email'] and data['password']:
            self.cur.execute(f"""
            INSERT INTO accounts VALUES
                ('{data['name']}', '{data['email']}', '{data['password']}')
            """)
            self.con.commit()
            self.account_frame.pack_forget()
            self.dashboard_page()
        else:
            self.signup_error.configure(text='Missing values')
            self.signup_error.lift()

if __name__ == '__main__':
    app = App()