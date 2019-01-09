/*
Author: Zayne Jeffries
Date: 09/01/2019
Descript: Retrieves data related to shippers, suppliers and products
*/
DROP TABLE shipInfo;
DROP TABLE supplyInfo;
DROP TABLE prodInfo;
CREATE TABLE shipInfo;
CREATE TABLE supplyInfo;
CREATE TABLE prodInfo;
/*handling table for data related to shippers*/
SELECT * INTO TABLE shipInfo FROM shippers
WHERE phone IN (SELECT phone FROM shippers
				WHERE shipper_id < 4);
/*handling table for data related to suppliers*/
SELECT company_name, address, city INTO TABLE supplyInfo FROM suppliers
WHERE country LIKE '%USA%' OR country LIKE '%uk%';
/*handling table for data related to products*/
SELECT product_name, unit_price INTO TABLE prodInfo FROM products
WHERE supplier_id IN (SELECT supplier_id FROM products
					WHERE supplier_id%2 = 0)
GROUP BY supplier_id, product_name, unit_price;
