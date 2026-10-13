import reflex as rx
from Wearly.Backend.login import Login
from Wearly.Frontend.Dark_n_Light_Mode import dark_light_theme_toggle


class SidebarState(rx.State):
    collapsed: bool = False

    def toggle_sidebar(self):
        self.collapsed = not self.collapsed



def home_page_main_content() -> rx.Component:
    return rx.vstack(    
        rx.divider(),    
        sidebar_items(),
        width="100%",
    )



def profile_n_settings() -> rx.Component:
    return rx.vstack(
        rx.divider(),
        sidebar_item("My Profile", "user-round", "/profile"),
        sidebar_item("Settings", "settings", "/settings"),
        width="100%",
        spacing="1",
    )


def sidebar_item(text: str, icon: str, href: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon, size=20),
            rx.cond(
                SidebarState.collapsed,
                rx.fragment(),
                rx.text(text, size="3"),
            ),
            width="100%",
            padding="0.75rem",
            align="center",
            justify=rx.cond(
                SidebarState.collapsed,
                "center",
                "start",
            ),
            spacing="3",
            border_radius="8px",
            _hover={
                "background": rx.color("accent", 3),
            },
        ),
        href=href,
        underline="none",
        width="100%",
    )



def sidebar_items() -> rx.Component:
    return rx.vstack(
        # Collapse / expand button
        rx.hstack(
            rx.spacer(),
            rx.button(
                rx.icon(
                    rx.cond(
                        SidebarState.collapsed,
                        "chevron-right",
                        "chevron-left",
                    )
                ),
                on_click=SidebarState.toggle_sidebar,
                variant="ghost",
                size="2",
            ),
            width="100%",
        ),

        # Main navigation
        dark_light_theme_toggle(),
        rx.vstack(
            sidebar_item("My Wardrobe", "shirt", "/wardrobe"),
            sidebar_item("Color Analysis", "palette", "/color-analysis"),
            sidebar_item("Outfit Recommendations", "sparkles", "/outfits"),
            sidebar_item("Virtual Try-On", "scan", "/try-on"),
            sidebar_item("Discover & Shop", "shopping-bag", "/shop"),
            width="100%",
            spacing="1",
        ),

        # Push profile/settings to the bottom
        rx.spacer(),

        profile_n_settings(),
        
        rx.button(
            rx.icon("log-out", size=20),
            rx.cond(
                SidebarState.collapsed,
                rx.fragment(),
                rx.text("Logout"),
            ),
            on_click=Login.execute_logout,
            variant="soft",
            color_scheme="red",
            width="100%",
            justify="center",
        ),

        width=rx.cond(
            SidebarState.collapsed,
            "65px",
            "250px",
        ),
        height="calc(100vh - 100px)",
        padding="0.75rem",
        border="1px solid #E5E7EB",
        border_radius="12px",
        spacing="3",
        align="stretch",
        flex_shrink="0",
        transition="width 0.2s ease",
    )
