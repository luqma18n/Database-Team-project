CREATE TABLE Customer(
    CustomerID INTEGER PRIMARY KEY,
    Name VARCHAR(20),
    CurrentBalance DECIMAL(10, 2)
);

CREATE TABLE Address(
    AddressID INTEGER PRIMARY KEY,
    CustomerID INTEGER,
    AddressLine1 VARCHAR(50), 
    AddressLine2 VARCHAR(50), 
    City VARCHAR(50), 
    State VARCHAR(20), 
    ZipCode VARCHAR(20), 
    AddressType VARCHAR(20),  
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);

CREATE TABLE CreditCard(
    CreditCardID INTEGER PRIMARY KEY,
    CustomerID INTEGER,
    CardNumber VARCHAR(16), 
    ExpirationDate DATE, 
    SecurityCode VARCHAR(5), 
    PaymentAddressID INTEGER, 
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
    FOREIGN KEY (PaymentAddressID) REFERENCES Address(AddressID)
);

CREATE TABLE CustomerOrder(
    OrderID INTEGER PRIMARY KEY,
    CustomerID INTEGER,
    OrderDate DATE, 
    Status VARCHAR(20), 
    CreditCardID INTEGER,  
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID), 
    FOREIGN KEY (CreditCardID) REFERENCES CreditCard(CreditCardID)   
);

CREATE TABLE Product(
    ProductID INTEGER PRIMARY KEY,
    Name VARCHAR(50),
    Category VARCHAR(50),
    Type VARCHAR(20),
    Brand VARCHAR(20),
    Size VARCHAR(20),
    Description TEXT,
    Price DECIMAL(10, 2)
);

CREATE TABLE OrderProduct(
    OrderProductID INTEGER PRIMARY KEY,
    OrderID INTEGER,
    ProductID INTEGER, 
    Quantity INTEGER,  
    FOREIGN KEY (OrderID) REFERENCES CustomerOrder(OrderID), 
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)   
);

CREATE TABLE DeliveryPlan(
    DeliveryPlanID INTEGER PRIMARY KEY,
    OrderID INTEGER,
    DeliveryType VARCHAR(20),
    DeliveryPrice DECIMAL(10, 2), 
    DeliveryDate DATE,
    ShipDate DATE, 
    FOREIGN KEY (OrderID) REFERENCES CustomerOrder(OrderID)   
);

CREATE TABLE Stock(
    StockID INTEGER PRIMARY KEY,
    ProductID INTEGER,
    WarehouseID INTEGER, 
    Quantity INTEGER,
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)   
);

CREATE TABLE Warehouse(
    WarehouseID INTEGER PRIMARY KEY,
    Address VARCHAR(50)
);

CREATE TABLE Supplier(
    SupplierID INTEGER PRIMARY KEY,
    Name VARCHAR(20),
    Address VARCHAR(50)
);

CREATE TABLE SupplierProduct(
    SupplierProductID INTEGER PRIMARY KEY,
    SupplierID INTEGER,
    ProductID INTEGER,
    SupplierPrice DECIMAL(10, 2),
    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID), 
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

CREATE TABLE StaffMember(
    StaffID INTEGER PRIMARY KEY,
    Name VARCHAR(20), 
    Address INTEGER,
    Salary DECIMAL(10, 2),
    JobTitle VARCHAR(20),
	FOREIGN KEY (Address) REFERENCES Address(AddressID)
);
