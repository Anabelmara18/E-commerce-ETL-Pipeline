CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    price NUMERIC(10,2),
    discount_pct NUMERIC(5,2),  
    stock INT,
    sku TEXT UNIQUE
);

CREATE TABLE product_details (
    detail_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(product_id) ON DELETE CASCADE,
    weight NUMERIC(10,2),
    width NUMERIC(10,2),
    height NUMERIC(10,2),
    depth NUMERIC(10,2),
    warranty_info TEXT,         
    shipping_info TEXT,
    availability_status TEXT,
    return_policy TEXT,
    min_order_qty INT,          
    comment TEXT
);

CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name TEXT UNIQUE
);

CREATE TABLE subcategories (
    subcategory_id SERIAL PRIMARY KEY,
    category_id INT REFERENCES categories(category_id) ON DELETE CASCADE,
    subcategory_name TEXT
);

CREATE TABLE product_category_map (
    map_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(product_id) ON DELETE CASCADE,
    category_id INT REFERENCES categories(category_id) ON DELETE CASCADE,
    subcategory_id INT REFERENCES subcategories(subcategory_id) ON DELETE CASCADE
);
