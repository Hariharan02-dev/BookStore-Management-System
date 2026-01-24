import tkinter as tk
from tkinter import messagebox, scrolledtext
import mysql.connector
from datetime import date

# --- DATABASE CONNECTION SETTINGS ---
# Note: Ensure MySQL is running before starting the app
def connect_db():
    try:
        # Provide your local MySQL details here
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password", # Change this for your lab PC
            database="bookstore_db"
        )
        return con
    except:
        messagebox.showerror("Error", "Check MySQL connection!")
        return None

# --- LOGIN FUNCTION ---
def login_check():
    u = user_entry.get()
    p = pass_entry.get()
    
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        # SQL Query to verify user
        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        cur.execute(query, (u, p))
        res = cur.fetchone()
        conn.close()

        if res:
            root.destroy()
            main_app() # Open the main window
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

# --- MAIN APPLICATION WINDOW ---
def main_app():
    win = tk.Tk()
    win.title("Book Store Management System")
    win.geometry("700x600")

    # --- ADD BOOK MODULE ---
    f1 = tk.LabelFrame(win, text=" Add Books ")
    f1.grid(row=0, column=0, padx=20, pady=20)

    tk.Label(f1, text="Title:").grid(row=0, column=0)
    e1 = tk.Entry(f1)
    e1.grid(row=0, column=1)

    tk.Label(f1, text="Author:").grid(row=1, column=0)
    e2 = tk.Entry(f1)
    e2.grid(row=1, column=1)

    tk.Label(f1, text="Price:").grid(row=2, column=0)
    e3 = tk.Entry(f1)
    e3.grid(row=2, column=1)

    tk.Label(f1, text="Stock:").grid(row=3, column=0)
    e4 = tk.Entry(f1)
    e4.grid(row=3, column=1)

    def save_book():
        # Validate data
        if e1.get()=="" or e2.get()=="" or e3.get()=="" or e4.get()=="":
            messagebox.showwarning("Warning", "Fill all fields")
            return
            
        db = connect_db()
        if db:
            c = db.cursor()
            sql = "INSERT INTO books (title, author, price, stock) VALUES (%s, %s, %s, %s)"
            vals = (e1.get(), e2.get(), e3.get(), e4.get())
            c.execute(sql, vals)
            db.commit()
            messagebox.showinfo("Done", "Book Added Successfully")
            # Clear entries
            e1.delete(0, 'end'); e2.delete(0, 'end'); e3.delete(0, 'end'); e4.delete(0, 'end')
            db.close()

    tk.Button(f1, text="Save", command=save_book, bg="lightgreen").grid(row=4, column=1)

    # --- SELL BOOK MODULE ---
    f2 = tk.LabelFrame(win, text=" Sales ")
    f2.grid(row=0, column=1, padx=20, pady=20)

    tk.Label(f2, text="Book ID:").grid(row=0, column=0)
    sid = tk.Entry(f2)
    sid.grid(row=0, column=1)

    tk.Label(f2, text="Qty:").grid(row=1, column=0)
    sqty = tk.Entry(f2)
    sqty.grid(row=1, column=1)

    def make_sale():
        b_id = sid.get()
        qty = sqty.get()
        
        db = connect_db()
        if db:
            c = db.cursor()
            c.execute("SELECT stock, price FROM books WHERE book_id=%s", (b_id,))
            record = c.fetchone()

            if record and record[0] >= int(qty):
                rem_stock = record[0] - int(qty)
                total_amt = record[1] * int(qty)
                
                # Update table and log date
                c.execute("UPDATE books SET stock=%s WHERE book_id=%s", (rem_stock, b_id))
                today = date.today()
                c.execute("INSERT INTO book_sales(book_id, quantity_sold, sale_date) VALUES (%s,%s,%s)", (b_id, qty, today))
                db.commit()
                messagebox.showinfo("Success", "Total: Rs." + str(total_amt))
                sid.delete(0, 'end'); sqty.delete(0, 'end')
            else:
                messagebox.showerror("Error", "No stock or wrong ID")
            db.close()

    tk.Button(f2, text="Sell", command=make_sale, bg="lightblue").grid(row=2, column=1)

    # --- INVENTORY VIEW ---
    txt = scrolledtext.ScrolledText(win, width=80, height=15)
    txt.grid(row=1, column=0, columnspan=2, pady=10)

    def show_data():
        db = connect_db()
        if db:
            c = db.cursor()
            c.execute("SELECT * FROM books")
            data = c.fetchall()
            txt.delete('1.0', 'end')
            txt.insert('end', "ID\tTitle\t\tAuthor\t\tPrice\tStock\n")
            txt.insert('end', "------------------------------------------------------------\n")
            for row in data:
                txt.insert('end', str(row[0]) + "\t" + str(row[1]) + "\t\t" + str(row[2]) + "\t\t" + str(row[3]) + "\t" + str(row[4]) + "\n")
            db.close()

    tk.Button(win, text="Show/Refresh Data", command=show_data).grid(row=2, column=0, columnspan=2)

    show_data() # Show data on window load
    win.mainloop()

# --- LOGIN SCREEN START ---
root = tk.Tk()
root.title("Login")
root.geometry("300x250")

tk.Label(root, text="ADMIN LOGIN", font=("Arial", 12, "bold")).pack(pady=10)
tk.Label(root, text="Username").pack()
user_entry = tk.Entry(root)
user_entry.pack()

tk.Label(root, text="Password").pack()
pass_entry = tk.Entry(root, show="*")
pass_entry.pack()

tk.Button(root, text="Enter", command=login_check).pack(pady=20)

root.mainloop()
