import sqlite3
from datetime import datetime

DATABASE_NAME = "shop.db"


def connect():
    """Return a connection to the SQLite database."""
    return sqlite3.connect(DATABASE_NAME)


def create_users_table():
    """Create the users table if it does not already exist."""

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def create_default_admin():
    """Create the default administrator account."""

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE username = ?",
        ("admin",)
    )

    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        """, (
            "admin",
            "admin123",
            "Owner"
        ))

        conn.commit()

    conn.close()


def create_user(username, password, role="Employee"):
    """Create a new user."""

    conn = connect()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        """, (
            username,
            password,
            role
        ))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def verify_user(username, password):
    """Verify a user's login credentials."""

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, username, role
        FROM users
        WHERE username = ?
        AND password = ?
    """, (
        username,
        password
    ))

    user = cursor.fetchone()

    conn.close()

    return user


def username_exists(username):
    """Return True if the username already exists."""

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE username = ?",
        (username,)
    )

    exists = cursor.fetchone() is not None

    conn.close()

    return exists


def get_user_role(username):
    """Return the user's role."""

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT role FROM users WHERE username = ?",
        (username,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return None


def create_products_table():
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER,
            category TEXT,
            supplier TEXT,
            price REAL
        )
    """)

    conn.commit()
    conn.close()


def add_product(name, quantity, category, supplier, price):
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO products (name, quantity, category, supplier, price)
        VALUES (?, ?, ?, ?, ?)
    """, (name, quantity, category, supplier, price))

    conn.commit()
    conn.close()


def delete_product(product_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM products
        WHERE id = ?
    """, (product_id,))

    conn.commit()
    conn.close()


def update_product(product_id, name, quantity, category, supplier, price):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE products
        SET name = ?,
            quantity = ?,
            category = ?,
            supplier = ?,
            price = ?
        WHERE id = ?
    """, (
        name,
        quantity,
        category,
        supplier,
        price,
        product_id
    ))

    conn.commit()
    conn.close()


def get_products():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.id,
            p.name,
            p.quantity,
            p.category,
            p.supplier,
            s.phone,
            s.email,
            p.price
        FROM products AS p
        LEFT JOIN suppliers AS s
            ON p.supplier = s.name
        ORDER BY p.id ASC
    """)

    products = cursor.fetchall()

    conn.close()

    return products


def get_low_stock_products():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, quantity
        FROM products
        WHERE quantity <= 5
        ORDER BY quantity ASC
    """)

    products = cursor.fetchall()

    conn.close()

    return products

# categories


def create_categories_table():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    conn.commit()
    conn.close()


def add_category(name):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO categories (name)
        VALUES (?)
    """, (name,))

    conn.commit()
    conn.close()


def get_categories():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM categories
    """)

    categories = cursor.fetchall()

    conn.close()

    return categories


def delete_category(category_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM categories
        WHERE id = ?
    """, (category_id,))

    conn.commit()
    conn.close()


def update_category(category_id, name):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE categories
        SET name = ?
        WHERE id = ?
    """, (
        name,
        category_id
    ))

    conn.commit()
    conn.close()


def get_category_product_count(category):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM products
        WHERE category = ?
    """, (category,))

    count = cursor.fetchone()[0]

    conn.close()

    return count
# sales


def update_product_stock(product_id, new_stock):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE products
        SET quantity = ?
        WHERE id = ?
        """,
        (new_stock, product_id)
    )

    conn.commit()
    conn.close()


def add_sale(product_id, quantity, total_price):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        INSERT INTO sales
        (product_id, quantity, total_price, date)
        VALUES (?, ?, ?, ?)
        """,
        (
            product_id,
            quantity,
            total_price,
            date
        )
    )

    conn.commit()
    conn.close()


def create_sales_table():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        quantity INTEGER,
        total_price REAL,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


def get_sales():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            sales.id,
            products.name,
            sales.quantity,
            sales.total_price,
            sales.date
        FROM sales
        JOIN products
            ON sales.product_id = products.id
        ORDER BY sales.id
    """)

    sales = cursor.fetchall()

    conn.close()

    return sales


def delete_sale(sale_id):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM sales
        WHERE id = ?
    """, (sale_id,))

    conn.commit()
    conn.close()
# reports


def get_most_sold_products():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT products.name, SUM(sales.quantity)
        FROM sales
        JOIN products
        ON sales.product_id = products.id
        GROUP BY products.name
        ORDER BY SUM(sales.quantity) DESC
        LIMIT 5
    """)

    data = cursor.fetchall()

    conn.close()

    return data


def get_total_revenue():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT SUM(total_price)
        FROM sales
        """
    )

    result = cursor.fetchone()[0]

    conn.close()

    return result if result else 0


def get_total_sales():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM sales
        """
    )

    result = cursor.fetchone()[0]

    conn.close()

    return result


def get_product_count():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM products
        """
    )

    result = cursor.fetchone()[0]

    conn.close()

    return result


def get_low_stock_count():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM products
        WHERE quantity <= 5
        """
    )

    result = cursor.fetchone()[0]

    conn.close()

    return result

# =========================
# Suppliers Table
# =========================


def create_suppliers_table():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            phone TEXT,

            email TEXT,

            address TEXT

        )
    """)

    conn.commit()
    conn.close()


# =========================
# Add Supplier
# =========================

def add_supplier(name, phone, email, address):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO suppliers
        (
            name,
            phone,
            email,
            address
        )

        VALUES (?, ?, ?, ?)

    """,
                   (
                       name,
                       phone,
                       email,
                       address
                   ))

    conn.commit()
    conn.close()


# =========================
# Get Suppliers
# =========================

def get_suppliers():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM suppliers
        ORDER BY id DESC
    """)

    suppliers = cursor.fetchall()

    conn.close()

    return suppliers


# =========================
# Update Supplier
# =========================

def update_supplier(
        supplier_id,
        name,
        phone,
        email,
        address
):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE suppliers

        SET
            name = ?,
            phone = ?,
            email = ?,
            address = ?

        WHERE id = ?

    """,
                   (
                       name,
                       phone,
                       email,
                       address,
                       supplier_id
                   ))

    conn.commit()
    conn.close()


# =========================
# Delete Supplier
# =========================

def delete_supplier(supplier_id):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM suppliers

        WHERE id = ?

    """,
                   (
                       supplier_id,
                   ))

    conn.commit()
    conn.close()


# =========================
# Search Suppliers
# =========================

def search_suppliers(keyword):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *

        FROM suppliers

        WHERE name LIKE ?
        OR phone LIKE ?
        OR email LIKE ?

        ORDER BY id DESC

    """,
                   (
                       f"%{keyword}%",
                       f"%{keyword}%",
                       f"%{keyword}%"
                   ))

    results = cursor.fetchall()

    conn.close()

    return results


def initialize_database():
    """Initialize the application database."""

    create_users_table()
    create_products_table()
    create_categories_table()
    create_sales_table()
    create_default_admin()
    create_suppliers_table()


if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully.")
