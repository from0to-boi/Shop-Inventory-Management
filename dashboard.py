import os
import sys

def resource_path(relative_path):
    """Get the correct path for development and PyInstaller."""
    
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)

    return os.path.join(os.path.abspath("."), relative_path)

import ctypes

myappid = "mycompany.shopinventorymanager.1.0"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

from PIL import Image
import customtkinter as ctk
import os
import webbrowser
import urllib.parse
from tkinter import messagebox
from products import Products
from categories import Categories
from sales import SalesPage
from reports import ReportsPage
from suppliers import SuppliersPage
from settings import SettingsPage
from users import UsersPage
from database import get_products, get_categories


class Dashboard(ctk.CTk):

    def __init__(self, user):
        super().__init__()

        self.user_id = user[0]
        self.username = user[1]
        self.role = user[2]

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.title("Shop Inventory Management")
        self.geometry("1200x700")
        self.iconbitmap(resource_path("Icons/icon.ico"))

        # ==========================
        # Configure window grid
        # ==========================

        self.grid_rowconfigure(0, weight=0)   # Header
        self.grid_rowconfigure(1, weight=1)   # Content

        self.grid_columnconfigure(0, weight=1)

        # ==========================
        # Header
        # ==========================

        self.header = ctk.CTkFrame(
            self, height=70, corner_radius=0)
        self.header.grid(row=0, column=0, sticky="ew")

        self.header.grid_propagate(False)

        title = ctk.CTkLabel(
            self.header,
            text="Inventory Manager",
            font=("Arial", 24, "bold")
        )

        title.pack(pady=20)

        # ==========================
        # Content Frame
        # ==========================

        self.content = ctk.CTkFrame(self, corner_radius=12)
        self.content.grid(row=1, column=0, sticky="nsew")

        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=0)
        self.content.grid_columnconfigure(1, weight=1)

        # ==========================
        # Sidebar
        # ==========================

        self.sidebar = ctk.CTkFrame(self.content, width=220)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.sidebar.grid_propagate(False)

        self.main = ctk.CTkFrame(self.content)
        self.main.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        DashboardHome(self.main).pack(fill="both", expand=True)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        buttons = [
            "Dashboard",
            "Products",
            "Categories",
            "Suppliers",
            "Sales",
            "Reports",
            "Users",
            "Settings"
        ]

        icons_files = [
            "dashboard.png",
            "products.png",
            "categories.png",
            "supplier.png",
            "sales.png",
            "reports.png",
            "user.png",
            "setting.png"
        ]

        self.icons = []

        for icon in icons_files:
            path = os.path.join(BASE_DIR, "Icons", icon)

            img = ctk.CTkImage(
                light_image=Image.open(path),
                dark_image=Image.open(path),
                size=(22, 22)
            )
            self.icons.append(img)

        for text, icon in zip(buttons, self.icons):

            command = None

            if text == "Products":
                def command():
                    self.show_page(Products)

            elif text == "Categories":
                def command():
                    self.show_page(Categories)

            elif text == "Dashboard":
                def command():
                    self.show_page(DashboardHome)
            elif text == "Sales":
                def command():
                    self.show_page(SalesPage)
            elif text == "Reports":
                def command():
                    self.show_page(ReportsPage)
            elif text == "Suppliers":
                def command():
                    self.show_page(SuppliersPage)
            elif text == "Settings":
                def command():
                    self.show_page(SettingsPage)
            elif text == "Users":
                def command():
                    self.show_page(UsersPage)
            btn = ctk.CTkButton(
                self.sidebar,
                text="      " + text,
                image=icon,
                compound="left",
                width=180,
                height=40,
                anchor="w",
                font=("Inter", 15, "bold"),
                corner_radius=12,
                fg_color="transparent",
                hover_color="#1f6aa5",
                text_color="#ffffff",
                command=command
            )
            btn.pack(pady=8, padx=20)

    def show_page(self, page):
        print("show_page called")
        # remove old content
        for widget in self.main.winfo_children():
            widget.destroy()

        # show new page
        new_page = page(self.main)
        new_page.pack(fill="both", expand=True)

    def create_stat_card(self, title, value):

        card = ctk.CTkFrame(
            self.stats_frame,
            width=220,
            height=120,
            corner_radius=15
        )

        card.pack(
            side="left",
            padx=10
        )

        card.pack_propagate(False)

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 16)
        )

        title_label.pack(
            pady=(20, 5)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 28, "bold")
        )

        value_label.pack()


class DashboardHome(ctk.CTkFrame):

    LOW_STOCK_THRESHOLD = 5

    def __init__(self, master):
        super().__init__(master)

        label = ctk.CTkLabel(
            self,
            text="Dashboard",
            font=("Arial", 28, "bold")
        )
        label.pack(anchor="w", padx=20, pady=20)

        # ==========================
        # Stat cards
        # ==========================

        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.pack(fill="x", padx=20, pady=10)

        self.stats_frame.grid_columnconfigure(
            (0, 1, 2, 3), weight=1, uniform="cards")

        self.value_labels = {}

        card_specs = [
            ("Products",   "0",      "#3B82F6"),  # blue
            ("Categories", "0",      "#8B5CF6"),  # purple
            ("Total Stock", "0",     "#10B981"),  # green
            ("Stock Value", "0 DH",  "#F59E0B"),  # amber
        ]

        for i, (title, value, color) in enumerate(card_specs):
            self.create_stat_card(i, title, value, color)

        # ==========================
        # Low stock section
        # ==========================

        low_stock_label = ctk.CTkLabel(
            self,
            text="⚠ Low Stock Alerts",
            font=("Arial", 20, "bold")
        )
        low_stock_label.pack(anchor="w", padx=20, pady=(20, 5))

        self.low_stock_frame = ctk.CTkFrame(self, corner_radius=15)
        self.low_stock_frame.pack(
            fill="both", expand=True, padx=20, pady=(0, 20))

        self.load_stats()

    def create_stat_card(self, column, title, value, color):
        card = ctk.CTkFrame(
            self.stats_frame,
            height=120,
            corner_radius=15
        )
        card.grid(row=0, column=column, sticky="ew", padx=10)
        card.grid_propagate(False)
        card.configure(height=120)

        # colored accent strip on the left
        accent = ctk.CTkFrame(card, width=6, corner_radius=0, fg_color=color)
        accent.pack(side="left", fill="y")

        text_frame = ctk.CTkFrame(card, fg_color="transparent")
        text_frame.pack(side="left", fill="both",
                        expand=True, padx=(15, 10), pady=15)

        title_label = ctk.CTkLabel(
            text_frame,
            text=title,
            font=("Arial", 14),
            text_color="#A0A0A0",
            anchor="w"
        )
        title_label.pack(anchor="w")

        value_label = ctk.CTkLabel(
            text_frame,
            text=value,
            font=("Arial", 26, "bold"),
            anchor="w"
        )
        value_label.pack(anchor="w", pady=(8, 0))

        self.value_labels[title] = value_label

    def load_stats(self):
        products = get_products()      # rows: (id, name, quantity, category, price)
        categories = get_categories()  # rows: (id, name)

        product_count = len(products)
        category_count = len(categories)

        total_stock = 0
        stock_value = 0.0
        low_stock_products = []

        print("---- DEBUG: raw product rows ----")

        for product in products:
            print(product)

            product_id, name, quantity, category, supplier, supplier_phone, supplier_email, price = product
            print(
                f"quantity={repr(quantity)} ({type(quantity)}), price={repr(price)} ({type(price)})")

            quantity = self.to_float(quantity)
            price = self.to_float(price)

            total_stock += quantity
            stock_value += quantity * price

            if quantity < self.LOW_STOCK_THRESHOLD:
                low_stock_products.append(
                    (
                        name,
                        quantity,
                        supplier_phone or "",
                        supplier_email or ""
                    )
                )

        print("---- END DEBUG ----")

        self.value_labels["Products"].configure(text=str(product_count))
        self.value_labels["Categories"].configure(text=str(category_count))
        self.value_labels["Total Stock"].configure(text=str(int(total_stock)))
        self.value_labels["Stock Value"].configure(
            text=f"{stock_value:.2f} DH")

        self.render_low_stock(low_stock_products)

    @staticmethod
    def to_float(value):
        if value is None:
            return 0.0

        if isinstance(value, (int, float)):
            return float(value)

        text = str(value).strip()

        if text == "":
            return 0.0

        # normalize a comma decimal separator (e.g. "10,5" -> "10.5")
        text = text.replace(",", ".")

        try:
            return float(text)
        except ValueError:
            print(
                f"!! could not convert {repr(value)} to float, defaulting to 0")
            return 0.0

    def render_low_stock(self, low_stock_products):

        for widget in self.low_stock_frame.winfo_children():
            widget.destroy()

        if not low_stock_products:
            ctk.CTkLabel(
                self.low_stock_frame,
                text="✓ All products are sufficiently stocked.",
                font=("Arial", 14),
                text_color="#A0A0A0"
            ).pack(pady=20)
            return

        for name, quantity, supplier_phone, supplier_email in low_stock_products:

            row = ctk.CTkFrame(
                self.low_stock_frame,
                height=50,
                corner_radius=10
            )

            row.pack(
                fill="x",
                padx=15,
                pady=5
            )

            ctk.CTkLabel(
                row,
                text=name,
                font=("Arial", 16, "bold")
            ).pack(
                side="left",
                padx=20
            )

            ctk.CTkLabel(
                row,
                text=f"{int(quantity)} left ⚠",
                font=("Arial", 16, "bold"),
                text_color="#D9534F"
            ).pack(
                side="right",
                padx=10
            )

            ctk.CTkButton(
                row,
                text="Contact Supplier",
                width=140,
                command=lambda p=supplier_phone, e=supplier_email, n=name, q=quantity:
                    self.contact_supplier(p, e, n, q)
            ).pack(
                side="right",
                padx=10
            )

    def contact_supplier(self, phone, email, product, quantity):

        window = ctk.CTkToplevel(self)
        window.title("Contact Supplier")
        window.geometry("350x250")
        window.resizable(False, False)

        ctk.CTkLabel(
            window,
            text=f"Contact Supplier\n{email}",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        ctk.CTkButton(
            window,
            text="💬 WhatsApp",
            width=200,
            height=40,
            command=lambda: self.open_whatsapp(phone, product, quantity)
        ).pack(pady=10)

        ctk.CTkButton(
            window,
            text="✉ Email",
            width=200,
            height=40,
            command=lambda: self.open_email(email, product, quantity)
        ).pack(pady=10)

    def open_whatsapp(self, phone, product, quantity):
        phone = phone.replace(" ", "").replace("+", "")
        message = f"""
    Salam,

    We are running low on {product}.
    Current stock: {quantity} units.

    Can you provide more stock?

    Thank you.
    """

        url = (
            f"https://wa.me/{phone}"
            f"?text={urllib.parse.quote(message)}"
        )

        webbrowser.open(url)

    def open_email(self, email, product, quantity):

        subject = f"Stock Request - {product}"

        body = f"""Hello,

    We are running low on {product}.
    Current stock: {quantity} units.

    Please let us know availability and price.

    Thank you.
    """

        url = (
            "https://mail.google.com/mail/?view=cm"
            f"&to={urllib.parse.quote(email)}"
            f"&su={urllib.parse.quote(subject)}"
            f"&body={urllib.parse.quote(body)}"
        )

        webbrowser.open(url)
