import tkinter as tk
from tkinter import messagebox, StringVar, OptionMenu
import mysql.connector


conn = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="Nitz@0620",
    
    database="hospital"
)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE if not exists appointments (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    age INT,
                    gender VARCHAR(50),
                    location VARCHAR(255),
                    doctor_name VARCHAR(255),
                    room_no VARCHAR(50),
                     date DATE,
                    time VARCHAR(50),
                    phone VARCHAR(20)
                )''')
conn.commit()


def add_appointment():
    name = name_var.get()
    age=age_var.get()
    gender = gender_var.get()
    location = location_var.get()
    doctor_name = doctor_name_var.get()
    room_no = room_no_var.get()
    date = date_var.get()  
    time = time_var.get()
    phone = phone_var.get()

    if name and age and gender and location and doctor_name and room_no and date and time and phone:
        try:
            cursor.execute("INSERT INTO appointments (name, age, gender, location, doctor_name, room_no, date, time, phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (name, age, gender, location, doctor_name, room_no, date, time, phone))
            conn.commit()
            update_summary()
            clear_screen()
            messagebox.showinfo("Success", "Appointment added successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
    else:
        messagebox.showerror("Error", "Please fill all fields.")

def search_appointment():
    appointment_id = search_id_var.get()
    cursor.execute("SELECT * FROM appointments WHERE id = %s", (appointment_id,))
    appointment = cursor.fetchone()
    if appointment:
        name_var.set(appointment[1])
        age_var.set(appointment[2])
        gender_var.set(appointment[3])
        location_var.set(appointment[4])
        doctor_name_var.set(appointment[5])
        room_no_var.set(appointment[6])
        date_var.set(appointment[7]) 
        time_var.set(appointment[8])
        phone_var.set(appointment[9])
    else:
        messagebox.showerror("Error", "Appointment not found.")

def update_appointment():
    appointment_id = search_id_var.get()
    new_time = reschedule_slot_var.get()
    new_date = reschedule_date_var.get()  
    cursor.execute("UPDATE appointments SET time = %s, date = %s WHERE id = %s", (new_time, new_date, appointment_id))
    conn.commit()
    update_summary()
    messagebox.showinfo("Success", "Appointment updated successfully!")

def cancel_appointment():
    appointment_id = search_id_var.get()
    cursor.execute("DELETE FROM appointments WHERE id = %s", (appointment_id,))
    conn.commit()
    update_summary()
    clear_screen()
    messagebox.showinfo("Success", "Appointment canceled successfully!")

def update_summary():
    cursor.execute("SELECT * FROM appointments") 
    appointments = cursor.fetchall()
    summary_text = f"TOTAL  APPOINTMENTS: {len(appointments)}\n"
    summary_text += "\n".join([f"\nPATIENT\t\tID:{appt[0]}\tNAME:{appt[1]}   AGE:{appt[2]}   GENDER:{appt[3]}   LOCATION:{appt[4]}   PHONE NO:{appt[9]} \nDOCTOR\t\tNAME:{appt[5]}\t\tROOM NO:{appt[6]}\nAPPOINTMENT\tDATE: {appt[7]}\t\tTIME:{appt[8]}" for appt in appointments])
    summary_label.config(text=summary_text)

def clear_screen():
    name_var.set("")
    age_var.set("")
    gender_var.set("Gender")
    location_var.set("")
    doctor_name_var.set("")
    room_no_var.set("")
    date_var.set("") 
    time_var.set("Slot")
    phone_var.set("")
    search_id_var.set("")
    reschedule_slot_var.set("Slot")
    reschedule_date_var.set("")  


root = tk.Tk()
root.title("Hospital Appointment System")
root.geometry("1400x900")


root.grid_columnconfigure(0, weight=1)  
root.grid_columnconfigure(1, weight=1)  
root.grid_columnconfigure(2, weight=1)  


name_var = StringVar()
age_var = StringVar()
gender_var = StringVar(value="Gender")
location_var = StringVar()
doctor_name_var = StringVar()
room_no_var = StringVar()
date_var = StringVar()  
time_var = StringVar(value="Slot")
phone_var = StringVar()
search_id_var = StringVar()
reschedule_slot_var = StringVar(value="Slot")
reschedule_date_var = StringVar()  

tk.Label(root, text="NLN HOSPITAL", font=("Times New Roman", 16, "bold")).grid(row=0, columnspan=3)

tk.Label(root, text="Patient Name").grid(row=1, column=0)
tk.Entry(root, textvariable=name_var).grid(row=1, column=1)

tk.Label(root, text="Age").grid(row=2, column=0)
tk.Entry(root, textvariable=age_var).grid(row=2, column=1)

tk.Label(root, text="Gender").grid(row=3, column=0)
OptionMenu(root, gender_var, "Male", "Female", "Other").grid(row=3, column=1)

tk.Label(root, text="Location").grid(row=4, column=0)
tk.Entry(root, textvariable=location_var).grid(row=4, column=1)


tk.Label(root, text="Doctor Name").grid(row=5, column=0)
tk.Entry(root, textvariable=doctor_name_var).grid(row=5, column=1)

tk.Label(root, text="Room No").grid(row=6, column=0)
tk.Entry(root, textvariable=room_no_var).grid(row=6, column=1)


tk.Label(root, text="Appointment Date (YYYY-MM-DD)").grid(row=7, column=0)
tk.Entry(root, textvariable=date_var).grid(row=7, column=1)  


tk.Label(root, text="Appointment Time").grid(row=8, column=0)
OptionMenu(root, time_var, "10:00 A.M.", "10:30 A.M.", "11:00 A.M.", "11:30 A.M.", "12:00 P.M.", "06:00 P.M", "06:30 P.M", "07:00P.M", "07:30 P.M", "08.00P.M").grid(row=8, column=1)

tk.Label(root, text="Phone Number").grid(row=9, column=0)
tk.Entry(root, textvariable=phone_var).grid(row=9, column=1)


tk.Button(root, text="Add appointment", command=add_appointment).grid(row=10, column=0)
tk.Button(root, text="Clear screen", command=clear_screen).grid(row=10, column=1)


tk.Label(root, text="Enter the Appointment ID to search",font=("Helvetica",10,"bold")).grid(row=11, column=0)
tk.Entry(root, textvariable=search_id_var).grid(row=11, column=1)
tk.Button(root, text="Search appointment", command=search_appointment).grid(row=11, column=2)


tk.Label(root, text="Reschedule Date (YYYY-MM-DD)").grid(row=12, column=0)
tk.Entry(root, textvariable=reschedule_date_var).grid(row=12, column=1) 

tk.Label(root, text="Reschedule Time").grid(row=13, column=0)
OptionMenu(root, reschedule_slot_var, "10:00 A.M.", "10:30 A.M.", "11:00 A.M.", "11:30 A.M.", "12:00 P.M.", "06:00 P.M", "06:30 P.M", "07:00P.M", "07:30 P.M", "08.00P.M").grid(row=13, column=1)

tk.Button(root, text="Update appointment", command=update_appointment).grid(row=14, column=0)
tk.Button(root, text="Cancel appointment", command=cancel_appointment).grid(row=14, column=1)

summary_label = tk.Label(root, text="", bg="light blue", anchor="nw", justify="left", width=100,height=45,font=("Arial",10))
summary_label.grid(row=0, column=3, rowspan=15, sticky="nsew")
update_summary()


root.mainloop()
 
