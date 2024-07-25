DROP TABLE IF EXISTS Address CASCADE;
DROP TABLE IF EXISTS CreditCard CASCADE;
DROP TABLE IF EXISTS CustomerOrder CASCADE;
DROP TABLE IF EXISTS OrderProduct CASCADE;
DROP TABLE IF EXISTS DeliveryPlan CASCADE;
DROP TABLE IF EXISTS Stock CASCADE;
DROP TABLE IF EXISTS Warehouse CASCADE;
DROP TABLE IF EXISTS SupplierProduct CASCADE;
DROP TABLE IF EXISTS Supplier CASCADE;
DROP TABLE IF EXISTS StaffMember CASCADE;
DROP TABLE IF EXISTS Product CASCADE;
DROP TABLE IF EXISTS Customer CASCADE;

CREATE TABLE Customer (
    CustomerID SERIAL PRIMARY KEY,
    Name VARCHAR(20),
    CurrentBalance DECIMAL(10, 2)
);

CREATE TABLE Address (
    AddressID SERIAL PRIMARY KEY,
    CustomerID INTEGER,
    AddressLine1 VARCHAR(50), 
    AddressLine2 VARCHAR(50), 
    City VARCHAR(50), 
    State VARCHAR(20), 
    ZipCode VARCHAR(20), 
    AddressType VARCHAR(20),  
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON DELETE CASCADE
);

CREATE TABLE Warehouse (
    WarehouseID SERIAL PRIMARY KEY,
    Address VARCHAR(50)
);

CREATE TABLE Product (
    ProductID SERIAL PRIMARY KEY,
    Name VARCHAR(50),
    Category VARCHAR(50),
    Type VARCHAR(20),
    Brand VARCHAR(20),
    Size VARCHAR(20),
    Description TEXT,
    Price DECIMAL(10, 2)
);

CREATE TABLE CreditCard (
    CreditCardID SERIAL PRIMARY KEY,
    CustomerID INTEGER,
    CardNumber VARCHAR(16), 
    ExpirationDate DATE, 
    SecurityCode VARCHAR(5), 
    PaymentAddressID INTEGER, 
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON DELETE CASCADE,
    FOREIGN KEY (PaymentAddressID) REFERENCES Address(AddressID) ON DELETE SET NULL
);

CREATE TABLE CustomerOrder (
    OrderID SERIAL PRIMARY KEY,
    CustomerID INTEGER,
    OrderDate DATE, 
    Status VARCHAR(20), 
    CreditCardID INTEGER,  
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON DELETE CASCADE, 
    FOREIGN KEY (CreditCardID) REFERENCES CreditCard(CreditCardID) ON DELETE SET NULL
);

CREATE TABLE OrderProduct (
    OrderProductID SERIAL PRIMARY KEY,
    OrderID INTEGER,
    ProductID INTEGER, 
    Quantity INTEGER,  
    FOREIGN KEY (OrderID) REFERENCES CustomerOrder(OrderID) ON DELETE CASCADE, 
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID) ON DELETE CASCADE
);

CREATE TABLE DeliveryPlan (
    DeliveryPlanID SERIAL PRIMARY KEY,
    OrderID INTEGER,
    DeliveryType VARCHAR(20),
    DeliveryPrice DECIMAL(10, 2), 
    DeliveryDate DATE,
    ShipDate DATE, 
    FOREIGN KEY (OrderID) REFERENCES CustomerOrder(OrderID) ON DELETE CASCADE
);

CREATE TABLE Stock (
    StockID SERIAL PRIMARY KEY,
    ProductID INTEGER,
    WarehouseID INTEGER, 
    Quantity INTEGER,
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID) ON DELETE CASCADE,
    FOREIGN KEY (WarehouseID) REFERENCES Warehouse(WarehouseID) ON DELETE CASCADE
);

CREATE TABLE Supplier (
    SupplierID SERIAL PRIMARY KEY,
    Name VARCHAR(20),
    Address VARCHAR(50)
);

CREATE TABLE SupplierProduct (
    SupplierProductID SERIAL PRIMARY KEY,
    SupplierID INTEGER,
    ProductID INTEGER,
    SupplierPrice DECIMAL(10, 2),
    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID) ON DELETE CASCADE, 
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID) ON DELETE CASCADE
);

CREATE TABLE StaffMember (
    StaffID SERIAL PRIMARY KEY,
    Name VARCHAR(20), 
    AddressID INTEGER,
    Salary DECIMAL(10, 2),
    JobTitle VARCHAR(20),
    FOREIGN KEY (AddressID) REFERENCES Address(AddressID) ON DELETE SET NULL
);
