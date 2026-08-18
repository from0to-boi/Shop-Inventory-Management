import customtkinter as ctk
from tkinter import messagebox
from tksheet import Sheet

from database import (
    add_product,
    get_products,
    delete_product,
    update_product,
    get_categories,
    get_suppliers
)


# =============================================================
# PRODUCTS PAGE
# =============================================================

class Products(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="transparent"
        )
        self.selected_product = None

        self.parent = parent
        self.selected_product = None

        self.create_ui()
        self.load_products()

    # =========================================================
    # MAIN UI
    # =========================================================

    def create_ui(self):

        # =====================================================
        # HEADER
        # =====================================================

        header = ctk.CTkFrame(
            self,
            height=85,
            corner_radius=20,
            fg_color="#242424"
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(15, 10)
        )

        header.pack_propagate(False)

        # Header left

        header_left = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        header_left.pack(
            side="left",
            padx=25,
            pady=15
        )

        title = ctk.CTkLabel(
            header_left,
            text="📦 Products",
            font=("Arial", 25, "bold")
        )

        title.pack(
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            header_left,
            text="Manage your inventory and product information",
            text_color="#9CA3AF",
            font=("Arial", 12)
        )

        subtitle.pack(
            anchor="w",
            pady=(2, 0)
        )

        # Add product

        add_btn = ctk.CTkButton(
            header,
            text="＋  Add Product",
            width=150,
            height=42,
            corner_radius=12,
            font=("Arial", 13, "bold"),
            command=self.add_product
        )

        add_btn.pack(
            side="right",
            padx=25
        )

        # =====================================================
        # STATISTICS
        # =====================================================

        stats_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        stats_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        # Total products

        self.total_card = self.create_stat_card(
            stats_frame,
            "📦",
            "Total Products"
        )

        self.total_card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 7)
        )

        # Total stock

        self.stock_card = self.create_stat_card(
            stats_frame,
            "📊",
            "Total Stock"
        )

        self.stock_card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=7
        )

        # Low stock

        self.low_stock_card = self.create_stat_card(
            stats_frame,
            "⚠",
            "Low Stock"
        )

        self.low_stock_card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=7
        )

        # Inventory value

        self.value_card = self.create_stat_card(
            stats_frame,
            "💰",
            "Inventory Value"
        )

        self.value_card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(7, 0)
        )

        # =====================================================
        # SEARCH / ACTION BAR
        # =====================================================

        search_card = ctk.CTkFrame(
            self,
            height=70,
            corner_radius=18,
            fg_color="#242424"
        )

        search_card.pack(
            fill="x",
            padx=20,
            pady=8
        )

        search_card.pack_propagate(False)

        # Search

        self.search_entry = ctk.CTkEntry(
            search_card,
            width=430,
            height=40,
            corner_radius=12,
            placeholder_text="🔍  Search products..."
        )

        self.search_entry.pack(
            side="left",
            padx=20,
            pady=15
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.search_products()
        )

        # Refresh

        refresh_btn = ctk.CTkButton(
            search_card,
            text="⟳  Refresh",
            width=110,
            height=40,
            corner_radius=12,
            fg_color="#333333",
            hover_color="#404040",
            command=self.refresh_products
        )

        refresh_btn.pack(
            side="left",
            padx=5
        )

        # Right action buttons

        self.delete_btn = ctk.CTkButton(
            search_card,
            text="🗑  Delete",
            width=110,
            height=40,
            corner_radius=12,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            state="disabled",
            command=self.delete_product
        )

        self.delete_btn.pack(
            side="right",
            padx=(5, 20)
        )

        self.edit_btn = ctk.CTkButton(
            search_card,
            text="✏  Edit",
            width=100,
            height=40,
            corner_radius=12,
            state="disabled",
            command=self.edit_product
        )

        self.edit_btn.pack(
            side="right",
            padx=5
        )

        # =====================================================
        # TABLE
        # =====================================================

        table_card = ctk.CTkFrame(
            self,
            corner_radius=20,
            fg_color="#242424"
        )

        table_card.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 8)
        )

        self.product_table = Sheet(
            table_card,
            headers=[
                "ID",
                "Product",
                "Stock",
                "Category",
                "Supplier",
                "Price"
            ],
            theme="dark",
            show_x_scrollbar=False
        )

        self.product_table.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=12
        )

        # =====================================================
        # TABLE STYLE
        # =====================================================

        self.product_table.change_theme(
            "dark"
        )

        self.product_table.set_options(
            header_bg="#1F1F1F",
            header_fg="#FFFFFF",

            index_bg="#1F1F1F",
            index_fg="#9CA3AF",

            table_bg="#242424",
            table_fg="#FFFFFF",

            selected_cells_bg="#1F6AA5",
            selected_cells_fg="#FFFFFF",

            grid_color="#383838"
        )

        self.product_table.align_columns(
            "center"
        )

        self.product_table.align_rows(
            "center"
        )

        # Column widths

        self.product_table.column_width(
            column=0,
            width=70
        )

        self.product_table.column_width(
            column=1,
            width=240
        )

        self.product_table.column_width(
            column=2,
            width=100
        )

        self.product_table.column_width(
            column=3,
            width=150
        )

        self.product_table.column_width(
            column=4,
            width=180
        )

        self.product_table.column_width(
            column=5,
            width=120
        )

        # =====================================================
        # TABLE BINDINGS
        # =====================================================

        self.product_table.enable_bindings(
            (
                "single_select",
                "row_select",
                "arrowkeys",
                "right_click_popup_menu",
                "rc_select"
            )
        )
        self.product_table.extra_bindings([
            ("cell_select", self.select_product),
            ("row_select", self.select_product)
        ])
        # =====================================================
        # SELECTED PRODUCT BAR
        # =====================================================

        self.bottom_bar = ctk.CTkFrame(
            self,
            height=55,
            corner_radius=15,
            fg_color="#242424"
        )

        self.bottom_bar.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        self.bottom_bar.pack_propagate(False)

        self.selected_label = ctk.CTkLabel(
            self.bottom_bar,
            text="No product selected",
            text_color="#9CA3AF",
            font=("Arial", 12)
        )

        self.selected_label.pack(
            side="left",
            padx=20
        )

    # =========================================================
    # STAT CARD
    # =========================================================

    def create_stat_card(
        self,
        parent,
        icon,
        title
    ):

        card = ctk.CTkFrame(
            parent,
            height=85,
            corner_radius=18,
            fg_color="#242424"
        )

        card.pack_propagate(False)

        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=("Arial", 25)
        )

        icon_label.pack(
            side="left",
            padx=(18, 10)
        )

        text_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        text_frame.pack(
            side="left"
        )

        value_label = ctk.CTkLabel(
            text_frame,
            text="0",
            font=("Arial", 21, "bold")
        )

        value_label.pack(
            anchor="w"
        )

        title_label = ctk.CTkLabel(
            text_frame,
            text=title,
            text_color="#9CA3AF",
            font=("Arial", 10)
        )

        title_label.pack(
            anchor="w"
        )

        card.value_label = value_label

        return card

    # =========================================================
    # LOAD PRODUCTS
    # =========================================================

    def load_products(self):

        try:

            products = get_products()

            display_products = []

            for product in products:

                display_products.append(
                    [
                        product[0],
                        product[1],
                        product[2],
                        product[3],
                        product[4],
                        product[7]
                    ]
                )

            self.product_table.set_sheet_data(
                display_products
            )

            self.product_table.refresh()

            self.update_statistics(
                products
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Could not load products.\n\n{e}"
            )

    # =========================================================
    # STATISTICS
    # =========================================================

    def update_statistics(
        self,
        products
    ):

        total_products = len(
            products
        )

        total_stock = 0
        low_stock = 0
        inventory_value = 0

        for product in products:

            try:

                quantity = int(
                    float(
                        product[2]
                    )
                )

            except:

                quantity = 0

            try:

                price = float(
                    str(
                        product[7]
                    ).replace(
                        ",",
                        "."
                    )
                )

            except:

                price = 0

            total_stock += quantity

            if quantity <= 5:
                low_stock += 1

            inventory_value += (
                quantity * price
            )

        self.total_card.value_label.configure(
            text=str(total_products)
        )

        self.stock_card.value_label.configure(
            text=str(total_stock)
        )

        self.low_stock_card.value_label.configure(
            text=str(low_stock)
        )

        self.value_card.value_label.configure(
            text=f"{inventory_value:.2f}"
        )

    # =========================================================
    # SELECT PRODUCT
    # =========================================================
    def select_product(self, event=None):
        try:
            selected = self.product_table.get_currently_selected()

            if not selected:
                return

            row = selected.row

            if row is None or row < 0:
                return

            product = self.product_table.get_row_data(row)

            if not product:
                return

            self.selected_product = tuple(product)

            self.selected_label.configure(
                text=(
                    f"Selected: {product[1]}"
                    f"   •   Stock: {product[2]}"
                    f"   •   Price: {product[5]}"
                ),
                text_color="#FFFFFF"
            )

            self.edit_btn.configure(state="normal")
            self.delete_btn.configure(state="normal")

            print("SELECTED PRODUCT:", self.selected_product)

        except Exception as e:
            print("PRODUCT SELECTION ERROR:", e)

    # =========================================================
    # SEARCH
    # =========================================================

    def search_products(
        self
    ):

        keyword = (
            self.search_entry
            .get()
            .strip()
            .lower()
        )

        if not keyword:

            self.load_products()

            return

        products = get_products()

        filtered = []

        for product in products:

            name = str(
                product[1]
            ).lower()

            category = str(
                product[3]
            ).lower()

            supplier = str(
                product[4]
            ).lower()

            if (
                keyword in name
                or keyword in category
                or keyword in supplier
            ):

                filtered.append(
                    [
                        product[0],
                        product[1],
                        product[2],
                        product[3],
                        product[4],
                        product[7]
                    ]
                )

        self.product_table.set_sheet_data(
            filtered
        )

        self.product_table.refresh()

    # =========================================================
    # ADD
    # =========================================================

    def add_product(self):

        AddProductWindow(
            self
        )

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh_products(self):

        self.selected_product = None

        self.edit_btn.configure(
            state="disabled"
        )

        self.delete_btn.configure(
            state="disabled"
        )

        self.selected_label.configure(
            text="No product selected",
            text_color="#9CA3AF"
        )

        self.load_products()

    # =========================================================
    # DELETE
    # =========================================================

    def delete_product(self):

        if not self.selected_product:
            from tkinter import messagebox

            messagebox.showwarning(
                "No Selection",
                "Please select a product first."
            )
            return

        product_id = self.selected_product[0]
        product_name = self.selected_product[1]

        from tkinter import messagebox

        confirm = messagebox.askyesno(
            "Delete Product",
            f"Are you sure you want to delete\n\n"
            f"'{product_name}'?"
        )

        if not confirm:
            return

        try:
            delete_product(product_id)

            self.selected_product = None

            self.refresh_products()

        except Exception as e:
            messagebox.showerror(
                "Delete Error",
                str(e)
            )
    # =========================================================
    # EDIT
    # =========================================================

    def edit_product(self):

        if not self.selected_product:

            from tkinter import messagebox

            messagebox.showwarning(
                "No Selection",
                "Please select a product first."
            )

            return

        product = self.selected_product

        product_id = product[0]
        name = product[1]
        quantity = product[2]
        category = product[3]
        supplier = product[4]
        price = product[5]

        EditProductWindow(
            self,
            product_id,
            name,
            quantity,
            category,
            supplier,
            price
        )

# =============================================================
# ADD PRODUCT WINDOW
# =============================================================


class AddProductWindow(
    ctk.CTkToplevel
):

    def __init__(
        self,
        parent
    ):

        super().__init__(
            parent
        )

        self.parent = parent

        self.title(
            "Add Product"
        )

        self.geometry(
            "500x560"
        )

        self.resizable(
            False,
            False
        )

        self.transient(
            parent
        )

        self.grab_set()

        self.create_ui()

    # =========================================================
    # UI
    # =========================================================

    def create_ui(self):

        # Header

        header = ctk.CTkFrame(
            self,
            height=105,
            corner_radius=0,
            fg_color="#242424"
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        icon = ctk.CTkLabel(
            header,
            text="📦",
            font=("Arial", 30)
        )

        icon.pack(
            pady=(14, 0)
        )

        title = ctk.CTkLabel(
            header,
            text="Add New Product",
            font=("Arial", 20, "bold")
        )

        title.pack()

        subtitle = ctk.CTkLabel(
            header,
            text="Add a product to your inventory",
            text_color="#9CA3AF",
            font=("Arial", 11)
        )

        subtitle.pack()

        # Form

        form = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        form.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=20
        )

        # Name

        self.name_entry = ctk.CTkEntry(
            form,
            height=42,
            corner_radius=10,
            placeholder_text="Product Name"
        )

        self.name_entry.pack(
            fill="x",
            pady=7
        )

        # Quantity

        self.quantity_entry = ctk.CTkEntry(
            form,
            height=42,
            corner_radius=10,
            placeholder_text="Quantity"
        )

        self.quantity_entry.pack(
            fill="x",
            pady=7
        )

        # Category

        self.category_box = ctk.CTkComboBox(
            form,
            height=42,
            corner_radius=10,
            values=self.get_category_names()
        )

        self.category_box.set(
            "Select Category"
        )

        self.category_box.pack(
            fill="x",
            pady=7
        )

        # Supplier

        self.supplier_box = ctk.CTkComboBox(
            form,
            height=42,
            corner_radius=10,
            values=self.get_supplier_names()
        )

        self.supplier_box.set(
            "Select Supplier"
        )

        self.supplier_box.pack(
            fill="x",
            pady=7
        )

        # Price

        self.price_entry = ctk.CTkEntry(
            form,
            height=42,
            corner_radius=10,
            placeholder_text="Price"
        )

        self.price_entry.pack(
            fill="x",
            pady=7
        )

        # Save

        self.save_btn = ctk.CTkButton(
            form,
            text="✓  Add Product",
            height=44,
            corner_radius=10,
            font=("Arial", 13, "bold"),
            command=self.save_product
        )

        self.save_btn.pack(
            fill="x",
            pady=(20, 5)
        )

        self.name_entry.focus()

    # =========================================================
    # DATA
    # =========================================================

    def get_category_names(
        self
    ):

        categories = get_categories()

        return [
            category[1]
            for category in categories
        ]

    def get_supplier_names(
        self
    ):

        suppliers = get_suppliers()

        return [
            supplier[1]
            for supplier in suppliers
        ]

    # =========================================================
    # SAVE
    # =========================================================

    def save_product(self):

        name = (
            self.name_entry
            .get()
            .strip()
        )

        quantity = (
            self.quantity_entry
            .get()
            .strip()
        )

        category = (
            self.category_box
            .get()
            .strip()
        )

        supplier = (
            self.supplier_box
            .get()
            .strip()
        )

        price = (
            self.price_entry
            .get()
            .strip()
            .replace(",", ".")
        )

        # Validation

        if not name:

            messagebox.showwarning(
                "Missing Product",
                "Product name is required.",
                parent=self
            )

            return

        try:

            quantity_value = int(
                quantity
            )

            if quantity_value < 0:
                raise ValueError

        except:

            messagebox.showwarning(
                "Invalid Quantity",
                "Quantity must be a valid positive number.",
                parent=self
            )

            return

        if (
            not category
            or category == "Select Category"
        ):

            messagebox.showwarning(
                "Missing Category",
                "Please select a category.",
                parent=self
            )

            return

        if (
            not supplier
            or supplier == "Select Supplier"
        ):

            messagebox.showwarning(
                "Missing Supplier",
                "Please select a supplier.",
                parent=self
            )

            return

        try:

            price_value = float(
                price
            )

            if price_value < 0:
                raise ValueError

        except:

            messagebox.showwarning(
                "Invalid Price",
                "Price must be a valid number.",
                parent=self
            )

            return

        try:

            add_product(
                name,
                quantity,
                category,
                supplier,
                price
            )

            self.parent.refresh_products()

            messagebox.showinfo(
                "Product Added",
                f"'{name}' was added successfully.",
                parent=self
            )

            self.destroy()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e),
                parent=self
            )


# =============================================================
# EDIT PRODUCT WINDOW
# =============================================================

class EditProductWindow(
    ctk.CTkToplevel
):

    def __init__(
        self,
        parent,
        product_id,
        name,
        quantity,
        category,
        supplier,
        price
    ):

        super().__init__(
            parent
        )

        self.parent = parent
        self.product_id = product_id

        self.title(
            "Edit Product"
        )

        self.geometry(
            "500x560"
        )

        self.resizable(
            False,
            False
        )

        self.transient(
            parent
        )

        self.grab_set()

        self.create_ui(
            name,
            quantity,
            category,
            supplier,
            price
        )

    # =========================================================
    # UI
    # =========================================================

    def create_ui(
        self,
        name,
        quantity,
        category,
        supplier,
        price
    ):

        # Header

        header = ctk.CTkFrame(
            self,
            height=105,
            corner_radius=0,
            fg_color="#242424"
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        icon = ctk.CTkLabel(
            header,
            text="✏️",
            font=("Arial", 30)
        )

        icon.pack(
            pady=(14, 0)
        )

        title = ctk.CTkLabel(
            header,
            text="Edit Product",
            font=("Arial", 20, "bold")
        )

        title.pack()

        subtitle = ctk.CTkLabel(
            header,
            text="Update product information",
            text_color="#9CA3AF",
            font=("Arial", 11)
        )

        subtitle.pack()

        # Form

        form = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        form.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=20
        )

        # Name

        self.name_entry = ctk.CTkEntry(
            form,
            height=42,
            corner_radius=10,
            placeholder_text="Product Name"
        )

        self.name_entry.insert(
            0,
            str(name)
        )

        self.name_entry.pack(
            fill="x",
            pady=7
        )

        # Quantity

        self.quantity_entry = ctk.CTkEntry(
            form,
            height=42,
            corner_radius=10,
            placeholder_text="Quantity"
        )

        self.quantity_entry.insert(
            0,
            str(quantity)
        )

        self.quantity_entry.pack(
            fill="x",
            pady=7
        )

        # Category

        categories = get_categories()

        category_names = [
            cat[1]
            for cat in categories
        ]

        self.category_box = ctk.CTkComboBox(
            form,
            height=42,
            corner_radius=10,
            values=category_names
        )

        self.category_box.set(
            str(category)
        )

        self.category_box.pack(
            fill="x",
            pady=7
        )

        # Supplier

        suppliers = get_suppliers()

        supplier_names = [
            sup[1]
            for sup in suppliers
        ]

        self.supplier_box = ctk.CTkComboBox(
            form,
            height=42,
            corner_radius=10,
            values=supplier_names
        )

        self.supplier_box.set(
            str(supplier)
        )

        self.supplier_box.pack(
            fill="x",
            pady=7
        )

        # Price

        self.price_entry = ctk.CTkEntry(
            form,
            height=42,
            corner_radius=10,
            placeholder_text="Price"
        )

        self.price_entry.insert(
            0,
            str(price)
        )

        self.price_entry.pack(
            fill="x",
            pady=7
        )

        # Save

        save_btn = ctk.CTkButton(
            form,
            text="✓  Save Changes",
            height=44,
            corner_radius=10,
            font=("Arial", 13, "bold"),
            command=self.save_changes
        )

        save_btn.pack(
            fill="x",
            pady=(20, 5)
        )

    # =========================================================
    # SAVE
    # =========================================================

    def save_changes(self):

        name = (
            self.name_entry
            .get()
            .strip()
        )

        quantity = (
            self.quantity_entry
            .get()
            .strip()
        )

        category = (
            self.category_box
            .get()
            .strip()
        )

        supplier = (
            self.supplier_box
            .get()
            .strip()
        )

        price = (
            self.price_entry
            .get()
            .strip()
            .replace(",", ".")
        )

        if not name:

            messagebox.showwarning(
                "Missing Product",
                "Product name is required.",
                parent=self
            )

            return

        try:

            quantity_value = int(
                quantity
            )

            if quantity_value < 0:
                raise ValueError

        except:

            messagebox.showwarning(
                "Invalid Quantity",
                "Quantity must be a valid positive number.",
                parent=self
            )

            return

        if not category:

            messagebox.showwarning(
                "Missing Category",
                "Please select a category.",
                parent=self
            )

            return

        if not supplier:

            messagebox.showwarning(
                "Missing Supplier",
                "Please select a supplier.",
                parent=self
            )

            return

        try:

            price_value = float(
                price
            )

            if price_value < 0:
                raise ValueError

        except:

            messagebox.showwarning(
                "Invalid Price",
                "Price must be a valid number.",
                parent=self
            )

            return

        try:

            update_product(
                self.product_id,
                name,
                quantity,
                category,
                supplier,
                price
            )

            self.parent.refresh_products()

            messagebox.showinfo(
                "Product Updated",
                f"'{name}' was updated successfully.",
                parent=self
            )

            self.destroy()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e),
                parent=self
            )
