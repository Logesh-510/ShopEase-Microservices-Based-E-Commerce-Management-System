USE shopease_product_db;

SELECT
    id,
    name,
    price,
    stock_quantity,
    status
FROM products
WHERE id = 2;