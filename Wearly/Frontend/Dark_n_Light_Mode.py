import reflex as rx


def dark_light_theme_toggle() -> rx.Component:
    return rx.icon_button(
        rx.cond(
            rx.color_mode == "light",
            rx.icon("moon"),
            rx.icon("sun"),
        ),
        on_click=rx.toggle_color_mode,
        variant="soft",
        size="3",
        aria_label="Toggle dark mode",
    )
