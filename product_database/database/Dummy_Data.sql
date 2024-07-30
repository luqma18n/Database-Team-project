-- Insert test data into Customer table
INSERT INTO Customer (Name, CurrentBalance) VALUES 
('John Doe', 100.00),
('Jane Smith', 200.00),
('Alice Johnson', 300.00);

-- Insert test data into Address table
INSERT INTO Address (CustomerID, AddressLine1, AddressLine2, City, State, ZipCode, AddressType) VALUES 
(1, '123 Main St', 'Apt 4B', 'Cincinnati', 'OH', '45202', 'Home'),
(2, '456 Oak St', 'Suite 101', 'Columbus', 'OH', '43215', 'Work'),
(3, '789 Pine St', '', 'Dayton', 'OH', '45402', 'Home');

-- Insert test data into Warehouse table
INSERT INTO Warehouse (Address) VALUES 
('101 Warehouse Lane'),
('202 Distribution Blvd'),
('303 Storage Drive');

-- Insert test data into Product table
INSERT INTO Product (Name, Category, Type, Brand, Size, Description, Price) VALUES 
('Laptop', 'Electronics', 'Portable', 'BrandA', '15 inch', 'High performance laptop', 999.99),
('Smartphone', 'Electronics', 'Mobile', 'BrandB', '6 inch', 'Latest model smartphone', 699.99),
('Headphones', 'Accessories', 'Audio', 'BrandC', 'One size', 'Noise-cancelling headphones', 199.99);

-- Insert test data into CreditCard table
INSERT INTO CreditCard (CustomerID, CreditCardID, CardNumber, ExpirationDate, SecurityCode, PaymentAddressID) VALUES 
(1, 1, '1111222233334444', '2025-12-31', '123', 1),
(2, 2, '5555666677778888', '2026-06-30', '456', 2),
(3, 3, '9999000011112222', '2024-09-15', '789', 3);

-- Insert test data into CustomerOrder table
INSERT INTO CustomerOrder (CustomerID, OrderDate, Status, CreditCardID) VALUES 
(1, '2023-07-20', 'Shipped', 1),
(2, '2023-07-21', 'Processing', 2),
(3, '2023-07-22', 'Delivered', 3);

-- Insert test data into OrderProduct table
INSERT INTO OrderProduct (OrderID, ProductID, Quantity) VALUES 
(1, 1, 1),
(2, 2, 2),
(3, 3, 3);

-- Insert test data into DeliveryPlan table
INSERT INTO DeliveryPlan (OrderID, DeliveryType, DeliveryPrice, DeliveryDate, ShipDate) VALUES 
(1, 'Standard', 10.00, '2023-07-25', '2023-07-21'),
(2, 'Express', 20.00, '2023-07-22', '2023-07-21'),
(3, 'Standard', 10.00, '2023-07-23', '2023-07-22');

-- Insert test data into Stock table
INSERT INTO Stock (ProductID, WarehouseID, Quantity) VALUES 
(1, 1, 50),
(2, 2, 100),
(3, 3, 200);

-- Insert test data into Supplier table
INSERT INTO Supplier (Name, Address) VALUES 
('SupplierA', '123 Supplier Rd'),
('SupplierB', '456 Supplier St'),
('SupplierC', '789 Supplier Blvd');

-- Insert test data into SupplierProduct table
INSERT INTO SupplierProduct (SupplierID, ProductID, SupplierPrice) VALUES 
(1, 1, 800.00),
(2, 2, 600.00),
(3, 3, 150.00);

-- Insert test data into StaffMember table
INSERT INTO StaffMember (Name, AddressID, Salary, JobTitle) VALUES 
('Tom Brown', 1, 50000.00, 'Manager'),
('Emma Green', 2, 55000.00, 'Supervisor'),
('Luke White', 3, 45000.00, 'Clerk');
