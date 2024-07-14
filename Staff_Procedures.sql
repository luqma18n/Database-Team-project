-- Staff Procedures

-- Add Product
CREATE OR REPLACE FUNCTION AddProduct(
    name VARCHAR(20), 
    category VARCHAR(20), 
    type VARCHAR(20), 
    brand VARCHAR(20), 
    size VARCHAR(20), 
    description TEXT, 
    price DECIMAL(10, 2))
RETURNS VOID AS $$
BEGIN
    INSERT INTO Product (Name, Category, Type, Brand, Size, Description, Price)
    VALUES (name, category, type, brand, size, description, price);
END;
$$ LANGUAGE plpgsql;


-- Delete Product
CREATE OR REPLACE FUNCTION DeleteProduct(productId INTEGER)
RETURNS VOID AS $$
BEGIN
    DELETE FROM Product WHERE ProductID = productId;
END;
$$ LANGUAGE plpgsql;


-- Modify Product
CREATE OR REPLACE FUNCTION ModifyProduct(
    productId INTEGER,
    newName VARCHAR(20), 
    newCategory VARCHAR(20), 
    newType VARCHAR(20), 
    newBrand VARCHAR(20), 
    newSize VARCHAR(20), 
    newDescription TEXT, 
    newPrice DECIMAL(10, 2))
RETURNS VOID AS $$
BEGIN
    UPDATE Product
    SET Name = newName,
        Category = newCategory,
        Type = newType,
        Brand = newBrand,
        Size = newSize,
        Description = newDescription,
        Price = newPrice
    WHERE ProductID = productId;
END;
$$ LANGUAGE plpgsql;


-- Add Stock
CREATE OR REPLACE FUNCTION AddStock(
    productId INTEGER, 
    warehouseId INTEGER, 
    quantity INTEGER)
RETURNS VOID AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM Stock WHERE ProductID = productId AND WarehouseID = warehouseId) THEN
        UPDATE Stock SET Quantity = Quantity + quantity WHERE ProductID = productId AND WarehouseID = warehouseId;
    ELSE
        INSERT INTO Stock (ProductID, WarehouseID, Quantity) VALUES (productId, warehouseId, quantity);
    END IF;
END;
$$ LANGUAGE plpgsql;

