CREATE DATABASE MechanicShop;
GO

USE MechanicShop;
GO

CREATE TABLE Customer (
    customer_id INT PRIMARY KEY IDENTITY(1,1),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    address VARCHAR(255)
);

CREATE TABLE Vehicle (
    vin VARCHAR(17) PRIMARY KEY,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year INT NOT NULL,
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

CREATE TABLE Service_Ticket (
    ticket_id INT PRIMARY KEY IDENTITY(1,1),
    service_date DATE NOT NULL,
    description TEXT NOT NULL,
    cost DECIMAL(10,2) NOT NULL,
    vin VARCHAR(17),
    FOREIGN KEY (vin) REFERENCES Vehicle(vin)
);

CREATE TABLE Mechanic (
    mechanic_id INT PRIMARY KEY IDENTITY(1,1),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    address VARCHAR(255),
    salary DECIMAL(10,2) NOT NULL
);

CREATE TABLE Service_Assignment (
    assignment_id INT PRIMARY KEY IDENTITY(1,1),
    ticket_id INT,
    mechanic_id INT,
    FOREIGN KEY (ticket_id) REFERENCES Service_Ticket(ticket_id),
    FOREIGN KEY (mechanic_id) REFERENCES Mechanic(mechanic_id)
);

INSERT INTO Customer (first_name, last_name, email, phone_number, address)
VALUES 
('John', 'Doe', 'john.doe@example.com', '123-456-7890', '123 Main St'),
('Jane', 'Smith', 'jane.smith@example.com', '555-123-4567', '456 Oak St');

INSERT INTO Vehicle (vin, make, model, year, customer_id)
VALUES 
('1HGCM82633A123456', 'Honda', 'Accord', 2020, 1),
('2HGFA16588H123457', 'Toyota', 'Camry', 2019, 2);

INSERT INTO Service_Ticket (service_date, description, cost, vin)
VALUES 
('2025-03-15', 'Oil Change and Tire Rotation', 100.00, '1HGCM82633A123456'),
('2025-03-20', 'Brake Pad Replacement', 150.00, '2HGFA16588H123457');

INSERT INTO Mechanic (first_name, last_name, email, phone_number, address, salary)
VALUES 
('Mike', 'Johnson', 'mike.j@example.com', '333-222-1111', '789 Pine St', 55000.00),
('Emma', 'Brown', 'emma.b@example.com', '222-111-9999', '987 Maple St', 62000.00);

INSERT INTO Service_Assignment (ticket_id, mechanic_id)
VALUES 
(1, 1), -- Mike worked on the Honda Accord service
(2, 2); -- Emma worked on the Toyota Camry service

SELECT 
    c.first_name,
    c.last_name,
    v.make,
    v.model,
    v.year
FROM 
    Customer c
JOIN 
    Vehicle v ON c.customer_id = v.customer_id;

SELECT 
    s.ticket_id,
    s.service_date,
    s.description,
    m.first_name AS mechanic_firstname,
    m.last_name AS mechanic_lastname
FROM 
    Service_Ticket s
JOIN 
    Service_Assignment sa ON s.ticket_id = sa.ticket_id
JOIN 
    Mechanic m ON sa.mechanic_id = m.mechanic_id;

SELECT 
    sa.ticket_id, 
    m.first_name, 
    m.last_name
FROM 
    Service_Assignment sa
JOIN 
    Mechanic m ON sa.mechanic_id = m.mechanic_id;

