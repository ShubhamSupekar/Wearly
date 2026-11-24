from pathlib import Path
from urllib.parse import quote

import requests


def download_model(model: dict, destination: Path, progress=None) -> Path:
    """Download a public LiteRT-LM model from Hugging Face without a token."""
    destination.mkdir(parents=True, exist_ok=True)
    filename = model["filename"]
    target = destination / filename
    partial = destination / (filename + ".part")
    url = (
        f"https://huggingface.co/{model['repo']}/resolve/main/"
        f"{quote(filename, safe='')}"
    )
    headers = {"User-Agent": "Wearly-Mobile-Model-Tester/0.2"}

    # Resume a partial download when the server supports HTTP byte ranges.
    existing = partial.stat().st_size if partial.exists() else 0
    if existing:
        headers["Range"] = f"bytes={existing}-"

    with requests.get(
        url, headers=headers, stream=True, allow_redirects=True, timeout=(30, 300)
    ) as response:
        if response.status_code in (401, 403):
            raise RuntimeError(
                "The public model file is not accessible anonymously. "
                "Check the model repository's access and license conditions."
            )
        if existing and response.status_code != 206:
            # Server ignored Range; restart cleanly to avoid a corrupt file.
            existing = 0
            partial.unlink(missing_ok=True)
        response.raise_for_status()

        total_header = response.headers.get("content-length")
        total = (int(total_header) + existing) if total_header else 0
        mode = "ab" if existing else "wb"
        done = existing

        with partial.open(mode) as output:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    output.write(chunk)
                    done += len(chunk)
                    if progress:
                        progress(done, total)

    partial.replace(target)
    return target
