CREATE TABLE product_staging_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_name VARCHAR(255),
    file_location VARCHAR(255),
    created_date TIMESTAMP ,
    updated_date TIMESTAMP ,
    status VARCHAR(1)
);


CREATE TABLE customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    address VARCHAR(255),
    pincode VARCHAR(10),
    phone_number VARCHAR(20),
    customer_joining_date DATE
);

-- Insert command for customer
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Saanvi', 'Krishna', 'Kathmandu', '44600', '9841312108', '2021-01-20');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Dhanush', 'Sahni', 'Lalitpur', '44700', '9855328165', '2022-03-27');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Yasmin', 'Shan', 'Bhaktapur', '44800', '9819147830', '2023-04-08');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Vidur', 'Mammen', 'Pokhara', '33700', '9811901751', '2020-10-12');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Shamik', 'Doctor', 'Biratnagar', '56613', '9805180499', '2022-10-30');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Ryan', 'Dugar', 'Chitwan', '44200', '9842616565', '2020-08-10');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Romil', 'Shanker', 'Butwal', '32907', '9812945131', '2021-10-29');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Krish', 'Tandon', 'Dharan', '56700', '9845683399', '2020-01-08');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Divij', 'Garde', 'Hetauda', '44100', '9841984713', '2020-11-10');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Hunar', 'Tank', 'Nepalgunj', '21900', '9816980808', '2023-01-27');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Zara', 'Dhaliwal', 'Itahari', '56705', '9829776379', '2023-06-13');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Sumer', 'Mangal', 'Birtamode', '57204', '9813860793', '2020-05-01');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Rhea', 'Chander', 'Janakpur', '45600', '9810343473', '2023-08-09');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Yuvaan', 'Bawa', 'Dhangadhi', '10900', '9816207701', '2023-02-18');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Sahil', 'Sabharwal', 'Banepa', '45210', '9817492878', '2021-03-16');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Tiya', 'Kashyap', 'Dhulikhel', '45200', '9805126094', '2023-03-23');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Kimaya', 'Lala', 'Gorkha', '34000', '9811561683', '2021-03-14');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Vardaniya', 'Jani', 'Lumbini', '32900', '9812506897', '2022-07-19');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Indranil', 'Dutta', 'Kirtipur', '44618', '9812066775', '2023-07-18');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Kavya', 'Sachar', 'Surkhet', '21700', '9815762871', '2022-05-04');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Manjari', 'Sule', 'Tansen', '32500', '9811252550', '2023-02-12');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Akarsh', 'Kalla', 'Ilam', '57300', '9813226332', '2021-03-05');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Miraya', 'Soman', 'Damak', '57217', '9811145545', '2023-07-06');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Shalv', 'Chaudhary', 'Baglung', '33300', '9815809949', '2021-03-14');
INSERT INTO customer (first_name, last_name, address, pincode, phone_number, customer_joining_date) VALUES ('Jhanvi', 'Bava', 'Dhankuta', '56800', '9811007409', '2022-07-14');


--store table
CREATE TABLE store (
    id INT PRIMARY KEY,
    address VARCHAR(255),
    store_pincode VARCHAR(10),
    store_manager_name VARCHAR(100),
    store_opening_date DATE,
    reviews TEXT
);

--data of store table
INSERT INTO store (id, address, store_pincode, store_manager_name, store_opening_date, reviews)
VALUES
    (121, 'Durbar Marg, Kathmandu', '44600', 'Manish', '2022-01-15', 'Great store with a friendly staff.'),
    (122, 'Lakeside, Pokhara', '33700', 'Nikita', '2021-08-10', 'Excellent selection of products.'),
    (123, 'Pulchowk, Lalitpur', '44700', 'Vikash', '2023-01-20', 'Clean and organized store.'),
    (124, 'Main Road, Biratnagar', '56613', 'Rakesh', '2020-05-05', 'Good prices and helpful staff.');

-- product table
CREATE TABLE product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    current_price DECIMAL(10, 2),
    old_price DECIMAL(10, 2),
    created_date TIMESTAMP ,
    updated_date TIMESTAMP ,
    expiry_date DATE
);


--product table data
INSERT INTO product (name, current_price, old_price, created_date, updated_date, expiry_date)
VALUES
    ('Quaker Oats', 550, 580, '2022-05-15', '2026-02-25', '2027-06-01'),
    ('Sugar', 110, 115, '2021-08-10', '2026-02-25', '2027-12-31'),
    ('Aalu', 60, 70, '2023-03-20', '2026-02-25', '2026-04-15'),
    ('Pidalu', 85, 90, '2020-05-05', '2026-02-25', '2026-05-10'),
    ('Refined Oil', 240, 260, '2022-01-15', '2026-02-25', '2027-08-20'),
    ('Clinic Plus', 2, 2, '2021-09-25', NULL, '2028-01-01'),
    ('Chatpata', 50, 50, '2023-07-10', NULL, '2026-03-01'),
    ('Panipuri', 40, 40, '2020-11-30', NULL, '2026-02-26');

--sales team table
CREATE TABLE sales_team (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    manager_id INT,
    is_manager CHAR(1),
    address VARCHAR(255),
    pincode VARCHAR(10),
    joining_date DATE
);


--sales team data
INSERT INTO sales_team (first_name, last_name, manager_id, is_manager, address, pincode, joining_date)
VALUES
    ('Rahul', 'Adhikari', 10, 'N', 'Baneshwor, Kathmandu', '44600', '2020-05-01'),
    ('Priya', 'Shrestha', 10, 'N', 'Patan, Lalitpur', '44700', '2020-05-01'),
    ('Amit', 'Thapa', 10, 'N', 'Koteshwor, Kathmandu', '44600', '2020-05-01'),
    ('Sneha', 'Tamang', 10, 'N', 'Chabahil, Kathmandu', '44600', '2020-05-01'),
    ('Neha', 'Gurung', 10, 'N', 'Boudha, Kathmandu', '44600', '2020-05-01'),
    ('Vijay', 'Maharjan', 10, 'N', 'Sanepa, Lalitpur', '44700', '2020-05-01'),
    ('Anita', 'Koirala', 10, 'N', 'Suryabinayak, Bhaktapur', '44800', '2020-05-01'),
    ('Alok', 'Paudel', 10, 'N', 'Kalanki, Kathmandu', '44600', '2020-05-01'),
    ('Monica', 'Rai', 10, 'N', 'Jhamsikhel, Lalitpur', '44700', '2020-05-01'),
    ('Rajesh', 'Gupta', 10, 'Y', 'Thamel, Kathmandu', '44600', '2020-05-01');


--s3 bucket table
CREATE TABLE s3_bucket_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bucket_name VARCHAR(255),
    file_location VARCHAR(255),
    created_date TIMESTAMP ,
    updated_date TIMESTAMP ,
    status VARCHAR(20)
);


--s3 bucket data
INSERT INTO s3_bucket_info (bucket_name, status, created_date, updated_date)
VALUES ('youtube-project-testing', 'active', NOW(), NOW());


--Data Mart customer
CREATE TABLE customers_data_mart (
    customer_id INT ,
    full_name VARCHAR(100),
    address VARCHAR(200),
    phone_number VARCHAR(20),
    sales_date_month DATE,
    total_sales DECIMAL(10, 2)
);


--sales mart table
CREATE TABLE sales_team_data_mart (
    store_id INT,
    sales_person_id INT,
    full_name VARCHAR(255),
    sales_month VARCHAR(10),
    total_sales DECIMAL(10, 2),
    incentive DECIMAL(10, 2)
);