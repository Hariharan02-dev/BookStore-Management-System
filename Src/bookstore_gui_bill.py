import tkinter as tk
from tkinter import messagebox, scrolledtext
import mysql.connector
from datetime import date

# --- 1. DATABASE CONNECTION ---
def connect_db():
    try:
        # UPDATE THIS: Change '1234' to your actual MySQL CLI password
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # <--- PUT YOUR PASSWORD HERE
            database="bookstore_db"
        )
        return con
    except Exception as e:
        messagebox.showerror("Connection Error", f"Error: {e}\nCheck MySQL connection!")
        return None

# --- 2. LOGIN FUNCTION ---
def login_check():
    u = user_entry.get()
    p = pass_entry.get()
    
    conn = connect_db()
    if conn:
        try:
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
        except Exception as e:
            messagebox.showerror("SQL Error", str(e))

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
            e1.delete(0,'end'); e2.delete(0,'end'); e3.delete(0,'end'); e4.delete(0,'end')
            db.close()
            show_data() 

    tk.Button(f1, text="Add Book", command=save_book, bg="#90EE90", width=15).grid(row=4, column=1, pady=5)

    # ==============================
    # MODULE B: SELL & GENERATE BILL
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
                    # 1. Update Database
                    new_stock = current_stock - qty
                    total_price = price * qty
                    today_date = date.today()
                    
                    c.execute("UPDATE books SET stock=%s WHERE book_id=%s", (new_stock, b_id))
                    # We still record the sale in DB even if we don't show the report button
                    c.execute("INSERT INTO book_sales(book_id, quantity_sold, sale_date) VALUES (%s,%s,%s)", (b_id, qty, today_date))
                    db.commit()
                    
                    # 2. PREPARE BILL TEXT
                    bill_content = f"""
    *************************************
          BOOK STORE RECEIPT      
    *************************************
    Date: {today_date}
    Invoice No: #INV-{b_id}-{qty}
    
    Item Details:
    -------------------------------------
    Book  : {title}
    Price : Rs. {price}
    Qty   : {qty}
    -------------------------------------
    
    TOTAL AMOUNT : Rs. {total_price:.2f}
    
    *************************************
         Thank you for shopping!
    *************************************
                    """
                    
                    # 3. OPEN BILL WINDOW
                    bill_win = tk.Toplevel(win)
                    bill_win.title("Payment Receipt")
                    bill_win.geometry("400x500")
                    bill_win.configure(bg="white")

                    # Display Bill
                    lbl_bill = tk.Text(bill_win, font=("Courier New", 12), bg="white", relief="flat")
                    lbl_bill.insert("1.0", bill_content)
                    lbl_bill.config(state="disabled") 
                    lbl_bill.pack(padx=10, pady=10, fill="both", expand=True)
                    
                    # --- SAVE BILL FUNCTION ---
                    def save_to_file():
                        filename = f"Bill_{b_id}_{today_date}.txt"
                        try:
                            with open(filename, "w") as f:
                                f.write(bill_content)
                            messagebox.showinfo("Saved", f"Bill Saved Successfully!\nFile: {filename}")
                        except Exception as e:
                            messagebox.showerror("Error", str(e))

                    # Buttons
                    btn_frame = tk.Frame(bill_win, bg="white")
                    btn_frame.pack(pady=10)

                    tk.Button(btn_frame, text="Save Bill", command=save_to_file, bg="#4CAF50", fg="white", width=15).pack(side=tk.LEFT, padx=5)
                    tk.Button(btn_frame, text="Close", command=bill_win.destroy, bg="#f44336", fg="white", width=10).pack(side=tk.LEFT, padx=5)

                    # Clear inputs and refresh main table
                    sid.delete(0, 'end'); sqty.delete(0, 'end')
                    show_data() 
                else:
                    messagebox.showerror("Stock Error", f"Not enough stock! Only {current_stock} left.")
            else:
                messagebox.showerror("Error", "Book ID not found")
            db.close()

    tk.Button(f2, text="Sell & Bill", command=make_sale, bg="#ADD8E6", width=15).grid(row=2, column=1, pady=5)

    # ==============================
    # MODULE C: DELETE BOOK
    # ==============================
    f3 = tk.LabelFrame(win, text=" Delete Book ")
    f3.grid(row=0, column=2, padx=10, pady=10, sticky="n")

    tk.Label(f3, text="Book ID:").grid(row=0, column=0)
    del_entry = tk.Entry(f3, width=15); del_entry.grid(row=0, column=1)

    def delete_book():
        bid = del_entry.get()
        if bid == "": return
        if messagebox.askyesno("Confirm", "Delete Book ID " + str(bid) + "?"):
            db = connect_db()
            if db:
                c = db.cursor()
                try:
                    c.execute("DELETE FROM books WHERE book_id=%s", (bid,))
                    db.commit()
                    messagebox.showinfo("Deleted", "Book Record Removed")
                    del_entry.delete(0, 'end')
                    show_data()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                db.close()

    tk.Button(f3, text="Delete", command=delete_book, bg="#FFcccb", width=15).grid(row=1, column=1, pady=5)

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
    txt = scrolledtext.ScrolledText(win, width=110, height=20)
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
            header = "{:<5} {:<30} {:<20} {:<10} {:<10}\n".format("ID", "Title", "Author", "Price", "Stock")
            txt.insert('end', header)
            txt.insert('end', "="*90 + "\n")
            
            for r in data:
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

tk.Label(f_log, text="User:").grid(row=0, column=0, pady=5); 
user_entry = tk.Entry(f_log); user_entry.grid(row=0, column=1)

tk.Label(f_log, text="Pass:").grid(row=1, column=0, pady=5); 
pass_entry = tk.Entry(f_log, show="*"); pass_entry.grid(row=1, column=1)

tk.Button(root, text="LOGIN", command=login_check, width=15, bg="silver").pack(pady=20)

root.mainloop()
