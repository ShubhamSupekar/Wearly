import reflex as rx
from Wearly.Frontend.Supportive_Functions.Dark_n_Light_Mode import dark_light_theme_toggle
from Wearly.Backend.login import Login


class SidebarState(rx.State):
    collapsed: bool = False

    def toggle_sidebar(self):
        self.collapsed = not self.collapsed


def sidebar_item(
    text: str,
    icon: str,
    href: str,
    active: bool = False,
) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(
                icon,
                size=20,
                flex_shrink="0",
                color=rx.cond(
                    active,
                    rx.color("accent", 11),
                    "currentColor",
                ),
                _hover={
                    "transform": "scale(1.12)",
                },
            ),
            rx.cond(
                SidebarState.collapsed,
                rx.fragment(),
                rx.text(
                    text,
                    size="3",
                    weight=rx.cond(active, "bold", "medium"),
                ),
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
            background=rx.cond(
                active,
                rx.color("accent", 3),
                "transparent",
            ),
            color=rx.cond(
                active,
                rx.color("accent", 11),
                "var(--gray-11)",
            ),
            border_left=rx.cond(
                active,
                f"3px solid {rx.color('accent', 9)}",
                "3px solid transparent",
            ),
            _hover={
                "background": rx.color("accent", 3),
                "transform": "translateX(4px)",
                "box_shadow": "0 3px 10px rgba(0, 0, 0, 0.06)",
            },
        ),
        href=href,
        underline="none",
        width="100%",
    )



def sidebar_items(active_item: str) -> rx.Component:
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
        rx.divider(),
        rx.vstack(
            sidebar_item("Outfit Recommendations", "sparkles", "/home", active=active_item == "outfit-recommendations"),
            sidebar_item("Color Analysis", "palette", "/color-analysis", active=active_item == "color-analysis"),
            sidebar_item("My Wardrobe", "shirt", "/wardrobe", active=active_item == "wardrobe"),
            sidebar_item("Virtual Try-On", "scan", "/try-on", active=active_item == "try-on"),
            sidebar_item("Discover & Shop", "shopping-bag", "/shop", active=active_item == "shop"),
            width="100%",
            spacing="1",
        ),

        # Push profile/settings to the bottom
        rx.spacer(),
        rx.vstack(
            rx.divider(),
            sidebar_item("My Profile", "user-round", "/profile", active=active_item == "profile"),
            sidebar_item("Settings", "settings", "/settings", active=active_item == "settings"),
            width="100%",
            spacing="1",
        ),

        
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
            transition="all 0.2s ease-in-out",
            _hover={
                "transform": "translateY(-2px)",
                "box_shadow": "0 4px 12px rgba(239, 68, 68, 0.18)",
            },
        ),

        position="fixed",
        top="25px",
        left="0px",
        width=rx.cond(
            SidebarState.collapsed,
            "65px",
            "250px",
        ),
        height="calc(100dvh - 100px)",
        max_height="calc(100dvh - 100px)",
        padding="0.75rem",
        border=rx.color_mode_cond(
            light="1px solid rgba(156, 163, 175, 0.9)",
            dark="1px solid rgba(75, 85, 99, 0.8)",
        ),
        border_radius="12px",
        background=rx.color_mode_cond(
            light="rgba(249, 250, 251, 0.98)",
            dark="rgba(31, 41, 55, 0.98)",
        ),
        box_shadow="0 4px 16px rgba(0, 0, 0, 0.12)",
        z_index="1000",
        overflow_y="auto",
        spacing="3",
        align="stretch",
        flex_shrink="0",
        transition="width 0.2s ease",
    )