
-- Customer Procedures:

-- Search for Product
CREATE OR REPLACE FUNCTION SearchProducts(productName VARCHAR(20))
RETURNS TABLE (ProductID INTEGER, Name VARCHAR, Price DECIMAL) AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM Product
    WHERE Name LIKE '%' || productName || '%';
END;
$$ LANGUAGE plpgsql;


-- Add order to cart
CREATE OR REPLACE FUNCTION AddToCart(customerId INTEGER, productId INTEGER, quantity INTEGER)
RETURNS VOID AS $$
DECLARE
    orderId INTEGER;
BEGIN
    -- Find or create an order in 'pending' status
    SELECT OrderID INTO orderId FROM CustomerOrder 
    WHERE CustomerID = customerId AND Status = 'pending' LIMIT 1;

    IF orderId IS NULL THEN
        INSERT INTO CustomerOrder (CustomerID, OrderDate, Status)
        VALUES (customerId, NOW(), 'pending') RETURNING OrderID INTO orderId;
    END IF;

    -- Add or update the product in the order
    IF EXISTS (SELECT 1 FROM OrderProduct WHERE OrderID = orderId AND ProductID = productId) THEN
        UPDATE OrderProduct SET Quantity = Quantity + quantity WHERE OrderID = orderId AND ProductID = productId;
    ELSE
        INSERT INTO OrderProduct (OrderID, ProductID, Quantity) VALUES (orderId, productId, quantity);
    END IF;
END;
$$ LANGUAGE plpgsql;


-- Place order
CREATE OR REPLACE FUNCTION PlaceOrder(customerId INTEGER, creditCardId INTEGER)
RETURNS VOID AS $$
DECLARE
    orderId INTEGER;
BEGIN
    -- Find the pending order
    SELECT OrderID INTO orderId FROM CustomerOrder 
    WHERE CustomerID = customerId AND Status = 'pending' LIMIT 1;

    IF orderId IS NOT NULL THEN
        -- Update the order to placed
        UPDATE CustomerOrder 
        SET Status = 'placed', CreditCardID = creditCardId, OrderDate = NOW()
        WHERE OrderID = orderId;
    END IF;
END;
$$ LANGUAGE plpgsql;


-- Add Credit Card
CREATE OR REPLACE FUNCTION AddCreditCard(
    customerId INTEGER, 
    cardNumber VARCHAR(20), 
    expirationDate DATE, 
    securityCode VARCHAR(5), 
    paymentAddressID INTEGER)
RETURNS VOID AS $$
BEGIN
    INSERT INTO CreditCard (CustomerID, CardNumber, ExpirationDate, SecurityCode, PaymentAddressID)
    VALUES (customerId, cardNumber, expirationDate, securityCode, paymentAddressID);
END;
$$ LANGUAGE plpgsql;


-- Delete Credit Card
CREATE OR REPLACE FUNCTION DeleteCreditCard(creditCardId INTEGER)
RETURNS VOID AS $$
BEGIN
    DELETE FROM CreditCard WHERE CreditCardID = creditCardId;
END;
$$ LANGUAGE plpgsql;


-- Modify Credit Card
CREATE OR REPLACE FUNCTION ModifyCreditCard(
    creditCardId INTEGER,
    newCardNumber VARCHAR(20), 
    newExpirationDate DATE, 
    newSecurityCode VARCHAR(5), 
    newPaymentAddressID INTEGER)
RETURNS VOID AS $$
BEGIN
    UPDATE CreditCard
    SET CardNumber = newCardNumber,
        ExpirationDate = newExpirationDate,
        SecurityCode = newSecurityCode,
        PaymentAddressID = newPaymentAddressID
    WHERE CreditCardID = creditCardId;
END;
$$ LANGUAGE plpgsql;


-- Add Address
CREATE OR REPLACE FUNCTION AddAddress(
    customerId INTEGER, 
    addressLine1 VARCHAR(20), 
    addressLine2 VARCHAR(20), 
    city VARCHAR(20), 
    state VARCHAR(20), 
    zipCode VARCHAR(20), 
    addressType VARCHAR(20))
RETURNS VOID AS $$
BEGIN
    INSERT INTO Address (CustomerID, AddressLine1, AddressLine2, City, State, ZipCode, AddressType)
    VALUES (customerId, addressLine1, addressLine2, city, state, zipCode, addressType);
END;
$$ LANGUAGE plpgsql;


-- Delete Address
CREATE OR REPLACE FUNCTION DeleteAddress(addressId INTEGER)
RETURNS VOID AS $$
BEGIN
    DELETE FROM Address WHERE AddressID = addressId;
END;
$$ LANGUAGE plpgsql;


-- Modify Address
CREATE OR REPLACE FUNCTION ModifyAddress(
    addressId INTEGER,
    newAddressLine1 VARCHAR(20), 
    newAddressLine2 VARCHAR(20), 
    newCity VARCHAR(20), 
    newState VARCHAR(20), 
    newZipCode VARCHAR(20), 
    newAddressType VARCHAR(20))
RETURNS VOID AS $$
BEGIN
    UPDATE Address
    SET AddressLine1 = newAddressLine1,
        AddressLine2 = newAddressLine2,
        City = newCity,
        State = newState,
        ZipCode = newZipCode,
        AddressType = newAddressType
    WHERE AddressID = addressId;
END;
$$ LANGUAGE plpgsql;

