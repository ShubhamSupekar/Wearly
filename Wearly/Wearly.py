import reflex as rx
from rxconfig import config
from Wearly.Backend.login import Login
from Wearly.home_page_structure import main_content

class State(rx.State):
    """The app state."""


def about_page() -> rx.Component:
    return rx.box(
        # Top navigation
        rx.hstack(
            rx.heading("Wearly", size="6"),
            rx.spacer(),
            rx.link(
                rx.button("Login"),
                href="/login",
            ),
            width="100%",
            align="center",
            padding="1.5em 2em",
        ),

        # About content
        rx.center(
            rx.vstack(
                rx.image(
                        src="/Logo.png",
                        alt="Wearly logo",
                        width="10.0em",
                        height="auto",
                        border_radius="25%",
                ),
                rx.heading("Dress with confidence.", size="8"),
                rx.text(
                    "Wearly helps you discover colors, create outfits, "
                    "and make everyday fashion decisions easier."
                ),
                spacing="4",
                align="center",
                text_align="center",
                max_width="600px",
            ),
            width="100%",
            min_height="70vh",
        ),
        width="100%",
    )     


@rx.page(route="/home",on_load=Login.check_login)
def home_page() -> rx.Component:
    return rx.cond(
        Login.is_logged_in,
        main_content(),
        rx.text("Please log in to continue."),
        )


@rx.page(route="/login")
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

app.add_page(about_page, route="/")