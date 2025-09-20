import psycopg2
import pandas as pd

# 1. Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="etl_project",
    user="postgres",
    password="#####"   # put your password here
)
cur = conn.cursor()
print("Connection successful!")

# 2. Load transformed CSV
df = pd.read_csv("data/transformed_products.csv")  # adjust path if needed
print("CSV loaded, inserting data...")

# 3. Insert into products table
for i, row in df.iterrows():
    # Insert product row
    cur.execute("""
        INSERT INTO products (title, price, discount_pct, stock, sku)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING product_id
    """, (
        row['title'],
        row['price'],
        row['discountPercentage'],  # matches CSV column
        row['stock'],
        row['sku']
    ))
    product_id = cur.fetchone()[0]  # get generated product_id

    # Insert product_details row
    cur.execute("""
        INSERT INTO product_details (
            product_id, weight, width, height, depth,
            warranty_info, shipping_info, availability_status,
            return_policy, min_order_qty, comment
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        product_id,
        row['weight'],
        row['width'],
        row['height'],
        row['depth'],
        row['warrantyInformation'],
        row['shippingInformation'],
        row['availabilityStatus'],
        row['returnPolicy'],
        row['minimumOrderQuantity'],
        row['comment']
    ))

    # Insert category (if not exists)
    cur.execute("""
        INSERT INTO categories (category_name)
        VALUES (%s)
        ON CONFLICT (category_name) DO NOTHING
        RETURNING category_id
    """, (row['category'],))
    category_result = cur.fetchone()
    if category_result:
        category_id = category_result[0]
    else:
        cur.execute("SELECT category_id FROM categories WHERE category_name = %s", (row['category'],))
        category_id = cur.fetchone()[0]

    # Insert subcategory (if not exists)
    cur.execute("""
        INSERT INTO subcategories (category_id, subcategory_name)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
        RETURNING subcategory_id
    """, (category_id, row['subcategory']))
    subcat_result = cur.fetchone()
    if subcat_result:
        subcategory_id = subcat_result[0]
    else:
        cur.execute("""
            SELECT subcategory_id FROM subcategories 
            WHERE category_id = %s AND subcategory_name = %s
        """, (category_id, row['subcategory']))
        subcategory_id = cur.fetchone()[0]

    # Insert into product_category_map
    cur.execute("""
        INSERT INTO product_category_map (product_id, category_id, subcategory_id)
        VALUES (%s, %s, %s)
    """, (product_id, category_id, subcategory_id))

# 4. Commit changes and close
conn.commit()
cur.close()
conn.close()
print("Data loaded successfully!")

