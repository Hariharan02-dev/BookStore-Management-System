import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import date

# ---------------- DATABASE CONNECTION ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="bookstore_db"
)

cursor = db.cursor()

# ---------------- LOGIN WINDOW ----------------
def login():
    user = username_entry.get()
    pwd = password_entry.get()

    query = "SELECT * FROM users WHERE username=%s AND password=%s"
    cursor.execute(query, (user, pwd))
    result = cursor.fetchone()

    if result:
        login_window.destroy()
        main_window()
    else:
        messagebox.showerror("Error", "Invalid Login")

login_window = tk.Tk()
login_window.title("Book Store Login")
login_window.geometry("300x200")

tk.Label(login_window, text="Username").pack()
username_entry = tk.Entry(login_window)
username_entry.pack()

tk.Label(login_window, text="Password").pack()
password_entry = tk.Entry(login_window, show="*")
password_entry.pack()

tk.Button(login_window, text="Login", command=login).pack(pady=10)

# ---------------- MAIN WINDOW ----------------
def main_window():
    window = tk.Tk()
    window.title("Book Store Management System")
    window.geometry("400x400")

    # -------- ADD BOOK --------
    def add_book():
        query = "INSERT INTO books (title, author, price, stock) VALUES (%s, %s, %s, %s)"
        values = (title_entry.get(), author_entry.get(), price_entry.get(), stock_entry.get())
        cursor.execute(query, values)
        db.commit()
        messagebox.showinfo("Success", "Book Added")

    # -------- VIEW BOOKS --------
    def view_books():
        cursor.execute("SELECT * FROM books")
        records = cursor.fetchall()
        output = ""
        for row in records:
            output += f"ID:{row[0]} | {row[1]} | Stock:{row[4]}\n"
        messagebox.showinfo("Books", output)

    # -------- SELL BOOK --------
    def sell_book():
        bid = int(book_id_entry.get())
        qty = int(quantity_entry.get())

        cursor.execute("SELECT stock, price FROM books WHERE book_id=%s", (bid,))
        data = cursor.fetchone()

        if data and data[0] >= qty:
            new_stock = data[0] - qty
            total = data[1] * qty

            cursor.execute("UPDATE books SET stock=%s WHERE book_id=%s", (new_stock, bid))
            cursor.execute(
                "INSERT INTO book_sales (book_id, quantity_sold, sale_date) VALUES (%s, %s, %s)",
                (bid, qty, date.today())
            )
            db.commit()
            messagebox.showinfo("Success", f"Book Sold\nTotal = ₹{total}")
        else:
            messagebox.showerror("Error", "Insufficient Stock")

    # -------- UI --------
    tk.Label(window, text="Add Book").pack()
    title_entry = tk.Entry(window)
    title_entry.pack()
    author_entry = tk.Entry(window)
    author_entry.pack()
    price_entry = tk.Entry(window)
    price_entry.pack()
    stock_entry = tk.Entry(window)
    stock_entry.pack()
    tk.Button(window, text="Add Book", command=add_book).pack(pady=5)

    tk.Button(window, text="View Books", command=view_books).pack(pady=10)

    tk.Label(window, text="Sell Book").pack()
    book_id_entry = tk.Entry(window)
    book_id_entry.pack()
    quantity_entry = tk.Entry(window)
    quantity_entry.pack()
    tk.Button(window, text="Sell Book", command=sell_book).pack(pady=5)

    window.mainloop()

login_window.mainloop()
