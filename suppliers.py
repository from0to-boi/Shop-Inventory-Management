import customtkinter as ctk
from tkinter import messagebox
from tksheet import Sheet

from database import (
    add_supplier,
    get_suppliers,
    update_supplier,
    delete_supplier,
    search_suppliers
)


# =========================
# Country Codes
# =========================

COUNTRY_CODES = [
    "+212",  # Morocco
    "+33",   # France
    "+34",   # Spain
    "+44",   # UK
    "+49",   # Germany
    "+32",   # Belgium
    "+31",   # Netherlands
    "+39",   # Italy
    "+1",    # USA / Canada
]


class SuppliersPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.selected_supplier = None

        self.create_ui()
        self.load_suppliers()

    def create_ui(self):

        # =========================
        # Header
        # =========================

        header = ctk.CTkFrame(
            self,
            height=75,
            corner_radius=20,
            fg_color="#242424"
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(15, 8)
        )

        header.pack_propagate(False)

        title = ctk.CTkLabel(
            header,
            text="🏢 Suppliers",
            font=("Arial", 24, "bold")
        )

        title.pack(
            side="left",
            padx=25
        )

        subtitle = ctk.CTkLabel(
            header,
            text="Manage your suppliers",
            text_color="#9CA3AF",
            font=("Arial", 12)
        )

        subtitle.pack(
            side="left",
            padx=5,
            pady=5
        )

        # =========================
        # Search
        # =========================

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

        self.search_entry = ctk.CTkEntry(
            search_card,
            placeholder_text="🔍 Search supplier...",
            width=500,
            height=40,
            corner_radius=12
        )

        self.search_entry.pack(
            side="left",
            padx=20,
            pady=15
        )

        search_btn = ctk.CTkButton(
            search_card,
            text="Search",
            width=110,
            height=40,
            corner_radius=12,
            command=self.search
        )

        search_btn.pack(
            side="left"
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.search()
        )

        add_btn = ctk.CTkButton(
            search_card,
            text="➕ Add Supplier",
            width=150,
            height=40,
            corner_radius=12,
            command=self.add
        )

        add_btn.pack(
            side="right",
            padx=20
        )

        # =========================
        # Table
        # =========================

        table_card = ctk.CTkFrame(
            self,
            corner_radius=20,
            fg_color="#242424"
        )

        table_card.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=8
        )

        self.sheet = Sheet(
            table_card,
            headers=[
                "ID",
                "Name",
                "Phone",
                "Email",
                "Address"
            ],
            theme="dark"
        )

        self.sheet.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.sheet.enable_bindings(
            (
                "single_select",
                "row_select"
            )
        )

        self.sheet.extra_bindings(
            [
                ("<ButtonRelease-1>", self.select_supplier)
            ]
        )

        # =========================
        # Bottom Form
        # =========================

        form = ctk.CTkFrame(
            self,
            height=155,
            corner_radius=20,
            fg_color="#242424"
        )

        form.pack(
            fill="x",
            padx=20,
            pady=(5, 12)
        )

        form.pack_propagate(False)

        # =========================
        # Entry Row
        # =========================

        entry_frame = ctk.CTkFrame(
            form,
            fg_color="transparent"
        )

        entry_frame.pack(
            fill="x",
            padx=20,
            pady=(18, 8)
        )

        # =========================
        # Supplier Name
        # =========================

        self.name = ctk.CTkEntry(
            entry_frame,
            placeholder_text="Supplier Name",
            height=38,
            corner_radius=12
        )

        self.name.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

        # =========================
        # Phone
        # =========================

        phone_frame = ctk.CTkFrame(
            entry_frame,
            fg_color="transparent"
        )

        phone_frame.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

        self.country_code = ctk.CTkComboBox(
            phone_frame,
            values=COUNTRY_CODES,
            width=85,
            height=38,
            corner_radius=12
        )

        self.country_code.set("+212")

        self.country_code.pack(
            side="left",
            padx=(0, 5)
        )

        self.phone = ctk.CTkEntry(
            phone_frame,
            placeholder_text="Phone",
            height=38,
            corner_radius=12
        )

        self.phone.pack(
            side="left",
            fill="x",
            expand=True
        )

        # =========================
        # Email
        # =========================

        self.email = ctk.CTkEntry(
            entry_frame,
            placeholder_text="Email",
            height=38,
            corner_radius=12
        )

        self.email.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

        # =========================
        # Address
        # =========================

        self.address = ctk.CTkEntry(
            entry_frame,
            placeholder_text="Address",
            height=38,
            corner_radius=12
        )

        self.address.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

        # =========================
        # Buttons Row
        # =========================

        btn_frame = ctk.CTkFrame(
            form,
            fg_color="transparent"
        )

        btn_frame.pack(
            pady=(5, 0)
        )

        edit_btn = ctk.CTkButton(
            btn_frame,
            text="📝 Edit",
            width=120,
            height=38,
            corner_radius=12,
            command=self.edit
        )

        edit_btn.pack(
            side="left",
            padx=8
        )

        delete_btn = ctk.CTkButton(
            btn_frame,
            text="🗑 Delete",
            width=120,
            height=38,
            corner_radius=12,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.delete
        )

        delete_btn.pack(
            side="left",
            padx=8
        )

    # =========================
    # Database Functions
    # =========================

    def load_suppliers(self):

        data = get_suppliers()

        self.sheet.set_sheet_data(
            data
        )

    # =========================
    # Add Supplier
    # =========================

    def add(self):

        if not self.name.get().strip():

            messagebox.showwarning(
                "Missing Data",
                "Supplier name is required."
            )

            return

        phone = (
            self.country_code.get().strip()
            + self.phone.get().strip()
        )

        add_supplier(
            self.name.get().strip(),
            phone,
            self.email.get().strip(),
            self.address.get().strip()
        )

        self.clear()
        self.load_suppliers()

    # =========================
    # Edit Supplier
    # =========================

    def edit(self):

        selected = self.sheet.get_currently_selected()

        if selected:

            row = selected.row

            supplier = self.sheet.get_row_data(row)

            supplier_id = supplier[0]
            name = supplier[1]
            phone = supplier[2]
            email = supplier[3]
            address = supplier[4]

            EditSupplierWindow(
                self,
                supplier_id,
                name,
                phone,
                email,
                address
            )

        else:

            messagebox.showwarning(
                "No Selection",
                "Select a supplier first."
            )

    # =========================
    # Delete Supplier
    # =========================

    def delete(self):

        selected = self.sheet.get_currently_selected()

        if selected:

            row = selected.row

            supplier = self.sheet.get_row_data(row)

            supplier_id = supplier[0]

            confirm = messagebox.askyesno(
                "Delete",
                "Delete this supplier?"
            )

            if confirm:

                delete_supplier(
                    supplier_id
                )

                self.clear()
                self.load_suppliers()

        else:

            messagebox.showwarning(
                "No Selection",
                "Select a supplier first."
            )

    # =========================
    # Search
    # =========================

    def search(self):

        keyword = self.search_entry.get().strip()

        if keyword == "":

            data = get_suppliers()

        else:

            data = search_suppliers(
                keyword
            )

        self.sheet.set_sheet_data(
            data
        )

    # =========================
    # Select Supplier
    # =========================

    def select_supplier(self, event=None):

        try:

            selected = self.sheet.get_currently_selected()

            print(
                "CURRENTLY SELECTED:",
                selected
            )

            if selected is None:
                return

            row = selected.row

            print(
                "SELECTED ROW:",
                row
            )

            if row is None or row < 0:
                return

            row_data = self.sheet.get_row_data(
                row
            )

            print(
                "ROW DATA:",
                row_data
            )

            if not row_data:
                return

            self.selected_supplier = tuple(
                row_data
            )

            print(
                "SELECTED SUPPLIER:",
                self.selected_supplier
            )

            # Name

            self.name.delete(
                0,
                "end"
            )

            self.name.insert(
                0,
                str(row_data[1])
            )

            # Phone

            phone = str(row_data[2])

            self.country_code.set("+212")

            for code in COUNTRY_CODES:

                if phone.startswith(code):

                    self.country_code.set(
                        code
                    )

                    phone = phone[
                        len(code):
                    ]

                    break

            self.phone.delete(
                0,
                "end"
            )

            self.phone.insert(
                0,
                phone
            )

            # Email

            self.email.delete(
                0,
                "end"
            )

            self.email.insert(
                0,
                str(row_data[3])
            )

            # Address

            self.address.delete(
                0,
                "end"
            )

            self.address.insert(
                0,
                str(row_data[4])
            )

        except Exception as e:

            print(
                "SELECTION ERROR:",
                e
            )

    # =========================
    # Clear
    # =========================

    def clear(self):

        self.selected_supplier = None

        for entry in [
            self.name,
            self.phone,
            self.email,
            self.address
        ]:

            entry.delete(
                0,
                "end"
            )

        self.country_code.set(
            "+212"
        )


# =========================================================
# Edit Supplier Window
# =========================================================

class EditSupplierWindow(ctk.CTkToplevel):

    def __init__(
            self,
            parent,
            supplier_id,
            name,
            phone,
            email,
            address
    ):

        super().__init__(parent)

        self.parent = parent

        self.supplier_id = supplier_id

        self.title(
            "Edit Supplier"
        )

        self.geometry(
            "450x400"
        )

        self.transient(
            parent
        )

        self.grab_set()

        # =========================
        # Name
        # =========================

        self.name_entry = ctk.CTkEntry(
            self,
            placeholder_text="Supplier Name"
        )

        self.name_entry.insert(
            0,
            name
        )

        self.name_entry.pack(
            pady=10,
            padx=20,
            fill="x"
        )

        # =========================
        # Phone
        # =========================

        phone_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        phone_frame.pack(
            pady=10,
            padx=20,
            fill="x"
        )

        self.country_code = ctk.CTkComboBox(
            phone_frame,
            values=COUNTRY_CODES,
            width=85,
            height=38,
            corner_radius=12
        )

        self.country_code.pack(
            side="left",
            padx=(0, 5)
        )

        self.phone_entry = ctk.CTkEntry(
            phone_frame,
            placeholder_text="Phone"
        )

        self.phone_entry.pack(
            side="left",
            fill="x",
            expand=True
        )

        # =========================
        # Detect Country Code
        # =========================

        phone = str(phone)

        self.country_code.set(
            "+212"
        )

        for code in COUNTRY_CODES:

            if phone.startswith(code):

                self.country_code.set(
                    code
                )

                phone = phone[
                    len(code):
                ]

                break

        self.phone_entry.insert(
            0,
            phone
        )

        # =========================
        # Email
        # =========================

        self.email_entry = ctk.CTkEntry(
            self,
            placeholder_text="Email"
        )

        self.email_entry.insert(
            0,
            email
        )

        self.email_entry.pack(
            pady=10,
            padx=20,
            fill="x"
        )

        # =========================
        # Address
        # =========================

        self.address_entry = ctk.CTkEntry(
            self,
            placeholder_text="Address"
        )

        self.address_entry.insert(
            0,
            address
        )

        self.address_entry.pack(
            pady=10,
            padx=20,
            fill="x"
        )

        # =========================
        # Save Button
        # =========================

        save_btn = ctk.CTkButton(
            self,
            text="Save Changes",
            command=self.save_changes
        )

        save_btn.pack(
            pady=20
        )

    # =========================
    # Save Changes
    # =========================

    def save_changes(self):

        name = self.name_entry.get().strip()

        phone = (
            self.country_code.get().strip()
            + self.phone_entry.get().strip()
        )

        email = self.email_entry.get().strip()

        address = self.address_entry.get().strip()

        if not name:

            messagebox.showwarning(
                "Missing Data",
                "Supplier name is required."
            )

            return

        update_supplier(
            self.supplier_id,
            name,
            phone,
            email,
            address
        )

        self.parent.clear()

        self.parent.load_suppliers()

        self.destroy()
