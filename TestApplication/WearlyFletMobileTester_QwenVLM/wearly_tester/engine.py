import time
from pathlib import Path


CLOTHING_ANALYSIS_PROMPT = """
You are a careful clothing and fashion image analyst for Wearly.
Inspect only what is visible in the uploaded photo. Describe:

1. Garment category and likely item type (for example shirt, T-shirt, trousers,
   jeans, dress, skirt, jacket, shoes or accessory).
2. Main colour and any secondary/accent colours. Use plain colour names; if
   useful, include approximate shade names such as navy, sky blue, burgundy,
   olive, beige or charcoal.
3. Pattern, print, texture and visible design.
4. Fabric appearance (for example denim-like, knitted, smooth, ribbed or woven).
   Do not claim exact fibre composition unless it is visibly labelled.
5. Cut, fit, silhouette, length, neckline, collar, sleeve type and hem details
   where visible.
6. Visible construction details such as buttons, zip, pockets, seams, cuffs,
   embroidery, logos or graphics.
7. Overall style and suitable occasions.
8. Suggest 2-3 colours or garment types that could pair well with it.

If a detail cannot be determined from the image, say "not clear from image".
Do not invent a brand, material composition, exact colour code or hidden details.
Use concise headings and bullet points.
"""


def runtime_status() -> str:
    try:
        import litert_lm  # noqa: F401
        return "LiteRT-LM Python runtime detected"
    except Exception:
        return "LiteRT-LM Python runtime not detected"


def _extract_text(response) -> str:
    pieces = []
    for item in response.get("content", []):
        if isinstance(item, dict) and item.get("type") == "text":
            pieces.append(item.get("text", ""))
    return "".join(pieces).strip() or str(response)


def _approx_metrics(text: str, started: float) -> dict:
    elapsed = max(time.perf_counter() - started, 0.001)
    tokens = max(1, len(text.split()))
    return {
        "text": text,
        "elapsed_s": elapsed,
        "output_tokens": tokens,
        "tokens_per_second": tokens / elapsed,
    }


def generate_text(model_path: str, prompt: str) -> dict:
    try:
        import litert_lm
    except ImportError as ex:
        raise RuntimeError(
            "No module named 'litert_lm'. Install and package the LiteRT-LM "
            "runtime for the target platform before running inference."
        ) from ex

    started = time.perf_counter()
    with litert_lm.Engine(model_path) as engine:
        with engine.create_conversation() as conversation:
            response = conversation.send_message(prompt)
    return _approx_metrics(_extract_text(response), started)


def generate_clothing_description(
    model_path: str, image_path: str, user_instructions: str = ""
) -> dict:
    """
    Multimodal inference using LiteRT-LM's documented Contents + ImageFile API.
    The selected photo is processed locally; it is not uploaded to a cloud API.
    """
    try:
        import litert_lm
    except ImportError as ex:
        raise RuntimeError(
            "No module named 'litert_lm'. The LiteRT-LM runtime is not available "
            "in this app build."
        ) from ex

    prompt = CLOTHING_ANALYSIS_PROMPT
    if user_instructions:
        prompt += "\nAdditional user instructions:\n" + user_instructions

    started = time.perf_counter()
    with litert_lm.Engine(
        model_path,
        vision_backend=litert_lm.Backend.GPU(),
    ) as engine:
        with engine.create_conversation() as conversation:
            response = conversation.send_message(
                litert_lm.Contents.of(
                    prompt,
                    litert_lm.Content.ImageFile(absolute_path=str(Path(image_path).resolve())),
                )
            )
    return _approx_metrics(_extract_text(response), started)
