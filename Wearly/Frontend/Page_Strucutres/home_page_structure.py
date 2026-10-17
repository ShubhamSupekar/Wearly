import reflex as rx
from Wearly.Frontend.Supportive_Functions.SideBar_Layout import sidebar_items


def home_page_main_content() -> rx.Component:
    return rx.vstack(    
        rx.divider(),    
        sidebar_items("outfit-recommendations"),
        width="100%",
    )



