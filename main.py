from login import LoginWindow
from database import initialize_database


def main():
    initialize_database()

    app = LoginWindow()
    app.root.mainloop()


if __name__ == "__main__":
    main()
