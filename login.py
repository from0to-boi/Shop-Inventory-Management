import ctypes

myappid = "mycompany.shopinventorymanager.1.0"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

import customtkinter as ctk
from tkinter import messagebox

from database import verify_user, create_user
from dashboard import Dashboard


class LoginWindow:

    def __init__(self):

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()

        self.root.title(
            "Shop Inventory Management"
        )

        self.root.geometry(
            "900x600"
        )

        self.root.resizable(
            False,
            False
        )
        self.root.iconbitmap("Icons/icon.ico")
        
        self.widgets()

        self.root.mainloop()

    # =========================================================
    # LOGIN UI
    # =========================================================

    def widgets(self):

        self.login_frame = ctk.CTkFrame(
            self.root,
            width=380,
            height=420,
            corner_radius=20
        )

        self.login_frame.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # -----------------------------------------------------
        # Title
        # -----------------------------------------------------

        self.title = ctk.CTkLabel(
            self.login_frame,
            text="Welcome Back",
            font=("Segoe UI", 28, "bold")
        )

        self.title.pack(
            pady=(35, 5)
        )

        self.subtitle = ctk.CTkLabel(
            self.login_frame,
            text="Sign in to continue",
            font=("Segoe UI", 14)
        )

        self.subtitle.pack(
            pady=(0, 30)
        )

        # -----------------------------------------------------
        # Username
        # -----------------------------------------------------

        self.username_entry = ctk.CTkEntry(
            self.login_frame,
            width=280,
            height=40,
            placeholder_text="Username"
        )

        self.username_entry.pack(
            pady=10
        )

        # -----------------------------------------------------
        # Password
        # -----------------------------------------------------

        self.password_entry = ctk.CTkEntry(
            self.login_frame,
            width=280,
            height=40,
            placeholder_text="Password",
            show="*"
        )

        self.password_entry.pack(
            pady=10
        )

        # -----------------------------------------------------
        # Remember Me
        # -----------------------------------------------------

        self.remember = ctk.CTkCheckBox(
            self.login_frame,
            text="Remember me"
        )

        self.remember.pack(
            pady=(10, 20)
        )

        # -----------------------------------------------------
        # Login
        # -----------------------------------------------------

        self.login_button = ctk.CTkButton(
            self.login_frame,
            text="Login",
            width=280,
            height=42,
            command=self.login
        )

        self.login_button.pack()

        # -----------------------------------------------------
        # Footer
        # -----------------------------------------------------

        self.footer = ctk.CTkLabel(
            self.login_frame,
            text="Shop Inventory Management",
            font=("Segoe UI", 12)
        )

        self.footer.pack(
            pady=(20, 5)
        )

        # -----------------------------------------------------
        # Create Account
        # -----------------------------------------------------

        self.create_account_btn = ctk.CTkButton(
            self.login_frame,
            text="Create an account",
            fg_color="transparent",
            hover=False,
            text_color="#4DA3FF",
            command=self.create_account_window
        )

        self.create_account_btn.pack()

        # Enter key = login

        self.password_entry.bind(
            "<Return>",
            lambda event: self.login()
        )

    # =========================================================
    # LOGIN
    # =========================================================

    def login(self):

        username = (
            self.username_entry
            .get()
            .strip()
        )

        password = (
            self.password_entry
            .get()
        )

        if not username or not password:

            messagebox.showerror(
                "Error",
                "Please fill in all fields."
            )

            return

        user = verify_user(
            username,
            password
        )

        if user:

            print("Login successful")

            self.root.destroy()

            print("Opening dashboard...")

            dashboard = Dashboard(
                user
            )

            dashboard.mainloop()

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid username or password."
            )

    # =========================================================
    # CREATE ACCOUNT WINDOW
    # =========================================================

    def create_account_window(self):

        self.register = ctk.CTkToplevel(
            self.root
        )

        self.register.title(
            "Create Account"
        )

        self.register.geometry(
            "420x420"
        )

        self.register.resizable(
            False,
            False
        )

        self.register.transient(
            self.root
        )

        self.register.grab_set()

        # -----------------------------------------------------
        # Header
        # -----------------------------------------------------

        title = ctk.CTkLabel(
            self.register,
            text="👤 Create Account",
            font=("Segoe UI", 24, "bold")
        )

        title.pack(
            pady=(30, 5)
        )

        subtitle = ctk.CTkLabel(
            self.register,
            text="Create a new application account",
            text_color="#9CA3AF",
            font=("Segoe UI", 12)
        )

        subtitle.pack(
            pady=(0, 20)
        )

        # -----------------------------------------------------
        # Username
        # -----------------------------------------------------

        self.new_username = ctk.CTkEntry(
            self.register,
            width=280,
            height=42,
            placeholder_text="Username"
        )

        self.new_username.pack(
            pady=8
        )

        # -----------------------------------------------------
        # Password
        # -----------------------------------------------------

        self.new_password = ctk.CTkEntry(
            self.register,
            width=280,
            height=42,
            placeholder_text="Password",
            show="*"
        )

        self.new_password.pack(
            pady=8
        )

        # -----------------------------------------------------
        # Confirm Password
        # -----------------------------------------------------

        self.confirm_password = ctk.CTkEntry(
            self.register,
            width=280,
            height=42,
            placeholder_text="Confirm Password",
            show="*"
        )

        self.confirm_password.pack(
            pady=8
        )

        # -----------------------------------------------------
        # Register
        # -----------------------------------------------------

        register_btn = ctk.CTkButton(
            self.register,
            text="Create Account",
            width=280,
            height=44,
            corner_radius=10,
            font=("Segoe UI", 13, "bold"),
            command=self.register_user
        )

        register_btn.pack(
            pady=(25, 10)
        )

        self.new_username.focus()

    # =========================================================
    # REGISTER USER
    # =========================================================

    def register_user(self):

        username = (
            self.new_username
            .get()
            .strip()
        )

        password = (
            self.new_password
            .get()
        )

        confirm = (
            self.confirm_password
            .get()
        )

        # -----------------------------------------------------
        # Empty fields
        # -----------------------------------------------------

        if not username or not password or not confirm:

            messagebox.showerror(
                "Error",
                "Please fill in all fields.",
                parent=self.register
            )

            return

        # -----------------------------------------------------
        # Username validation
        # -----------------------------------------------------

        if len(username) < 3:

            messagebox.showerror(
                "Invalid Username",
                "Username must be at least 3 characters long.",
                parent=self.register
            )

            return

        if " " in username:

            messagebox.showerror(
                "Invalid Username",
                "Username cannot contain spaces.",
                parent=self.register
            )

            return

        # -----------------------------------------------------
        # Password validation
        # -----------------------------------------------------

        if len(password) < 6:

            messagebox.showerror(
                "Invalid Password",
                "Password must be at least 6 characters long.",
                parent=self.register
            )

            return

        if password != confirm:

            messagebox.showerror(
                "Password Error",
                "Passwords do not match.",
                parent=self.register
            )

            return

        # -----------------------------------------------------
        # Create account
        # -----------------------------------------------------

        try:

            success = create_user(
                username,
                password
            )

            if success:

                messagebox.showinfo(
                    "Account Created",
                    "Account created successfully.",
                    parent=self.register
                )

                self.register.destroy()

            else:

                messagebox.showerror(
                    "Username Exists",
                    "That username is already taken.",
                    parent=self.register
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e),
                parent=self.register
            )


# =============================================================
# RUN
# =============================================================

if __name__ == "__main__":

    LoginWindow()
