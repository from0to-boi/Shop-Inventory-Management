import customtkinter as ctk
from tkinter import messagebox
from tksheet import Sheet
import sqlite3

from database import DATABASE_NAME


class UsersPage(ctk.CTkFrame):

    def __init__(self, parent, user=None):

        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.parent = parent
        self.current_user = user
        self.selected_user = None

        self.create_ui()
        self.load_users()

    # =========================================================
    # UI
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

        left_header = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        left_header.pack(
            side="left",
            padx=25,
            pady=15
        )

        title = ctk.CTkLabel(
            left_header,
            text="👥 User Management",
            font=("Arial", 25, "bold")
        )

        title.pack(
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            left_header,
            text="Manage users and accounts",
            text_color="#9CA3AF",
            font=("Arial", 12)
        )

        subtitle.pack(
            anchor="w",
            pady=(2, 0)
        )

        add_button = ctk.CTkButton(
            header,
            text="＋  Add User",
            width=145,
            height=42,
            corner_radius=12,
            font=("Arial", 13, "bold"),
            command=self.open_add_window
        )

        add_button.pack(
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

        self.total_card = self.create_stat_card(
            stats_frame,
            "👥",
            "Total Users"
        )

        self.total_card.pack(
            side="left",
            fill="x",
            expand=True
        )

        # =====================================================
        # SEARCH
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

        self.search_entry = ctk.CTkEntry(
            search_card,
            placeholder_text="🔍  Search by username...",
            width=450,
            height=40,
            corner_radius=12
        )

        self.search_entry.pack(
            side="left",
            padx=20,
            pady=15
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.refresh_table()
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

        self.sheet = Sheet(
            table_card,
            headers=[
                "ID",
                "Username",
                "Status"
            ],
            theme="dark",
            show_x_scrollbar=False
        )

        self.sheet.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=12
        )

        self.sheet.enable_bindings(
            (
                "single_select",
                "row_select"
            )
        )

        self.sheet.extra_bindings(
            [
                (
                    "<ButtonRelease-1>",
                    self.select_user
                )
            ]
        )

        # =====================================================
        # ACTION BAR
        # =====================================================

        action_bar = ctk.CTkFrame(
            self,
            height=70,
            corner_radius=18,
            fg_color="#242424"
        )

        action_bar.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        action_bar.pack_propagate(False)

        self.selected_label = ctk.CTkLabel(
            action_bar,
            text="No user selected",
            text_color="#9CA3AF",
            font=("Arial", 12)
        )

        self.selected_label.pack(
            side="left",
            padx=20
        )

        self.delete_btn = ctk.CTkButton(
            action_bar,
            text="🗑 Delete",
            width=110,
            height=38,
            corner_radius=10,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            state="disabled",
            command=self.delete_user
        )

        self.delete_btn.pack(
            side="right",
            padx=(5, 20)
        )

        self.password_btn = ctk.CTkButton(
            action_bar,
            text="🔐 Password",
            width=125,
            height=38,
            corner_radius=10,
            state="disabled",
            command=self.open_password_window
        )

        self.password_btn.pack(
            side="right",
            padx=5
        )

        self.edit_btn = ctk.CTkButton(
            action_bar,
            text="✏ Edit",
            width=100,
            height=38,
            corner_radius=10,
            state="disabled",
            command=self.open_edit_window
        )

        self.edit_btn.pack(
            side="right",
            padx=5
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
            height=90,
            corner_radius=18,
            fg_color="#242424"
        )

        card.pack_propagate(False)

        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=("Arial", 26)
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

        value = ctk.CTkLabel(
            text_frame,
            text="0",
            font=("Arial", 23, "bold")
        )

        value.pack(
            anchor="w"
        )

        label = ctk.CTkLabel(
            text_frame,
            text=title,
            text_color="#9CA3AF",
            font=("Arial", 11)
        )

        label.pack(
            anchor="w"
        )

        card.value_label = value

        return card

    # =========================================================
    # DATABASE
    # =========================================================

    def get_users(self):

        conn = sqlite3.connect(
            DATABASE_NAME
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, username
            FROM users
            ORDER BY id
            """
        )

        users = cursor.fetchall()

        conn.close()

        return users

    # =========================================================
    # LOAD USERS
    # =========================================================

    def load_users(self):

        try:

            self.refresh_table()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    # =========================================================
    # REFRESH TABLE
    # =========================================================

    def refresh_table(self):

        try:

            users = self.get_users()

            keyword = (
                self.search_entry
                .get()
                .strip()
                .lower()
            )

            filtered = []

            for user in users:

                user_id = user[0]
                username = str(user[1])

                if keyword:

                    if keyword not in username.lower():
                        continue

                filtered.append(
                    (
                        user_id,
                        username,
                        "Active"
                    )
                )

            self.sheet.set_sheet_data(
                filtered
            )

            self.total_card.value_label.configure(
                text=str(len(users))
            )

        except Exception as e:

            print(
                "REFRESH ERROR:",
                e
            )

    # =========================================================
    # SELECT USER
    # =========================================================

    def select_user(self, event=None):

        try:

            selected = (
                self.sheet
                .get_currently_selected()
            )

            if selected is None:
                return

            row = selected.row

            if row is None or row < 0:
                return

            data = self.sheet.get_row_data(
                row
            )

            if not data:
                return

            self.selected_user = tuple(
                data
            )

            username = data[1]

            self.selected_label.configure(
                text=f"Selected: {username}"
            )

            self.edit_btn.configure(
                state="normal"
            )

            self.password_btn.configure(
                state="normal"
            )

            self.delete_btn.configure(
                state="normal"
            )

        except Exception as e:

            print(
                "SELECTION ERROR:",
                e
            )

    # =========================================================
    # ADD USER
    # =========================================================

    def open_add_window(self):

        AddUserWindow(
            self
        )

    # =========================================================
    # EDIT USER
    # =========================================================

    def open_edit_window(self):

        if not self.selected_user:

            messagebox.showwarning(
                "No Selection",
                "Select a user first."
            )

            return

        EditUserWindow(
            self,
            self.selected_user[0],
            self.selected_user[1]
        )

    # =========================================================
    # CHANGE PASSWORD
    # =========================================================

    def open_password_window(self):

        if not self.selected_user:

            messagebox.showwarning(
                "No Selection",
                "Select a user first."
            )

            return

        ChangePasswordWindow(
            self,
            self.selected_user[0],
            self.selected_user[1]
        )

    # =========================================================
    # DELETE USER
    # =========================================================

    def delete_user(self):

        if not self.selected_user:
            return

        user_id = self.selected_user[0]
        username = self.selected_user[1]

        # -----------------------------------------------------
        # Prevent deleting current account
        # -----------------------------------------------------

        current_username = None

        if isinstance(
            self.current_user,
            dict
        ):

            current_username = (
                self.current_user
                .get("username")
            )

        elif isinstance(
            self.current_user,
            (tuple, list)
        ):

            if len(self.current_user) > 1:

                current_username = (
                    self.current_user[1]
                )

        if (
            current_username
            and username == current_username
        ):

            messagebox.showwarning(
                "Action Not Allowed",
                "You cannot delete the account you are currently using."
            )

            return

        # -----------------------------------------------------
        # Confirmation
        # -----------------------------------------------------

        confirm = messagebox.askyesno(
            "Delete User",
            f"Are you sure you want to delete\n\n"
            f"'{username}'?\n\n"
            f"This action cannot be undone."
        )

        if not confirm:
            return

        try:

            conn = sqlite3.connect(
                DATABASE_NAME
            )

            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM users
                WHERE id = ?
                """,
                (user_id,)
            )

            conn.commit()
            conn.close()

            self.selected_user = None

            self.edit_btn.configure(
                state="disabled"
            )

            self.password_btn.configure(
                state="disabled"
            )

            self.delete_btn.configure(
                state="disabled"
            )

            self.selected_label.configure(
                text="No user selected"
            )

            self.load_users()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )


# =============================================================
# ADD USER WINDOW
# =============================================================

class AddUserWindow(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(
            parent
        )

        self.parent = parent

        self.title(
            "Create User"
        )

        self.geometry(
            "460x430"
        )

        self.resizable(
            False,
            False
        )

        self.transient(
            parent
        )

        self.grab_set()

        # =====================================================
        # HEADER
        # =====================================================

        header = ctk.CTkFrame(
            self,
            height=95,
            corner_radius=0,
            fg_color="#242424"
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        icon = ctk.CTkLabel(
            header,
            text="👤",
            font=("Arial", 30)
        )

        icon.pack(
            pady=(15, 0)
        )

        title = ctk.CTkLabel(
            header,
            text="Create New User",
            font=("Arial", 19, "bold")
        )

        title.pack()

        # =====================================================
        # FORM
        # =====================================================

        form = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        form.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20
        )

        self.username = ctk.CTkEntry(
            form,
            placeholder_text="Username",
            height=44,
            corner_radius=10
        )

        self.username.pack(
            fill="x",
            pady=7
        )

        self.password = ctk.CTkEntry(
            form,
            placeholder_text="Password",
            show="•",
            height=44,
            corner_radius=10
        )

        self.password.pack(
            fill="x",
            pady=7
        )

        self.confirm = ctk.CTkEntry(
            form,
            placeholder_text="Confirm Password",
            show="•",
            height=44,
            corner_radius=10
        )

        self.confirm.pack(
            fill="x",
            pady=7
        )

        create_btn = ctk.CTkButton(
            form,
            text="Create User",
            height=44,
            corner_radius=10,
            font=("Arial", 13, "bold"),
            command=self.save
        )

        create_btn.pack(
            fill="x",
            pady=(20, 5)
        )

        self.username.focus()

    # =========================================================
    # SAVE
    # =========================================================

    def save(self):

        username = (
            self.username
            .get()
            .strip()
        )

        password = self.password.get()
        confirm = self.confirm.get()

        if not username:

            messagebox.showwarning(
                "Missing Username",
                "Please enter a username.",
                parent=self
            )

            return

        if not password:

            messagebox.showwarning(
                "Missing Password",
                "Please enter a password.",
                parent=self
            )

            return

        if password != confirm:

            messagebox.showerror(
                "Password Error",
                "Passwords do not match.",
                parent=self
            )

            return

        if len(password) < 4:

            messagebox.showwarning(
                "Weak Password",
                "Password must contain at least 4 characters.",
                parent=self
            )

            return

        try:

            conn = sqlite3.connect(
                DATABASE_NAME
            )

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE username = ?
                """,
                (username,)
            )

            if cursor.fetchone():

                conn.close()

                messagebox.showerror(
                    "Username Exists",
                    "That username is already in use.",
                    parent=self
                )

                return

            cursor.execute(
                """
                INSERT INTO users
                (username, password)
                VALUES (?, ?)
                """,
                (
                    username,
                    password
                )
            )

            conn.commit()
            conn.close()

            self.parent.load_users()

            messagebox.showinfo(
                "User Created",
                f"'{username}' has been added successfully.",
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
# EDIT USER WINDOW
# =============================================================

class EditUserWindow(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        user_id,
        username
    ):

        super().__init__(
            parent
        )

        self.parent = parent
        self.user_id = user_id

        self.title(
            "Edit User"
        )

        self.geometry(
            "440x270"
        )

        self.resizable(
            False,
            False
        )

        self.transient(
            parent
        )

        self.grab_set()

        title = ctk.CTkLabel(
            self,
            text="✏  Edit User",
            font=("Arial", 21, "bold")
        )

        title.pack(
            pady=(25, 20)
        )

        self.username = ctk.CTkEntry(
            self,
            placeholder_text="Username",
            height=44,
            corner_radius=10
        )

        self.username.insert(
            0,
            username
        )

        self.username.pack(
            fill="x",
            padx=30,
            pady=8
        )

        save_btn = ctk.CTkButton(
            self,
            text="Save Changes",
            height=44,
            corner_radius=10,
            font=("Arial", 13, "bold"),
            command=self.save
        )

        save_btn.pack(
            fill="x",
            padx=30,
            pady=20
        )

        self.username.focus()

    # =========================================================
    # SAVE
    # =========================================================

    def save(self):

        username = (
            self.username
            .get()
            .strip()
        )

        if not username:

            messagebox.showwarning(
                "Missing Username",
                "Username cannot be empty.",
                parent=self
            )

            return

        try:

            conn = sqlite3.connect(
                DATABASE_NAME
            )

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE username = ?
                AND id != ?
                """,
                (
                    username,
                    self.user_id
                )
            )

            if cursor.fetchone():

                conn.close()

                messagebox.showerror(
                    "Username Exists",
                    "That username is already in use.",
                    parent=self
                )

                return

            cursor.execute(
                """
                UPDATE users
                SET username = ?
                WHERE id = ?
                """,
                (
                    username,
                    self.user_id
                )
            )

            conn.commit()
            conn.close()

            self.parent.load_users()

            self.destroy()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e),
                parent=self
            )


# =============================================================
# CHANGE PASSWORD WINDOW
# =============================================================

class ChangePasswordWindow(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        user_id,
        username
    ):

        super().__init__(
            parent
        )

        self.parent = parent
        self.user_id = user_id

        self.title(
            "Reset Password"
        )

        self.geometry(
            "440x350"
        )

        self.resizable(
            False,
            False
        )

        self.transient(
            parent
        )

        self.grab_set()

        title = ctk.CTkLabel(
            self,
            text="🔐 Reset Password",
            font=("Arial", 21, "bold")
        )

        title.pack(
            pady=(25, 5)
        )

        username_label = ctk.CTkLabel(
            self,
            text=f"Changing password for  •  {username}",
            text_color="#9CA3AF",
            font=("Arial", 11)
        )

        username_label.pack(
            pady=(0, 20)
        )

        self.password = ctk.CTkEntry(
            self,
            placeholder_text="New Password",
            show="•",
            height=44,
            corner_radius=10
        )

        self.password.pack(
            fill="x",
            padx=30,
            pady=8
        )

        self.confirm = ctk.CTkEntry(
            self,
            placeholder_text="Confirm New Password",
            show="•",
            height=44,
            corner_radius=10
        )

        self.confirm.pack(
            fill="x",
            padx=30,
            pady=8
        )

        save_btn = ctk.CTkButton(
            self,
            text="Update Password",
            height=44,
            corner_radius=10,
            font=("Arial", 13, "bold"),
            command=self.save
        )

        save_btn.pack(
            fill="x",
            padx=30,
            pady=20
        )

        self.password.focus()

    # =========================================================
    # SAVE
    # =========================================================

    def save(self):

        password = self.password.get()
        confirm = self.confirm.get()

        if not password:

            messagebox.showwarning(
                "Missing Password",
                "Please enter a new password.",
                parent=self
            )

            return

        if password != confirm:

            messagebox.showerror(
                "Password Error",
                "Passwords do not match.",
                parent=self
            )

            return

        if len(password) < 4:

            messagebox.showwarning(
                "Weak Password",
                "Password must contain at least 4 characters.",
                parent=self
            )

            return

        try:

            conn = sqlite3.connect(
                DATABASE_NAME
            )

            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE users
                SET password = ?
                WHERE id = ?
                """,
                (
                    password,
                    self.user_id
                )
            )

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Password Updated",
                "The password has been updated successfully.",
                parent=self
            )

            self.destroy()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e),
                parent=self
            )
