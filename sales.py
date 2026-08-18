import customtkinter as ctk
from tksheet import Sheet
from database import get_products, update_product_stock, add_sale, get_sales, delete_sale
from datetime import datetime
from tkinter import messagebox


def parse_price(price):
    if isinstance(price, str):
        price = price.replace(",", ".")
    return float(price)


class SalesPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.cart = []

        label = ctk.CTkLabel(
            self,
            text="Sales Page",
            font=("Inter", 28, "bold")
        )
        label.pack(pady=10)

        # Selected product frame
        self.product_frame = ctk.CTkFrame(
            self,
            height=280
        )
        self.product_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.product_frame.pack_propagate(False)

        # info frame
        self.info_frame = ctk.CTkFrame(
            self.product_frame,
            fg_color="transparent",

        )
        self.info_frame.pack(fill="both",
                             side="left",
                             expand=True,
                             padx=20,
                             pady=(20, 10))

        self.product_label = ctk.CTkLabel(
            self.info_frame,
            text="No Product Selected",
            font=("Arial", 24, "bold")
        )
        self.product_label.pack(expand=True)

        self.button_frame = ctk.CTkFrame(
            self.product_frame,
            fg_color="transparent"
        )
        self.button_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )
        choose_button = ctk.CTkButton(
            self.button_frame,
            text="Choose Product",
            font=("Arial", 15, "bold"),
            corner_radius=8,
            fg_color="#1f6aa5",
            hover_color="#155a8a",
            text_color="#ffffff",
            border_width=0,
            command=self.open_product_window
        )
        choose_button.pack(expand=True)

        # sales frame
        self.sales_frame = ctk.CTkFrame(
            self,
            height=380
        )
        self.sales_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )
        self.sales_frame.pack_propagate(False)

        self.sheet = Sheet(
            self.sales_frame,
            headers=[
                "Sale ID",
                "Product",
                "Quantity",
                "Total Price",
                "Date"
            ]
        )

        self.sheet.change_theme(
            "dark"
        )

        self.sheet.set_options(
            header_bg="#1f1f1f",
            header_fg="#ffffff",
            index_bg="#1f1f1f",
            index_fg="#ffffff",
            table_bg="#2b2b2b",
            table_fg="#ffffff",
            selected_cells_bg="#1f6aa5",
            selected_cells_fg="#ffffff"
        )

        self.sheet.align_columns(
            "center"
        )

        self.sheet.align_rows(
            "center"
        )

        self.sheet.column_width(
            column=0,
            width=80
        )

        self.sheet.column_width(
            column=1,
            width=120
        )

        self.sheet.column_width(
            column=2,
            width=120
        )

        self.sheet.column_width(
            column=3,
            width=400
        )
        self.sheet.enable_bindings(
            (
                "single_select",
                "row_select",
                "arrowkeys",
                "right_click_popup_menu",
                "rc_select"
            )
        )

        self.table_frame = ctk.CTkFrame(
            self.sales_frame,
            fg_color="transparent"
        )

        self.table_frame.pack(
            fill="both",
            expand=True
        )

        self.sheet.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.actions_frame = ctk.CTkFrame(
            self.table_frame,
            fg_color="transparent"
        )

        self.actions_frame.pack(
            side="right",
            padx=10
        )

        delete_btn = ctk.CTkButton(
            self.actions_frame,
            text="Delete",
            width=80,
            height=40,
            font=("Montserrat", 15, "bold"),
            fg_color="#D32F2F",
            hover_color="#B71C1C",
            command=self.delete_page_sale
        )

        delete_btn.pack(
            pady=10
        )
        self.sheet.set_sheet_data(self.load_sales_data())

        self.quantity = 1

        self.quantity_frame = ctk.CTkFrame(
            self.info_frame,
            fg_color="transparent"
        )

        self.plus_btn = ctk.CTkButton(
            self.quantity_frame,
            text="+",
            font=("Arial", 24, "bold"),
            height=40,
            width=40,
            fg_color="#2FA572",
            hover_color="#238052",
            command=self.add_btn
        )

        self.minus_btn = ctk.CTkButton(
            self.quantity_frame,
            text="-",
            font=("Arial", 24, "bold"),
            height=40,
            width=40,
            hover_color="#B52B27",
            fg_color="#D9534F",
            command=self.minus_button
        )

        self.quantity_label = ctk.CTkLabel(
            self.quantity_frame,
            text=self.quantity,
            font=("Arial", 22, "bold"),
            width=50
        )

        self.confirm_btn = ctk.CTkButton(
            self.info_frame,
            text="Confirm",
            font=("Arial", 20, "bold"),
            width=60,
            height=40,
            command=self.confirm_sale,
            corner_radius=16,
            fg_color="transparent",
            border_color="#1f6aa5",
            border_width=2
        )

    def open_product_window(self):
        self.product_window = ctk.CTkToplevel(self)

        self.product_window.title("Select Product")
        self.product_window.geometry("500x400")

        title = ctk.CTkLabel(
            self.product_window,
            text="Select Product",
            font=("Arial", 20, "bold")
        )

        title.pack(pady=10)

        self.product_list = ctk.CTkScrollableFrame(
            self.product_window
        )

        self.product_list.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )
        self.load_products()

    def load_products(self):

        products = get_products()

        for product in products:

            button = ctk.CTkButton(
                self.product_list,
                text=product[1],
                command=lambda p=product: self.select_product(p)
            )

            button.pack(
                fill="x",
                pady=5
            )

    def select_product(self, product):

        self.selected_product = product

        self.quantity = 1

        self.quantity_label.configure(
            text="1"
        )

        self.product_label.configure(
            text=f"{product[1]}\nStock left : {product[2]}\nTotal price : {product[7]} DH"
        )

        self.quantity_frame.pack(pady=10)

        self.plus_btn.pack(side='left', padx=5)
        self.plus_btn.configure(state="normal")

        self.quantity_label.pack(side="left", padx=10)

        self.minus_btn.pack(side="left", padx=5)

        self.confirm_btn.pack(side="left", padx=5)
        self.confirm_btn.configure(state="normal")

        self.product_window.destroy()

    def add_btn(self):

        if self.quantity < self.selected_product[2]:

            self.quantity += 1

            self.quantity_label.configure(
                text=str(self.quantity)
            )

            name = self.selected_product[1]
            stock = self.selected_product[2] - self.quantity

            price = parse_price(self.selected_product[7])*self.quantity

            self.product_label.configure(
                text=f"{name}\nStock left : {stock}\nTotal price : {price:.2f} DH"
            )

        if self.selected_product[2] - self.quantity == 0:
            self.plus_btn.configure(state="disabled")

    def minus_button(self):
        if self.quantity > 1:

            self.quantity -= 1

            self.quantity_label.configure(
                text=str(self.quantity)
            )

        name = self.selected_product[1]
        stock = self.selected_product[2]-self.quantity
        price = parse_price(self.selected_product[7])*self.quantity

        self.product_label.configure(
            text=f"{name}\nStock left : {stock}\nTotal price : {price:.2f} DH"
        )
        if stock > 0:
            self.plus_btn.configure(state="normal")

    def confirm_sale(self):

        # No product selected
        if self.selected_product is None:
            messagebox.showwarning(
                "No Product",
                "Please select a product first."
            )
            return

        current_stock = self.selected_product[2]

        # Quantity cannot be 0
        if self.quantity <= 0:
            messagebox.showwarning(
                "Invalid Quantity",
                "Please select a quantity greater than 0."
            )
            return

        # Product out of stock
        if current_stock <= 0:
            messagebox.showwarning(
                "Out of Stock",
                "This product is currently out of stock."
            )
            return

        # Quantity exceeds stock
        if self.quantity > current_stock:
            messagebox.showwarning(
                "Not Enough Stock",
                f"Only {current_stock} item(s) available."
            )
            return

        product = {
            "id": self.selected_product[0],
            "quantity": self.quantity,
            "stock": current_stock,
            "price": parse_price(self.selected_product[7]) * self.quantity
        }

        self.cart.append(product)

        for product in self.cart:

            product_id = product["id"]
            quantity = product["quantity"]

            new_stock = product["stock"] - quantity

            update_product_stock(
                product_id,
                new_stock
            )

            add_sale(
                product_id,
                quantity,
                product["price"]
            )

        self.sheet.set_sheet_data(
            self.load_sales_data()
        )

        self.sheet.refresh()

        self.cart.clear()

    def delete_page_sale(self):

        selected = self.sheet.get_currently_selected()

        if selected is None:
            return

        row = selected.row
        sale = self.sheet.get_row_data(row)
        sale_id = sale[0]

        delete_sale(sale_id)

        # Reload the table
        self.sheet.set_sheet_data(self.load_sales_data())

        # Clear any old selection
        self.sheet.deselect("all")

        self.sheet.refresh()

    def load_sales_data(self):

        sales = get_sales()

        return [
            [sale[0], sale[1], sale[2], f"{sale[3]:.2f}", sale[4]]
            for sale in sales
        ]
