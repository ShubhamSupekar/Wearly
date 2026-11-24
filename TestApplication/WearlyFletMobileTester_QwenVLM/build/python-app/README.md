# Wearly Mobile Model Tester — Qwen VLM + Flet

This revision removes the Gemma entry and the Hugging Face token field. It uses one public Qwen vision-language model so the app can accept both text prompts and clothing photos.

## Model

- Model: `litert-community/Qwen2-VL-2B`
- File: `Qwen2-VL-2B.litertlm`
- Approximate bundle size: 1.78 GB
- License: Apache-2.0
- Public download: no Hugging Face token is requested by this app.
- Model card: https://huggingface.co/litert-community/Qwen2-VL-2B

Important: the previous Qwen3 0.6B entry was a text-only model and could not inspect photos. This project switches to Qwen2-VL 2B because it is a Qwen vision-language model with an actual image encoder. It is much larger than Qwen3 0.6B; allow additional storage and RAM.

## Features

- Flet 1.1.3+ interface.
- Download one public Qwen2-VL LiteRT-LM model without a Hugging Face token.
- Resume partial downloads when HTTP range requests are supported.
- Text-only prompt testing.
- Pick a JPG, PNG, WebP or BMP clothing photo.
- Analyze garment type, visible colours, pattern, texture, fit, construction details, style and outfit pairing suggestions.
- Image inference uses LiteRT-LM locally; no image is sent to a cloud model API.
- Displays elapsed time and approximate output tokens/second.

## Install and run on desktop

Python 3.10–3.12 is recommended for the native inference package. Your Flet app may run on Python 3.14, but native LiteRT-LM wheels must exist for that Python/platform combination.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flet run main.py
```

## Build Android APK

Install Flutter and Android SDK/Android Studio, then:

```bash
pip install "flet[all]"
flet build apk --verbose
```

The LiteRT-LM Python runtime has documented Android support, but Flet's APK build must actually package the matching Android native extension and dependencies. Verify this on a physical ARM64 Android phone. Installing the package on macOS alone does not install it into the APK.

Official LiteRT-LM Python docs: https://developers.google.com/edge/litert-lm/python

## How to use

1. Launch the app.
2. Tap **Download Qwen2-VL model**. The file is around 1.78 GB.
3. Wait for the download to finish.
4. Use **Text inference** for ordinary prompts.
5. Under **Clothing photo analysis**, choose a garment photo.
6. Tap **Analyze clothing photo**.
7. The model describes visible garment attributes locally.

## Device requirements and caveats

- The model file is approximately 1.78 GB; additional temporary storage is required during download.
- Runtime memory use is larger than the file size. A 4 GB phone may not have enough free RAM. An 8 GB+ Android device is a more realistic starting point, but performance varies by chipset and Android version.
- The app configures the vision backend to GPU. GPU delegate support varies by phone. If initialization fails, change `vision_backend=litert_lm.Backend.GPU()` in `wearly_tester/engine.py` to `litert_lm.Backend.CPU()` and rebuild.
- Tokens/second is approximate because this prototype estimates output tokens using whitespace-separated words.
- The app does not guarantee colour accuracy: lighting, shadows, camera white balance and image processing affect perceived colour. Use well-lit photos with the garment filling most of the frame.
- It cannot reliably identify exact fibre composition, hidden garment details or brand names unless visible in the photo.

## Model redistribution

This app downloads the public model from its Hugging Face repository without an access token. If you later mirror the model on Wearly infrastructure, review and follow the model's Apache-2.0 license and include required notices.
