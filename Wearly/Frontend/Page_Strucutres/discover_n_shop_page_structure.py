import reflex as rx
from Wearly.Frontend.Page_Strucutres.home_page_structure import sidebar_items


def discover_n_shop_page_main_content() -> rx.Component:
    return rx.vstack(
        rx.divider(),
        rx.hstack(
            sidebar_items("shop"),
            rx.center(
                rx.vstack(
                    rx.icon(
                        "store",
                        size=56,
                        color="#8B5CF6",
                    ),
                    rx.heading(
                        "Wearly Shop",
                        size="8",
                        text_align="center",
                    ),
                    rx.badge(
                        "COMING SOON",
                        color_scheme="purple",
                        variant="soft",
                    ),
                    rx.text(
                        "Something exciting is on its way!",
                        size="4",
                        weight="medium",
                        text_align="center",
                    ),
                    rx.text(
                        "We're working on bringing your favorite fashion "
                        "stores and businesses closer to you. Soon, you'll "
                        "be able to explore clothing collections and discover "
                        "new styles through Wearly.",
                        text_align="center",
                        color="gray",
                        max_width="520px",
                    ),
                    rx.divider(width="100%"),
                    rx.heading(
                        "Are you a shop owner or business?",
                        size="5",
                        text_align="center",
                    ),
                    rx.text(
                        "Want to expand your business, showcase your "
                        "inventory, and connect with more customers? "
                        "Partner with Wearly!",
                        text_align="center",
                        max_width="500px",
                    ),
                    rx.link(
                        rx.button(
                            rx.icon("mail", size=18),
                            "Connect with Us",
                            size="3",
                            width="100%",
                        ),
                        href="mailto:shubham26supekar@gmail.com"
                        "?subject=Wearly%20Business%20Partnership",
                        is_external=False,
                    ),
                    rx.text(
                        "shubham26supekar@gmail.com",
                        size="2",
                        color="gray",
                    ),
                    align="center",
                    spacing="4",
                    width="100%",
                    max_width="600px",
                    padding="6",
                ),
                width="100%",
                min_height="85vh",
                margin_left="65px"
            ),
            width="100%",
            align="start",
        ),
        width="100%",
    )
