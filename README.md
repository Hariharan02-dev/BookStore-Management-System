# 📚 Book Store Management System

A GUI-based Book Store Management System developed using Python, MySQL, and Tkinter.  
This project is designed to manage book inventory, handle sales, and store records efficiently using a relational database.

This project is created as part of the Class 12 Computer Science (CBSE) curriculum and demonstrates Python–SQL connectivity, database operations, and GUI-based interaction.

---

## ✨ Features

- Secure login authentication  
- Add new books to inventory  
- View available books with stock details  
- Sell books with automatic stock update  
- Maintain sales records  
- User-friendly graphical interface  
- MySQL database connectivity  
- Input validation and error handling  

---

## 🛠️ Technologies Used

- Python 3  
- MySQL  
- Tkinter (GUI)  
- mysql-connector-python  

---

## 🗄️ Database Structure

### books  
Stores book information.  
- book_id (Primary Key)  
- title  
- author  
- price  
- stock  

### book_sales  
Stores sales records.  
- sale_id (Primary Key)  
- book_id (Foreign Key)  
- quantity_sold  
- sale_date  

### users  
Stores login credentials.  
- username (Primary Key)  
- password  

---

## ▶️ How to Run the Project

### Step 1: Create Database  
Run the SQL file located in:
database/bookstore.sql  

---

### Step 2: Configure MySQL Credentials  
Open:
src/bookstore_gui.py  

Update:
host = "localhost"  
user = "root"  
password = "your_password"  

---

### Step 3: Run the Program  

python bookstore_gui.py  

---

## 🔐 Default Login Credentials

Username: admin  
Password: admin123  

---

## 📁 Project Structure

BookStore-Management-System/  
│  
├── src/  
│   └── bookstore_gui.py  
│  
├── database/  
│   └── bookstore.sql  
│  
├── screenshots/  
│   └── (optional)  
│  
├── README.md  
│  
└── .gitignore  

---

## 🔒 Security Features

- Uses parameterized SQL queries (%s) to prevent SQL injection  
- Data integrity using primary and foreign keys  
- Proper error handling  

---

## 🚀 Future Enhancements

- Invoice and billing system  
- ISBN-based search  
- Multiple user roles  
- Web-based version  

---

## 📌 Note

This project is developed for educational purposes and demonstrates:
- Python–MySQL connectivity  
- CRUD operations  
- GUI-based application development  

---

## 🧠 Author
****  
Class 12 – Computer Science  
CBSE
