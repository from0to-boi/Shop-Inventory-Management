import customtkinter as ctk
from database import (add_category,
                      get_categories,
                      delete_category as db_delete_category,
                      update_category,
                      get_category_product_count)


class Categories(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        label = ctk.CTkLabel(
            self,
            text="Categories",
            font=("Inter", 28, "bold")
        )
        label.pack(pady=10)

        # ==========================
        # Top bar
        # ==========================

        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(
            fill="x",
            padx=20
        )

        # Cat Frame
        self.categories_frame = ctk.CTkScrollableFrame(self)
        self.categories_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.load_categories()

        # Search
        self.search_entry = ctk.CTkEntry(
            self.top_frame,
            placeholder_text="Search category..."
        )
        self.search_entry.pack(
            side="left",
            padx=10,
            pady=10
        )

        # Add button
        add_btn = ctk.CTkButton(
            self.top_frame,
            text="Add Category",
            command=self.add_btn
        )
        add_btn.pack(
            side="right",
            padx=10
        )

    def add_btn(self):
        AddCategorie(self)

    def load_categories(self):

        # Remove old cards
        for widget in self.categories_frame.winfo_children():
            widget.destroy()

        # Get categories from database
        categories = get_categories()

    # Create a card for each category
        for category in categories:

            card = ctk.CTkFrame(
                self.categories_frame

            )

            card.pack(
                padx=10,
                pady=10,
                fill="x"
            )

            ctk.CTkLabel(
                card,
                text=category[1],
                font=("Arial", 18, "bold")
            ).pack(pady=20)

            product_count = get_category_product_count(category[1])

            count_label = ctk.CTkLabel(
                card,
                text=f"Products: {product_count}",
                font=("Arial", 14)
            )

            count_label.pack()

            buttons_frame = ctk.CTkFrame(card, fg_color="transparent")
            buttons_frame.pack(pady=10)

            # delete
            delete_btn = ctk.CTkButton(
                buttons_frame,
                text="Delete",
                fg_color="#D32F2F",
                hover_color="#B71C1C",
                width=40,
                height=40,
                command=lambda cid=category[0]: self.delete_category(cid)
            )

            delete_btn.pack(side="left",
                            padx=5)

            edit_btn = ctk.CTkButton(
                buttons_frame,
                text="Edit",
                height=40,
                width=40,
                command=lambda cid=category[0], name=category[1]: EditCategorie(
                    self,
                    cid,
                    name
                )
            )
            edit_btn.pack(side="left",
                          padx=5)

    def refresh_categories(self):
        self.load_categories()

    def delete_category(self, category_id):

        db_delete_category(category_id)
        self.refresh_categories()


class AddCategorie(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.geometry("200x200")
        self.title("Add Categorie")

        # Entry
        self.name = ctk.CTkEntry(
            self,
            placeholder_text="Add Categorie..."
        )
        self.name.pack(
            pady=10
        )
        # Save
        self.save_btn = ctk.CTkButton(
            self,
            text="Save",
            command=self.save_cat
        )

        self.save_btn.pack(
            pady=10
        )

    def save_cat(self):

        cat = self.name.get()

        add_category(cat)

        self.parent.refresh_categories()

        self.destroy()


class EditCategorie(ctk.CTkToplevel):

    def __init__(self, parent, category_id, category_name):
        super().__init__(parent)

        self.parent = parent
        self.category_id = category_id

        self.geometry("300x200")
        self.title("Edit Category")

        # Entry
        self.name = ctk.CTkEntry(
            self,
            placeholder_text="Category Name"
        )

        self.name.pack(
            pady=20,
            padx=20
        )

        # Put old name inside
        self.name.insert(
            0,
            category_name
        )

        # Save button
        save_btn = ctk.CTkButton(
            self,
            text="Save",
            command=self.save_edit
        )

        save_btn.pack(
            pady=10
        )

    def save_edit(self):

        new_name = self.name.get()

        update_category(
            self.category_id,
            new_name
        )

        self.parent.refresh_categories()

        self.destroy()
