import asyncio
from pathlib import Path
import shutil
import flet as ft

from wearly_tester.catalog import MODEL
from wearly_tester.downloader import download_model
from wearly_tester.engine import (
    generate_text,
    generate_clothing_description,
    runtime_status,
)


import os

def initialize_storage():
    storage_root = os.environ.get("FLET_APP_STORAGE_DATA")

    if storage_root:
        base_dir = Path(storage_root)
    else:
        # Mac development fallback
        base_dir = Path.home() / ".wearly_mobile_model_tester"

    app_dir = base_dir / "models"
    image_dir = base_dir / "images"

    app_dir.mkdir(parents=True, exist_ok=True)
    image_dir.mkdir(parents=True, exist_ok=True)

    print(f"Models directory: {app_dir}")
    print(f"Images directory: {image_dir}")

    return app_dir, image_dir


def main(page: ft.Page):
    APP_DIR, IMAGE_DIR = initialize_storage()
    
    page.title = "Wearly Mobile Model Tester"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 16
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = "#10131A"

    status = ft.Text("Ready", color="#AAB4C5", size=12)
    progress = ft.ProgressBar(
        value=0, visible=False, color="#8B9CFF", bgcolor="#293044"
    )

    prompt_field = ft.TextField(
        label="Text prompt",
        multiline=True,
        min_lines=3,
        max_lines=5,
        value="Explain three ways to match a navy blue shirt with trousers.",
    )
    text_output = ft.Text("Text response will appear here.", selectable=True)
    text_metrics = ft.Text("No text inference run yet.", color="#AAB4C5", size=12)

    download_button = ft.Button(
        "Download Qwen2-VL model", icon=ft.Icons.DOWNLOAD
    )
    text_run_button = ft.Button(
        "Run text prompt", icon=ft.Icons.PLAY_ARROW
    )
    delete_button = ft.OutlinedButton(
        "Delete local model", icon=ft.Icons.DELETE_OUTLINE
    )

    selected_image_path = None
    image_name = ft.Text("No clothing photo selected.", color="#AAB4C5")
    image_output = ft.Text(
        "Clothing analysis will appear here.", selectable=True
    )
    image_metrics = ft.Text(
        "No image analysis run yet.", color="#AAB4C5", size=12
    )
    image_prompt = ft.TextField(
        label="Optional instructions",
        multiline=True,
        min_lines=2,
        max_lines=4,
        value=(
            "Analyze this clothing item for a fashion wardrobe. Describe the "
            "garment type, main and secondary colours, pattern or print, fabric "
            "appearance, neckline, sleeves, fit, silhouette, visible design "
            "details, closures, pockets, and style. Distinguish visible facts "
            "from uncertain guesses. Do not invent a brand or exact fabric "
            "composition. Finish with suitable occasions and matching colours."
        ),
    )
    choose_image_button = ft.Button(
        "Choose clothing photo", icon=ft.Icons.IMAGE
    )
    analyze_image_button = ft.Button(
        "Analyze clothing photo", icon=ft.Icons.AUTO_AWESOME, disabled=True
    )

    file_picker = ft.FilePicker()
    page.services.append(file_picker)

    def model_path():
        return APP_DIR / MODEL["filename"]

    def refresh_local_state():
        p = model_path()
        if p.exists():
            status.value = (
                f"Qwen2-VL downloaded · {p.stat().st_size / (1024**3):.2f} GB"
            )
        else:
            status.value = "Qwen2-VL not downloaded"
        page.update()

    async def do_download(_):
        progress.visible = True
        progress.value = 0
        download_button.disabled = True
        status.value = "Starting public Qwen2-VL download…"
        page.update()

        def on_progress(done, total):
            progress.value = done / total if total else None
            if total:
                status.value = (
                    f"Downloading Qwen2-VL · {done / (1024**3):.2f} / "
                    f"{total / (1024**3):.2f} GB"
                )
            else:
                status.value = f"Downloaded {done / (1024**3):.2f} GB"
            page.update()

        try:
            path = await asyncio.to_thread(
                download_model, MODEL, APP_DIR, on_progress
            )
            progress.value = 1
            status.value = (
                f"Download complete · {path.stat().st_size / (1024**3):.2f} GB"
            )
        except Exception as ex:
            status.value = f"Download failed: {ex}"
        finally:
            progress.visible = False
            download_button.disabled = False
            page.update()

    async def do_text_generate(_):
        p = model_path()
        if not p.exists():
            status.value = "Download Qwen2-VL first."
            page.update()
            return
        if not prompt_field.value.strip():
            status.value = "Enter a prompt first."
            page.update()
            return

        text_run_button.disabled = True
        text_output.value = "Loading Qwen2-VL and generating…"
        text_metrics.value = "First model load can take time and use substantial RAM."
        status.value = "Running text inference locally…"
        page.update()

        try:
            result = await asyncio.to_thread(
                generate_text, str(p), prompt_field.value.strip()
            )
            text_output.value = result["text"]
            text_metrics.value = (
                f"Elapsed: {result['elapsed_s']:.2f} s · "
                f"Approx. output tokens: {result['output_tokens']} · "
                f"Approx. speed: {result['tokens_per_second']:.2f} tokens/s"
            )
            status.value = "Text inference complete · on-device"
        except Exception as ex:
            text_output.value = f"Inference failed:\n\n{ex}"
            status.value = "Text inference failed"
        finally:
            text_run_button.disabled = False
            page.update()

    async def choose_clothing_photo(_):
        nonlocal selected_image_path
        try:
            files = await file_picker.pick_files(
                dialog_title="Choose a clothing photo",
                file_type=ft.FilePickerFileType.IMAGE,
                allow_multiple=False,
                with_data=True,
            )
            if not files:
                return

            picked = files[0]
            suffix = Path(picked.name).suffix.lower() or ".jpg"
            if suffix not in {".jpg", ".jpeg", ".png", ".webp", ".bmp"}:
                image_name.value = "Unsupported image type. Choose JPG, PNG or WebP."
                analyze_image_button.disabled = True
                page.update()
                return

            destination = IMAGE_DIR / f"clothing_upload{suffix}"
            if picked.bytes:
                destination.write_bytes(picked.bytes)
            elif picked.path and Path(picked.path).exists():
                shutil.copy2(picked.path, destination)
            else:
                raise RuntimeError(
                    "The selected image could not be read by Flet. "
                    "Try selecting it again."
                )

            selected_image_path = str(destination)
            image_name.value = (
                f"Selected: {picked.name} · {destination.stat().st_size / 1024:.0f} KB"
            )
            analyze_image_button.disabled = False
            image_output.value = "Photo ready. Tap Analyze clothing photo."
            image_metrics.value = "Image will be processed locally by Qwen2-VL."
        except Exception as ex:
            image_name.value = f"Could not select image: {ex}"
            analyze_image_button.disabled = True
        page.update()

    async def do_image_analysis(_):
        p = model_path()
        if not p.exists():
            status.value = "Download Qwen2-VL first."
            page.update()
            return
        if not selected_image_path or not Path(selected_image_path).exists():
            status.value = "Choose a clothing photo first."
            page.update()
            return

        analyze_image_button.disabled = True
        image_output.value = "Analyzing clothing photo…"
        image_metrics.value = (
            "The image is sent to the local vision encoder; this may take a while."
        )
        status.value = "Running image inference locally…"
        page.update()

        try:
            result = await asyncio.to_thread(
                generate_clothing_description,
                str(p),
                selected_image_path,
                image_prompt.value.strip(),
            )
            image_output.value = result["text"]
            image_metrics.value = (
                f"Elapsed: {result['elapsed_s']:.2f} s · "
                f"Approx. output tokens: {result['output_tokens']} · "
                f"Approx. speed: {result['tokens_per_second']:.2f} tokens/s"
            )
            status.value = "Clothing analysis complete · on-device"
        except Exception as ex:
            image_output.value = (
                "Image analysis failed:\n\n"
                f"{ex}\n\n"
                "Check that the downloaded model is the Qwen2-VL multimodal "
                "LiteRT-LM bundle and that the installed runtime supports its "
                "vision path."
            )
            status.value = "Image analysis failed"
        finally:
            analyze_image_button.disabled = False
            page.update()

    async def do_delete(_):
        p = model_path()
        if p.exists():
            p.unlink()
            status.value = "Local Qwen2-VL model deleted."
        else:
            status.value = "No local model file to delete."
        page.update()

    download_button.on_click = do_download
    text_run_button.on_click = do_text_generate
    choose_image_button.on_click = choose_clothing_photo
    analyze_image_button.on_click = do_image_analysis
    delete_button.on_click = do_delete

    rt = runtime_status()
    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.AUTO_AWESOME, color="#A8B4FF", size=30),
                        ft.Column(
                            [
                                ft.Text("Wearly", size=24, weight=ft.FontWeight.BOLD),
                                ft.Text(
                                    "Mobile Model Tester · Qwen Vision",
                                    size=13,
                                    color="#AAB4C5",
                                ),
                            ],
                            spacing=0,
                        ),
                    ],
                    spacing=10,
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("1 · Qwen model manager", size=17, weight=ft.FontWeight.BOLD),
                            ft.Text(MODEL["label"], weight=ft.FontWeight.BOLD),
                            ft.Text(MODEL["notes"], size=12, color="#AAB4C5"),
                            ft.Text(
                                "Public Hugging Face file. No Hugging Face token is used.",
                                size=12,
                                color="#AAB4C5",
                            ),
                            download_button,
                            progress,
                            status,
                            delete_button,
                        ],
                        spacing=10,
                    ),
                    padding=16,
                    border=ft.Border.all(width=1, color="#30384A"),
                    border_radius=14,
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("2 · Text inference", size=17, weight=ft.FontWeight.BOLD),
                            ft.Text(f"Runtime: {rt}", size=12, color="#AAB4C5"),
                            prompt_field,
                            text_run_button,
                            ft.Divider(color="#30384A"),
                            ft.Text("Text response", weight=ft.FontWeight.BOLD),
                            text_output,
                            text_metrics,
                        ],
                        spacing=10,
                    ),
                    padding=16,
                    border=ft.Border.all(width=1, color="#30384A"),
                    border_radius=14,
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("3 · Clothing photo analysis", size=17, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                "Upload a clothing photo and let Qwen2-VL inspect its visible details.",
                                size=12,
                                color="#AAB4C5",
                            ),
                            choose_image_button,
                            image_name,
                            image_prompt,
                            analyze_image_button,
                            ft.Divider(color="#30384A"),
                            ft.Text("Clothing description", weight=ft.FontWeight.BOLD),
                            image_output,
                            image_metrics,
                        ],
                        spacing=10,
                    ),
                    padding=16,
                    border=ft.Border.all(width=1, color="#30384A"),
                    border_radius=14,
                ),
                ft.Text(
                    "Model size is approximately 1.78 GB. Actual RAM use is higher. "
                    "Use a phone with sufficient free storage and memory; run one task at a time.",
                    size=11,
                    color="#8D98AA",
                ),
            ],
            spacing=16,
        )
    )
    refresh_local_state()


if __name__ == "__main__":
    ft.run(main)
