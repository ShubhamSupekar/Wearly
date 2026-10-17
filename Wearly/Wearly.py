import reflex as rx
from Wearly.Frontend.Page_Strucutres import about_page_structure
from rxconfig import config
from Wearly.Backend.login import Login
from Wearly.Frontend.Page_Strucutres.home_page_structure import home_page_main_content
from Wearly.Frontend.Page_Strucutres.about_page_structure import about_page_main_Content
from Wearly.Frontend.Page_Strucutres.login_page_strucutre import login_page_main_content
from Wearly.Frontend.Page_Strucutres.profile_page_structure import profile_page_main_content
from Wearly.Frontend.Page_Strucutres.discover_n_shop_page_structure import discover_n_shop_page_main_content
from Wearly.Frontend.Supportive_Functions.Responsive_Layout import responsive_page


class State(rx.State):
    """The app state."""


def about_page() -> rx.Component:
    return responsive_page(about_page_main_Content())


@rx.page(route="/home",on_load=Login.check_login)
def home_page() -> rx.Component:
    return rx.cond(
        Login.is_logged_in,
        responsive_page(home_page_main_content()),
        rx.text("Please log in to continue."),
        )


@rx.page(route="/profile",on_load=Login.check_login)
def profile_page() -> rx.Component:
    return rx.cond(
            Login.is_logged_in,
            responsive_page(profile_page_main_content()),
            rx.text("Please log in to continue."),
            )


@rx.page(route="/shop",on_load=Login.check_login)
def shop_page() -> rx.Component:
    return rx.cond(
            Login.is_logged_in,
            responsive_page(discover_n_shop_page_main_content()),
            rx.text("Please log in to continue."),
            )


@rx.page(route="/login")
def login_page() -> rx.Component:
    return responsive_page(login_page_main_content())


app = rx.App(    
    style={
        "*": {
            "box_sizing": "border-box",
        },
        "html, body": {
            "margin": "0",
            "padding": "0",
            "width": "100%",
            "min_height": "100%",
        },
        "body": {
            "overflow_x": "hidden",
        },
    })

app.add_page(about_page, route="/")