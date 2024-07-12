create table Customer(
	CustomerID integer PRIMARY KEY,
	Name VARCHAR(20),
	CurrentBalance float
);

create table Address(
	CustomerID integer ,
	AddressID integer,
	AddressLine1 VARCHAR(20), 
	AddressLine2 VARCHAR(20), 
	City VARCHAR(20), 
	State VARCHAR(20), 
	ZipCode VARCHAR(20), 
	AddressType VARCHAR(20),  
	primary key(AddressID), 
	FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);

create table CreditCard(
	CustomerID integer ,
	CreditCardID integer,
	CardNumber VARCHAR(20), 
	EpirationDate date, 
	SecurityCode integer, 
	PaymentAddressID integer, 
	primary key(CreditCardID), 
	FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
	FOREIGN KEY (PaymentAddressID) REFERENCES Address(AddressID)
);


create table CustomerOrder( -- changed from Order to CustomerOrder
	CustomerID integer,
	OrderID integer,
	OrderDate date, 
	status VARCHAR(20), 
	CreditCardID integer,  
	primary key(OrderID), 
	FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID), 
	FOREIGN KEY (CreditCardID) REFERENCES CreditCard(CreditCardID) 	
);

create table Product(
	ProductID integer,
	Name VARCHAR(20),
	Category VARCHAR(20),
	Type VARCHAR(20),
	Brand VARCHAR(20),
	Size VARCHAR(20),
	Description integer,
	Price float,
	primary key(ProductID)
);

create table OderProduct(
	OrderProductID integer,
	OrderID integer,
	ProductID integer, 
	Quantity integer,  
	primary key(OrderProductID), 
	FOREIGN KEY (OrderID) REFERENCES CustomerOrder(OrderID), 
	FOREIGN KEY (ProductID) REFERENCES Product(ProductID) 	
);

create table DeliveryPlan(
	DeliveryPlanID integer,
	OrderID integer,
	DeliveryType VARCHAR(20),
	DeliveryPrice float, 
	DeliveryDate date,
	shipeDate date, 
	primary key(DeliveryPlanID), 
	FOREIGN KEY (OrderID) REFERENCES CustomerOrder(OrderID) 	
);

create table Stock(
	StockID integer,
	ProductID integer,
	WarehouseID integer, 
	Quantity integer,
	primary key(StockID), 
	FOREIGN KEY (ProductID) REFERENCES Product(ProductID) 	
);

create table Warehouse(
	WarehouseID integer,
	Address VARCHAR(20),
	primary key(WarehouseID)	
);



create table Supplier(
	SupplierID integer,
	Name VARCHAR(20),
	Address VARCHAR(20),
	primary key(SupplierID)	
);


create table SupplierProduct(
	SupplierProductID integer,
	SupplierID integer,
	ProductID integer,
	SupplierPrice float,
	primary key(SupplierProductID), 
	FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID), 
	FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);


create table StaffMember(
	StaffID integer,
	Name VARCHAR(20), 
	Address VARCHAR(20),
	Salary float,
	JobTitle VARCHAR(20),
	primary key(StaffID)
);















