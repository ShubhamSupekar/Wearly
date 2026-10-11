import reflex as rx
from Wearly.Backend.login import Login


def main_content() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.heading("Welcome to Wearly!"),
            rx.spacer(),
            rx.image(
                src="/Logo.png",
                alt="Wearly logo",
                width="3em",
                height="auto",
            ),
            rx.spacer(),
            rx.button(
                "Logout",
                on_click=Login.execute_logout,
            ),
            width="100%",
            align="center",
        ),
        sidebar_items(),
        width="100%",
    )


def sidebar_item(text: str, icon: str, href: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon),
            rx.text(text, size="4"),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            style={
                "_hover": {
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "border-radius": "0.5em",
            },
        ),
        href=href,
        underline="none",
        weight="medium",
        width="25%",
    )


def sidebar_items() -> rx.Component:
    return rx.vstack(
        sidebar_item("Dashboard", "layout-dashboard", "/#"),
        sidebar_item("Projects", "square-library", "/#"),
        sidebar_item("Analytics", "bar-chart-4", "/#"),
        sidebar_item("Messages", "mail", "/#"),
        spacing="1",
        width="50%",
    )