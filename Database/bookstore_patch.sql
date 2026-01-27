create database bookstore_db;
use bookstore_db;

create table books (
    book_id int auto_increment primary key,
    title varchar(100),
    author varchar(100),
    price decimal(10,2),
    stock int
);

create table users (
    id int auto_increment primary key,
    username varchar(50),
    password varchar(50)
);

create table book_sales (
    sale_id int auto_increment primary key,
    book_id int,
    quantity_sold int,
    sale_date date
);

insert into users (username, password) values ('admin', '1234');
