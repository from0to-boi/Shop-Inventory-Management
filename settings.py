import customtkinter as ctk
from tkinter import messagebox, filedialog
import sqlite3
import os
import shutil

from database import DATABASE_NAME


class SettingsPage(ctk.CTkFrame):

    def __init__(self, parent, user=None):

        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.parent = parent
        self.user = user

        self.create_ui()

    # =========================================================
    # UI
    # =========================================================

    def create_ui(self):

        # =====================================================
        # Header
        # =====================================================

        header = ctk.CTkFrame(
            self,
            height=80,
            corner_radius=20,
            fg_color="#242424"
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(15, 10)
        )

        header.pack_propagate(False)

        title_frame = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        title_frame.pack(
            side="left",
            padx=25
        )

        title = ctk.CTkLabel(
            title_frame,
            text="⚙️ Settings",
            font=("Arial", 25, "bold")
        )

        title.pack(
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            title_frame,
            text="Customize and manage your application",
            text_color="#9CA3AF",
            font=("Arial", 12)
        )

        subtitle.pack(
            anchor="w"
        )

        # =====================================================
        # Scrollable Area
        # =====================================================

        self.scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.scroll.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 10)
        )

        # =====================================================
        # General
        # =====================================================

        self.create_section(
            "🎨 Appearance",
            "Customize how the application looks."
        )

        appearance_card = self.create_card()

        # Appearance

        appearance_label = ctk.CTkLabel(
            appearance_card,
            text="Appearance Mode",
            font=("Arial", 14, "bold")
        )

        appearance_label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(18, 3)
        )

        appearance_desc = ctk.CTkLabel(
            appearance_card,
            text="Choose between dark, light or system appearance.",
            text_color="#9CA3AF",
            font=("Arial", 11)
        )

        appearance_desc.grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=(0, 18)
        )

        self.appearance_menu = ctk.CTkComboBox(
            appearance_card,
            values=[
                "Dark",
                "Light",
                "System"
            ],
            width=150,
            height=38,
            command=self.change_appearance
        )

        self.appearance_menu.set(
            "Dark"
        )

        self.appearance_menu.grid(
            row=0,
            column=1,
            rowspan=2,
            padx=20,
            pady=15
        )

        # =====================================================
        # Theme
        # =====================================================

        theme_label = ctk.CTkLabel(
            appearance_card,
            text="Theme Color",
            font=("Arial", 14, "bold")
        )

        theme_label.grid(
            row=2,
            column=0,
            sticky="w",
            padx=20,
            pady=(10, 3)
        )

        theme_desc = ctk.CTkLabel(
            appearance_card,
            text="Choose the main accent color of the application.",
            text_color="#9CA3AF",
            font=("Arial", 11)
        )

        theme_desc.grid(
            row=3,
            column=0,
            sticky="w",
            padx=20,
            pady=(0, 18)
        )

        self.theme_menu = ctk.CTkComboBox(
            appearance_card,
            values=[
                "Blue",
                "Green",
                "Dark Blue"
            ],
            width=150,
            height=38,
            command=self.change_theme
        )

        self.theme_menu.set(
            "Blue"
        )

        self.theme_menu.grid(
            row=2,
            column=1,
            rowspan=2,
            padx=20,
            pady=15
        )

        # =====================================================
        # Account
        # =====================================================

        self.create_section(
            "👤 Account",
            "Manage your account information and security."
        )

        account_card = self.create_card()

        # Username

        username_label = ctk.CTkLabel(
            account_card,
            text="Username",
            font=("Arial", 14, "bold")
        )

        username_label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(18, 3)
        )

        username_value = "Administrator"

        if self.user:

            if isinstance(self.user, dict):

                username_value = self.user.get(
                    "username",
                    "Administrator"
                )

            elif isinstance(self.user, (tuple, list)):

                if len(self.user) > 1:
                    username_value = self.user[1]

        username = ctk.CTkLabel(
            account_card,
            text=str(username_value),
            text_color="#9CA3AF",
            font=("Arial", 12)
        )

        username.grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=(0, 18)
        )

        change_password_btn = ctk.CTkButton(
            account_card,
            text="🔐 Change Password",
            width=170,
            height=38,
            corner_radius=10,
            command=self.change_password
        )

        change_password_btn.grid(
            row=0,
            column=1,
            rowspan=2,
            padx=20
        )

        # =====================================================
        # Database
        # =====================================================

        self.create_section(
            "💾 Database",
            "Backup or restore your inventory database."
        )

        database_card = self.create_card()

        backup_btn = ctk.CTkButton(
            database_card,
            text="📦 Backup Database",
            width=180,
            height=42,
            corner_radius=10,
            command=self.backup_database
        )

        backup_btn.grid(
            row=0,
            column=0,
            padx=20,
            pady=20
        )

        restore_btn = ctk.CTkButton(
            database_card,
            text="📂 Restore Database",
            width=180,
            height=42,
            corner_radius=10,
            command=self.restore_database
        )

        restore_btn.grid(
            row=0,
            column=1,
            padx=20,
            pady=20
        )

        # Database location

        location_label = ctk.CTkLabel(
            database_card,
            text=f"Current database: {os.path.basename(DATABASE_NAME)}",
            text_color="#9CA3AF",
            font=("Arial", 11)
        )

        location_label.grid(
            row=1,
            column=0,
            columnspan=2,
            pady=(0, 15)
        )

        # =====================================================
        # Danger Zone
        # =====================================================

        self.create_section(
            "⚠️ Danger Zone",
            "These actions can permanently affect your data."
        )

        danger_card = ctk.CTkFrame(
            self.scroll,
            corner_radius=18,
            fg_color="#2A1D1D"
        )

        danger_card.pack(
            fill="x",
            pady=(0, 20)
        )

        danger_label = ctk.CTkLabel(
            danger_card,
            text="Reset Database",
            font=("Arial", 14, "bold")
        )

        danger_label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(18, 3)
        )

        danger_desc = ctk.CTkLabel(
            danger_card,
            text="Delete all products, suppliers, sales and other stored data.",
            text_color="#FCA5A5",
            font=("Arial", 11)
        )

        danger_desc.grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
            pady=(0, 18)
        )

        reset_btn = ctk.CTkButton(
            danger_card,
            text="🗑 Reset Database",
            width=170,
            height=40,
            corner_radius=10,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.reset_database
        )

        reset_btn.grid(
            row=0,
            column=1,
            rowspan=2,
            padx=20
        )

        # =====================================================
        # About
        # =====================================================

        self.create_section(
            "ℹ️ About",
            "Information about your inventory management system."
        )

        about_card = self.create_card()

        app_name = ctk.CTkLabel(
            about_card,
            text="Inventory Management System",
            font=("Arial", 17, "bold")
        )

        app_name.pack(
            anchor="w",
            padx=20,
            pady=(18, 3)
        )

        version = ctk.CTkLabel(
            about_card,
            text="Version 1.0.0",
            text_color="#9CA3AF",
            font=("Arial", 11)
        )

        version.pack(
            anchor="w",
            padx=20
        )

        description = ctk.CTkLabel(
            about_card,
            text="A modern desktop solution for managing products, suppliers, sales and inventory.",
            text_color="#9CA3AF",
            font=("Arial", 11),
            wraplength=700,
            justify="left"
        )

        description.pack(
            anchor="w",
            padx=20,
            pady=(8, 18)
        )

    # =========================================================
    # Section
    # =========================================================

    def create_section(
        self,
        title,
        description
    ):

        frame = ctk.CTkFrame(
            self.scroll,
            fg_color="transparent"
        )

        frame.pack(
            fill="x",
            pady=(10, 5)
        )

        title_label = ctk.CTkLabel(
            frame,
            text=title,
            font=("Arial", 17, "bold")
        )

        title_label.pack(
            anchor="w"
        )

        desc_label = ctk.CTkLabel(
            frame,
            text=description,
            text_color="#9CA3AF",
            font=("Arial", 11)
        )

        desc_label.pack(
            anchor="w",
            pady=(2, 5)
        )

    # =========================================================
    # Card
    # =========================================================

    def create_card(self):

        card = ctk.CTkFrame(
            self.scroll,
            corner_radius=18,
            fg_color="#242424"
        )

        card.pack(
            fill="x",
            pady=(0, 15)
        )

        return card

    # =========================================================
    # Appearance
    # =========================================================

    def change_appearance(self, choice):

        modes = {
            "Dark": "dark",
            "Light": "light",
            "System": "system"
        }

        mode = modes.get(
            choice,
            "dark"
        )

        ctk.set_appearance_mode(
            mode
        )

    # =========================================================
    # Theme
    # =========================================================

    def change_theme(self, choice):

        themes = {
            "Blue": "blue",
            "Green": "green",
            "Dark Blue": "dark-blue"
        }

        theme = themes.get(
            choice,
            "blue"
        )

        ctk.set_default_color_theme(
            theme
        )

        messagebox.showinfo(
            "Theme Changed",
            "The theme has been changed.\n"
            "Some elements may require restarting the application."
        )

    # =========================================================
    # Change Password
    # =========================================================

    def change_password(self):

        window = ctk.CTkToplevel(
            self
        )

        window.title(
            "Change Password"
        )

        window.geometry(
            "400x330"
        )

        window.resizable(
            False,
            False
        )

        window.transient(
            self
        )

        window.grab_set()

        title = ctk.CTkLabel(
            window,
            text="🔐 Change Password",
            font=("Arial", 20, "bold")
        )

        title.pack(
            pady=(25, 20)
        )

        old_password = ctk.CTkEntry(
            window,
            placeholder_text="Current Password",
            show="•",
            height=40
        )

        old_password.pack(
            fill="x",
            padx=30,
            pady=8
        )

        new_password = ctk.CTkEntry(
            window,
            placeholder_text="New Password",
            show="•",
            height=40
        )

        new_password.pack(
            fill="x",
            padx=30,
            pady=8
        )

        confirm_password = ctk.CTkEntry(
            window,
            placeholder_text="Confirm New Password",
            show="•",
            height=40
        )

        confirm_password.pack(
            fill="x",
            padx=30,
            pady=8
        )

        def save():

            old = old_password.get()
            new = new_password.get()
            confirm = confirm_password.get()

            if not old or not new or not confirm:

                messagebox.showwarning(
                    "Missing Data",
                    "Please fill in all fields.",
                    parent=window
                )

                return

            if new != confirm:

                messagebox.showerror(
                    "Error",
                    "New passwords do not match.",
                    parent=window
                )

                return

            if len(new) < 4:

                messagebox.showwarning(
                    "Weak Password",
                    "Password must contain at least 4 characters.",
                    parent=window
                )

                return

            try:

                conn = sqlite3.connect(
                    DATABASE_NAME
                )

                cursor = conn.cursor()

                username = None

                if isinstance(self.user, dict):

                    username = self.user.get(
                        "username"
                    )

                elif isinstance(self.user, (tuple, list)):

                    if len(self.user) > 1:
                        username = self.user[1]

                if username is None:

                    messagebox.showerror(
                        "Error",
                        "Unable to identify the current user.",
                        parent=window
                    )

                    conn.close()

                    return

                cursor.execute(
                    "SELECT password FROM users WHERE username = ?",
                    (username,)
                )

                result = cursor.fetchone()

                if not result:

                    conn.close()

                    messagebox.showerror(
                        "Error",
                        "User account not found.",
                        parent=window
                    )

                    return

                if result[0] != old:

                    conn.close()

                    messagebox.showerror(
                        "Error",
                        "Current password is incorrect.",
                        parent=window
                    )

                    return

                cursor.execute(
                    """
                    UPDATE users
                    SET password = ?
                    WHERE username = ?
                    """,
                    (
                        new,
                        username
                    )
                )

                conn.commit()
                conn.close()

                messagebox.showinfo(
                    "Success",
                    "Password changed successfully.",
                    parent=window
                )

                window.destroy()

            except Exception as e:

                messagebox.showerror(
                    "Database Error",
                    str(e),
                    parent=window
                )

        save_btn = ctk.CTkButton(
            window,
            text="Save Password",
            height=40,
            command=save
        )

        save_btn.pack(
            fill="x",
            padx=30,
            pady=20
        )

    # =========================================================
    # Backup
    # =========================================================

    def backup_database(self):

        if not os.path.exists(
            DATABASE_NAME
        ):

            messagebox.showerror(
                "Error",
                "Database file was not found."
            )

            return

        path = filedialog.asksaveasfilename(
            title="Backup Database",
            defaultextension=".db",
            filetypes=[
                (
                    "SQLite Database",
                    "*.db"
                )
            ],
            initialfile="shop_backup.db"
        )

        if not path:
            return

        try:

            shutil.copy2(
                DATABASE_NAME,
                path
            )

            messagebox.showinfo(
                "Backup Complete",
                "Database backup created successfully."
            )

        except Exception as e:

            messagebox.showerror(
                "Backup Error",
                str(e)
            )

    # =========================================================
    # Restore
    # =========================================================

    def restore_database(self):

        path = filedialog.askopenfilename(
            title="Restore Database",
            filetypes=[
                (
                    "SQLite Database",
                    "*.db"
                )
            ]
        )

        if not path:
            return

        confirm = messagebox.askyesno(
            "Restore Database",
            "Restoring a database will replace your current data.\n\n"
            "Are you sure you want to continue?"
        )

        if not confirm:
            return

        try:

            shutil.copy2(
                path,
                DATABASE_NAME
            )

            messagebox.showinfo(
                "Restore Complete",
                "Database restored successfully.\n\n"
                "Please restart the application."
            )

        except Exception as e:

            messagebox.showerror(
                "Restore Error",
                str(e)
            )

    # =========================================================
    # Reset Database
    # =========================================================

    def reset_database(self):

        confirm = messagebox.askyesno(
            "⚠ Reset Database",
            "THIS WILL DELETE YOUR DATA.\n\n"
            "All products, suppliers, sales and other records "
            "may be permanently deleted.\n\n"
            "Are you absolutely sure?"
        )

        if not confirm:
            return

        confirm_again = messagebox.askyesno(
            "Final Confirmation",
            "This action cannot be easily undone.\n\n"
            "Continue?"
        )

        if not confirm_again:
            return

        try:

            conn = sqlite3.connect(
                DATABASE_NAME
            )

            cursor = conn.cursor()

            # Delete application data.
            # Keep users so you can still log in.

            tables = [
                "sales",
                "products",
                "suppliers",
                "categories"
            ]

            for table in tables:

                try:

                    cursor.execute(
                        f"DELETE FROM {table}"
                    )

                except sqlite3.OperationalError:

                    pass

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Database Reset",
                "Application data has been reset."
            )

        except Exception as e:

            messagebox.showerror(
                "Reset Error",
                str(e)
            )
