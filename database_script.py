import sys
import psycopg2
from faker import Faker

# Ensure correct module path
sys.path.append(r"C:\Users\Muhammad Bilal Atiq\AppData\Local\Programs\Python\Python39\Lib\site-packages")

# Initialize Faker
fake = Faker()

# Database connection details (Replace with your actual database credentials)
DB_NAME = "Retail Store"
DB_USER = "postgres"
DB_PASSWORD = "12345"
DB_HOST = "localhost"
DB_PORT = "5432"

# Establish database connection
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Database connection successful.")
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        exit()

# Create tables if they do not exist
# def create_tables(conn):
#     try:
#         cur = conn.cursor()
#         cur.execute("""
#         CREATE TABLE IF NOT EXISTS vendor (
#             vendor_id SERIAL PRIMARY KEY,
#             category VARCHAR(50) UNIQUE
#         );

#         CREATE TABLE IF NOT EXISTS product (
#             product_id SERIAL PRIMARY KEY,
#             product_name VARCHAR(100),
#             category VARCHAR(50),
#             CONSTRAINT fk_product FOREIGN KEY (category) REFERENCES vendor(category)
#         );
#         """)
#         conn.commit()
#         print("Tables created successfully.")
#         cur.close()
#     except Exception as e:
#         print(f"Error creating tables: {e}")
#         conn.rollback()

# Insert dummy vendors
def insert_dummy_vendors(conn, num_vendors):
    try:
        cur = conn.cursor()
        vendor_categories = set()
        
        while len(vendor_categories) < num_vendors:
            vendor_categories.add(fake.unique.word().capitalize())  # Ensure unique category names

        for category in vendor_categories:
            cur.execute("INSERT INTO vendors (category) VALUES (%s) ON CONFLICT DO NOTHING", (category,))

        conn.commit()
        print(f"{num_vendors} vendors inserted successfully.")
        cur.close()
    except Exception as e:
        print(f"Error inserting vendors: {e}")
        conn.rollback()

# # Insert dummy products
# def insert_dummy_products(conn, num_products):
#     try:
#         cur = conn.cursor()
#         cur.execute("SELECT category FROM vendor")
#         vendor_categories = [row[0] for row in cur.fetchall()]  # Get all existing categories

#         if not vendor_categories:
#             print("No vendors available. Insert vendors first.")
#             return

#         for _ in range(num_products):
#             product_name = fake.company()  # Generate a fake company/product name
#             category = random.choice(vendor_categories)  # Pick a random category from vendor table
#             cur.execute(
#                 "INSERT INTO product (product_name, category) VALUES (%s, %s)",
#                 (product_name, category)
#             )

#         conn.commit()
#         print(f"{num_products} products inserted successfully.")
#         cur.close()
#     except Exception as e:
#         print(f"Error inserting products: {e}")
#         conn.rollback()

# Main function
def main():
    conn = connect_to_db()
    try:
        # create_tables(conn)
        insert_dummy_vendors(conn, num_vendors=10)  # Insert 10 vendors
        # insert_dummy_products(conn, num_products=50)  # Insert 50 products
    finally:
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()
