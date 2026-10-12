import reflex as rx


def about_page_main_Content():
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