
from ollama import chat

response = chat(
    model="qwen3-vl:8b",
    messages=[
        {
            "role": "user",
            "content": """
You are a visual facial feature analysis assistant for
a fashion and grooming application called Wearly.

Analyze the supplied face image and return ONLY valid JSON.

Analyze these characteristics:

1. Skin color:
   - Approximate visible skin color in plain language.
   - Approximate HEX color of representative visible facial skin,
     if it can be estimated reliably.
   - Skin depth: very_fair, fair, light_medium, medium,
     tan, deep, very_deep, or uncertain.
   - Undertone: warm, cool, neutral, or uncertain.
   - Mention lighting or image quality limitations.

2. Beard:
   - beard_present: true, false, or null if uncertain.
   - beard_style: clean_shaven, stubble, short_beard,
     full_beard, long_beard, mustache_only, or uncertain.
   - beard_density: sparse, medium, dense, or uncertain.
   - beard_length: clean_shaven, short, medium, long,
     or uncertain.
   - mustache_present: true, false, or null.
   - Mention whether facial hair obscures the jawline.

3. Jawline:
   - jawline_shape: square, oval, round, angular, tapered,
     or uncertain.
   - jawline_definition: soft, moderate, well_defined,
     or uncertain.
   - chin_shape: round, square, pointed, or uncertain.
   - left_right_symmetry: appears_symmetric, appears_asymmetric,
     or uncertain.
   - Do not infer hidden anatomy from the image.

4. Additional visible facial characteristics:
   - face_shape: oval, round, square, oblong, heart,
     diamond, or uncertain.
   - forehead_width: narrow, medium, wide, or uncertain.
   - cheekbone_definition: soft, moderate, prominent,
     or uncertain.
   - hair_visibility: visible, partially_visible, or not_visible.
   - glasses_present: true, false, or null.
   - image_quality: good, acceptable, or poor.
   - face_visibility: full, partial, or insufficient.

5. Confidence:
   - Provide a confidence value from 0.0 to 1.0 for each
     major analysis category.
   - Do not claim certainty when the image is unclear.

Rules:
- Analyze only visible characteristics.
- Do not infer ethnicity, race, identity, or medical conditions.
- Do not judge attractiveness or personality.
- Do not assume the image's lighting represents natural skin color.
- If a feature cannot be assessed, return "uncertain".
- Return valid JSON only, without Markdown fences.

Use this JSON structure:

{
  "skin_analysis": {
    "observed_color": "",
    "estimated_hex": null,
    "skin_depth": "",
    "undertone": "",
    "confidence": 0.0,
    "limitations": []
  },
  "beard_analysis": {
    "beard_present": null,
    "beard_style": "",
    "beard_density": "",
    "beard_length": "",
    "mustache_present": null,
    "jawline_obscured_by_facial_hair": null,
    "confidence": 0.0
  },
  "jawline_analysis": {
    "jawline_shape": "",
    "jawline_definition": "",
    "chin_shape": "",
    "left_right_symmetry": "",
    "confidence": 0.0
  },
  "other_features": {
    "face_shape": "",
    "forehead_width": "",
    "cheekbone_definition": "",
    "hair_visibility": "",
    "glasses_present": null,
    "image_quality": "",
    "face_visibility": ""
  }
}
""",
            "images": [
                "/Users/shubham/Projects/20241125_152515.jpg"
            ],
        }
    ],
    options={
        "num_ctx": 8192,
        "temperature": 0
    }
)

print(response.message.content)
