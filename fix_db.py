import sqlite3

conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

# View all products
cursor.execute("SELECT id, name, supplier, price FROM products")
print("=== ALL PRODUCTS ===")
for row in cursor.fetchall():
    print(f"ID: {row[0]}, Name: {row[1]}, Supplier: {row[2]}, Price: {row[3]}")

print("\n" + "="*50 + "\n")

# Enter the product ID and correct price
product_id = input("Enter product ID to fix: ")
correct_price = input("Enter correct price: ")

cursor.execute("UPDATE products SET price = ? WHERE id = ?",
               (correct_price, product_id))
conn.commit()

print(f"✓ Fixed! Product {product_id} price is now {correct_price}")

conn.close()
