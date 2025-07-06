import tkinter as tk
import customtkinter
from tkinter import messagebox,filedialog
import sqlite3
import re
from PIL import Image, ImageTk
from tkcalendar import Calendar
import uuid
from fpdf import FPDF
import os
from tkinter import StringVar, Entry, Label
from reportlab.lib.pagesizes import landscape
from tkinter import messagebox
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from PIL import Image
from customtkinter import CTkImage, CTkLabel
import customtkinter as ctk
from tkinter import ttk
import ast
from tkcalendar import DateEntry
import json
from datetime import datetime
from tkinter import Tk, messagebox, StringVar, OptionMenu, Button, Label, Entry, Text
from tkinter import messagebox, StringVar, OptionMenu, Entry, Button, Text, Toplevel, Frame, Label






# ฟังก์ชันเข้าสู่ระบบผู้ใช้
def login():
    username = entry_user.get()
    password = entry_pass.get()
    if username and password:
        login_user(username, password)
    else:
        messagebox.showerror("Error", "Please enter both username and password.")

def login_user(username, password):
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password)
    )
    user = cursor.fetchone()
    if user:
        open_next_window()  
    else:
        messagebox.showerror("Error", "Invalid username or password.")


#---------------------- ฟังก์ชันลงทะเบียนผู้ใช้ --------------------------
def register_user(username, password, email):
    # บันทึกข้อมูลในฐานข้อมูล
    print(f"ลงทะเบียน: {username}, {email}")
    register_window.withdraw()
    messagebox.showinfo("Success", "ลงทะเบียนสำเร็จ!")
    app.deiconify()  

# ฟังก์ชันเปิดหน้าต่างลงทะเบียน
def open_register_window():
    app.withdraw()
    global register_window 
    register_window = create_window_with_frame("Register")
    register_window.geometry("1000x700")
    
    try:
        profile_image = Image.open("profile3.png")
        profile_image = profile_image.resize((900, 650), Image.LANCZOS)
        profile_photo = CTkImage(profile_image, size=(900, 650))  

        profile_label = customtkinter.CTkLabel(master=register_window, image=profile_photo, text="")
        profile_label.image = profile_photo  
        profile_label.place(relx=0.5, rely=0.5, anchor="center")
    except Exception as e:
        print(f"Unable to load image: {e}")

    # ช่องป้อนข้อมูลการลงทะเบียน
    reg_user_label = customtkinter.CTkLabel(master=register_window, text="Username:", text_color="black", bg_color="#9EC082")
    reg_user_label.place(relx=0.3, rely=0.4, anchor="e")
    reg_user_entry = customtkinter.CTkEntry(master=register_window, width=200, border_color="#9EC082", fg_color="#FFFFFF")  
    reg_user_entry.place(relx=0.5, rely=0.4, anchor="center")

    reg_pass_label = customtkinter.CTkLabel(master=register_window, text="Password:", text_color="black", bg_color="#9EC082")
    reg_pass_label.place(relx=0.3, rely=0.5, anchor="e")
    reg_pass_entry = customtkinter.CTkEntry(master=register_window, width=200, show="*", border_color="#9EC082", fg_color="#FFFFFF")  
    reg_pass_entry.place(relx=0.5, rely=0.5, anchor="center")

    reg_email_label = customtkinter.CTkLabel(master=register_window, text="Email:", text_color="black", bg_color="#9EC082")
    reg_email_label.place(relx=0.3, rely=0.6, anchor="e")
    reg_email_entry = customtkinter.CTkEntry(master=register_window, width=200, border_color="#9EC082", fg_color="#FFFFFF")  
    reg_email_entry.place(relx=0.5, rely=0.6, anchor="center")

# ปุ่มลงทะเบียน
    register_button = customtkinter.CTkButton(
    master=register_window,
    text="Register",
    command=lambda: register_user(
        reg_user_entry.get(),
        reg_pass_entry.get(),
        reg_email_entry.get(),
        register_window 
        ),
        width=200
    )
    register_button.place(relx=0.5, rely=0.7, anchor="center")


# ตรวจสอบในฐานข้อมูล
def register_user(username, password, email, parent_window):
    # ตรวจสอบเงื่อนไขของ username
    if not validate_username(username):
        messagebox.showerror(
            "Error",
            "Username must be 5-20 characters long and contain only letters and numbers.",
            parent=parent_window
        )
        return

    # ตรวจสอบเงื่อนไขของ password
    if not validate_password(password):
        messagebox.showerror(
            "Error",
            "Password must be 8-20 characters long, and include uppercase, lowercase, and numbers.",
            parent=parent_window
        )
        return

    # ตรวจสอบว่าชื่อผู้ใช้ซ้ำหรือไม่
    if check_username_exists(username):
        messagebox.showerror("Error", "Username already exists. Please choose a different one.",
            parent=parent_window
        )
        return

    # บันทึกข้อมูลลงฐานข้อมูล
    try:
        cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email,))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!", parent=parent_window)  
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        messagebox.showerror("Error", "Registration failed. Please try again.", parent=parent_window)  


# ตรวจสอบ username
def validate_username(username):
    return len(username) >= 6 and len(username) <= 20 and username.isalnum()

# ตรวจสอบ password
def validate_password(password):
    if len(password) < 8 or len(password) > 20:
        return False
    if not re.search(r'[A-Z]', password): 
        return False
    if not re.search(r'[a-z]', password):  
        return False
    if not re.search(r'[0-9]', password):  
        return False
    return True

# ตรวจสอบว่าชื่อผู้ใช้ซ้ำหรือไม่
def check_username_exists(username):
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone() is not None

# สร้างหน้าต่างที่เป็นหน้าหลักก
def create_window_with_frame(title):
    window = customtkinter.CTkToplevel(app)
    window.geometry("1000x700")
    window.title(title)
    window.attributes('-topmost', True)  
    window.update_idletasks() 
    x = (window.winfo_screenwidth() // 2) - (1000 // 2)  
    y = (window.winfo_screenheight() // 2) - (700 // 2)  
    window.geometry(f"1000x700+{x}+{y}")

    frame = customtkinter.CTkFrame(
        master=window,
        fg_color="#DBEFDA",
        width=1000,
        height=700
    )
    frame.pack(pady=20)

    return window

app = customtkinter.CTk()
app_width = 1000
app_height = 700
app.geometry(f"{app_width}x{app_height}")

x = (app.winfo_screenwidth() // 2) - (app_width // 2)
y = (app.winfo_screenheight() // 2) - (app_height // 2)
app.geometry(f"{app_width}x{app_height}+{x}+{y}")

app.title("Welcome")
customtkinter.set_appearance_mode("light")

# frameป้อนชื่อผู้ใช้และรหัสผ่าน
frame_1 = customtkinter.CTkFrame(master=app, fg_color="#DBEFDA", width=1000, height=700)
frame_1.pack(pady=20)

image_path = "profile1.png"
try:
    png_file = Image.open(image_path)
    png_file = png_file.resize((900, 650), Image.LANCZOS)
    photo = CTkImage(png_file, size=(900, 650)) 
    image_label = customtkinter.CTkLabel(master=frame_1, image=photo)
    image_label.image = photo
    image_label.pack(fill="both", expand=True)
except Exception as e:
    print(f"Unable to load image: {e}")

# ป้อนชื่อผู้ใช้และรหัสผ่าน
label_user = customtkinter.CTkLabel(master=frame_1, text="Username:", text_color="black")
label_user.place(relx=0.3, rely=0.4, anchor="e")
entry_user = customtkinter.CTkEntry(master=frame_1, width=200)
entry_user.place(relx=0.5, rely=0.4, anchor="center")

label_pass = customtkinter.CTkLabel(master=frame_1, text="Password:", text_color="black")
label_pass.place(relx=0.3, rely=0.5, anchor="e")
entry_pass = customtkinter.CTkEntry(master=frame_1, width=200, show="*")
entry_pass.place(relx=0.5, rely=0.5, anchor="center")


icon_login_image = Image.open("icon1.png")
icon_login_image = icon_login_image.resize((24, 24), Image.LANCZOS)
icon_login_photo = CTkImage(icon_login_image, size=(24, 24))

icon_register_image = Image.open("icon2.png")
icon_register_image = icon_register_image.resize((24, 24), Image.LANCZOS)
icon_register_photo = CTkImage(icon_register_image, size=(24, 24))

# ปุ่มเข้าสู่ระบบ
login_button = customtkinter.CTkButton(
    master=frame_1,
    text="Login",
    command=login,
    image=icon_login_photo,
    compound="left",
    width=200
)
login_button.place(relx=0.5, rely=0.6, anchor="center")

# ปุ่มลงทะเบียน
register_button = customtkinter.CTkButton(
    master=frame_1,
    text="Register",
    command=open_register_window,
    image=icon_register_photo,
    compound="left",
    width=200
)
register_button.place(relx=0.5, rely=0.7, anchor="center")

#--------------------------- หน้าAdmin ---------------------------------
# กำหนดรหัสแอดมิน
def verify_admin_password():
    admin_password = "spd888" 

    # ตรวจสอบรหัส
    entered_password = password_entry.get()

    if entered_password == admin_password:
        open_admin_window()  
        password_window.after(100, password_window.destroy)  
    else:
        messagebox.showerror("Error", "รหัสผ่านไม่ถูกต้อง")  


# **************** ฟังก์ชันเปิดหน้าต่างสำหรับกรอกรหัสผ่าน ***************
def open_password_window():
    global password_window  
    password_window = ctk.CTkToplevel()  
    password_window.title("Enter Admin Password") 
    password_window.geometry("400x200")  

    screen_width = password_window.winfo_screenwidth()
    screen_height = password_window.winfo_screenheight()
    position_x = int((screen_width - 400) / 2)
    position_y = int((screen_height - 200) / 2)

    password_window.geometry(f"400x200+{position_x}+{position_y}")
    password_window.attributes('-topmost', True)

    # Label/Entry สำหรับกรอกรหัสผ่าน
    password_label = ctk.CTkLabel(password_window, text="กรอกรหัสผ่านแอดมิน", font=("Arial", 14))
    password_label.pack(pady=10)

    global password_entry
    password_entry = ctk.CTkEntry(password_window, show="*", width=200)
    password_entry.pack(pady=10)

    verify_button = ctk.CTkButton(password_window, text="ยืนยัน", command=verify_admin_password)
    verify_button.pack(pady=10)


# **************** ฟังก์ชันเปิดหน้าต่าง Admin ***************
def open_admin_window():
    global admin_window  
    admin_window = ctk.CTkToplevel()  
    admin_window.title("Admin")  
    admin_window.geometry("1000x700")  

    screen_width = admin_window.winfo_screenwidth()
    screen_height = admin_window.winfo_screenheight()
    position_x = int((screen_width - 1000) / 2)
    position_y = int((screen_height - 700) / 2)

    admin_window.geometry(f"1000x700+{position_x}+{position_y}")
    admin_window.attributes('-topmost', True)
    admin_window.focus_force() 

    # โหลดและปรับขนาดรูปภาพ
    image_path = "profile13.png"
    try:
        image = Image.open(image_path)
        resized_image = image.resize((900, 650), Image.LANCZOS) 
        ct_image = CTkImage(resized_image, size=(900, 650))  

        image_label = CTkLabel(admin_window, image=ct_image, text="")  
        image_label.image = ct_image 
        image_label.pack(pady=10)  
    except Exception as e:
        error_label = CTkLabel(admin_window, text=f"Unable to load image: {e}", text_color="red")
        error_label.pack(pady=20)



    # ฟังก์ชันสำหรับแสดงข้อมูลของชาวไทย
    def show_thai_data():
        global current_table
        current_table = 'thai'  
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, first_name, last_name, ticket_details, total_price, visit_date FROM dataticket_thai")
        thai_data = cursor.fetchall()
        conn.close()

        # ล้างข้อมูลใน Treeview และเพิ่มข้อมูลใหม่
        for row in tree.get_children():
            tree.delete(row)

        for row in thai_data:
            tree.insert("", "end", values=row)



    # ฟังก์ชันสำหรับแสดงข้อมูลของชาวต่างชาติ
    def show_foreign_data():
        global current_table
        current_table = 'foreign'  
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, first_name, last_name, ticket_details, total_price, visit_date FROM dataticket_foreign")
        foreign_data = cursor.fetchall()
        conn.close()

        # ล้างข้อมูลใน Treeview และเพิ่มข้อมูลใหม่
        for row in tree.get_children():
            tree.delete(row)

        # เพิ่มข้อมูลจากชาวต่างชาติ
        for row in foreign_data:
            tree.insert("", "end", values=row)

        # เพิ่ม Date Picker สำหรับเลือกวันที่
    date_picker = DateEntry(admin_window, date_pattern="yyyy-mm-dd", width=12, background="darkblue", foreground="white", borderwidth=2)
    date_picker.place(relx=0.25, rely=0.5, anchor="center")

    # ฟังก์ชันการค้นหาตามวันที่
    # ฟังก์ชันการค้นหาตามวันที่ (แยกค้นหาชาวไทยและชาวต่างชาติ)
    def search_by_date():
        selected_date = date_picker.get_date()  # รับวันที่จาก DateEntry
        formatted_date = selected_date.strftime("%m/%d/%y")  # แปลงเป็นรูปแบบที่ฐานข้อมูลรองรับ (MM/DD/YY)

        print("ค้นหาวันที่:", formatted_date)  # เพิ่มการแสดงวันที่ที่เลือกเพื่อเช็ค

    # ล้างข้อมูลใน Treeview ก่อน
        for row in tree.get_children():
            tree.delete(row)

    # ค้นหาข้อมูลจากตารางชาวไทย
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, first_name, last_name, ticket_details, total_price, visit_date FROM dataticket_thai WHERE visit_date = ?", (formatted_date,))
        thai_data = cursor.fetchall()

    # ค้นหาข้อมูลจากตารางชาวต่างชาติ
        cursor.execute("SELECT id, first_name, last_name, ticket_details, total_price, visit_date FROM dataticket_foreign WHERE visit_date = ?", (formatted_date,))
        foreign_data = cursor.fetchall()
        conn.close()

    # แสดงผลข้อมูลชาวไทย
        if thai_data:
            for row in thai_data:
                tree.insert("", "end", values=row)
          
        else:
            tree.insert("", "end", values=("ไม่มีข้อมูลชาวไทย", "", "", "", "", ""))

    # แสดงผลข้อมูลชาวต่างชาติ
        if foreign_data:
            for row in foreign_data:
                tree.insert("", "end", values=row)
        
        else:
            tree.insert("", "end", values=("ไม่มีข้อมูลชาวต่างชาติ", "", "", "", "", ""))

    # ปุ่มค้นหาตามวันที่
    search_date_button = ctk.CTkButton(
        admin_window, 
        text="ค้นหาตามวันที่", 
        command=search_by_date,
        fg_color="#6ba8c5"  # กำหนดสีพื้นหลังให้กับปุ่ม
    )
    search_date_button.place(relx=0.25, rely=0.55, anchor="center")


    # สร้าง Treeview แสดงข้อมูลในรูปแบบตาราง
    tree = ttk.Treeview(admin_window, columns=("id", "first_name", "last_name", "ticket_details", "total_price", "visit_date"), show="headings")
    tree.heading("id", text="ID")
    tree.heading("first_name", text="ชื่อ")
    tree.heading("last_name", text="นามสกุล")
    tree.heading("ticket_details", text="รายละเอียดตั๋ว")
    tree.heading("total_price", text="ราคาทั้งหมด")
    tree.heading("visit_date", text="วันที่เข้าชม")

    tree.column("id", width=40, anchor="center")
    tree.column("first_name", width=150, anchor="center")
    tree.column("last_name", width=150, anchor="center")
    tree.column("ticket_details", width=350, anchor="center")
    tree.column("total_price", width=100, anchor="center")  
    tree.column("visit_date", width=100, anchor="center") 

    tree.place(relx=0.5, rely=0.27, anchor="center")

    thai_button = ctk.CTkButton(admin_window, text="แสดงข้อมูลชาวไทย", command=show_thai_data, fg_color="#5096ae")
    thai_button.place(relx=0.25, rely=0.1, anchor="center")

    foreign_button = ctk.CTkButton(admin_window, text="แสดงข้อมูลชาวต่างชาติ", command=show_foreign_data, fg_color="#5096ae")
    foreign_button.place(relx=0.75, rely=0.1, anchor="center")

    show_thai_data()

        # **************** ฟีเจอร์การค้นหา ***************
    # สร้างฟังก์ชันค้นหา
    def search_data():
        search_query = search_entry.get().strip().lower()
        for row in tree.get_children():
            tree.delete(row)

        # ดึงข้อมูลที่กรองตามคำค้นหา
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, first_name, last_name, ticket_details, total_price, visit_date FROM dataticket_thai")
        thai_data = cursor.fetchall()
        conn.close()

        # กรองข้อมูล
        filtered_data = [
            row for row in thai_data if search_query in str(row).lower()
        ]
        for row in filtered_data:
            tree.insert("", "end", values=row)
        

    # เพิ่มช่องค้นหาและปุ่ม Search
    search_entry = ctk.CTkEntry(admin_window, placeholder_text="กรอกคำค้นหา...")
    search_entry.place(relx=0.5, rely=0.5, anchor="center")

    search_button = ctk.CTkButton(admin_window, text="Search", command=search_data)
    search_button.place(relx=0.5, rely=0.55, anchor="center")


    # **************** ฟีเจอร์การแก้ไขข้อมูล ***************
    #ฟังก์ชันการแก้ไขข้อมูล
    def edit_data_window(selected_item):
        edit_window = ctk.CTkToplevel()
        edit_window.title("แก้ไขข้อมูล")
        edit_window.geometry("1000x700")

        screen_width = edit_window.winfo_screenwidth() 
        screen_height = edit_window.winfo_screenheight()
        position_x = int((screen_width - 1000) / 2)
        position_y = int((screen_height - 700) / 2)  
        edit_window.geometry(f"1000x700+{position_x}+{position_y}")

        edit_window.attributes('-topmost', True)
    
        selected_values = tree.item(selected_item, "values")
        labels = ["ID", "ชื่อ", "นามสกุล", "รายละเอียดตั๋ว", "ราคาทั้งหมด", "วันที่เข้าชม"]

        entries = []
        for i, label in enumerate(labels):
            lbl = ctk.CTkLabel(edit_window, text=label)
            lbl.pack(pady=5)
            entry = ctk.CTkEntry(edit_window)
            entry.insert(0, selected_values[i])
            entry.pack(pady=5)
            entries.append(entry)

        def save_changes():
            updated_values = [entry.get() for entry in entries]
            tree.item(selected_item, values=updated_values)
            # อัปเดตข้อมูลในฐานข้อมูล
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE dataticket_thai
                SET first_name=?, last_name=?, ticket_details=?, total_price=?, visit_date=?
                WHERE id=?
            """, (*updated_values[1:], updated_values[0]))
            conn.commit()
            conn.close()
            edit_window.destroy()

        save_button = ctk.CTkButton(edit_window, text="Save", command=save_changes)
        save_button.pack(pady=10)

    # ฟังก์ชันสำหรับลบข้อมูล
        def delete_data():
            tree.delete(selected_item)
        
            # ลบข้อมูลจากฐานข้อมูล
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM dataticket_thai WHERE id=?", (selected_values[0],))
            conn.commit()
            conn.close()
            edit_window.destroy()

        delete_button = ctk.CTkButton(edit_window, text="Delete", command=delete_data)
        delete_button.pack(pady=10)

    # ฟังก์ชันออกจากระบบ 
    def logout():
        admin_window.destroy()  

    logout_button = ctk.CTkButton(admin_window, text="Logout", command=logout, fg_color="#ffe7d0",text_color=("#8e4500"))
    logout_button.place(relx=0.5, rely=0.9, anchor="center")  

    # ดับเบิลคลิกเพื่อเปิดหน้าต่างการแก้ไข
    def on_tree_item_double_click(event):
        selected_item = tree.selection()
        if selected_item:
            edit_data_window(selected_item[0])

    tree.bind("<Double-1>", on_tree_item_double_click)
  
    # ปุ่มสรุปยอดขาย
    sales_report_button = ctk.CTkButton(
        master=admin_window,
        text="สรุปยอดขายตั๋ว",
        command=open_report_window, 
        fg_color="#6ba8c5",
        text_color="white",
        width=100,
        height=40
    )
    sales_report_button.place(relx=0.7, rely=0.5, anchor="center")  

    # ปุ่มยอดรายได้
    Income_report_button = ctk.CTkButton(
        master=admin_window,
        text="สรุปยอดรายได้",
        command=open_sales_window,  
        fg_color="#6ba8c5",
        text_color="white",
        width=100,
        height=40
    )
    Income_report_button.place(relx=0.7, rely=0.6, anchor="center")  


# ****************ปุ่ม Admin (ใช้รูปภาพเป็นปุ่ม)***************
# โหลดรูปภาพสำหรับปุ่ม
icon_image = Image.open("icon5.png")
icon_image = icon_image.resize((50, 50))  
icon_image = ImageTk.PhotoImage(icon_image)

admin_button = ctk.CTkButton(
    master=frame_1,
    image=icon_image,  
    command=open_password_window,  
    fg_color="transparent", 
    width=50,
    height=50,  
    text=""  
)
admin_button.place(relx=0.06, rely=0.1, anchor="center") 

# ข้อความที่จะแสดงข้างปุ่ม
admin_label = ctk.CTkLabel(
    master=frame_1,
    text="Admin",  
    font=("Arial", 16), 
)
admin_label.place(relx=0.13, rely=0.1, anchor="center")  

#--------------------หน้าแสดงยอดขายรายวัน รายเดือน รายปี----------------------------------


# ตรวจสอบความถูกต้องของวันที่
def is_valid_date(date_str, date_format):
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False

# ดึงข้อมูลยอดขายของชาวไทย
def fetch_sales_thai(period, date_value):
    return fetch_sales_data(period, date_value, "dataticket_thai")

# ดึงข้อมูลยอดขายของชาวต่างชาติ
def fetch_sales_foreign(period, date_value):
    return fetch_sales_data(period, date_value, "dataticket_foreign")

# ฟังก์ชันกลางสำหรับดึงข้อมูลจากฐานข้อมูล
def fetch_sales_data(period, date_value, table_name):
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        if period == "daily":
            if not is_valid_date(date_value, "%m/%d/%y"):
                raise ValueError("รูปแบบวันที่สำหรับรายวันควรเป็น MM/DD/YY หรือ M/D/YY")
            query = f"""
                SELECT ticket_details, total_price
                FROM {table_name}
                WHERE visit_date = ?
            """
            cursor.execute(query, (date_value,))

        elif period == "monthly":
            if not is_valid_date(date_value, "%m/%y"):
                raise ValueError("รูปแบบวันที่สำหรับรายเดือนควรเป็น MM/YY หรือ M/YY")

            month, year = date_value.split("/")
            query = f"""
                SELECT ticket_details, total_price
                FROM {table_name}
                WHERE SUBSTR(visit_date, 1, INSTR(visit_date, '/') - 1) = ? 
                AND SUBSTR(visit_date, -2) = ?
            """
            cursor.execute(query, (month, year))  # เช่น ("01", "25")

        elif period == "yearly":
            if not is_valid_date(date_value, "%y"):
                raise ValueError("รูปแบบวันที่สำหรับรายปีควรเป็น YY")

            query = f"""
                SELECT ticket_details, total_price
                FROM {table_name}
                WHERE SUBSTR(visit_date, -2) = ?
            """
            cursor.execute(query, (date_value,))  # เช่น ("25")


        else:
            raise ValueError("ช่วงเวลาที่ระบุไม่ถูกต้อง")

        sales_data = cursor.fetchall()
        conn.close()

        # เพิ่มการพิมพ์ข้อความเพื่อตรวจสอบข้อมูลที่ดึงมา
        print(f"Query: {query}")
        print(f"Date Value: {date_value}")
        print(f"Sales Data: {sales_data}")

        return sales_data

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"เกิดข้อผิดพลาดในฐานข้อมูล: {e}")
        return []
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
        return []

# ฟังก์ชันสำหรับคำนวณราคาตั๋ว
def calculate_ticket_price(ticket_type, count, is_foreign):
    prices_thai = {
        "ตั๋วเข้าชมสวนสัตว์ (เด็กเล็ก)": 29,
        "ตั๋วเข้าชมสวนสัตว์ (เด็กโต)": 59,
        "ตั๋วเข้าชมสวนสัตว์ (ผู้ใหญ่)": 139,
        "ตั๋วเข้าชมสวนสัตว์ (ผู้สูงอายุ)": 0,
        "ตั๋วเข้าชมอควาเรียม (เด็ก)": 40,
        "ตั๋วเข้าชมอควาเรียม (ผู้ใหญ่)": 80,
        "ตั๋วเข้าชมการแสดงสัตว์ (เด็ก)": 30,
        "ตั๋วเข้าชมการแสดงสัตว์ (ผู้ใหญ่)": 50
    }

    prices_foreign = {
        "Zoo Ticket (Teeneger)": 89,
        "Zoo Ticket (Child)": 159,
        "Zoo Ticket (Adult)": 249,
        "Zoo Ticket (Senior)": 0,
        "Aquarium Ticket (Child)": 100,
        "Aquarium Ticket (Adult)": 140,
        "Animal Show Ticket (Child)": 50,
        "Animal Show Ticket (Adult)": 100
    }

    prices = prices_foreign if is_foreign else prices_thai
    return prices.get(ticket_type, 0) * count

def display_report(period, date_value, customer_type):
    thai_sales = fetch_sales_thai(period, date_value) if customer_type in ["Thai", "Both"] else []
    foreign_sales = fetch_sales_foreign(period, date_value) if customer_type in ["Foreign", "Both"] else []

    combined_thai_details = {}
    combined_foreign_details = {}
    total_price_thai = 0
    total_price_foreign = 0
    total_tickets_thai = 0
    total_tickets_foreign = 0

    # ประมวลผลข้อมูลชาวไทย
    for sales_data in thai_sales:
        details, price = sales_data  # แยกข้อมูลเป็น 'รายละเอียดตั๋ว' และ 'ราคา'
        try:
            details = details.replace("'", "\"")
            ticket_details = json.loads(details)
        except json.JSONDecodeError as e:
            messagebox.showerror("JSON Error", f"เกิดข้อผิดพลาดในการแปลงข้อมูล JSON: {e}")
            continue

        for t_type, count in ticket_details.items():  # วนลูปข้อมูลประเภทตั๋ว และจำนวนที่ขาย
            combined_thai_details[t_type] = combined_thai_details.get(t_type, 0) + count
            total_tickets_thai += count
            total_price_thai += calculate_ticket_price(t_type, count, is_foreign=False)

    # ประมวลผลข้อมูลชาวต่างชาติ
    for sales_data in foreign_sales:
        details, price = sales_data  # แยกข้อมูลเป็น 'รายละเอียดตั๋ว' และ 'ราคา'
        try:
            details = details.replace("'", "\"")
            ticket_details = json.loads(details)
        except json.JSONDecodeError as e:
            messagebox.showerror("JSON Error", f"เกิดข้อผิดพลาดในการแปลงข้อมูล JSON: {e}")
            continue

        for t_type, count in ticket_details.items(): # วนลูปข้อมูลประเภทตั๋ว และจำนวนที่ขาย
            combined_foreign_details[t_type] = combined_foreign_details.get(t_type, 0) + count
            total_tickets_foreign += count
            total_price_foreign += calculate_ticket_price(t_type, count, is_foreign=True)

    # สร้างหน้าต่างแสดงผล
    report_window = Toplevel()
    report_window.title("Sales Report")
    report_window.geometry("1200x900")

    # ทำให้หน้าต่างอยู่หน้าสุด
    report_window.attributes("-topmost", True)
    report_window.lift()
    report_window.focus_force()
    report_window.after(100, lambda: report_window.lift())
    report_window.after(100, lambda: report_window.focus_force())

    # ทำให้หน้าต่างอยู่กลางหน้าจอ
    screen_width = report_window.winfo_screenwidth()
    screen_height = report_window.winfo_screenheight()
    position_x = int((screen_width - 1200) / 2)
    position_y = int((screen_height - 900) / 2)
    report_window.geometry(f"1200x900+{position_x}+{position_y}")

    # สร้างตารางสำหรับชาวไทย
    thai_frame = Frame(report_window)
    thai_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    Label(thai_frame, text="ยอดขายชาวไทย", font=("THSarabun", 20)).pack()

    thai_table = ttk.Treeview(thai_frame, columns=("Type", "Count", "Price"), show="headings")
    thai_table.heading("Type", text="ประเภทตั๋ว")
    thai_table.heading("Count", text="จำนวน")
    thai_table.heading("Price", text="ราคา (บาท)")
    thai_table.pack(fill="both", expand=True)

    # เพิ่มข้อมูลในตารางชาวไทยและเรียงตามประเภทตั๋ว
    for t_type in sorted(combined_thai_details.keys()):
        count = combined_thai_details[t_type]
        price = calculate_ticket_price(t_type, count, is_foreign=False)
        thai_table.insert("", "end", values=(t_type, count, f"{price:,.2f}"))

    # เพิ่มแถวสำหรับยอดขายรวมของชาวไทย
    thai_table.insert("", "end", values=("รวมทั้งหมด", total_tickets_thai, f"{total_price_thai:,.2f}"), tags=("total",))
    thai_table.tag_configure("total", background="#e0e0e0")

    # สร้างตารางสำหรับชาวต่างชาติ
    foreign_frame = Frame(report_window)
    foreign_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    Label(foreign_frame, text="ยอดขายชาวต่างชาติ", font=("THSarabun", 20)).pack()

    foreign_table = ttk.Treeview(foreign_frame, columns=("Type", "Count", "Price"), show="headings")
    foreign_table.heading("Type", text="ประเภทตั๋ว")
    foreign_table.heading("Count", text="จำนวน")
    foreign_table.heading("Price", text="ราคา (THB)")
    foreign_table.pack(fill="both", expand=True)

    # เพิ่มข้อมูลในตารางชาวต่างชาติและเรียงตามประเภทตั๋ว
    for t_type in sorted(combined_foreign_details.keys()):
        count = combined_foreign_details[t_type]
        price = calculate_ticket_price(t_type, count, is_foreign=True)
        foreign_table.insert("", "end", values=(t_type, count, f"{price:,.2f}"))

    # เพิ่มแถวสำหรับยอดขายรวมของชาวต่างชาติ
    foreign_table.insert("", "end", values=("รวมทั้งหมด", total_tickets_foreign, f"{total_price_foreign:,.2f}"), tags=("total",))
    foreign_table.tag_configure("total", background="#e0e0e0")

    # แสดงยอดขายรวมทั้งหมดในกรอบข้อความ
    total_combined_price = total_price_thai + total_price_foreign
    total_combined_tickets = total_tickets_thai + total_tickets_foreign

    summary_frame = Frame(report_window)
    summary_frame.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)

    # เพิ่มข้อความบอกช่วงเวลาที่เลือก
    period_text = {
        "daily": "รายวัน",
        "monthly": "รายเดือน",
        "yearly": "รายปี"
    }.get(period, "ไม่ทราบช่วงเวลา")

    Label(summary_frame, text=f"ยอดขาย{period_text} สำหรับช่วงเวลา: {date_value}", font=("THSarabun", 15)).pack(anchor="center", pady=5)
    Label(summary_frame, text=f"ยอดขายรวมทั้งหมด: {total_combined_price:,.2f} บาท", font=("THSarabun", 15)).pack(anchor="center", pady=5)
    Label(summary_frame, text=f"ตั๋วที่ขายได้ทั้งหมด: {total_combined_tickets:,} ใบ", font=("THSarabun", 15)).pack(anchor="center", pady=5)
    Label(summary_frame, text=f"ยอดขายชาวไทย: {total_price_thai:,.2f} บาท", font=("THSarabun", 15)).pack(anchor="center", pady=5)
    Label(summary_frame, text=f"ยอดขายชาวต่างชาติ: {total_price_foreign:,.2f} บาท", font=("THSarabun", 15)).pack(anchor="center", pady=5)
    
def open_sales_window():
    sales_window = ctk.CTkToplevel()
    sales_window.title("Sales")
    sales_window.geometry("1000x700")

    screen_width = sales_window.winfo_screenwidth()
    screen_height = sales_window.winfo_screenheight()
    position_x = int((screen_width - 1000) / 2)
    position_y = int((screen_height - 700) / 2)
    sales_window.geometry(f"1000x700+{position_x}+{position_y}")

    sales_window.attributes("-topmost", True)  
    sales_window.lift()  
    sales_window.focus_force() 
    sales_window.after(100, lambda: sales_window.lift())  
    sales_window.after(100, lambda: sales_window.focus_force())  

    image_path = "profile20.png"
    try:
        image = Image.open(image_path)
        resized_image = image.resize((900, 650), Image.LANCZOS) 
        ct_image = CTkImage(resized_image, size=(900, 650))  

        # สร้าง Label สำหรับแสดงรูปภาพ
        image_label = CTkLabel(sales_window, image=ct_image, text="")  
        image_label.image = ct_image 
        image_label.place(relx=0.5, rely=0.5, anchor="center") 
    except Exception as e:
        error_label = CTkLabel(sales_window, text=f"Unable to load image: {e}", text_color="red")
        error_label.place(relx=0.5, rely=0.2, anchor="center")  

    back_button = ctk.CTkButton(
        master=sales_window,
        text="Back",
        command=lambda: [sales_window.destroy(), open_admin_window()],
        width=150,
        fg_color="#aed7ac",
        text_color="#056a00"
    )
    back_button.place(relx=0.5, rely=0.9, anchor="center")

    # ส่วนของการแสดงรายงาน
    period_var = StringVar(sales_window)
    period_var.set("daily")
    period_menu = OptionMenu(sales_window, period_var, "daily", "monthly", "yearly")
    period_menu.place(relx=0.5, rely=0.25, anchor="center")

    date_var = StringVar(sales_window)
    date_entry = DateEntry(sales_window, textvariable=date_var, date_pattern='mm/dd/yy')
    date_entry.place(relx=0.5, rely=0.30, anchor="center")

    month_var = StringVar(sales_window)
    month_menu = OptionMenu(sales_window, month_var, *[f"{i:02d}" for i in range(1, 13)])
    month_menu.place_forget()

    year_var = StringVar(sales_window)
    year_menu = OptionMenu(sales_window, year_var, *[str(i) for i in range(2018, 2027)])
    year_menu.place_forget()

    customer_type_var = StringVar(sales_window)
    customer_type_var.set("Both")
    customer_type_menu = OptionMenu(sales_window, customer_type_var, "Both", "Thai", "Foreign")
    customer_type_menu.place(relx=0.5, rely=0.34, anchor="center")

    def update_date_entry(*args):
        period = period_var.get()
        if period == "daily":
            date_entry.place(relx=0.5, rely=0.34, anchor="center")
            month_menu.place_forget()
            year_menu.place_forget()
        elif period == "monthly":
            date_entry.place_forget()
            month_menu.place(relx=0.45, rely=0.34, anchor="center")
            year_menu.place(relx=0.55, rely=0.34, anchor="center")
        elif period == "yearly":
            date_entry.place_forget()
            month_menu.place_forget()
            year_menu.place(relx=0.5, rely=0.3, anchor="center")

    period_var.trace_add("write", update_date_entry)

    def show_report():
        period = period_var.get()

        if period == "daily":
            date_value = date_var.get()  # ใช้รูปแบบเต็ม MM/DD/YY
        elif period == "monthly":
            month = month_var.get()
            year = year_var.get()[-2:]  # ใช้เฉพาะ YY
            date_value = f"{month}/{year}"  # ใช้ MM/YY
        elif period == "yearly":
            date_value = year_var.get()[-2:]  # ใช้เฉพาะ YY

        customer_type = customer_type_var.get()
        display_report(period, date_value, customer_type)

    show_button = Button(sales_window, text="Show Report", command=show_report)
    show_button.place(relx=0.5, rely=0.38, anchor="center")

# เรียกใช้ฟังก์ชันเปิดหน้าต่างสรุปยอดขาย
#open_sales_window()


# --------------ฟังก์ชันเปิดหน้าต่าง Report-------------

def update_ticket_data(ticket_type, count, table_name):
    # เชื่อมต่อกับฐานข้อมูล
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # อัพเดตข้อมูลตั๋วในฐานข้อมูล
    query = f"UPDATE {table_name} SET count = ? WHERE ticket_type = ?"
    cursor.execute(query, (count, ticket_type))
    
    # บันทึกการเปลี่ยนแปลง
    conn.commit()
    conn.close()


# -------------------ฟังก์ชันเปิดหน้าต่าง Report-----------------

def open_report_window():
    report_window = ctk.CTkToplevel()
    report_window.title("Report")
    report_window.geometry("1000x700")

    screen_width = report_window.winfo_screenwidth()
    screen_height = report_window.winfo_screenheight()
    position_x = int((screen_width - 1000) / 2)
    position_y = int((screen_height - 700) / 2)
    report_window.geometry(f"1000x700+{position_x}+{position_y}")

    report_window.attributes("-topmost", True)  
    report_window.lift()  
    report_window.focus_force() 
    report_window.after(100, lambda: report_window.lift())  
    report_window.after(100, lambda: report_window.focus_force())  

    image_path = "profile19.png"
    try:
        image = Image.open(image_path)
        resized_image = image.resize((900, 650), Image.LANCZOS) 
        ct_image = CTkImage(resized_image, size=(900, 650))  

        # สร้าง Label สำหรับแสดงรูปภาพ
        image_label = CTkLabel(report_window, image=ct_image, text="")  
        image_label.image = ct_image 
        image_label.pack(pady=10)  
    except Exception as e:
        error_label = CTkLabel(report_window, text=f"Unable to load image: {e}", text_color="red")
        error_label.pack(pady=20)

    back_button = ctk.CTkButton(
        master=report_window,
        text="Back",
        command=lambda: [report_window.destroy(), open_admin_window()], 
        width=150,
        fg_color="#aed7ac", 
        text_color="#056a00"  
    )
    back_button.place(relx=0.5, rely=0.83, anchor="center")

    # ดึงข้อมูลยอดขายจากฐานข้อมูล
    thai_ticket_counts = get_ticket_counts("dataticket_thai")
    foreign_ticket_counts = get_ticket_counts("dataticket_foreign")

    # label แสดงข้อมูลของชาวไทย ใช้ f-string เพื่อดึงค่าจาก thai_ticket_counts
    thai_report_text = f"""
ยอดขายชาวไทย


-  -  - สวนสัตว์ -  -  -

เด็กเล็ก  {thai_ticket_counts['สวนสัตว์']['เด็กเล็ก']}  ใบ
เด็กโต  {thai_ticket_counts['สวนสัตว์']['เด็กโต']}  ใบ
ผู้ใหญ่  {thai_ticket_counts['สวนสัตว์']['ผู้ใหญ่']}  ใบ
ผู้สูงอายุ  {thai_ticket_counts['สวนสัตว์']['ผู้สูงอายุ']}  ใบ


-  -  - อควาเรียม -  -  -

เด็ก  {thai_ticket_counts['อควาเรียม']['เด็ก']}  ใบ
ผู้ใหญ่  {thai_ticket_counts['อควาเรียม']['ผู้ใหญ่']}  ใบ


-  -  -  การแสดงสัตว์ -  -  -

เด็ก  {thai_ticket_counts['การแสดงสัตว์']['เด็ก']}  ใบ
ผู้ใหญ่  {thai_ticket_counts['การแสดงสัตว์']['ผู้ใหญ่']}  ใบ
"""
    report_label_thai = ctk.CTkLabel(
        report_window, 
        text=thai_report_text, 
        justify="left", 
        font=("TH Sarabun", 15), 
        bg_color= '#f2f2f2', 
        text_color="#054e2d"  
    )
    report_label_thai.place(relx=0.3, rely=0.2)

    # label แสดงข้อมูลของชาวต่างชาติ
    foreign_report_text = f"""
Foreign Sales


-  -  - Zoo Tickets -  -  -

Child   {foreign_ticket_counts['สวนสัตว์']['เด็กเล็ก'] + foreign_ticket_counts['สวนสัตว์']['เด็กโต']} 
Teenager  {foreign_ticket_counts['สวนสัตว์']['เด็กโต']} 
Adult   {foreign_ticket_counts['สวนสัตว์']['ผู้ใหญ่']} 
Senior Citizen  {foreign_ticket_counts['สวนสัตว์']['ผู้สูงอายุ']} 


-  -  - Aquarium Tickets -  -  -

Child  {foreign_ticket_counts['อควาเรียม']['เด็ก']} 
Adult  {foreign_ticket_counts['อควาเรียม']['ผู้ใหญ่']} 


-  -  - Animal Show -  -  -

Child  {foreign_ticket_counts['การแสดงสัตว์']['เด็ก']} 
Adult  {foreign_ticket_counts['การแสดงสัตว์']['ผู้ใหญ่']} 
"""
    report_label_foreign = ctk.CTkLabel(
        report_window, 
        text=foreign_report_text, 
        justify="left", 
        font=("TH Sarabun", 15), 
        bg_color= '#f2f2f2', 
        text_color="#054e2d" 
    )
    report_label_foreign.place(relx=0.6, rely=0.2)
  
# ฟังก์ชันดึงข้อมูลยอดขายจากฐานข้อมูล
def get_ticket_counts(table_name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # ดึงข้อมูลทั้งหมดจากตาราง
    cursor.execute(f"SELECT ticket_details FROM {table_name}")
    all_ticket_details = cursor.fetchall()

    ticket_counts = {
        "สวนสัตว์": {"เด็กเล็ก": 0, "เด็กโต": 0, "ผู้ใหญ่": 0, "ผู้สูงอายุ": 0},
        "อควาเรียม": {"เด็ก": 0, "ผู้ใหญ่": 0},
        "การแสดงสัตว์": {"เด็ก": 0, "ผู้ใหญ่": 0}
    }

    # จับคู่ชื่อประเภทตั๋ว
    ticket_mapping = {
        "สวนสัตว์": {
            "เด็กเล็ก": ["ตั๋วเข้าชมสวนสัตว์ (เด็กเล็ก)", "Zoo Ticket (Child)"],
            "เด็กโต": ["ตั๋วเข้าชมสวนสัตว์ (เด็กโต)", "Zoo Ticket (Toddler)"],
            "ผู้ใหญ่": ["ตั๋วเข้าชมสวนสัตว์ (ผู้ใหญ่)", "Zoo Ticket (Adult)"],
            "ผู้สูงอายุ": ["ตั๋วเข้าชมสวนสัตว์ (ผู้สูงอายุ)", "Zoo Ticket (Senior)"]
        },
        "อควาเรียม": {
            "เด็ก": ["ตั๋วเข้าชมอควาเรียม (เด็ก)", "Aquarium Ticket (Child)"],
            "ผู้ใหญ่": ["ตั๋วเข้าชมอควาเรียม (ผู้ใหญ่)", "Aquarium Ticket (Adult)"]
        },
        "การแสดงสัตว์": {
            "เด็ก": ["ตั๋วเข้าชมการแสดงสัตว์ (เด็ก)", "Animal Show Ticket (Child)"],
            "ผู้ใหญ่": ["ตั๋วเข้าชมการแสดงสัตว์ (ผู้ใหญ่)", "Animal Show Ticket (Adult)"]
        }
    }

    for row in all_ticket_details:
        try:
            # แปลงข้อมูล string เป็น dictionary
            ticket_summary = ast.literal_eval(row[0]) 
            print(f"Parsed data for {table_name}: {ticket_summary}")  

            # วนลูปข้อมูลใน dictionary
            for ticket_type, count in ticket_summary.items():
                print(f"Ticket Type: {ticket_type} | Count: {count}")  

                # ตรวจสอบและจับคู่ประเภทตั๋ว
                for category, types in ticket_mapping.items():
                    for sub_category, names in types.items():
                        if any(name in ticket_type for name in names):
                            ticket_counts[category][sub_category] += count
                            break  

        except Exception as e:
            print(f"Error parsing ticket details for {table_name}: {e}")

    conn.close()
    print("Final ticket counts:", ticket_counts)  # ตรวจสอบผลลัพธ์สุดท้าย
    return ticket_counts



# ****************ฟังก์ชันเปิดหน้าต่าง About Us***************
def open_about_window():

    about_window = ctk.CTkToplevel()  
    about_window.title("About Us")  
    about_window.geometry("1000x700")  

    screen_width =about_window.winfo_screenwidth()
    screen_height = about_window.winfo_screenheight()
    position_x = int((screen_width - 1000) / 2)
    position_y = int((screen_height - 700) / 2)
    about_window.geometry(f"1000x700+{position_x}+{position_y}")

    about_window.attributes('-topmost', True)
    about_window.focus_force()  

    image_path = "profile14.png"
    try:
        image = Image.open(image_path)
        resized_image = image.resize((900, 650), Image.LANCZOS) 
        ct_image = CTkImage(resized_image, size=(900, 650))  

        image_label = ctk.CTkLabel(about_window, image=ct_image, text="")  
        image_label.image = ct_image  
        image_label.pack(pady=10)  
    except Exception as e:
        error_label = ctk.CTkLabel(about_window, text=f"Unable to load image: {e}", text_color="red")
        error_label.pack(pady=20)

    # ฟังก์ชันปิดหน้าต่าง About
    def close_about_window():
        about_window.destroy()

    back_button = ctk.CTkButton(about_window, text="กลับ", command=close_about_window, fg_color="#a8d9e0",text_color="#0f5785")
    back_button.place(relx=0.1,rely=0.1)  

# ****************ปุ่ม Developer (ใช้รูปภาพเป็นปุ่ม)***************
icon_image = Image.open("icon6.png")
icon_image = icon_image.resize((50, 50))  
icon_image = ImageTk.PhotoImage(icon_image)

developer_button = ctk.CTkButton(
    master=frame_1,
    image=icon_image,  
    command=open_about_window,
    fg_color="transparent",  
    width=50,
    height=50,  
    text=""  
)
developer_button.place(relx=0.06, rely=0.2, anchor="center") 

developer_label = ctk.CTkLabel(
    master=frame_1,
    text="About Us",  
    font=("TH Sarabun", 16),  
)
developer_label.place(relx=0.10, rely=0.2, anchor="w")  


# เชื่อมต่อกับฐานข้อมูล
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# สร้างตารางผู้ใช้
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL
)
''')
conn.commit()

# เพิ่มคอลัมน์ email
try:
    cursor.execute("ALTER TABLE users ADD COLUMN email TEXT")
except sqlite3.OperationalError:
    pass  


# ****************ฟังก์ชันเปิดหน้าต่างถัดไป***************
def open_next_window():
    next_window = customtkinter.CTkToplevel()  
    next_window.title("Welcome")  
    next_window.geometry("1000x700")  
    
    screen_width = next_window.winfo_screenwidth()
    screen_height = next_window.winfo_screenheight()
    position_x = int((screen_width - 1000) / 2)
    position_y = int((screen_height - 700) / 2)

    next_window.geometry(f"1000x700+{position_x}+{position_y}")
    next_window.attributes('-topmost', True)
    next_window.focus_force()  

    image_path = "profile2.png"
    image = Image.open(image_path)
    resized_image = image.resize((900, 650), Image.LANCZOS)  
    ct_image = CTkImage(resized_image, size=(900, 650))  
    image_label = customtkinter.CTkLabel(next_window, image=ct_image, text="")  
    image_label.image = ct_image  
    image_label.pack(pady=10)  

    # ปุ่มสำหรับซื้อบัตร
    ticket_button = customtkinter.CTkButton(
        master=next_window,
        text="ซื้อตั๋ว/Purchase Ticket",
        command=lambda : (next_window.destroy(),open_buyers_type_window()),  
        width=200,
        fg_color="#6A9682",       
        text_color="white",      
        font=("Georgia", 14)
    )
    ticket_button.place(relx=0.5, rely=0.8, anchor="center")

    # ปุ่ม Extra Tickets
    extra_tickets_button = customtkinter.CTkButton(
        master=next_window,
        text="Extra Tickets",
        command=lambda : (next_window.destroy(),open_extra_tickets_window()), 
        fg_color="#8dbc73",  
        hover_color="#1C86EE",  
        text_color="white",
        font=("Georgia", 14)
    )
    extra_tickets_button.place(relx=0.8, rely=0.82, anchor="center")

    # ปุ่มย้อนกลับ
    back_button = customtkinter.CTkButton(
        master=next_window,
        text="Back/กลับ",
        command=lambda : (next_window.destroy(),frame_1()),
        fg_color="gray",     
        text_color="white" 
    )
    back_button.place(relx=0.8, rely=0.9, anchor="center")  


########ฟังก์ชันเปิดหน้าต่าง Extra Tickets
def open_extra_tickets_window():
    extra_tickets_window = customtkinter.CTkToplevel()  
    extra_tickets_window.title("Extra Tickets")  
    extra_tickets_window.geometry("1000x700")  
 
    buyers_width = 1000
    buyers_height = 700
    extra_tickets_window.geometry(f"{buyers_width}x{buyers_height}")

    screen_width = extra_tickets_window.winfo_screenwidth()
    screen_height = extra_tickets_window.winfo_screenheight()
    position_x = int((screen_width - buyers_width) / 2)
    position_y = int((screen_height - buyers_height) / 2)

    extra_tickets_window.geometry(f"{buyers_width}x{buyers_height}+{position_x}+{position_y}")
    extra_tickets_window.attributes('-topmost', True)
    extra_tickets_window.after(100, lambda: (extra_tickets_window.lift(), extra_tickets_window.focus_force()))

    image_path = "profile15.png"
    image = Image.open(image_path)
    resized_image = image.resize((900, 650), Image.LANCZOS) 
    ct_image = CTkImage(resized_image, size=(900, 650))  

    image_label = customtkinter.CTkLabel(
        master=extra_tickets_window,
        image=ct_image,
        text=""  
    )
    image_label.image = ct_image  
    image_label.pack(pady=10) 


    # ปุ่มปิดหน้าต่าง
    close_button = customtkinter.CTkButton(
        master=extra_tickets_window,
        text="Close",
        command=lambda : (extra_tickets_window.destroy(),open_next_window()),
        fg_color="White",
        text_color="Black"
    )
    close_button.place(relx=0.17, rely=0.9, anchor="center")  


    # ปุ่มสำหรับซื้อบัตร
    ticket_button = customtkinter.CTkButton(
        master=extra_tickets_window,
        text="ซื้อตั๋ว/Purchase Ticket",
        command=lambda : (extra_tickets_window.destroy(),open_buyers_type_window()), 
        width=200,
        fg_color="#a8d6eb",    
        text_color="#07587e",     
        font=("Georgia", 14)
    )
    ticket_button.place(relx=0.5, rely=0.9, anchor="center") 

    # ปุ่มอื่นๆ
    other_button = ctk.CTkButton(
        master=extra_tickets_window,
        text="อื่นๆ/Other",
        command=lambda : (extra_tickets_window.destroy(),open_showanimal_window()),  
        width=200,
        fg_color="White",  
        text_color="Black",  
        font=("Georgia", 14)
    )
    other_button.place(relx=0.8, rely=0.9, anchor="center")  


# ฟังก์ชันเปิดหน้าต่าง Show Animal
def open_showanimal_window():
    showanimal_window = ctk.CTkToplevel()  
    showanimal_window.title("Show Animal") 
    showanimal_window.geometry("1000x700") 
    showanimal_width = 1000
    showanimal_height = 700
    showanimal_window.geometry(f"{showanimal_width}x{showanimal_height}")

    screen_width = showanimal_window.winfo_screenwidth()
    screen_height = showanimal_window.winfo_screenheight()
    position_x = int((screen_width - showanimal_width) / 2)
    position_y = int((screen_height - showanimal_height) / 2)
    showanimal_window.geometry(f"{showanimal_width}x{showanimal_height}+{position_x}+{position_y}")
    showanimal_window.attributes('-topmost', True)

    showanimal_window.after(100, lambda: (showanimal_window.lift(), showanimal_window.focus_force()))

    image_path = "profile16.png"  
    image = Image.open(image_path)
    resized_image = image.resize((900, 650), Image.LANCZOS)  
    ct_image = CTkImage(resized_image, size=(900, 650))  

    image_label = ctk.CTkLabel(
        master=showanimal_window,
        image=ct_image,
        text="" 
    )
    image_label.image = ct_image  
    image_label.pack(pady=10)  

    # ปุ่มปิดหน้าต่าง
    close_button = ctk.CTkButton(
        master=showanimal_window,
        text="Close",
        command=lambda : (showanimal_window.destroy(),open_extra_tickets_window()),
        fg_color="White",
        text_color="Black"
    )
    close_button.place(relx=0.17, rely=0.9, anchor="center") 

    # ปุ่มสำหรับซื้อบัตร
    ticket_button = customtkinter.CTkButton(
        master=showanimal_window,
        text="ซื้อตั๋ว/Purchase Ticket",
        command=lambda : (showanimal_window.destroy(),open_buyers_type_window()),  
        width=200,
        fg_color="#e6ba91",      
        text_color="#7c3c00",     
        font=("Georgia", 14)
    )
    ticket_button.place(relx=0.5, rely=0.9, anchor="center")  

# เปิดหน้าต่างประเภทผู้ซื้อ
def open_buyers_type_window():
    buyers_window = customtkinter.CTkToplevel()
    buyers_window.geometry("1000x700")
    buyers_window.title("Types Of Buyers")

    buyers_width = 1000
    buyers_height = 700
    buyers_window.geometry(f"{buyers_width}x{buyers_height}")

    screen_width = buyers_window.winfo_screenwidth()
    screen_height = buyers_window.winfo_screenheight()
    position_x = int((screen_width - buyers_width) / 2)
    position_y = int((screen_height - buyers_height) / 2)
    buyers_window.geometry(f"{buyers_width}x{buyers_height}+{position_x}+{position_y}")
    buyers_window.attributes('-topmost', True)
    buyers_window.after(100, lambda: (buyers_window.lift(), buyers_window.focus_force()))

    # โหลดและปรับขนาดรูปภาพ
    image_path = "profile5.png"
    image = Image.open(image_path)
    resized_image = image.resize((900, 650), Image.LANCZOS)  
    ct_image = CTkImage(resized_image, size=(900, 650))  

    image_label = customtkinter.CTkLabel(
        master=buyers_window,
        image=ct_image,
        text=""  
    )
    image_label.image = ct_image 
    image_label.pack(pady=10) 

    # ปุ่มสำหรับชาวไทย
    thai_button = customtkinter.CTkButton(
        master=buyers_window,
        text="ชาวไทย / Thai",
        command=lambda: (buyers_window.destroy(), open_ticket_window("Thai")),
        width=200,
        fg_color="#6A9682",
        text_color="white",
        font=("Georgia", 14)
    )
    thai_button.place(relx=0.5, rely=0.45, anchor="center")

    # ปุ่มสำหรับชาวต่างชาติ
    foreign_button = customtkinter.CTkButton(
        master=buyers_window,
        text="ชาวต่างชาติ / Foreign",
        command=lambda: (buyers_window.destroy(), open_foreign_window("Foreign")),
        width=200,
        fg_color="#6A9682",
        text_color="white",
        font=("Georgia", 14)
    )
    foreign_button.place(relx=0.5, rely=0.55, anchor="center")

    back_button = customtkinter.CTkButton(
        master= buyers_window,
        text="Back/กลับ",
        command= lambda : (buyers_window.destroy(),open_next_window()),
        fg_color="gray",     
        text_color="white"    
    )
    back_button.place(relx=0.5, rely=0.7, anchor="center")  

#*****--------------------เปิดหน้าซื้อบัตรคนไทยจ้------------------*****
def open_ticket_window(buyer_type):
    ticket_window = customtkinter.CTkToplevel()
    ticket_window.geometry("1000x700")
    ticket_window.title("การซื้อตั๋ว")

    # กำหนดขนาดหน้าต่าง
    window_width = 1000
    window_height = 700
    ticket_window.geometry(f"{window_width}x{window_height}")

    # คำนวณตำแหน่งเพื่อให้หน้าต่างอยู่ตรงกลาง
    screen_width = ticket_window.winfo_screenwidth()
    screen_height = ticket_window.winfo_screenheight()
    position_x = int((screen_width - window_width) / 2)
    position_y = int((screen_height - window_height) / 2)
    ticket_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
    ticket_window.attributes('-topmost', True)

    # โหลดและปรับขนาดรูปภาพ
    image_path = "profile4.png"
    image = Image.open(image_path)
    resized_image = image.resize((900, 650), Image.LANCZOS) 
    ct_image = CTkImage(resized_image, size=(900, 650))  

    # สร้าง Label สำหรับแสดงรูปภาพ
    image_label = customtkinter.CTkLabel(
        master=ticket_window, 
        image=ct_image,        
        text=""               
    )
    image_label.image = ct_image 
    image_label.pack(pady=10)    

    # เพิ่มปฏิทินสำหรับเลือกวันที่
    calendar_label = customtkinter.CTkLabel(
        master=ticket_window,
        text="เลือกวันที่เข้าชม",
        font=("Georgia", 16),
        text_color="black"
    )
    calendar_label.place(relx=0.68, rely=0.62, anchor="center")

    calendar = Calendar(
        master=ticket_window,
        selectmode="day",
        year=2025,
        month=1,
        day=31
    )
    calendar.place(relx=0.68, rely=0.62, anchor="center")

    # ฟังก์ชันที่แสดงวันที่ที่เลือกจากปฏิทิน
    def display_selected_date(event, label):
        selected_date = calendar.get_date()  # ดึงวันที่ที่เลือก
        label.configure(text=f"คุณได้เลือกเข้าชมวันที่ {selected_date}")

    # กรอบข้อความแสดงวันที่ที่เลือก
    selected_date_label = customtkinter.CTkLabel(
        master=ticket_window,
        text="คุณได้เลือกเข้าชมวันที่",
        font=("Prompt", 18),
        text_color="#17531b",
        bg_color="#edffed"
    )
    selected_date_label.place(relx=0.68, rely=0.78, anchor="center")

    # เชื่อมต่อการเลือกวันที่จากปฏิทินกับฟังก์ชัน
    calendar.bind("<<CalendarSelected>>", lambda event, label=selected_date_label: display_selected_date(event, label))

    # คำนวณราคารวม
    def calculate_total(zoo_entries, aquarium_entries, show_entries):
        total_zoo = sum(int(entry.get()) * price for entry, price in zoo_entries)
        total_aquarium = sum(int(entry.get()) * price for entry, price in aquarium_entries)
        total_show = sum(int(entry.get()) * price for entry, price in show_entries)
        
        total_price = total_zoo + total_aquarium + total_show

        zoo_total_label.configure(text=f"ราคารวม: {total_zoo} บาท",font=("Prompt", 15))
        aquarium_total_label.configure(text=f"ราคารวม: {total_aquarium} บาท",font=("Prompt", 15))
        show_total_label.configure(text=f"ราคารวม: {total_show} บาท",font=("Prompt", 15))
        total_price_label.configure(text=f"ราคารวมทั้งหมด: {total_price} บาท",font=("Prompt", 15))

    # ฟังก์ชันอัปเดตจำนวน
    def update_quantity(entry, amount, entries, zoo_entries, aquarium_entries, show_entries):
        try:
            quantity = int(entry.get()) + amount
            if quantity < 0:
                quantity = 0  # ห้ามจำนวนติดลบ
            entry.delete(0, "end")
            entry.insert(0, str(quantity))
        except ValueError:
            entry.delete(0, "end")
            entry.insert(0, "0")
        calculate_total(zoo_entries, aquarium_entries, show_entries)  # เรียก calculate_total หลังจากอัปเดตจำนวน

    # ฟังก์ชันที่อัปเดตราคาเมื่อกรอกข้อมูล
    def update_price(entry, zoo_entries, aquarium_entries, show_entries):
        try:
            # ตรวจสอบว่าเป็นตัวเลขและถ้าตัวเลขเป็นลบให้ตั้งค่าเป็น 0
            quantity = int(entry.get())
            if quantity < 0:
                quantity = 0  # ป้องกันไม่ให้กรอกจำนวนติดลบ
            entry.delete(0, "end")
            entry.insert(0, str(quantity))  

            # คำนวณราคารวมหลังจากอัปเดตจำนวน
            calculate_total(zoo_entries, aquarium_entries, show_entries)
        except ValueError:
            # ถ้าผู้ใช้กรอกไม่ใช่ตัวเลขให้ตั้งค่าเป็น 0
            entry.delete(0, "end")
            entry.insert(0, "0")

    # สร้างกรอบและรายการตั๋ว
    def create_ticket_frame(master, title, ticket_types, x, y,frame_color ):
        frame = customtkinter.CTkFrame(master=master, fg_color=frame_color,width=350, height=300)
        frame.place(x=x, y=y)  
        
        title_label = customtkinter.CTkLabel(master=frame, text=title, font=("Helvetica", 16), text_color="black")
        title_label.pack(pady=10)

        entries = []

        for ticket_type, price in ticket_types:
            ticket_frame = customtkinter.CTkFrame(master=frame, fg_color="#cae9c9")
            ticket_frame.pack(fill="x", pady=5)

            ticket_label = customtkinter.CTkLabel(
                master=ticket_frame,
                text=f"{ticket_type}: {price} บาท",
                font=("Helvetica", 14),
                text_color="black"
            )
            ticket_label.pack(side="left", padx=10)

            quantity_entry = customtkinter.CTkEntry(master=ticket_frame, width=35)
            quantity_entry.insert(0, "0")
            quantity_entry.pack(side="left", padx=10)

            # เพิ่มปุ่มเพื่อเพิ่มและลดจำนวน
            add_button = customtkinter.CTkButton(
                master=ticket_frame, text="+", width=25,
                fg_color="#84ae62",  
                command=lambda entry=quantity_entry: update_quantity(entry, 1, entries, zoo_entries, aquarium_entries, show_entries)
            )
            add_button.pack(side="left", padx=5)

            subtract_button = customtkinter.CTkButton(
                master=ticket_frame, text="-", width=25,
                fg_color="#eb9f7c", 
                command=lambda entry=quantity_entry: update_quantity(entry, -1, entries, zoo_entries, aquarium_entries, show_entries)
            )
            subtract_button.pack(side="left", padx=5)

            quantity_entry.bind("<KeyRelease>", lambda event, entry=quantity_entry: update_price(entry, entries, zoo_entries, aquarium_entries, show_entries))

            entries.append((quantity_entry, price))

        total_label = customtkinter.CTkLabel(master=frame, text="ราคารวม: 0 บาท", font=("Helvetica", 16))
        total_label.pack(pady=10)

        return entries, total_label

    # เพิ่มประเภทตั๋วและกรอบต่าง ๆ 
    zoo_ticket_types = [
        ("ซื้อตั๋วชมสวนสัตว์ (เด็ก)", 29),
        ("ซื้อตั๋วชมสวนสัตว์ (เด็กโต)", 59),
        ("ซื้อตั๋วชมสวนสัตว์ (ผู้ใหญ่)", 139),
        ("ซื้อตั๋วชมสวนสัตว์ (ผู้สูงอายุ)", 0)
    ]
    aquarium_ticket_types = [
        ("ซื้อตั๋วเข้าชมอควาเรียม (เด็ก)", 40),
        ("ซื้อตั๋วเข้าชมอควาเรียม (ผู้ใหญ่)", 80)
    ]
    show_ticket_types = [
        ("ซื้อตั๋วชมการแสดงสัตว์ (เด็ก)", 30),
        ("ซื้อตั๋วชมการแสดงสัตว์ (ผู้ใหญ่)", 50)
    ]


    # กำหนดตำแหน่งกรอบแต่ละประเภท
    zoo_entries, zoo_total_label = create_ticket_frame(ticket_window, "ตั๋วเข้าชมสวนสัตว์", zoo_ticket_types, 70, 350, "#cae9c9")  
    aquarium_entries, aquarium_total_label = create_ticket_frame(ticket_window, "ตั๋วเข้าชมอควาเรียม", aquarium_ticket_types, 70, 115, "#cae9c9")  
    show_entries, show_total_label = create_ticket_frame(ticket_window, "ตั๋วเข้าชมการแสดงสัตว์", show_ticket_types, 500, 115, "#cae9c9")  

    # lebel แสดงราคารวมทั้งหมด
    total_price_label = customtkinter.CTkLabel(master=ticket_window, text="ราคารวมทั้งหมด: 0 บาท", font=("Prompt", 18),bg_color="#edffed",text_color="#275700")
    total_price_label.place(relx=0.68, rely=0.85, anchor="center")

    # คำนวณราคาเริ่มต้น
    calculate_total(zoo_entries, aquarium_entries, show_entries)

    # ปุ่มย้อนกลับ
    back_button = customtkinter.CTkButton(
        master=ticket_window,
        text="Back/กลับ",
        command=lambda : (ticket_window.destroy(),open_buyers_type_window()),        
        fg_color="#e2e2e2",     
        text_color="Black"  
    )
    back_button.place(relx=0.15, rely=0.1, anchor="center")  

    # ปุ่มยืนยันคำสั่งซื้อ
    confirm_button = customtkinter.CTkButton(
        master=ticket_window,
        text="ยืนยันคำสั่งซื้อ",
        command=lambda: (
        confirm_order(calendar.get_date(), zoo_entries, aquarium_entries, show_entries), 
        ticket_window.destroy()
        ),  
        fg_color="#6AA573",
        text_color="white",
        width=100,
        height=40
    )
    confirm_button.place(relx=0.87, rely=0.85, anchor="center")

    # ฟังก์ชันยืนยันคำสั่งซื้อ
def confirm_order(selected_date, zoo_entries, aquarium_entries, show_entries):
    ticket_summary = {}
    total_price = 0

    # วนลูปเพื่อคำนวณจำนวนตั๋วและราคารวม
    for entry, price_per_ticket in zoo_entries + aquarium_entries + show_entries:
        quantity = int(entry.get()) if entry.get() else 0  
        total_price += quantity * price_per_ticket 
        ticket_summary[entry.get()] = quantity  

    # เรียกใช้งานฟังก์ชันเพื่อเปิดหน้าต่างยืนยัน
    open_thai_confirm_window(selected_date, ticket_summary, total_price)

#------------------------------------------------------------------------------------------------------------------------------------
# ฟังก์ชันสำหรับการเปิดหน้าต่างซื้อบัตร (ชาวต่างชาติ)
def open_foreign_window(buyer_type):
    foreign_window = customtkinter.CTkToplevel()
    foreign_window.geometry("1000x700")
    foreign_window.title("Foreign Ticket")

    # กำหนดขนาดหน้าต่าง
    window_width = 1000
    window_height = 700
    foreign_window.geometry(f"{window_width}x{window_height}")

    # คำนวณตำแหน่งเพื่อให้หน้าต่างอยู่ตรงกลาง
    screen_width = foreign_window.winfo_screenwidth()
    screen_height = foreign_window.winfo_screenheight()
    position_x = int((screen_width - window_width) / 2)
    position_y = int((screen_height - window_height) / 2)

    # ตั้งค่าตำแหน่งและขนาดของหน้าต่าง
    foreign_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    # ทำให้หน้าต่างอยู่ด้านบนสุด
    foreign_window.attributes('-topmost', True)

    # โหลดและปรับขนาดรูปภาพ
    image_path = "profile6.png"
    image = Image.open(image_path)
    resized_image = image.resize((900, 650), Image.LANCZOS)  
    ct_image = CTkImage(resized_image, size=(900, 650))  

    # สร้าง Label สำหรับแสดงรูปภาพ
    image_label = customtkinter.CTkLabel(
        master=foreign_window, 
        image=ct_image,        
        text=""             
    )
    image_label.image = ct_image 
    image_label.pack(pady=10)     

    # เพิ่มปฏิทินสำหรับเลือกวันที่
    calendar_label = customtkinter.CTkLabel(
        master=foreign_window,
        text="Select Your Visit Date",
        font=("Georgia", 16),
        text_color="black"
    )
    calendar_label.place(relx=0.68, rely=0.62, anchor="center")

    calendar = Calendar(
        master=foreign_window,
        selectmode="day",
        year=2025,
        month=1,
        day=26
    )
    calendar.place(relx=0.68, rely=0.62, anchor="center")

    # ฟังก์ชันที่แสดงวันที่ที่เลือกจากปฏิทิน
    def display_selected_date(event, label):
        selected_date = calendar.get_date()  # ดึงวันที่ที่เลือก
        label.configure(text=f"You have selected to visit on :{selected_date}")

    # กรอบข้อความแสดงวันที่ที่เลือก
    selected_date_label = customtkinter.CTkLabel(
        master=foreign_window,
        text="You have selected to visit on",
        font=("Prompt", 16),
        text_color="black",
        bg_color="#edffed"

    )
    selected_date_label.place(relx=0.68, rely=0.78, anchor="center")

    # เชื่อมต่อการเลือกวันที่จากปฏิทินกับฟังก์ชัน
    calendar.bind("<<CalendarSelected>>", lambda event, label=selected_date_label: display_selected_date(event, label))

        # ฟังก์ชันคำนวณราคารวม
    def calculate_total(zoo_entries, aquarium_entries, show_entries):
        total_zoo = sum(int(entry.get()) * price for entry, price in zoo_entries)
        total_aquarium = sum(int(entry.get()) * price for entry, price in aquarium_entries)
        total_show = sum(int(entry.get()) * price for entry, price in show_entries)
        
        total_price = total_zoo + total_aquarium + total_show

        zoo_total_label.configure(text=f"Total: {total_zoo} THB",font=("Prompt", 15))
        aquarium_total_label.configure(text=f"Total: {total_aquarium} THB",font=("Prompt", 15))
        show_total_label.configure(text=f"Total: {total_show} THB",font=("Prompt", 15))
        total_price_label.configure(text=f"Total Price: {total_price} THB",font=("Prompt", 15))

    # ฟังก์ชันอัปเดตจำนวน
    def update_quantity(entry, amount, entries, zoo_entries, aquarium_entries, show_entries):
        try:
            quantity = int(entry.get()) + amount
            if quantity < 0:
                quantity = 0  # ห้ามจำนวนติดลบ
            entry.delete(0, "end")
            entry.insert(0, str(quantity))
        except ValueError:
            entry.delete(0, "end")
            entry.insert(0, "0")
        calculate_total(zoo_entries, aquarium_entries, show_entries)  # เรียก calculate_total หลังจากอัปเดตจำนวน

    # ฟังก์ชันที่อัปเดตราคาเมื่อกรอกข้อมูล
    def update_price(entry, entries, zoo_entries, aquarium_entries, show_entries):
        try:
            # ตรวจสอบว่าเป็นตัวเลขและถ้าตัวเลขเป็นลบให้ตั้งค่าเป็น 0
            quantity = int(entry.get())
            if quantity < 0:
                quantity = 0  # ป้องกันไม่ให้กรอกจำนวนติดลบ
            entry.delete(0, "end")
            entry.insert(0, str(quantity))  

            # คำนวณราคารวมหลังจากอัปเดตจำนวน
            calculate_total(zoo_entries, aquarium_entries, show_entries)
        except ValueError:
            # ถ้าผู้ใช้กรอกไม่ใช่ตัวเลขให้ตั้งค่าเป็น 0
            entry.delete(0, "end")
            entry.insert(0, "0")

    # สร้างกรอบและรายการตั๋ว
    def create_ticket_frame(master, title, ticket_types, x, y,frame_color ):
        frame = customtkinter.CTkFrame(master=master, fg_color=frame_color,width=350, height=300)
        frame.place(x=x, y=y) 
        
        title_label = customtkinter.CTkLabel(master=frame, text=title, font=("Helvetica", 16), text_color="black")
        title_label.pack(pady=10)

        entries = []

        for ticket_type, price in ticket_types:
            ticket_frame = customtkinter.CTkFrame(master=frame, fg_color="#cae9c9")
            ticket_frame.pack(fill="x", pady=5)

            ticket_label = customtkinter.CTkLabel(
                master=ticket_frame,
                text=f"{ticket_type}: {price} THB",
                font=("Helvetica", 14),
                text_color="black"
            )
            ticket_label.pack(side="left", padx=10)

            quantity_entry = customtkinter.CTkEntry(master=ticket_frame, width=35)
            quantity_entry.insert(0, "0")
            quantity_entry.pack(side="left", padx=10)

            # เพิ่มปุ่มเพื่อเพิ่มและลดจำนวน
            add_button = customtkinter.CTkButton(
                master=ticket_frame, text="+", width=25,
                fg_color="#84ae62",  
                command=lambda entry=quantity_entry: update_quantity(entry, 1, entries, zoo_entries, aquarium_entries, show_entries)
            )
            add_button.pack(side="left", padx=5)

            subtract_button = customtkinter.CTkButton(
                master=ticket_frame, text="-", width=25,
                fg_color="#eb9f7c", 
                command=lambda entry=quantity_entry: update_quantity(entry, -1, entries, zoo_entries, aquarium_entries, show_entries)
            )
            subtract_button.pack(side="left", padx=5)

            quantity_entry.bind("<KeyRelease>", lambda event, entry=quantity_entry: update_price(entry, entries, zoo_entries, aquarium_entries, show_entries))

            entries.append((quantity_entry, price))

        total_label = customtkinter.CTkLabel(master=frame, text="Total: 0 THB", font=("Helvetica", 14))
        total_label.pack(pady=10)

        return entries, total_label

        # เพิ่มประเภทตั๋วและกรอบต่าง ๆ 
    zoo_ticket_types = [
        ("Zoo Ticket (Child)", 89),
        ("Zoo Ticket (Teenager)", 159),
        ("Zoo Ticket (Adult)", 249),
        ("Zoo Ticket (Senior)", 0)
    ]
    aquarium_ticket_types = [
        ("Aquarium Ticket (Child)", 100),
        ("Aquarium Ticket (Adult)", 140)
    ]
    show_ticket_types = [
        ("Animal Show Ticket (Child)", 50),
        ("Animal Show Ticket (Adult)", 100)
    ]

    # กำหนดตำแหน่งกรอบแต่ละประเภท
    zoo_entries, zoo_total_label = create_ticket_frame(foreign_window, "Zoo Ticket", zoo_ticket_types, 70, 350, "#cae9c9")  
    aquarium_entries, aquarium_total_label = create_ticket_frame(foreign_window, "Aquarium Ticket", aquarium_ticket_types, 70, 115, "#cae9c9")  
    show_entries, show_total_label = create_ticket_frame(foreign_window, "Animal Show Animal", show_ticket_types, 500, 115, "#cae9c9")  

    # ป้ายแสดงราคารวมทั้งหมด
    total_price_label = customtkinter.CTkLabel(master=foreign_window, text="Total: 0 THB", font=("Prompt", 16),bg_color="#edffed")
    total_price_label.place(relx=0.68, rely=0.85, anchor="center")

    # คำนวณราคาเริ่มต้น
    calculate_total(zoo_entries, aquarium_entries, show_entries)

    # ปุ่มย้อนกลับ
    back_button = customtkinter.CTkButton(
        master=foreign_window,
        text="Back/กลับ",
        command=lambda : (foreign_window.destroy(),open_buyers_type_window()), 
        fg_color="#e2e2e2",     
        text_color="Black"    
    )
    back_button.place(relx=0.15, rely=0.1, anchor="center") 

    # สร้างปุ่ม "ยืนยันคำสั่งซื้อ"
    approve_button = customtkinter.CTkButton(
        master=foreign_window,
        text="Confirm Order",
        command=lambda: (
        approve_order(calendar.get_date(), zoo_entries, aquarium_entries, show_entries), # ส่งวันที่ที่เลือกไปพร้อมกับ quantity_entries
        foreign_window.destroy()
        ),
        fg_color="#6AA573",
        text_color="white",
        width=100,
        height=40
    )
    approve_button.place(relx=0.85, rely=0.85, anchor="center")

# ฟังก์ชันยืนยันคำสั่งซื้อ
def approve_order(selected_date, zoo_entries, aquarium_entries, show_entries):
    ticket_summary = {}
    total_price = 0

    # วนลูปเพื่อคำนวณจำนวนตั๋วและราคารวม
    for entry, price_per_ticket in zoo_entries + aquarium_entries + show_entries:
        quantity = int(entry.get()) if entry.get() else 0  
        total_price += quantity * price_per_ticket  
        ticket_summary[entry.get()] = quantity  

    # เรียกใช้งานฟังก์ชันเพื่อเปิดหน้าต่างยืนยัน
    open_foreign_confirm_window(selected_date, ticket_summary, total_price)



def attach_file():
    file_path = filedialog.askopenfilename(title="Select File")
    
    if file_path:
        # แสดงข้อความยืนยัน
        messagebox.showinfo("File Selected", f"You have selected: {file_path}")

        # เชื่อมต่อกับฐานข้อมูล
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        try:
            # เพิ่มคอลัมน์ file_path ถ้ายังไม่มีในตาราง
            cursor.execute("ALTER TABLE dataticket_thai ADD COLUMN file_path TEXT")
        except sqlite3.OperationalError:
            pass  # ถ้าคอลัมน์มีอยู่แล้ว ให้ข้ามไป

        try:
            cursor.execute("ALTER TABLE dataticket_foreign ADD COLUMN file_path TEXT")
        except sqlite3.OperationalError:
            pass  # ถ้าคอลัมน์มีอยู่แล้ว ให้ข้ามไป

        # อัปเดตค่าของ file_path ในแต่ละตาราง
        cursor.execute("UPDATE dataticket_thai SET file_path = ? WHERE file_path IS NULL OR file_path = ''", (file_path,))
        cursor.execute("UPDATE dataticket_foreign SET file_path = ? WHERE file_path IS NULL OR file_path = ''", (file_path,))
        
        conn.commit()  
        conn.close() 
        
        messagebox.showinfo("Success", "File path has been saved to both tables.")


    
def submit_data(entries, ticket_summary, total_price):
    print("เริ่มการทำงานของ submit_data") 

    # เชื่อมต่อกับฐานข้อมูล
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        print("เชื่อมต่อกับฐานข้อมูลสำเร็จ") 

        # สร้างตาราง
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                surname TEXT,
                id_card TEXT,
                phone TEXT,
                email TEXT
            )
        ''')
        print("สร้างตารางสำเร็จ")  

        # จัดการข้อมูลที่กรอก
        data = {f"Field {i+1}": entry.get() for i, entry in enumerate(entries)}
        print("ข้อมูลที่กรอก:", data) 

        # ตรวจสอบข้อมูลก่อนบันทึก
        if any(not value for value in data.values()):
            messagebox.showwarning("Warning", "กรุณากรอกข้อมูลให้ครบถ้วน")
            return

        # บันทึกข้อมูลลงในตาราง
        cursor.execute('''INSERT INTO tickets (name, surname, id_card, phone, email) VALUES (?, ?, ?, ?, ?)''', 
                       (data["Field 1"], data["Field 2"], data["Field 3"], data["Field 4"], data["Field 5"]))
        print("บันทึกข้อมูลลงในฐานข้อมูลสำเร็จ")  #

        # บันทึกการเปลี่ยนแปลง
        conn.commit()
        print("ข้อมูลถูกบันทึกเรียบร้อยแล้ว")  
        messagebox.showinfo("Success", "ข้อมูลถูกบันทึกลงในฐานข้อมูลเรียบร้อยแล้ว")
    except Exception as e:
        print(f"Error: {e}")  
        messagebox.showerror("Error", f"เกิดข้อผิดพลาดในการบันทึกข้อมูล: {e}")
    finally:
        conn.close()
        print("ปิดการเชื่อมต่อฐานข้อมูลแล้ว")  

#----------------------------------------------------------------------------------------------------------------------------#
#กดยืนยันไทย********
def confirm_order(selected_date, zoo_entries, aquarium_entries, show_entries):
    ticket_summary = {}
    total_price = 0

    # วนลูปเพื่อคำนวณจำนวนตั๋วและราคารวมจากข้อมูลในช่อง Entry สำหรับสวนสัตว์
    zoo_ticket_types = [
        ("เด็กเล็ก", 29, zoo_entries[0][0]),  
        ("เด็กโต", 59, zoo_entries[1][0]),
        ("ผู้ใหญ่", 139, zoo_entries[2][0]),
        ("ผู้สูงอายุ", 0, zoo_entries[3][0])
    ]
    
    # คำนวณจำนวนและราคารวมสวนสัตว์
    for ticket_type, price_per_ticket, entry in zoo_ticket_types:
        quantity = 0
        entry_value = entry.get()
        if entry_value.isdigit():
            quantity = int(entry_value) 
        if quantity > 0:
            ticket_summary[f"ตั๋วเข้าชมสวนสัตว์ ({ticket_type})"] = quantity
        total_price += quantity * price_per_ticket 

    # วนลูปเพื่อคำนวณจำนวนตั๋วและราคารวมจากข้อมูลในช่อง Entry สำหรับอควาเรียม
    aquarium_ticket_types = [
        ("เด็ก", 40, aquarium_entries[0][0]),  
        ("ผู้ใหญ่", 80, aquarium_entries[1][0])
    ]
    for ticket_type, price_per_ticket, entry in aquarium_ticket_types:
        quantity = 0
        entry_value = entry.get()
        if entry_value.isdigit():
            quantity = int(entry_value)  
        if quantity > 0:
            ticket_summary[f"ตั๋วเข้าชมอควาเรียม ({ticket_type})"] = quantity
        total_price += quantity * price_per_ticket 

    # วนลูปเพื่อคำนวณจำนวนตั๋วและราคารวมจากข้อมูลในช่อง Entry สำหรับการแสดง
    show_ticket_types = [
        ("เด็ก", 30, show_entries[0][0]),  
        ("ผู้ใหญ่", 50, show_entries[1][0])
    ]
    for ticket_type, price_per_ticket, entry in show_ticket_types:
        quantity = 0
        entry_value = entry.get()
        if entry_value.isdigit():
            quantity = int(entry_value)  
        if quantity > 0:
            ticket_summary[f"ตั๋วเข้าชมการแสดงสัตว์ ({ticket_type})"] = quantity
        total_price += quantity * price_per_ticket  

    # เรียกใช้งานฟังก์ชันเพื่อเปิดหน้าต่างยืนยัน
    open_thai_confirm_window(selected_date, ticket_summary, total_price)

#-------------เปิดหน้ายืนยันการสั่งซื้อของชาวไทย--------------
def open_thai_confirm_window(selected_date, ticket_summary, total_price):
    confirm_window = customtkinter.CTkToplevel()
    confirm_window.title("ยืนยันคำสั่งซื้อ")
    window_width = 1000
    window_height = 700
    confirm_window.geometry(f"{window_width}x{window_height}")

    screen_width = confirm_window.winfo_screenwidth()
    screen_height = confirm_window.winfo_screenheight()
    position_x = int((screen_width - window_width) / 2)
    position_y = int((screen_height - window_height) / 2)
    confirm_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    confirm_window.attributes('-topmost', True)
    confirm_window.lift()  
    confirm_window.focus_force()  

    confirm_window.after(100, lambda: confirm_window.lift())

    image_path = "profile7.png"
    image = Image.open(image_path)

    image_margin_width = 15  
    image_margin_height = 15  

    new_width = window_width - (2 * image_margin_width)
    new_height = window_height - (2 * image_margin_height)

    img_width, img_height = image.size
    aspect_ratio = img_width / img_height

    if new_width / new_height > aspect_ratio:
        resized_width = int(new_height * aspect_ratio)
        resized_height = new_height
    else:
        resized_width = new_width
        resized_height = int(new_width / aspect_ratio)

    resized_image = image.resize((resized_width, resized_height), Image.LANCZOS)

    photo = customtkinter.CTkImage(resized_image, size=(resized_width, resized_height))

    image_label = customtkinter.CTkLabel(
        master=confirm_window,
        image=photo,
        text=""  
    )
    image_label.image = photo  
    image_label.place(relx=0.5, rely=0.5, anchor="center")  

    # ข้อความยืนยัน
    confirmation_label = customtkinter.CTkLabel(
        master=confirm_window,
        text=f"คุณได้เลือกเข้าชมในวันที่ {selected_date}",
        bg_color=("#ffc794"),
        text_color=("#b05400"),
        font=("Helvetica", 16)
    )
    confirmation_label.place(relx=0.3, rely=0.68, anchor="center")

    # แสดงรายละเอียดตั๋วจากข้อมูลที่กรอกใน Entry
    summary_y_pos = 0.25
    for ticket_type, quantity in ticket_summary.items():
        ticket_label = customtkinter.CTkLabel(
            master=confirm_window,
            text=f"{ticket_type}: {quantity} ใบ",
            font=("Helvetica", 16),
            text_color="#B75C30",
            bg_color="#FFDAC6"
        )
        ticket_label.place(relx=0.3, rely=summary_y_pos, anchor="center")
        summary_y_pos += 0.05

    # แสดงราคารวมทั้งหมด
    total_label = customtkinter.CTkLabel(
        master=confirm_window,
        text=f"ราคารวมทั้งหมด: {total_price} บาท",
        font=("Helvetica", 16),
        text_color="#8e1300",
        bg_color="#f2aba0"
    )
    total_label.place(relx=0.3, rely=0.77, anchor="center")

    # ปุ่มย้อนกลับ
    back_button = customtkinter.CTkButton(
        master=confirm_window,
        text="Back/กลับ",
        command=lambda : (confirm_window.destroy(),open_ticket_window()),
        fg_color="#f1c6a4",
        text_color="Black"
    )
    back_button.place(relx=0.15, rely=0.1, anchor="center")

    # ปุ่มสำหรับแนบไฟล์
    attach_button = customtkinter.CTkButton(
        master=confirm_window,
        text="แนบหลักฐานการชำระเงิน",
        command=attach_file,  
        fg_color="#A7C2A5",  
        text_color="white",  
        hover_color="#A8C8B9",
        font=("Helvetica", 16)  
        
    )
    attach_button.place(relx=0.75, rely=0.71, anchor="center")


     # สร้างปุ่มหน้าถัดไป
    next_button = customtkinter.CTkButton(
        master=confirm_window,
        text="หน้าถัดไป",
        command=lambda: (open_thai_data_window(selected_date, ticket_summary, total_price),
        confirm_window.destroy()),  # ส่งค่าอาร์กิวเมนต์ 
        fg_color="#C0E0EF",             
        text_color="Black"              
    )
    next_button.place(relx=0.75, rely=0.8, anchor="center")  


#*****************************************#
# เมื่อกดปุ่ม Approve Order สำหรับชาวต่างชาติ
def approve_order(selected_date, zoo_entries, aquarium_entries, show_entries):
    ticket_summary = {}
    total_price = 0

    # วนลูปเพื่อคำนวณจำนวนตั๋วและราคารวมจากข้อมูลในช่อง Entry สำหรับสวนสัตว์
    zoo_ticket_types = [
        ("Child", 89, zoo_entries[0][0]),  
        ("Teeneger", 159, zoo_entries[1][0]),
        ("Adult", 249, zoo_entries[2][0]),
        ("Senior", 0, zoo_entries[3][0])
]

    # คำนวณจำนวนและราคารวม
    for ticket_type, price_per_ticket, entry in zoo_ticket_types:
        quantity = 0
        entry_value = entry.get()
        if entry_value.isdigit():             
            quantity = int(entry_value)  
        if quantity > 0:
            ticket_summary[f"Zoo Ticket ({ticket_type})"] = quantity
        total_price += quantity * price_per_ticket  

    # วนลูปเพื่อคำนวณจำนวนตั๋วและราคารวมจากข้อมูลในช่อง Entry สำหรับอควาเรียม
    aquarium_ticket_types = [
        ("Child", 100, aquarium_entries[0][0]),  
        ("Adult", 140, aquarium_entries[1][0])
    ]
    for ticket_type, price_per_ticket, entry in aquarium_ticket_types:
        quantity = 0
        entry_value = entry.get()
        if entry_value.isdigit():
            quantity = int(entry_value) 
        if quantity > 0:
            ticket_summary[f"Aquarium Ticket ({ticket_type})"] = quantity
        total_price += quantity * price_per_ticket  

    # วนลูปเพื่อคำนวณจำนวนตั๋วและราคารวมจากข้อมูลในช่อง Entry สำหรับการแสดง
    show_ticket_types = [
        ("Child", 50, show_entries[0][0]), 
        ("Adult", 100, show_entries[1][0])
    ]
    for ticket_type, price_per_ticket, entry in show_ticket_types:
        quantity = 0
        entry_value = entry.get()
        if entry_value.isdigit():
            quantity = int(entry_value) 
        if quantity > 0:
            ticket_summary[f"Animal Show Ticket ({ticket_type})"] = quantity
        total_price += quantity * price_per_ticket  

    # เรียกใช้งานฟังก์ชันเพื่อเปิดหน้าต่างยืนยัน
    open_foreign_confirm_window(selected_date, ticket_summary, total_price)

#เปิดหน้ายืนยันการสั่งซื้อของชาวต่างชาติ
def open_foreign_confirm_window(selected_date, ticket_summary, total_price):
    confirm_window = customtkinter.CTkToplevel()
    confirm_window.title("Approve Order")
    
    window_width = 1000
    window_height = 700
    confirm_window.geometry(f"{window_width}x{window_height}")

    screen_width = confirm_window.winfo_screenwidth()
    screen_height = confirm_window.winfo_screenheight()
    position_x = int((screen_width - window_width) / 2)
    position_y = int((screen_height - window_height) / 2)
    confirm_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    confirm_window.attributes('-topmost', True)
    confirm_window.lift() 
    confirm_window.focus_force() 
    confirm_window.after(100, lambda: confirm_window.lift())
    image_path = "profile8.png"
    image = Image.open(image_path)

    image_margin_width = 15  
    image_margin_height = 15  

    new_width = window_width - (2 * image_margin_width)
    new_height = window_height - (2 * image_margin_height)
    img_width, img_height = image.size
    aspect_ratio = img_width / img_height

    if new_width / new_height > aspect_ratio:
        resized_width = int(new_height * aspect_ratio)
        resized_height = new_height
    else:
        resized_width = new_width
        resized_height = int(new_width / aspect_ratio)

    resized_image = image.resize((resized_width, resized_height), Image.LANCZOS)
    photo = customtkinter.CTkImage(resized_image, size=(resized_width, resized_height))

    # สร้าง label สำหรับแสดงรูปภาพ
    image_label = customtkinter.CTkLabel(
        master=confirm_window,
        image=photo,
        text="" 
    )
    image_label.image = photo  
    image_label.place(relx=0.5, rely=0.5, anchor="center")  

    # ข้อความยืนยัน
    confirmation_label = customtkinter.CTkLabel(
        master=confirm_window,
        text=f"You have selected to visit on{selected_date}",
        font=("Helvetica", 16),
        bg_color=("#ffc794"),
        text_color=("#8a4200")
    )
    confirmation_label.place(relx=0.3, rely=0.68, anchor="center")

    # แสดงรายละเอียดตั๋วจากข้อมูลที่กรอกใน Entry
    summary_y_pos = 0.25
    for ticket_type, quantity in ticket_summary.items():
        ticket_label = customtkinter.CTkLabel(
            master=confirm_window,
            text=f"{ticket_type}: {quantity} ",
            font=("Helvetica", 16),
            text_color="#B75C30",
            bg_color="#FFDAC6"
        )
        ticket_label.place(relx=0.3, rely=summary_y_pos, anchor="center")
        summary_y_pos += 0.05

    # แสดงราคารวมทั้งหมด
    total_label = customtkinter.CTkLabel(
        master=confirm_window,
        text=f"Total: {total_price} THB",
        font=("Helvetica", 16),
        text_color="#8e1300",
        bg_color="#f2aba0"
    )
    total_label.place(relx=0.3, rely=0.77, anchor="center")

    # ปุ่มย้อนกลับ
    back_button = customtkinter.CTkButton(
        master=confirm_window,
        text="Back/กลับ",
        command=lambda : (confirm_window.destroy(),open_foreign_window()),  
        fg_color="#f1c6a4",
        text_color="Black"
    )
    back_button.place(relx=0.15, rely=0.1, anchor="center") 

    # ปุ่มสำหรับแนบไฟล์
    attach_button = customtkinter.CTkButton(
        master=confirm_window,
        text="Attach payment proof",
        command=attach_file,  
        fg_color="#A7C2A5", 
        text_color="white",  
        hover_color="#A8C8B9",
        font=("Helvetica", 16)  
        
    )
    attach_button.place(relx=0.75, rely=0.71, anchor="center")


     # สร้างปุ่มหน้าถัดไป
    next_button = customtkinter.CTkButton(
        master=confirm_window,
        text="Next",
        command=lambda: (open_foreign_data_window(selected_date, ticket_summary, total_price),
        confirm_window.destroy()),  # ส่งค่าอาร์กิวเมนต์
        fg_color="#C0E0EF",          
        text_color="Black"            
    )
    next_button.place(relx=0.75, rely=0.8, anchor="center")  


#********สร้างหน้าต่างเมื่อกดปุ่ม"หน้าถัดไป"---สำหรับคนไทย **********
def open_thai_data_window(selected_date, ticket_summary, total_price):
    # สร้างหน้าต่างใหม่ชื่อ Thai Data
    thai_data_window = customtkinter.CTkToplevel()
    thai_data_window.title("Thai Data")

    window_width = 1000
    window_height = 700
    thai_data_window.geometry(f"{window_width}x{window_height}")

    screen_width = thai_data_window.winfo_screenwidth()
    screen_height = thai_data_window.winfo_screenheight()
    position_x = int((screen_width - window_width) / 2)
    position_y = int((screen_height - window_height) / 2)
    thai_data_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    thai_data_window.attributes('-topmost', True)
    thai_data_window.lift()  
    thai_data_window.focus_force()  
    thai_data_window.after(100, lambda: thai_data_window.lift())

    image_path = "profile9.png"
    image = Image.open(image_path)
    image_margin_width = 15  
    image_margin_height = 15  

    new_width = window_width - (2 * image_margin_width)
    new_height = window_height - (2 * image_margin_height)

    img_width, img_height = image.size
    aspect_ratio = img_width / img_height

    if new_width / new_height > aspect_ratio:
        resized_width = int(new_height * aspect_ratio)
        resized_height = new_height
    else:
        resized_width = new_width
        resized_height = int(new_width / aspect_ratio)

    resized_image = image.resize((resized_width, resized_height), Image.LANCZOS)

    photo = customtkinter.CTkImage(resized_image, size=(resized_width, resized_height))

    # สร้าง label สำหรับแสดงรูปภาพ
    image_label = customtkinter.CTkLabel(
        master=thai_data_window,
        image=photo,
        text=""  # แสดงเฉพาะรูปภาพ
    )
    image_label.image = photo 
    image_label.place(relx=0.5, rely=0.5, anchor="center")  

    # สร้างฟอร์มกรอกข้อมูล
    create_thai_data_form(thai_data_window, selected_date, ticket_summary, total_price)

def create_thai_data_form(thai_data_window, selected_date, ticket_summary, total_price):
    # สร้างฟิลด์กรอกข้อมูล
    labels = ["ชื่อ:", "นามสกุล:", "หมายเลขบัตรประชาชน:", "เบอร์โทรศัพท์:", "อีเมล:"]
    entries = []  

    for i, label_text in enumerate(labels):
        label = customtkinter.CTkLabel(
            thai_data_window,
            text=label_text,
            text_color="Black",  
            font=("Prompt", 15),  
            bg_color="white" 
        )
        label.place(relx=0.3, rely=0.3 + i * 0.1, anchor="w")  

        entry = customtkinter.CTkEntry(thai_data_window, width=220)
        entry.place(relx=0.45, rely=0.3 + i * 0.1, anchor="w")  
        entries.append(entry)  # เก็บ Entry ลงในลิสต์

    # ปุ่มบันทึก
    confirm_button = customtkinter.CTkButton(thai_data_window, text="บันทึก", 
        command=lambda: submit_data_thai(entries, selected_date, ticket_summary, total_price))
    confirm_button.place(relx=0.5, rely=0.8, anchor="center")  

    # เพิ่มปุ่มกลับ
    back_button = customtkinter.CTkButton(
        master=thai_data_window,
        text="กลับ",
        command=lambda: (open_thai_confirm_window(selected_date, ticket_summary, total_price), thai_data_window.destroy()), 
        fg_color="#c0e0ef",  # สีพื้นหลังของปุ่ม
        hover_color="lightgreen",  # สีเมื่อวางเมาส์
        text_color="Black"  # สีข้อความ
    )
    back_button.place(relx=0.1, rely=0.07, anchor="center")  


def submit_data_thai(entries):
    print("เริ่มการทำงานของ submit_data") 

    # เชื่อมต่อกับฐานข้อมูล
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        print("เชื่อมต่อกับฐานข้อมูลสำเร็จ")  

        # สร้างตาราง
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                surname TEXT,
                id_card TEXT,
                phone TEXT,
                email TEXT
            )
        ''')
        print("สร้างตารางสำเร็จ") 

        # จัดการข้อมูลที่กรอก
        data = {f"Field {i+1}": entry.get() for i, entry in enumerate(entries)}
        print("ข้อมูลที่กรอก:", data)  

        # บันทึกข้อมูลลงในตาราง
        cursor.execute('''
            INSERT INTO tickets (name, surname, id_card, phone, email)
            VALUES (?, ?, ?, ?, ?)
        ''', (data["Field 1"], data["Field 2"], data["Field 3"], data["Field 4"], data["Field 5"]))
        print("บันทึกข้อมูลลงในฐานข้อมูลสำเร็จ")  

        # บันทึกการเปลี่ยนแปลง
        conn.commit()
        print("ข้อมูลถูกบันทึกเรียบร้อยแล้ว")  
        messagebox.showinfo("Success", "ข้อมูลถูกบันทึกลงในฐานข้อมูลเรียบร้อยแล้ว")
    except Exception as e:
        print(f"Error: {e}")  # พิมพ์ข้อผิดพลาด
        messagebox.showerror("Error", f"เกิดข้อผิดพลาดในการบันทึกข้อมูล: {e}")
    finally:
        conn.close()
        print("ปิดการเชื่อมต่อฐานข้อมูลแล้ว")  


#******************สร้างหน้าต่างเมื่อกดปุ่ม"Next Page"---สำหรับชาวต่างชาติ***************
# สำหรับ open_foreign_data_window
def open_foreign_data_window(selected_date, ticket_summary, total_price):
    # สร้างหน้าต่างใหม่ชื่อ Foreign Data
    foreign_data_window = customtkinter.CTkToplevel()
    foreign_data_window.title("Foreign Data")
    window_width = 1000
    window_height = 700
    foreign_data_window.geometry(f"{window_width}x{window_height}")

    screen_width = foreign_data_window.winfo_screenwidth()
    screen_height = foreign_data_window.winfo_screenheight()
    position_x = int((screen_width - window_width) / 2)
    position_y = int((screen_height - window_height) / 2)
    foreign_data_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    foreign_data_window.attributes('-topmost', True)
    foreign_data_window.lift()  
    foreign_data_window.focus_force()  
    foreign_data_window.after(100, lambda: foreign_data_window.lift())

    image_path = "profile10.png"
    image = Image.open(image_path)
    image_margin_width = 100  
    image_margin_height = 100  

    new_width = window_width - (2 * image_margin_width)
    new_height = window_height - (2 * image_margin_height)

    img_width, img_height = image.size
    aspect_ratio = img_width / img_height

    if new_width / new_height > aspect_ratio:
        resized_width = int(new_height * aspect_ratio)
        resized_height = new_height
    else:
        resized_width = new_width
        resized_height = int(new_width / aspect_ratio)

    resized_image = image.resize((resized_width, resized_height), Image.LANCZOS)

    photo = customtkinter.CTkImage(resized_image, size=(resized_width, resized_height))

    # สร้าง label สำหรับแสดงรูปภาพ
    image_label = customtkinter.CTkLabel(
        master=foreign_data_window,
        image=photo,
        text="" 
    )
    image_label.image = photo  
    image_label.place(relx=0.5, rely=0.5, anchor="center")  


    # โหลดและปรับขนาดรูปภาพ
    image_path = "profile10.png"
    try:
        image = Image.open(image_path)

        # กำหนดขนาดใหม่ที่เหมาะสม
        resized_image = image.resize((window_width, window_height))
        photo = customtkinter.CTkImage(resized_image, size=(window_width, window_height))

        # แสดงรูปภาพในหน้าต่าง
        image_label = customtkinter.CTkLabel(foreign_data_window, image=photo, text="")
        image_label.image = photo  
        image_label.pack() 
    except Exception as e:
        print(f"ไม่สามารถโหลดรูปภาพได้: {e}")

    # สร้างฟอร์มกรอกข้อมูล
    create_foreign_data_form(foreign_data_window, selected_date, ticket_summary, total_price)

def create_foreign_data_form(foreign_data_window, selected_date, ticket_summary, total_price):
    # สร้างฟิลด์กรอกข้อมูล
    labels = ["First Name:", "Last Name:", "Passport Number:", "Phone Number:", "Email:"]
    entries = []  # เก็บช่องกรอกข้อมูล

    for i, label_text in enumerate(labels):
        label = customtkinter.CTkLabel(
            foreign_data_window,
            text=label_text,
            text_color="Black", 
            font=("Prompt", 15),  
            bg_color="white"  
        )
        label.place(relx=0.3, rely=0.3 + i * 0.1, anchor="w")  

        
        entry = customtkinter.CTkEntry(foreign_data_window, width=220)
        entry.place(relx=0.45, rely=0.3 + i * 0.1, anchor="w")  
        entries.append(entry) 

    # ปุ่มบันทึก
    confirm_button = customtkinter.CTkButton(foreign_data_window, text="SAVE", 
    command=lambda: submit_data_foreign(entries, selected_date, ticket_summary, total_price))
    confirm_button.place(relx=0.5, rely=0.8, anchor="center") 
     
# ฟังก์ชันที่ใช้ในการกลับไปหน้าก่อนหน้า
    def go_back():
        foreign_data_window.destroy()  

# ปุ่ม "Back"
    back_button = customtkinter.CTkButton(foreign_data_window, text="Back", command=go_back, fg_color="#00567e")
    back_button.place(relx=0.5, rely=0.87, anchor="center")  


def submit_data_foreign(entries, selected_date, ticket_summary, total_price):
    # ชื่อฟิลด์ในฟอร์ม
    field_names = ["First Name", "Last Name", "Passport Number", "Phone Number", "Email"]
    data = {field_names[i]: entry.get() or "N/A" for i, entry in enumerate(entries)}

    # ตรวจสอบว่าชื่อและนามสกุลไม่ว่างเปล่า
    if data["First Name"] == "N/A" or data["Last Name"] == "N/A":
        print("กรุณากรอกชื่อและนามสกุลให้ครบถ้วน")
        return

    # บันทึกข้อมูลลงในฐานข้อมูล SQLite
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ticket_data (first_name, last_name, passport_number, phone_number, email, date, ticket_summary, total_price) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (data["First Name"], data["Last Name"], data["Passport Number"], data["Phone Number"], data["Email"], selected_date, str(ticket_summary), total_price)
        )
        conn.commit()
        conn.close()
        print("บันทึกข้อมูลลงในฐานข้อมูลสำเร็จ")
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการบันทึกข้อมูล: {e}")





####***********สร้างใบเสร็จ ต่างชาติ************#######
# ลงทะเบียนฟอนต์ THSarabun
pdfmetrics.registerFont(TTFont('THSarabun', r'C:\\Python Project\\THSarabun.ttf'))

# ฟังก์ชันในการสร้างตารางใหม่ชื่อ dataticket_foreign
def create_new_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dataticket_foreign (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            id_card TEXT,
            phone TEXT,
            email TEXT,
            visit_date TEXT,
            ticket_details TEXT,
            total_price REAL
        )
    ''')
    conn.commit()
    conn.close()
    print("สร้างตาราง dataticket_foreign เรียบร้อยแล้ว")

# ฟังก์ชันในการบันทึกข้อมูลลงในฐานข้อมูล
def save_to_database_foreign(data, selected_date, ticket_summary, total_price):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    ticket_number = str(uuid.uuid4())
    first_name = data["first_name"]
    last_name = data["last_name"]
    id_card = data["id_card"]
    phone = data["phone"]
    email = data["email"]
    ticket_details = str(ticket_summary)
    cursor.execute('''
        INSERT INTO dataticket_foreign (first_name, last_name, id_card, phone, email, visit_date, ticket_details, total_price)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (first_name, last_name, id_card, phone, email, selected_date, ticket_details, total_price))
    conn.commit()
    conn.close()
    print(f"บันทึกข้อมูลลงในฐานข้อมูลเรียบร้อยแล้ว: {first_name} {last_name}")

# ฟังก์ชันสร้างใบเสร็จสำหรับต่างชาติ
def create_receipt_foreign(selected_date, ticket_summary, total_price, first_name, last_name, width, height):
    ticket_number = str(uuid.uuid4())
    receipt_filename = f"receipt_foreign_{first_name}_{last_name}.pdf"
    c = canvas.Canvas(receipt_filename, pagesize=(width, height))
    c.drawImage("profile11.png", 0, 0, width=width, height=height)
    c.setFont("Helvetica", 9)
    c.drawString(10, height - 70, f"Ticket Number: {ticket_number}")
    c.drawString(10, height - 90, f"Name: {first_name} {last_name}")
    c.drawString(10, height - 110, f"Date of Visit: {selected_date}")
    y_position = height - 140
    c.drawString(10, y_position, "Ticket Summary:")
    for ticket_type, quantity in ticket_summary.items():
        y_position -= 20
        c.drawString(10, y_position, f"{ticket_type}: {quantity}")
    c.drawString(10, y_position - 20, f"Total Price: {total_price:.2f} THB")
    c.save()
    print(f"ใบเสร็จถูกสร้างเรียบร้อย: {receipt_filename}")
    open_pdf_topmost(receipt_filename)

# ฟังก์ชันเปิด PDF ในโหมดหน้าต่างท็อป
def open_pdf_topmost(file_path):
    try:
        os.startfile(file_path)
        top_window = tk.Tk()
        top_window.withdraw()
        top_window.attributes('-topmost', True)
        top_window.update()
        top_window.after(100, lambda: top_window.destroy())
    except Exception as e:
        print(f"ไม่สามารถเปิดไฟล์ PDF ได้: {e}")

# ฟังก์ชันในการส่งข้อมูลและบันทึกลงฐานข้อมูล
def submit_data_foreign(entries, selected_date, ticket_summary, total_price):
    field_names = ["first_name", "last_name", "id_card", "phone", "email"]
    data = {field_names[i]: entry.get() for i, entry in enumerate(entries)}
    print("ข้อมูลที่กรอก:", data)
    if "first_name" not in data or not data["first_name"]:
        print("Error: ไม่พบฟิลด์ 'first_name' หรือไม่มีข้อมูลในฟิลด์นี้")
        return
    width_mm = 110
    height_mm = 160
    dpi = 72
    width = width_mm * dpi / 25.4
    height = height_mm * dpi / 25.4
    create_new_table()
    save_to_database_foreign(data, selected_date, ticket_summary, total_price)
    create_receipt_foreign(selected_date, ticket_summary, total_price, data["first_name"], data["last_name"], width, height)


####***********สร้างใบเสร็จ คนไทยยยยยยยย************#######
###################################################  
# ลงทะเบียนฟอนต์ THSarabun
pdfmetrics.registerFont(TTFont('THSarabun', r'C:\\Python Project\\THSarabun.ttf'))

# ฟังก์ชันในการสร้างตารางใหม่ชื่อ dataticket_thai
def create_new_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # สร้างตารางใหม่ชื่อ dataticket_thai
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dataticket_thai (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            id_card TEXT,
            phone TEXT,
            email TEXT,
            visit_date TEXT,
            ticket_details TEXT,
            total_price REAL
        )
    ''')
    conn.commit()
    conn.close()
    print("สร้างตาราง dataticket_thai เรียบร้อยแล้ว")

# ฟังก์ชันในการบันทึกข้อมูลลงในฐานข้อมูล
def save_to_database_thai(data, selected_date, ticket_summary, total_price):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # สร้างหมายเลขตั๋วแบบสุ่ม
    ticket_number = str(uuid.uuid4())

    # เตรียมข้อมูลที่จะบันทึก
    first_name = data["first_name"]
    last_name = data["last_name"]
    id_card = data["id_card"]
    phone = data["phone"]
    email = data["email"]
    ticket_details = str(ticket_summary)

    # บันทึกข้อมูลลงในตาราง dataticket_thai
    cursor.execute('''
        INSERT INTO dataticket_thai (first_name, last_name, id_card, phone, email, visit_date, ticket_details, total_price)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (first_name, last_name, id_card, phone, email, selected_date, ticket_details, total_price))
    
    conn.commit()
    conn.close()
    print(f"บันทึกข้อมูลลงในฐานข้อมูลเรียบร้อยแล้ว: {first_name} {last_name}")

# ฟังก์ชันสร้างใบเสร็จสำหรับคนไทย
def create_receipt_thai(selected_date, ticket_summary, total_price, first_name, last_name, width, height):
    # สร้างหมายเลขตั๋วแบบสุ่ม
    ticket_number = str(uuid.uuid4())

    # สร้าง PDF ใบเสร็จ
    receipt_filename = f"receipt_thai_{first_name}_{last_name}.pdf"
    c = canvas.Canvas(receipt_filename, pagesize=(width, height))

    # วาดรูปภาพในใบเสร็จให้ขนาดเท่าใบเสร็จ
    c.drawImage("C:\\Python Project\\profile12.png", 0, 0, width=width, height=height)

    # ใช้ฟอนต์ THSarabun
    c.setFont("THSarabun", 14)

    # ใช้ TextObject เพื่อวาดข้อความ
    text_object = c.beginText(10, height - 70) 
    text_object.setFont("THSarabun", 14)

    # วาดหมายเลขตั๋วและข้อมูลด้านซ้าย
    text_object.textLine(f"หมายเลขตั๋ว: {ticket_number}")
    text_object.textLine(f"ชื่อ: {first_name} {last_name}")
    text_object.textLine(f"วันที่เข้าชม: {selected_date}")

    # เขียนรายละเอียดตั๋ว
    text_object.textLine("รายละเอียดตั๋ว:")
    for ticket_type, quantity in ticket_summary.items():
        text_object.textLine(f"{ticket_type}: {quantity}")

    text_object.textLine(f"ราคารวม: {total_price:.2f} บาท")

    # วาดข้อความใน PDF
    c.drawText(text_object)

    # บันทึก PDF
    c.save()
    print(f"ใบเสร็จถูกสร้างเรียบร้อย: {receipt_filename}")

    # เปิดไฟล์ PDF และทำให้หน้าต่างเด้งขึ้นมาหน้าสุด
    open_pdf_topmost(receipt_filename)

# ฟังก์ชันเปิด PDF ในโหมดหน้าต่างท็อป
def open_pdf_topmost(file_path):
    try:
        # เปิดไฟล์ PDF
        os.startfile(file_path)

        # สร้างหน้าต่าง Tkinter ชั่วคราวเพื่อบังคับให้หน้าต่าง PDF เด้งขึ้นมาด้านบน
        top_window = tk.Tk()
        top_window.withdraw()  # ซ่อนหน้าต่างหลัก
        top_window.attributes('-topmost', True) 
        top_window.update()  
        top_window.after(100, lambda: top_window.destroy())  
    except Exception as e:
        print(f"ไม่สามารถเปิดไฟล์ PDF ได้: {e}")

# ฟังก์ชันในการส่งข้อมูลและบันทึกลงฐานข้อมูล
def submit_data_thai(entries, selected_date, ticket_summary, total_price):
    # ฟังก์ชันสำหรับจัดการข้อมูลที่กรอก
    field_names = ["first_name", "last_name", "id_card", "phone", "email"]
    data = {field_names[i]: entry.get() for i, entry in enumerate(entries)}
    print(data)  

    # กำหนดขนาดใบเสร็จเป็น 110 x 160 มม. (แปลงเป็นพิกเซล)
    width_mm = 110
    height_mm = 160
    dpi = 72
    width = width_mm * dpi / 25.4  
    height = height_mm * dpi / 25.4  

    # สร้างตารางใหม่ในฐานข้อมูล
    create_new_table()

    # บันทึกข้อมูลลงในฐานข้อมูล
    save_to_database_thai(data, selected_date, ticket_summary, total_price)

    # เรียกใช้ฟังก์ชันสร้างใบเสร็จที่มีการใช้ข้อมูลจากฟิลด์
    create_receipt_thai(selected_date, ticket_summary, total_price, data["first_name"], data["last_name"], width, height)




app.mainloop()  # เริ่มต้นการทำงานของแอปพลิเคชัน
