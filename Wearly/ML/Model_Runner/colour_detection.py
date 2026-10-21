import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


MODEL_PATH = "Wearly/ML/Face_Landmark_Weights/face_landmarker.task"


def get_forehead_colour(image_path):
    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"Could not load image: {image_path}")

    height, width = image.shape[:2]

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=np.ascontiguousarray(rgb_image)
    )

    options = vision.FaceLandmarkerOptions(
        base_options=python.BaseOptions(
            model_asset_path=MODEL_PATH
        ),
        num_faces=1
    )

    with vision.FaceLandmarker.create_from_options(options) as detector:
        result = detector.detect(mp_image)

    if not result.face_landmarks:
        raise ValueError("No face detected.")

    landmarks = result.face_landmarks[0]

    def point(index):
        landmark = landmarks[index]
        return np.array([
            int(landmark.x * width),
            int(landmark.y * height)
        ])

    # Forehead reference points
    top_center = point(10)
    left_side = point(109)
    right_side = point(338)

    eyebrow_indices = [70, 63, 105, 66, 107,
                       336, 296, 334, 293, 300]

    eyebrows = np.array([point(i) for i in eyebrow_indices])
    eyebrows = eyebrows[np.argsort(eyebrows[:, 0])]

    unique_x, indices = np.unique(
        eyebrows[:, 0], return_index=True
    )
    unique_y = eyebrows[indices, 1]

    x_min = max(0, int(min(left_side[0], unique_x[0])))
    x_max = min(width - 1, int(max(right_side[0], unique_x[-1])))

    x_values = np.arange(x_min, x_max + 1)
    y_values = np.interp(x_values, unique_x, unique_y) - 8

    lower_boundary = np.column_stack((
        x_values,
        np.clip(y_values, 0, height - 1).astype(int)
    ))

    polygon = np.vstack((
        [left_side, top_center, right_side],
        lower_boundary[::-1]
    )).astype(np.int32)

    mask = np.zeros((height, width), dtype=np.uint8)
    cv2.fillPoly(mask, [polygon], 255)

    forehead_pixels = rgb_image[mask == 255]

    if len(forehead_pixels) == 0:
        raise ValueError("No forehead pixels detected.")

    median_rgb = np.median(forehead_pixels, axis=0).round().astype(int)

    return "#{:02X}{:02X}{:02X}".format(*median_rgb)


colour = get_forehead_colour(
    "/Users/shubham/Projects/20241125_152515.jpg"
)

print(colour)