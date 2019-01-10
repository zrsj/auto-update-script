CREATE TABLE shipInfo
CREATE TABLE supplyInfo
CREATE TABLE prodInfo
SELECT * INTO TABLE shipInfo FROM shippers
WHERE phone IN (SELECT phone FROM shippers
WHERE shipper_id < 4)
SELECT company_name, address, city INTO TABLE supplyInfo FROM suppliers
WHERE country LIKE '%USA%' OR country LIKE '%uk%'
SELECT product_name, unit_price INTO TABLE prodInfo FROM products
WHERE supplier_id IN (SELECT supplier_id FROM products
WHERE supplier_id%2 = 0)
GROUP BY supplier_id, product_name, unit_price
