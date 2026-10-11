import reflex as rx
from rxconfig import config
from Wearly.Backend.login import Login


class State(rx.State):
    """The app state."""


@rx.page(route="/home",on_load=Login.check_login)
def home_page() -> rx.Component:
    return rx.cond(
        Login.is_logged_in,
        rx.vstack(
            rx.heading("Welcome to Wearly!"),
            rx.button("Logout", on_click=Login.execute_logout),
        )
    ) 


def login_page() -> rx.Component:
    return rx.center(
        rx.card(
            rx.vstack(
                rx.center(
                    rx.image(
                        src="/Logo.png",
                        alt="Wearly logo",
                        width="6.0em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading(
                        "Sign in to your account",
                        size="6",
                        as_="h2",
                        text_align="center",
                        width="100%",
                    ),
                    direction="column",
                    spacing="5",
                    width="100%",
                ),
                rx.vstack(
                    rx.text(
                        "Email address",
                        size="3",
                        weight="medium",
                        text_align="left",
                        width="100%",
                    ),
                    rx.input(
                        placeholder="user@gmail.com",
                        type="email",
                        size="3",
                        width="100%",
                        value=Login.email,
                        on_change=Login.set_email,
                    ),
                    justify="start",
                    spacing="2",
                    width="100%",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text("Password", size="3", weight="medium"),
                        justify="between",
                        width="100%",
                    ),
                    rx.input(
                        placeholder="Enter your password",
                        type="password",
                        size="3",
                        width="100%",
                        value=Login.password,
                        on_change=Login.set_password,
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.button("Sign in", size="3", width="100%",on_click=Login.execute_login),
            ),
            max_width="400px",
            width="100%",
        ),
        width="100%",
        height="100vh",
    )


app = rx.App()

app.add_page(login_page, route="/login")