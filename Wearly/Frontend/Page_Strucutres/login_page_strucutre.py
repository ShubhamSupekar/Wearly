import reflex as rx
from Wearly.Backend.login import Login
from Wearly.Frontend.Supportive_Functions.Dark_n_Light_Mode import dark_light_theme_toggle


def login_page_main_content() -> rx.Component:
    return rx.box(
        rx.box(
            dark_light_theme_toggle(),
            align="start",
            padding="1.5em 2em",
        ),
        rx.center(
            rx.card(
                rx.vstack(
                    rx.center(
                        rx.image(
                            src="/Logo.png",
                            alt="Wearly logo",
                            width="8.0em",
                            height="auto",
                            border_radius="25%",
                            border="3px solid",
                        ),
                        rx.heading(
                            "Sign in to your account",
                            size="5",
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
            height="60vh",
        ),
    )