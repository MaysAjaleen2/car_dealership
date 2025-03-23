-- create database Cars ;
 use Cars;
 -- drop database Cars;
-- DROP TABLE IF EXISTS Filter_Log;
-- DROP TABLE IF EXISTS Car;
 -- Create the Car table
CREATE TABLE IF NOT EXISTS Car (
    Car_ID INT AUTO_INCREMENT PRIMARY KEY,
    Model VARCHAR(50) NOT NULL,
    Make VARCHAR(50) NOT NULL,
    Year INT NOT NULL CHECK (Year > 1900),
    Price DECIMAL(10, 2) NOT NULL CHECK (Price > 0),
    Color VARCHAR(50) NOT NULL,
    Status VARCHAR(50) NOT NULL,
    Image VARCHAR(255)
);

-- Create the Filter Log table
CREATE TABLE IF NOT EXISTS Filter_Log (
    Filter_ID INT AUTO_INCREMENT PRIMARY KEY,
    Filtered_By VARCHAR(255),  -- User or filter source (optional)
    Year_Filter INT,
    Make_Filter VARCHAR(50),
    Price_Filter DECIMAL(10, 2),
    Filter_Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Automatically logs the time
);


						-- ---------- done ---------- -- 

CREATE TABLE Employee (
    Emp_ID INT PRIMARY KEY,            
    EmName VARCHAR(100) NOT NULL,        
    EmRole VARCHAR(50) NOT NULL,   
    Salalry DECIMAL(10, 2) NOT NULL, 
    Statuss TINYINT(1) NOT NULL DEFAULT 1
);


CREATE TABLE Employee_Phone (
    Phone_ID INT PRIMARY KEY auto_increment , 
    Emp_ID INT NOT NULL,                     
    Phone VARCHAR(15) NOT NULL,              
    FOREIGN KEY (Emp_ID) REFERENCES Employee(Emp_ID)
);
CREATE TABLE Employee_Email (
    Email_ID INT PRIMARY KEY auto_increment , 
    Emp_ID INT NOT NULL,                     
    Email VARCHAR(100) NOT NULL,             
    FOREIGN KEY (Emp_ID) REFERENCES Employee(Emp_ID) 
);
-- select * from Employee ;
							-- ---------- done ---------- -- 
                            
-- Insert sample data into the Customer table

CREATE TABLE IF NOT EXISTS Customer (
    Customer_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Address VARCHAR(255) NOT NULL,
    Phone VARCHAR(15) UNIQUE NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL
);

									-- ---------- done ---------- -- 
-- Create the Service table
CREATE TABLE IF NOT EXISTS Service (
    Service_ID INT AUTO_INCREMENT PRIMARY KEY,
    TypeSer VARCHAR(50) NOT NULL,
    Date DATE NOT NULL,
    Price DECIMAL(10, 2) NOT NULL,
    Employee_ID INT NOT NULL,
    FOREIGN KEY (Employee_ID) REFERENCES Employee(Emp_ID)
);

									-- ---------- done ---------- -- 

CREATE TABLE Sale (
    Sale_ID INT PRIMARY KEY,           
    Date DATE NOT NULL,                
    Total_Amount DECIMAL(10, 2) NOT NULL, 
    Customer_ID INT NOT NULL,         
    FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID) 
);
									-- ---------- done ---------- -- 

CREATE TABLE Appointment (
    Appoint_ID INT PRIMARY KEY,         
    Date DATE NOT NULL,                 
    Time TIME NOT NULL,                 
    Purpose VARCHAR(255) NOT NULL,      
    Car_ID INT,                         
    FOREIGN KEY (Car_ID) REFERENCES Car(Car_ID) 
);
ALTER TABLE Appointment
ADD Customer_ID INT,
ADD CONSTRAINT FK_Appointment_Customer
FOREIGN KEY (Customer_ID)
REFERENCES Customer(Customer_ID);
									-- ---------- done ---------- -- 

CREATE TABLE Order_Line (
    Order_Line_ID INT PRIMARY KEY AUTO_INCREMENT,                 
    Real_Price DECIMAL(10, 2) NOT NULL,
    Final_Price DECIMAL(10, 2) NOT NULL  
);

-- Create Order Totals table
CREATE TABLE Order_Totals (
    Order_Line_ID INT NOT NULL,
    Order_ID INT NOT NULL,
    PRIMARY KEY (Order_Line_ID, Order_ID),
    FOREIGN KEY (Order_Line_ID) REFERENCES Order_Line(Order_Line_ID),
    FOREIGN KEY (Order_ID) REFERENCES Sale(Sale_ID)
);



-- Additions
use Cars;
 select * from Employee ;
 -- Insert sample data into the Car table
 -- Insert dummy data into Employee table
INSERT INTO Employee (Emp_ID, EmName, EmRole, Salalry, Statuss)
VALUES 
(1, 'John Doe', 'Manager', 5000.00, 1),
(2, 'Jane Smith', 'Sales Associate', 3000.00, 1),
(3, 'Michael Brown', 'Technician', 3500.00, 1),
(4, 'Sarah Davis', 'HR Specialist', 4000.00, 1),
(5, 'Chris Wilson', 'Customer Service', 2800.00, 0);

-- Insert dummy data into Employee_Phone table
INSERT INTO Employee_Phone (Emp_ID, Phone)
VALUES 
(1, '123-456-7890'),
(1, '987-654-3210'),
(2, '456-789-1230'),
(3, '789-123-4560'),
(4, '321-654-9870'),
(5, '654-987-3210');

-- Insert dummy data into Employee_Email table
INSERT INTO Employee_Email (Emp_ID, Email)
VALUES 
(1, 'johndoe@example.com'),
(2, 'janesmith@example.com'),
(3, 'michaelbrown@example.com'),
(4, 'sarahdavis@example.com'),
(5, 'chriswilson@example.com');

INSERT INTO Car (Model, Make, Year, Price, Color, Status, Image)
VALUES
('BMW', 'BMW', 2021, 200000.00, 'Black', 'Available', 'bmw.png'),
('G-Class', 'Mercedes', 2022, 150000.00, 'White', 'Sold', 'Mercedes_G.png'),
('Range Rover', 'Land Rover', 2020, 180000.00, 'White', 'Available', 'Rang_rover.png'),
('BMW', 'BMW', 2023, 1800000.00, 'Blue', 'Available', 'bmw.png'),
('Cadillac', 'Cadillac', 2018, 92000.00, 'Red', 'Sold', 'Cadilac.png'),
('Ford', 'Ford', 2015, 40000.00, 'Blue', 'Available', 'Ford.png'),
('Hyundai', 'Hyundai', 2017, 30000.00, 'Blue', 'Sold', 'hundai.png'),
('Jaguar', 'Jaguar', 2023, 1000000.00, 'Black', 'Available', 'Jaguar.png'),
('Jeep', 'Jeep', 2016, 500000.00, 'Pink', 'Available', 'Jeep.png'),
('KIA', 'KIA', 2014, 20000.00, 'Gray', 'Available', 'KIA.png'),
('Mazda', 'Mazda', 2016, 200000.00, 'Red', 'Sold', 'Mazda.png'),
('Nissan', 'Nissan', 2021, 4500000.00, 'Red', 'Available', 'Nissan.png'),
('Opel', 'Opel', 2020, 330000.00, 'Blue', 'Available', 'Opel.png'),
('Peugeot', 'Peugeot', 2023, 300500.00, 'Blue', 'Sold', 'Peugeot.png'),
('Rolls Royce', 'Rolls Royce', 2024, 10000000.00, 'Black', 'Available', 'Rolls_Royce.png'),
('Shelby', 'Shelby', 2024, 90000000.00, 'Orange', 'Available', 'Shelby.png'),
('Skoda', 'Skoda', 2023, 900500.00, 'White', 'Available', 'Skoda.png'),
('Tesla', 'Tesla', 2020, 65000000.00, 'White', 'Available', 'Tesla.png'),
('Toyota Supra', 'Toyota', 2024, 50050000.00, 'Yellow', 'Available', 'toyota_super.png'),
('VM JEEP', 'VM', 2022, 50070000.00, 'Black', 'Available', 'VM_JEEP.png'),
('Volkswagen', 'Volkswagen', 2020, 5003400.00, 'Red', 'Sold', 'Volkswagen.png'),
('Volvo', 'Volvo', 2022, 990000.00, 'Gray', 'Available', 'Volvo.png');


-- Insert sample data into the Customer table
INSERT INTO Customer (Name, Address, Phone, Email)
VALUES
('John Doe', '123 Elm St, NY', '555-1234', 'john.doe@example.com'),
('Jane Smith', '456 Maple St, CA', '555-5678', 'jane.smith@example.com'),
('Alice Johnson', '789 Oak St, TX', '555-9101', 'alice.johnson@example.com');

-- Insert sample data into Service table
 INSERT INTO Service (Type, Date, Price, Employee_ID) VALUES
('Oil Change', '2025-01-01', 100.00, 1),
('Tire Replacement', '2025-01-02', 150.00, 3),
('Car Wash', '2025-01-03', 50.00, 1);


-- Insert sample data into the Employee table
-- Insert sample data into the Appointment table
-- Insert sample data into the Order_Line table



SELECT * FROM Filter_Log;
select * from Appointment ;
select * from Sale ;
SELECT * FROM Service;
SELECT * FROM Car;
SELECT * FROM Customer;