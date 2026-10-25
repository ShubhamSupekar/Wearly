import reflex as rx
from Wearly.Frontend.Supportive_Functions.SideBar_Layout import sidebar_items,SidebarState


def photo_upload_card(
    title: str,
    description: str,
    upload_id: str,
) -> rx.Component:
    return rx.vstack(
        rx.heading(
            title,
            size="4",
            width="100%",
        ),
        rx.text(
            description,
            size="2",
            color="gray",
            width="100%",
        ),
        rx.upload(
            rx.vstack(
                rx.icon(
                    "camera",
                    size=28,
                ),
                rx.text(
                    "Tap to upload photo",
                    weight="medium",
                    text_align="center",
                ),
                rx.text(
                    "JPG, PNG or WEBP",
                    size="1",
                    color="gray",
                ),
                align="center",
                justify="center",
                spacing="2",
                width="100%",
                min_height="100px",
            ),
            id=upload_id,
            accept={
                "image/png": [".png"],
                "image/jpeg": [".jpg", ".jpeg"],
                "image/webp": [".webp"],
            },
            max_files=1,
            border="2px dashed #A0AEC0",
            border_radius="12px",
            padding="16px",
            width="100%",
            cursor="pointer",
        ),
        rx.text(
            rx.selected_files(upload_id),
            size="2",
            width="100%",
            overflow_wrap="anywhere",
        ),
        rx.hstack(
            rx.icon(
                "info",
                size=15,
                color="orange",
                flex_shrink="0",
            ),
            rx.text(
                "Keep your full face clearly visible. "
                "Avoid filters and strong shadows.",
                size="1",
                color="orange",
            ),
            align="start",
            spacing="2",
            width="100%",
        ),
        width="100%",
        align="start",
        spacing="3",
        padding=["14px", "16px", "18px"],
        border="1px solid #E2E8F0",
        border_radius="14px",
        box_shadow="0 2px 8px rgba(0, 0, 0, 0.04)",
    )




def profile_page_main_content() -> rx.Component:
    return rx.vstack(
        rx.divider(),

        rx.hstack(
            # Existing sidebar — unchanged
            sidebar_items("profile"),

            # Main profile content
            rx.vstack(
                rx.heading(
                    "My Profile",
                    size="6",
                    width="90%",
                ),

                rx.text(
                    "Upload three photos of your face in different "
                    "lighting conditions to help Wearly estimate "
                    "your skin tone.",
                    size="2",
                    color="gray",
                    width="90%",
                ),

                rx.callout(
                    "Use unfiltered photos. Daylight and neutral, "
                    "even lighting generally give more reliable "
                    "skin-tone estimates than artificial lighting.",
                    icon="info",
                    color_scheme="blue",
                    size="2",
                    width="90%",
                ),

                # Compact upload cards
                rx.vstack(
                    photo_upload_card(
                        "1. Night Lighting",
                        "Take a photo indoors at night with "
                        "your face clearly visible.",
                        "night_photo",
                    ),
                    photo_upload_card(
                        "2. Daylight",
                        "Take a photo in natural daylight, "
                        "preferably in open shade.",
                        "day_photo",
                    ),
                    photo_upload_card(
                        "3. Good Lighting",
                        "Take a front-facing photo in bright, "
                        "even, neutral lighting.",
                        "good_light_photo",
                    ),
                    width="90%",
                    spacing="2",
                ),

                rx.text(
                    "Your photos will be sent to Wearly's backend "
                    "for processing when you submit them.",
                    size="1",
                    color="gray",
                    width="90%",
                ),

                rx.button(
                    "Submit Photos",
                    width="90%",
                    size="3",
                ),

                width="90%",
                min_width="0",
                flex="1",
                align="start",
                spacing="3",
                padding=["12px", "16px"],
            ),

            # Main layout containing sidebar and page content
            width="100%",
            min_width="0",
            min_height="85vh",
            align="start",
            spacing="2",
            margin_left="55px",
            flex_direction=[
                "column",
                "column",
                "row",
            ],

        ),

        width="100%",
        min_width="0",
        align="stretch",
        spacing="0",
        padding="0",
    )
