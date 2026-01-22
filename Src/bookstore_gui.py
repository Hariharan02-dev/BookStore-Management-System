import mysql.connector
from tkinter import *
from tkinter import messagebox
from datetime import date

# ---------- DATABASE CONNECTION ----------
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="bookstore_db"
)
cur = con.cursor()

# ---------- LOGIN WINDOW ----------
login_window = Tk()
login_window.title("Login")
login_window.geometry("300x200")

def login():
    u = user_entry.get()
    p = pass_entry.get()

    cur.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s",
        (u, p)
    )
    if cur.fetchone():
        login_window.destroy()
        main_app()
    else:
        messagebox.showerror("Error", "Invalid Login")

Label(login_window, text="Username").pack()
user_entry = Entry(login_window)
user_entry.pack()

Label(login_window, text="Password").pack()
pass_entry = Entry(login_window, show="*")
pass_entry.pack()

Button(login_window, text="Login", command=login).pack(pady=10)

# ---------- MAIN APPLICATION ----------
def main_app():
    root = Tk()
    root.title("Book Store Management System")
    root.geometry("750x550")

    # ---------- FUNCTIONS ----------
    def add_book():
        t = title_entry.get()
        a = author_entry.get()
        p = price_entry.get()
        s = stock_entry.get()

        if t == "" or a == "" or p == "" or s == "":
            messagebox.showerror("Error", "All fields required")
            return

        cur.execute(
            "INSERT INTO books(title, author, price, stock) VALUES(%s,%s,%s,%s)",
            (t, a, float(p), int(s))
        )
        con.commit()
        messagebox.showinfo("Success", "Book Added")
        clear_entries()

    def view_books():
        display.delete(1.0, END)
        cur.execute("SELECT * FROM books")
        rows = cur.fetchall()
        display.insert(END, "ID  Title  Author  Price  Stock\n")
        display.insert(END, "-"*60 + "\n")
        for r in rows:
            display.insert(END, f"{r[0]}  {r[1]}  {r[2]}  {r[3]}  {r[4]}\n")

    def sell_book():
        bid = sell_id.get()
        qty = sell_qty.get()

        cur.execute("SELECT stock FROM books WHERE book_id=%s", (bid,))
        result = cur.fetchone()

        if not result:
            messagebox.showerror("Error", "Book not found")
            return

        if result[0] < int(qty):
            messagebox.showerror("Error", "Insufficient Stock")
            return

        cur.execute(
            "UPDATE books SET stock=stock-%s WHERE book_id=%s",
            (int(qty), int(bid))
        )
        cur.execute(
            "INSERT INTO book_sales(book_id, quantity_sold, sale_date) VALUES(%s,%s,%s)",
            (int(bid), int(qty), date.today())
        )
        con.commit()
        messagebox.showinfo("Success", "Book Sold")

    def view_sales():
        display.delete(1.0, END)
        cur.execute("SELECT * FROM book_sales")
        rows = cur.fetchall()
        display.insert(END, "SaleID  BookID  Qty  Date\n")
        display.insert(END, "-"*60 + "\n")
        for r in rows:
            display.insert(END, f"{r[0]}  {r[1]}  {r[2]}  {r[3]}\n")

    def clear_entries():
        title_entry.delete(0, END)
        author_entry.delete(0, END)
        price_entry.delete(0, END)
        stock_entry.delete(0, END)

    # ---------- UI ----------
    Label(root, text="Book Store Management System", font=("Arial", 18, "bold")).pack(pady=10)

    frame = Frame(root)
    frame.pack()

    Label(frame, text="Title").grid(row=0, column=0)
    Label(frame, text="Author").grid(row=1, column=0)
    Label(frame, text="Price").grid(row=2, column=0)
    Label(frame, text="Stock").grid(row=3, column=0)

    title_entry = Entry(frame)
    author_entry = Entry(frame)
    price_entry = Entry(frame)
    stock_entry = Entry(frame)

    title_entry.grid(row=0, column=1)
    author_entry.grid(row=1, column=1)
    price_entry.grid(row=2, column=1)
    stock_entry.grid(row=3, column=1)

    Button(frame, text="Add Book", command=add_book, width=20).grid(row=4, columnspan=2, pady=5)

    Label(frame, text="Sell Book ID").grid(row=5, column=0)
    Label(frame, text="Quantity").grid(row=6, column=0)

    sell_id = Entry(frame)
    sell_qty = Entry(frame)

    sell_id.grid(row=5, column=1)
    sell_qty.grid(row=6, column=1)

    Button(frame, text="Sell Book", command=sell_book, width=20).grid(row=7, columnspan=2, pady=5)

    Button(root, text="View Books", command=view_books, width=20).pack(pady=5)
    Button(root, text="View Sales", command=view_sales, width=20).pack(pady=5)

    display = Text(root, height=10, width=85)
    display.pack(pady=10)

    root.mainloop()

login_window.mainloop()
