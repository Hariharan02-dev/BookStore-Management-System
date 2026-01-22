CREATE DATABASE IF NOT EXISTS bookstore_db;
USE bookstore_db;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(50) NOT NULL
);

INSERT IGNORE INTO users VALUES ('admin', 'admin123');

-- Books table
CREATE TABLE IF NOT EXISTS books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    author VARCHAR(100),
    price FLOAT,
    stock INT
);

-- Sales table
CREATE TABLE IF NOT EXISTS book_sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT,
    quantity_sold INT,
    sale_date DATE,
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);
