import reflex as rx


def responsive_page(*children) -> rx.Component:
    return rx.box(
        *children,
        width="100%",
        max_width="1440px",
        margin="0 auto",
        padding=["12px", "16px", "24px"],
        font_size=["14px", "15px", "16px"],
    )