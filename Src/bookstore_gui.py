import tkinter as tk
from tkinter import messagebox, scrolledtext
import mysql.connector
from datetime import date

# --- 1. DATABASE CONNECTION ---
def connect_db():
    try:
        # UPDATE THIS: Change 'your_password' to your actual MySQL password
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password", 
            database="bookstore_db"
        )
        return con
    except:
        messagebox.showerror("Error", "Check MySQL connection! Is XAMPP/MySQL running?")
        return None

# --- 2. LOGIN FUNCTION ---
def login_check():
    u = user_entry.get()
    p = pass_entry.get()
    
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        cur.execute(query, (u, p))
        res = cur.fetchone()
        conn.close()

        if res:
            root.destroy() # Close login window
            main_app()     # Open dashboard
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

# --- 3. MAIN DASHBOARD ---
def main_app():
    win = tk.Tk()
    win.title("Book Store Management System")
    win.geometry("950x650") 

    # ==============================
    # MODULE A: ADD BOOKS
    # ==============================
    f1 = tk.LabelFrame(win, text=" Add New Book ")
    f1.grid(row=0, column=0, padx=10, pady=10, sticky="n")

    tk.Label(f1, text="Title:").grid(row=0, column=0, sticky="w")
    e1 = tk.Entry(f1); e1.grid(row=0, column=1)

    tk.Label(f1, text="Author:").grid(row=1, column=0, sticky="w")
    e2 = tk.Entry(f1); e2.grid(row=1, column=1)

    tk.Label(f1, text="Price:").grid(row=2, column=0, sticky="w")
    e3 = tk.Entry(f1); e3.grid(row=2, column=1)

    tk.Label(f1, text="Stock:").grid(row=3, column=0, sticky="w")
    e4 = tk.Entry(f1); e4.grid(row=3, column=1)

    def save_book():
        # Validation
        title = e1.get()
        author = e2.get()
        price_txt = e3.get()
        stock_txt = e4.get()

        if title == "" or author == "" or price_txt == "" or stock_txt == "":
            messagebox.showwarning("Warning", "All fields are required!")
            return

        try:
            price = float(price_txt)
            stock = int(stock_txt)
            if price < 0 or stock < 0:
                messagebox.showerror("Error", "Price/Stock cannot be negative.")
                return
        except ValueError:
            messagebox.showerror("Error", "Price must be a number\nStock must be an integer")
            return

        db = connect_db()
        if db:
            c = db.cursor()
            sql = "INSERT INTO books (title, author, price, stock) VALUES (%s, %s, %s, %s)"
            c.execute(sql, (title, author, price, stock))
            db.commit()
            messagebox.showinfo("Success", "Book Added!")
            # Clear boxes
            e1.delete(0,'end'); e2.delete(0,'end'); e3.delete(0,'end'); e4.delete(0,'end')
            db.close()
            show_data() 

    tk.Button(f1, text="Add Book", command=save_book, bg="#90EE90").grid(row=4, column=1, pady=5)

    # ==============================
    # MODULE B: SALES
    # ==============================
    f2 = tk.LabelFrame(win, text=" Sell Book ")
    f2.grid(row=0, column=1, padx=10, pady=10, sticky="n")

    tk.Label(f2, text="Book ID:").grid(row=0, column=0, sticky="w")
    sid = tk.Entry(f2); sid.grid(row=0, column=1)

    tk.Label(f2, text="Qty:").grid(row=1, column=0, sticky="w")
    sqty = tk.Entry(f2); sqty.grid(row=1, column=1)

    def make_sale():
        b_id = sid.get()
        q_val = sqty.get()

        if b_id == "" or q_val == "": 
            messagebox.showwarning("Warning", "Enter ID and Quantity")
            return
        
        db = connect_db()
        if db:
            c = db.cursor()
            c.execute("SELECT stock, price, title FROM books WHERE book_id=%s", (b_id,))
            rec = c.fetchone()

            if rec:
                current_stock = rec[0]
                price = rec[1]
                title = rec[2]
                
                try:
                    qty = int(q_val)
                except:
                    messagebox.showerror("Error", "Quantity must be a number")
                    return

                if current_stock >= qty:
                    new_stock = current_stock - qty
                    total = price * qty
                    
                    # Update Stock
                    c.execute("UPDATE books SET stock=%s WHERE book_id=%s", (new_stock, b_id))
                    # Record Sale
                    c.execute("INSERT INTO book_sales(book_id, quantity_sold, sale_date) VALUES (%s,%s,%s)", (b_id, qty, date.today()))
                    db.commit()
                    
                    msg = "Sold " + str(qty) + " x " + str(title) + "\nTotal Bill: Rs. " + str(total)
                    messagebox.showinfo("Sold!", msg)
                    sid.delete(0, 'end'); sqty.delete(0, 'end')
                    show_data() 
                else:
                    msg = "Not enough stock! Only " + str(current_stock) + " left."
                    messagebox.showerror("Stock Error", msg)
            else:
                messagebox.showerror("Error", "Book ID not found")
            db.close()

    tk.Button(f2, text="Sell Now", command=make_sale, bg="#ADD8E6").grid(row=2, column=1, pady=5)

    # ==============================
    # MODULE C: DELETE BOOK
    # ==============================
    f3 = tk.LabelFrame(win, text=" Delete Book ")
    f3.grid(row=0, column=2, padx=10, pady=10, sticky="n")

    tk.Label(f3, text="Book ID:").grid(row=0, column=0)
    del_entry = tk.Entry(f3, width=10); del_entry.grid(row=0, column=1)

    def delete_book():
        bid = del_entry.get()
        if bid == "": return

        confirm = messagebox.askyesno("Confirm", "Delete Book ID " + str(bid) + "?")
        
        if confirm:
            db = connect_db()
            if db:
                c = db.cursor()
                try:
                    c.execute("DELETE FROM books WHERE book_id=%s", (bid,))
                    if c.rowcount > 0:
                        db.commit()
                        messagebox.showinfo("Deleted", "Book Record Removed")
                        del_entry.delete(0, 'end')
                        show_data()
                    else:
                        messagebox.showerror("Error", "ID not found")
                except Exception as e:
                    messagebox.showerror("SQL Error", str(e))
                db.close()

    tk.Button(f3, text="Delete", command=delete_book, bg="#FFcccb").grid(row=1, column=0, columnspan=2, pady=5)

    # ==============================
    # SEARCH & DISPLAY AREA
    # ==============================
    
    search_frame = tk.Frame(win)
    search_frame.grid(row=1, column=0, columnspan=3, pady=10)
    
    tk.Label(search_frame, text="Search Book Title: ").pack(side=tk.LEFT)
    search_var = tk.Entry(search_frame)
    search_var.pack(side=tk.LEFT, padx=5)

    def run_search():
        keyword = search_var.get()
        load_data(keyword) 
    
    def run_show_all():
        load_data("")

    tk.Button(search_frame, text="Search", command=run_search, bg="yellow").pack(side=tk.LEFT)
    tk.Button(search_frame, text="Show All", command=run_show_all, bg="white").pack(side=tk.LEFT, padx=5)

    # Text Area
    txt = scrolledtext.ScrolledText(win, width=100, height=20)
    txt.grid(row=2, column=0, columnspan=3, padx=10)

    def load_data(filter_word):
        db = connect_db()
        if db:
            c = db.cursor()
            if filter_word == "":
                sql = "SELECT * FROM books"
                c.execute(sql)
            else:
                sql = "SELECT * FROM books WHERE title LIKE %s"
                c.execute(sql, ("%" + filter_word + "%",))
            
            data = c.fetchall()
            
            txt.delete('1.0', 'end')
            # Using basic string formatting instead of f-strings
            header = "{:<5} {:<30} {:<20} {:<10} {:<10}\n".format("ID", "Title", "Author", "Price", "Stock")
            txt.insert('end', header)
            txt.insert('end', "="*85 + "\n")
            
            for r in data:
                # Basic formatting
                row_str = "{:<5} {:<30} {:<20} {:<10} {:<10}\n".format(r[0], r[1], r[2], r[3], r[4])
                txt.insert('end', row_str)
            
            db.close()

    global show_data
    show_data = run_show_all

    show_data() 
    win.mainloop()

# --- 4. STARTUP (LOGIN SCREEN) ---
root = tk.Tk()
root.title("System Login")
root.geometry("300x200")

tk.Label(root, text="BOOKSTORE ADMIN", font=("Arial", 14, "bold")).pack(pady=10)

f_log = tk.Frame(root)
f_log.pack()

tk.Label(f_log, text="User:").grid(row=0, column=0); 
user_entry = tk.Entry(f_log); user_entry.grid(row=0, column=1)

tk.Label(f_log, text="Pass:").grid(row=1, column=0); 
pass_entry = tk.Entry(f_log, show="*"); pass_entry.grid(row=1, column=1)

tk.Button(root, text="LOGIN", command=login_check, width=15, bg="silver").pack(pady=20)

root.mainloop()
