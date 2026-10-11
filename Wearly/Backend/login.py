import reflex as rx

class Login(rx.State):
    """The app state."""

    email: str = ""
    password: str = ""
    is_logged_in: bool = False

    def set_email(self, email: str):
        self.email = email

    def set_password(self, password: str):
        self.password = password

    def execute_login(self):
        # Implement your login logic here
        print("Logging in with email:", self.email, "and password:", self.password)
        self.is_logged_in = True
        return rx.redirect("/home")

    def execute_logout(self):
        # Implement your logout logic here
        print("Logging out")
        self.email = ""
        self.password = ""
        self.is_logged_in = False
        return rx.redirect("/login")

    def check_login(self):
        if not self.is_logged_in:
            return rx.redirect("/login")