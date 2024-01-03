import customtkinter

def button_callback():
    print("button clicked")

app = customtkinter.CTk()
app.geometry("1280x720")

frame = customtkinter.CTkFrame(master=app, width=500,fg_color="white", height=200)
frame.place(x=400,y=250)
button = customtkinter.CTkButton(frame, text="my button", command=button_callback)
button.pack(padx=20, pady=20)
app.mainloop()