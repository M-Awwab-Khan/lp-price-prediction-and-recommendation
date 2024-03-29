from customtkinter import *
from PIL import Image
from contants import *
import sqlite3
import pickle
import pandas as pd
import numpy as np
from rec_mdl import get_recommendations
from CTkMessagebox import CTkMessagebox


pipe = pickle.load(open('pipe.pkl', 'rb'))
df = pd.read_csv('cleaned_data.csv')


set_appearance_mode("light")

class App:
    def __init__(self):


        # Creating master window
        self.root = CTk()
        self.root.geometry("1280x720")
        self.root.resizable(False, False)

        self.create_account_page()
        self.con = sqlite3.connect("database.db")
        self.cur = self.con.cursor()
        self.root.title("LAPTOP PRICE PREDICTION & RECOMMENDATION SYSTEM")
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
        # Dashboard Frame
        self.dashboard_frame = CTkFrame(master=self.root, fg_color=THEME_COlOR)
        self.dashboard_frame.pack(fill=BOTH, expand=True)
        self.dashboard_frame.pack_propagate(0)

        # Title Frame
        self.title_frame = CTkFrame(master=self.dashboard_frame, width=self.root.winfo_width(), height=50, fg_color=WHITE)
        self.title_frame.pack()
        self.title_frame.pack_propagate(0)

        # Title and Logout Button
        CTkLabel(master=self.title_frame, text='Laptop Price Prediction and Recommendation System', text_color=THEME_COlOR, font=('Arial', 20, 'bold')).pack(side=LEFT, padx=20)
        CTkButton(master=self.title_frame, text='Logout', command=self.logout, height=30, width=100, corner_radius=20, fg_color=THEME_COlOR).pack(side=RIGHT, padx=20)
        CTkButton(master=self.title_frame, text='Saved', command=self.saved_remmendations_page, height=30, width=100, corner_radius=20, fg_color=THEME_COlOR).pack(side=RIGHT, padx=10)

        # Recommendation Frame
        self.recommendation_frame = CTkScrollableFrame(master=self.dashboard_frame, width=450, height=400, fg_color=WHITE, corner_radius=10)

        # Scrollable Input Frame
        self.input_frame = CTkScrollableFrame(master=self.dashboard_frame, width=450 , height=400, fg_color=WHITE, corner_radius=10)
        self.input_frame.place(in_=self.dashboard_frame, anchor='c', relx=.5, rely=.5)

        # Heading
        CTkLabel(master=self.input_frame, text="Enter Specifications", text_color=THEME_COlOR, font=("Arial", 30, "bold")).pack(pady=(30, 0))

        # Labels and Entry Frame
        labels_frame=CTkFrame(master=self.input_frame , width=300 , height=220, fg_color=WHITE)
        labels_frame.pack(pady=30, side=LEFT,expand=True,fill=BOTH)
        entry_frame=CTkFrame(master=self.input_frame , width=300 , height=220, fg_color=WHITE)
        entry_frame.pack(pady=30, side=RIGHT,expand=True,fill=BOTH)

        #Labels
        CTkLabel(labels_frame, text="Enter Company Name", fg_color="transparent", font=("Arial", 15)).pack(padx=13, pady=10, anchor="w")
        CTkLabel(labels_frame, text="Enter Type Name", fg_color="transparent", font=("Arial", 15)).pack(padx=13, pady=10, anchor="w")
        CTkLabel(labels_frame, text="Enter Weight (kg)", fg_color="transparent", font=("Arial", 15)).pack(padx=13, pady=10, anchor="w")
        CTkLabel(labels_frame, text="Enter RAM (GB)", fg_color="transparent", font=("Arial", 15)).pack(padx=13, pady=10, anchor="w")
        CTkLabel(labels_frame, text="Enter GPU Name", fg_color="transparent", font=("Arial", 15)).pack(padx=13, pady=10, anchor="w")    
        CTkLabel(labels_frame, text="Enter IPS", fg_color="transparent", font=("Arial", 15)).pack(padx=13, pady=10, anchor="w")
        CTkLabel(labels_frame, text="Enter Touchscreen", fg_color="transparent", font=("Arial", 15)).pack(padx=13, pady=10, anchor="w")
        CTkLabel(labels_frame, text="Enter Screen Size (inches)", fg_color="transparent", font=("Arial", 15)).pack(padx=13, pady=10, anchor="w")
        CTkLabel(labels_frame, text="Enter Screen Resolution", fg_color="transparent", font=("Arial", 15)).pack(padx=13, pady=10, anchor="w")
        CTkLabel(labels_frame, text="Enter Processor Speed (GHz)", fg_color="transparent", font=("Arial", 15)).pack(padx=13, pady=10, anchor="w")
        CTkLabel(labels_frame, text="Enter HDD (GB)", fg_color="transparent", font=("Arial", 15)).pack(padx=13, pady=10, anchor="w")
        CTkLabel(labels_frame, text="Enter SSD (GB)", fg_color="transparent", font=("Arial", 15)).pack(padx=13, pady=10, anchor="w")
        CTkLabel(labels_frame, text="Enter CPU Name", fg_color="transparent", font=("Arial", 15)).pack(padx=13, pady=10, anchor="w")
        CTkLabel(labels_frame, text="Enter Operating System", fg_color="transparent", font=("Arial", 15)).pack(padx=13, pady=10, anchor="w")

        #Dropdowns
        self.brandname=CTkComboBox(master=entry_frame,values=list(df['Company'].unique()), dropdown_fg_color=WHITE, dropdown_hover_color =THEME_COlOR, button_color=THEME_COlOR, width=150, corner_radius=5)
        self.brandname.pack(pady=10,padx=10, fill='x', expand=True)
        self.typename=CTkComboBox(master=entry_frame,values=list(df['TypeName'].unique()), dropdown_fg_color=WHITE, dropdown_hover_color =THEME_COlOR, button_color=THEME_COlOR, width=150, corner_radius=5)
        self.typename.pack(pady=10,padx=10, fill='x', expand=True)
        self.weight=CTkEntry(master=entry_frame, height=30)
        self.weight.pack(pady=10,padx=10, fill='x', expand=True)
        self.ram=CTkComboBox(master=entry_frame,values=["2", "4","8", "12", "16", "24","32","64","128"], dropdown_fg_color=WHITE, dropdown_hover_color =THEME_COlOR, button_color=THEME_COlOR, width=150, corner_radius=5)
        self.ram.pack(pady=10,padx=10, fill='x', expand=True)
        self.gpu=CTkComboBox(master=entry_frame,values=list(df['Gpu'].unique()), dropdown_fg_color=WHITE, dropdown_hover_color =THEME_COlOR, button_color=THEME_COlOR, width=150, corner_radius=5)
        self.gpu.pack(pady=10,padx=10, fill='x', expand=True)
        self.ips=CTkComboBox(master=entry_frame,values=["Yes","No"], dropdown_fg_color=WHITE, dropdown_hover_color =THEME_COlOR, button_color=THEME_COlOR, width=150, corner_radius=5)
        self.ips.pack(pady=10,padx=10, fill='x', expand=True)
        self.touchscreen=CTkComboBox(master=entry_frame,values=["Yes","No"], dropdown_fg_color=WHITE, dropdown_hover_color =THEME_COlOR, button_color=THEME_COlOR, width=150, corner_radius=5)
        self.touchscreen.pack(pady=10,padx=10, fill='x', expand=True)
        self.screensize=CTkEntry(master=entry_frame, height=30)
        self.screensize.pack(pady=10,padx=10, fill='x', expand=True)
        self.resolution=CTkComboBox(master=entry_frame,values=['1920x1080','1366x768','1600x900','3840x2160','3200x1800','2880x1800','2560x1600','2560x1440','2304x1440'], dropdown_fg_color=WHITE, dropdown_hover_color =THEME_COlOR, button_color=THEME_COlOR, width=150, corner_radius=5)
        self.resolution.pack(pady=10,padx=10, fill='x', expand=True)
        self.ghz=CTkEntry(master=entry_frame, height=30)
        self.ghz.pack(pady=10,padx=10, fill='x', expand=True)
        self.hdd=CTkComboBox(master=entry_frame,values=["0","128","256","512","1024","2048"], dropdown_fg_color=WHITE, dropdown_hover_color =THEME_COlOR, button_color=THEME_COlOR, width=150, corner_radius=5)
        self.hdd.pack(pady=10,padx=10, fill='x', expand=True)
        self.ssd=CTkComboBox(master=entry_frame,values=['0','128','256','512', "1024"], dropdown_fg_color=WHITE, dropdown_hover_color =THEME_COlOR, button_color=THEME_COlOR, width=150, corner_radius=5)
        self.ssd.pack(pady=10,padx=10, fill='x', expand=True)
        self.cpu=CTkComboBox(master=entry_frame,values=list(df['CPU Name'].unique()), dropdown_fg_color=WHITE, dropdown_hover_color =THEME_COlOR, button_color=THEME_COlOR, width=150, corner_radius=5)
        self.cpu.pack(pady=10,padx=10, fill='x', expand=True)
        self.os=CTkComboBox(master=entry_frame,values=list(df['os'].unique()), dropdown_fg_color=WHITE, dropdown_hover_color =THEME_COlOR, button_color=THEME_COlOR, width=150, corner_radius=5)
        self.os.pack(pady=(10, 40),padx=10, fill='x', expand=True)

        #predict button
        CTkButton(self.input_frame, text="Predict", command=self.predict_and_recommend, height=40, width=150, corner_radius=20, fg_color=THEME_COlOR).place(in_=self.input_frame, anchor='s', relx=.5, rely=1)
    
    def back_to_dashboard_page(self):
        self.recommendations_page.pack_forget()
        self.dashboard_frame.pack(fill=BOTH, expand=True)
        self.dashboard_frame.pack_propagate(0)


    def saved_remmendations_page(self):
        # forgetting the previous i.e dashboard page
        self.dashboard_frame.pack_forget()

        # Creating main frame for recommendations page
        self.recommendations_page = CTkFrame(master=self.root, fg_color=THEME_COlOR)
        self.recommendations_page.pack(fill=BOTH, expand=True)
        self.recommendations_page.pack_propagate(0)

        # Creating title bar
        self.title_frame = CTkFrame(master=self.recommendations_page, width=self.root.winfo_width(), height=50, fg_color=WHITE)
        self.title_frame.pack()
        self.title_frame.pack_propagate(0)

        # Title and logout button
        # Title and Logout Button
        CTkLabel(master=self.title_frame, text='Laptop Price Prediction and Recommendation System', text_color=THEME_COlOR, font=('Arial', 20, 'bold')).pack(side=LEFT, padx=20)
        CTkButton(master=self.title_frame, text='Logout', command=self.logout, height=30, width=100, corner_radius=20, fg_color=THEME_COlOR).pack(side=RIGHT, padx=20)

        # Back button
        CTkButton(master=self.recommendations_page, width=70, height=30, fg_color=WHITE, text_color=THEME_COlOR, text='⬅ Back', font=('Arial', 14), corner_radius=20, command=self.back_to_dashboard_page).pack(anchor='nw', pady=20 , padx=20)
    
        # Creating scrollable self.saved_recommendations_frame 
        self.saved_recommendations_frame = CTkScrollableFrame(master=self.recommendations_page, width=700, height=550, fg_color=WHITE, corner_radius=10)
        self.saved_recommendations_frame.place(in_=self.recommendations_page, anchor='c', relx=.5, rely=.5)
        
        # heading
        CTkLabel(master=self.saved_recommendations_frame, text='Your Saved Recommendations', font=('Arial', 30, 'bold'), text_color=THEME_COlOR).pack(padx=10, pady=20)
        
        # fetching user's saved_recommendations from database
        query = f"""
            SELECT * FROM saved_recommendations
            WHERE email='{self.email}'
        """
        res = self.cur.execute(query)
        results = res.fetchall()

        if len(results) == 0:
            CTkLabel(master=self.saved_recommendations_frame, text='No saved recommendations to show', font=('Arial', 20)).pack(pady=20)
        else:
            for rec in results:
                rec_frame = CTkFrame(master=self.saved_recommendations_frame, width=670, height=170, fg_color=LIGHT_BLUE, corner_radius=5)
                rec_frame.pack(pady=10)
                rec_frame.pack_propagate(0)
                CTkButton(rec_frame, text='Delete', height=30, width=70, fg_color=ERROR_COLOR, corner_radius=5, command=lambda x=rec, y=rec_frame: self.delete_recommendation(x, y)).pack(anchor='e')
                CTkLabel(rec_frame, height=14, text=f"Rs. {round(int(rec[-1]))}", font=('Arial', 20, 'bold'), anchor='w').pack(anchor='w',padx=17, pady=(0, 10))
                CTkLabel(rec_frame, height=14, text=f"{rec[1]} {rec[2]} {rec[3]} inches {rec[4]}", font=('Arial', 15), wraplength=600).pack(anchor="w",padx=17, pady=3)
                CTkLabel(rec_frame, height=14, text=f"{rec[5]} {rec[6]} {rec[7]}", font=('Arial', 15), wraplength=600).pack(anchor="w",padx=17, pady=3)
                CTkLabel(rec_frame, height=14, text=f"{rec[8]} {rec[9]} {rec[10]}", font=('Arial', 15), wraplength=600).pack(anchor="w",padx=17, pady=3)

    def delete_recommendation(self, rec, rec_frame):
        query = f"""
            DELETE FROM saved_recommendations
            WHERE email = '{self.email}' AND company='{rec[1]}' AND typename='{rec[2]}' AND inches={rec[3]} AND screen_resolution='{rec[4]}' AND cpu='{rec[5]}' AND ram = '{rec[6]}' AND memory='{rec[7]}' AND gpu='{rec[8]}' AND os='{rec[9]}' AND weight='{rec[10]}' AND price={rec[11]}
        """
        self.cur.execute(query)
        self.con.commit()
        rec_frame.destroy()

    def logout(self):
        try:
            self.recommendations_page.pack_forget()
        except AttributeError:
            pass
        self.dashboard_frame.pack_forget()
        self.create_account_page()

    def save_recommendation(self, rec):
        query = f"""SELECT * FROM saved_recommendations 
                    WHERE email = '{self.email}' AND company='{rec['Company']}' AND typename='{rec['TypeName']}' AND inches={rec['Inches']} AND screen_resolution='{rec['ScreenResolution']}' AND cpu='{rec['Cpu']}' AND ram = '{rec['Ram']}' AND memory='{rec['Memory']}' AND gpu='{rec['Gpu']}' AND os='{rec['OpSys']}' AND weight='{rec['Weight']}' AND price={rec['Price']}"""
        res = self.cur.execute(query)
        results = res.fetchall()
        if len(results) == 0:
            self.cur.execute(f"""INSERT INTO saved_recommendations VALUES
                            ('{self.email}', '{rec['Company']}', '{rec['TypeName']}', {rec['Inches']}, '{rec['ScreenResolution']}', '{rec['Cpu']}', '{rec['Ram']}', '{rec['Memory']}', '{rec['Gpu']}', '{rec['OpSys']}', '{rec['Weight']}', {rec['Price']})
                        """)
            self.con.commit()
            CTkMessagebox(title='Success', message="Recommendation Successfully Saved",
                  icon="check", option_1="OK")
        else:
            CTkMessagebox(
                  message="Recommedation Already Saved", 
                  icon="cancel", 
                  option_1="OK",
                  title='Error'
                )
        

    def show_recommendations(self, recommendations_df):
        # input frame reposition
        self.input_frame.place(in_=self.dashboard_frame, anchor='c', relx=.3, rely=.5)
        # Recommendation Frame
        self.recommendation_frame.pack(side=RIGHT, padx=(0, 100), pady=(0, 45))

        # Heading
        CTkLabel(master=self.recommendation_frame, text='Suggested Laptops', text_color=THEME_COlOR, font=('Arial', 20, 'bold')).pack(pady=(10, 20))
        # dataframe to list of dictionaries
        rec_list = recommendations_df.to_dict('records')

        for rec in rec_list:
            rec_frame = CTkFrame(master=self.recommendation_frame, width=430, height=140, fg_color=LIGHT_BLUE, corner_radius=5)
            rec_frame.pack(pady=10)
            rec_frame.pack_propagate(0)
            CTkButton(rec_frame, text='Save', height=20, width=60, fg_color=THEME_COlOR, corner_radius=3, command=lambda x=rec: self.save_recommendation(x)).pack(anchor='e')
            CTkLabel(rec_frame, height=14, text=f"Rs. {round(int(rec['Price']))}", font=('Arial', 17, 'bold'), anchor='w').pack(anchor='w',padx=10, pady=(0, 5))
            CTkLabel(rec_frame, height=14, text=f"{rec['Company']} {rec['TypeName']} {rec['Inches']} inches {rec['ScreenResolution']}", font=('Arial', 13), wraplength=400).pack(anchor="w",padx=10, pady=3)
            CTkLabel(rec_frame, height=14, text=f"{rec['Cpu']} {rec['Ram']} {rec['Memory']}", font=('Arial', 13), wraplength=400).pack(anchor="w",padx=10, pady=3)
            CTkLabel(rec_frame, height=14, text=f"{rec['Gpu']} {rec['OpSys']} {rec['Weight']}", font=('Arial', 13), wraplength=400).pack(anchor="w",padx=10, pady=3)

    def show_prediction(self, price):
        try:
            self.price_label.configure(text=f"The predicted price for this configuration is Rs. {price}")
        except AttributeError:
            #prediciton frame
            prediction_frame = CTkFrame(master=self.dashboard_frame , width=400 , height=50 ,fg_color=WHITE,corner_radius=10)
            prediction_frame.place(in_=self.dashboard_frame, anchor='s', relx=.5, rely=.94)
            
            #price label in prediction frame
            self.price_label = CTkLabel(master=prediction_frame, text=f"The predicted price for this configuration is Rs. {price}", font=("Arial", 20))
            self.price_label.pack(pady=20, padx=30)        

    def predict_and_recommend(self):
        brandname = self.brandname.get()
        typename = self.typename.get()
        ram = int(self.ram.get())
        gpu = self.gpu.get()
        cpu = self.cpu.get()
        hdd = int(self.hdd.get())
        ssd = int(self.ssd.get())
        os = self.os.get()
        x_res = int(self.resolution.get().split('x')[0])
        y_res = int(self.resolution.get().split('x')[1])
        if self.touchscreen.get() == "Yes":
            touchscreen = 1
        else:
            touchscreen = 0
        if self.ips.get() == "Yes":
            ips = 1
        else:
            ips = 0
        try:
            weight = float(self.weight.get())
            ghz = float(self.ghz.get())
            screensize = float(self.screensize.get())
            ppi = (((x_res**2) + (y_res**2))**0.5) / screensize
            input_array = np.array([brandname, typename, ram, gpu, weight, touchscreen, ips, ppi, cpu, ghz, hdd, ssd, os], dtype='object')
            input_array = input_array.reshape(1, 13)
            price = round(np.exp(pipe.predict(input_array)[0]))
            recommendations_df = get_recommendations(brandname, typename, ram, gpu, weight, price, touchscreen, ips, ppi, cpu, ghz, hdd, ssd, os)
            self.show_prediction(price)
            for widget in self.recommendation_frame.winfo_children():
                widget.destroy()
            self.show_recommendations(recommendations_df)
        except ValueError:
            CTkMessagebox(
                  message="Enter valid values for all fields", 
                  icon="cancel", 
                  option_1="OK",
                  title='Error'
                )

    def login(self, email, password):
        data = {
            "email": email.get(),
            "password": password.get()
        }
        
        res = self.cur.execute(f"SELECT * FROM accounts WHERE email='{data['email']}'")
        results = res.fetchall()

        if len(results) != 0:
            if results[0][2] == data['password']:
                self.account_frame.pack_forget()
                self.dashboard_page()
                self.email = data['email']
        else:
            self.signin_error.configure(text='Invalid email or password')
            self.signin_error.lift()

    def signup(self, name, email, password):
        data = {
            "name": str(name.get()),
            "email": str(email.get()),
            "password": str(password.get())
        }
        if data['name'] and data['email'] and data['password']:
            res = self.cur.execute(f"""SELECT email FROM accounts WHERE email='{data['email']}'""")
            results = res.fetchall()
            if len(results) == 0:
                self.cur.execute(f"""
                INSERT INTO accounts VALUES
                    ('{data['name']}', '{data['email']}', '{data['password']}')
                """)
                self.con.commit()
                self.email = data['email']
                self.account_frame.pack_forget()
                self.dashboard_page()
            else:
                self.signup_error.configure(text='This email already exists.')
                self.signup_error.lift()
        else:
            self.signup_error.configure(text='Missing values')
            self.signup_error.lift()

if __name__ == '__main__':
    app = App()