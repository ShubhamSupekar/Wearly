import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import drawing_utils, drawing_styles


# --------------------------------------------------
# Configuration
# --------------------------------------------------

IMAGE_PATH = "/Users/shubham/Projects/20241125_152515.jpg"
MODEL_PATH = "Wearly/ML/Face_Landmark_Weights/face_landmarker.task"
OUTPUT_PATH = "Wearly/ML/Model_Runner/annotated_face.png"


FOREHEAD_OUTPUT_PATH = "Wearly/ML/Model_Runner/forehead_selection.png"
FOREHEAD_MASK_OUTPUT_PATH = "Wearly/ML/Model_Runner/forehead_mask.png"
# Vertical clearance above the eyebrows, in pixels.
EYEBROW_MARGIN = 8
# Extra distance above the eyebrows to include more forehead.
FOREHEAD_HEIGHT_SCALE = 0.45


# Set to None to keep the original resolution.
# Otherwise, resize images so their longest side is at most this size.
MAX_IMAGE_DIMENSION = 1600


# --------------------------------------------------
# Image loading and validation
# --------------------------------------------------

def load_image(image_path):
    # OpenCV loads images in BGR format.
    bgr_image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    if bgr_image is None:
        raise FileNotFoundError(
            f"Could not load image: {image_path}"
        )

    if bgr_image.ndim != 3 or bgr_image.shape[2] != 3:
        raise ValueError("Expected a three-channel color image.")

    height, width = bgr_image.shape[:2]

    # Optional resize for large images.
    if MAX_IMAGE_DIMENSION is not None:
        longest_side = max(height, width)

        if longest_side > MAX_IMAGE_DIMENSION:
            scale = MAX_IMAGE_DIMENSION / longest_side

            new_width = max(1, int(width * scale))
            new_height = max(1, int(height * scale))

            bgr_image = cv2.resize(
                bgr_image,
                (new_width, new_height),
                interpolation=cv2.INTER_AREA
            )

    return bgr_image


# --------------------------------------------------
# Draw landmarks
# drawing_utils requires a BGR image.
# --------------------------------------------------

def draw_landmarks_on_image(bgr_image, detection_result):
    annotated_image = np.copy(bgr_image)

    face_landmarks_list = detection_result.face_landmarks

    for face_landmarks in face_landmarks_list:

        drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks,
            connections=(
                vision.FaceLandmarksConnections
                .FACE_LANDMARKS_TESSELATION
            ),
            landmark_drawing_spec=None,
            connection_drawing_spec=(
                drawing_styles
                .get_default_face_mesh_tesselation_style()
            )
        )

        drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks,
            connections=(
                vision.FaceLandmarksConnections
                .FACE_LANDMARKS_CONTOURS
            ),
            landmark_drawing_spec=None,
            connection_drawing_spec=(
                drawing_styles
                .get_default_face_mesh_contours_style()
            )
        )

        drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks,
            connections=(
                vision.FaceLandmarksConnections
                .FACE_LANDMARKS_LEFT_IRIS
            ),
            landmark_drawing_spec=None,
            connection_drawing_spec=(
                drawing_styles
                .get_default_face_mesh_iris_connections_style()
            )
        )

        drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks,
            connections=(
                vision.FaceLandmarksConnections
                .FACE_LANDMARKS_RIGHT_IRIS
            ),
            landmark_drawing_spec=None,
            connection_drawing_spec=(
                drawing_styles
                .get_default_face_mesh_iris_connections_style()
            )
        )

    return annotated_image


def extract_forehead(bgr_image, face_landmarks):
    height, width = bgr_image.shape[:2]

    def point(index):
        landmark = face_landmarks[index]
        return np.array([
            int(landmark.x * width),
            int(landmark.y * height)
        ], dtype=np.int32)

    # Face outline / upper forehead reference points.
    top_center = point(10)
    left_side = point(109)
    right_side = point(338)

    # Collect both eyebrow contours.
    eyebrow_indices = [
        70, 63, 105, 66, 107,
        336, 296, 334, 293, 300
    ]

    eyebrow_points = np.array(
        [point(i) for i in eyebrow_indices],
        dtype=np.int32
    )

    # Sort eyebrow points from left to right across the image.
    eyebrow_points = eyebrow_points[
        np.argsort(eyebrow_points[:, 0])
    ]

    # Create a continuous lower boundary using interpolation.
    # Shift upward so eyebrow hairs are excluded.
    eyebrow_x = eyebrow_points[:, 0].astype(float)
    eyebrow_y = eyebrow_points[:, 1].astype(float)

    # Remove duplicate x-coordinates before interpolation.
    unique_x, unique_indices = np.unique(
        eyebrow_x,
        return_index=True
    )
    unique_y = eyebrow_y[unique_indices]

    x_min = max(0, int(min(left_side[0], unique_x[0])))
    x_max = min(width - 1, int(max(right_side[0], unique_x[-1])))

    x_values = np.arange(x_min, x_max + 1)

    # Interpolate between eyebrow landmarks.
    y_values = np.interp(
        x_values,
        unique_x,
        unique_y
    )

    # Move the boundary upward to avoid eyebrows.
    y_values = y_values - EYEBROW_MARGIN

    lower_boundary = np.column_stack((
        x_values,
        np.clip(y_values, 0, height - 1).astype(np.int32)
    )).astype(np.int32)

    # Build a broad upper boundary from the left temple,
    # over the top of the face, to the right temple.
    upper_boundary = np.array([
        left_side,
        top_center,
        right_side
    ], dtype=np.int32)

    # Connect the upper and lower boundaries.
    forehead_polygon = np.vstack((
        upper_boundary,
        lower_boundary[::-1]
    )).astype(np.int32)

    # Create a mask.
    mask = np.zeros((height, width), dtype=np.uint8)
    cv2.fillPoly(mask, [forehead_polygon], 255)

    # Extract original RGB pixel values.
    rgb_image = cv2.cvtColor(
        bgr_image,
        cv2.COLOR_BGR2RGB
    )

    forehead_pixels_rgb = rgb_image[mask == 255]

    # Build a clear visual verification image.
    preview = bgr_image.copy()
    overlay = bgr_image.copy()

    overlay[mask == 255] = (0, 255, 0)

    preview = cv2.addWeighted(
        bgr_image, 0.45,
        overlay, 0.55,
        0
    )

    # Draw the polygon boundary in red.
    cv2.polylines(
        preview,
        [forehead_polygon],
        True,
        (0, 0, 255),
        2
    )

    # Draw the original eyebrow landmarks in blue.
    for x, y in eyebrow_points:
        cv2.circle(
            preview,
            (int(x), int(y)),
            3,
            (255, 0, 0),
            -1
        )

    cv2.imwrite(FOREHEAD_OUTPUT_PATH, preview)
    cv2.imwrite(FOREHEAD_MASK_OUTPUT_PATH, mask)

    print("Forehead pixel matrix shape:",
          forehead_pixels_rgb.shape)
    print("Preview saved:", FOREHEAD_OUTPUT_PATH)
    print("Mask saved:", FOREHEAD_MASK_OUTPUT_PATH)

    return forehead_pixels_rgb, mask, preview


def calculate_forehead_colour(forehead_pixels_rgb):
    if forehead_pixels_rgb.size == 0:
        raise ValueError("No forehead pixels selected.")

    # Method 1: Average RGB colour
    mean_rgb = np.mean(
        forehead_pixels_rgb,
        axis=0
    )

    mean_rgb = np.round(mean_rgb).astype(np.uint8)

    # Method 2: Median RGB colour (recommended)
    median_rgb = np.median(
        forehead_pixels_rgb,
        axis=0
    )

    median_rgb = np.round(median_rgb).astype(np.uint8)

    # Convert RGB values into hexadecimal colour codes.
    mean_hex = "#{:02X}{:02X}{:02X}".format(*mean_rgb)
    median_hex = "#{:02X}{:02X}{:02X}".format(*median_rgb)

    print("\n--- Forehead Colour Analysis ---")
    print("Total selected pixels:", len(forehead_pixels_rgb))

    print("\nAverage RGB:", mean_rgb)
    print("Average HEX:", mean_hex)

    print("\nMedian RGB:", median_rgb)
    print("Median HEX:", median_hex)

    # Display both representative colours.
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(8, 3))

    for ax, rgb, hex_code, label in [
        (axes[0], mean_rgb, mean_hex, "Average"),
        (axes[1], median_rgb, median_hex, "Median")
    ]:
        ax.imshow(np.array([[rgb]], dtype=np.uint8))
        ax.set_title(f"{label}\n{hex_code}")
        ax.axis("off")

    plt.tight_layout()
    plt.show()

    return {
        "mean_rgb": mean_rgb,
        "mean_hex": mean_hex,
        "median_rgb": median_rgb,
        "median_hex": median_hex,
        "pixel_count": len(forehead_pixels_rgb)
    }


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():
    bgr_image = load_image(IMAGE_PATH)

    height, width = bgr_image.shape[:2]
    print(f"Image dimensions: {width} x {height}")

    # MediaPipe FaceLandmarker expects SRGB/RGB input.
    rgb_image = cv2.cvtColor(
        bgr_image,
        cv2.COLOR_BGR2RGB
    )

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=np.ascontiguousarray(rgb_image)
    )

    base_options = python.BaseOptions(
        model_asset_path=MODEL_PATH
    )

    options = vision.FaceLandmarkerOptions(
        base_options=base_options,
        output_face_blendshapes=True,
        output_facial_transformation_matrixes=True,
        num_faces=1
    )

    # Close the detector automatically after processing.
    with vision.FaceLandmarker.create_from_options(options) as detector:
        detection_result = detector.detect(mp_image)

    if not detection_result.face_landmarks:
        print(
            "No face detected. Try a clearer, front-facing image "
            "with sufficient lighting."
        )
        return

    print(
        f"Detected {len(detection_result.face_landmarks)} face(s)."
    )

    # Drawing uses BGR, not the RGB array used for detection.
    annotated_bgr = draw_landmarks_on_image(
        bgr_image,
        detection_result
    )

    face_landmarks = detection_result.face_landmarks[0]

    forehead_pixels_rgb, forehead_mask, forehead_preview = (
        extract_forehead(
            bgr_image,
            face_landmarks
        )
    )
    forehead_colour = calculate_forehead_colour(forehead_pixels_rgb)
    print("\nForehead Colour Summary:", forehead_colour)
    
    # Show the selected forehead region.
    plt.figure(figsize=(8, 8))
    plt.imshow(cv2.cvtColor(forehead_preview, cv2.COLOR_BGR2RGB))
    plt.title("Selected Forehead Region")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


    if not cv2.imwrite(OUTPUT_PATH, annotated_bgr):
        raise OSError(f"Could not save image: {OUTPUT_PATH}")

    print(f"Annotated image saved as {OUTPUT_PATH}")

    # Matplotlib expects RGB.
    annotated_rgb = cv2.cvtColor(
        annotated_bgr,
        cv2.COLOR_BGR2RGB
    )

    plt.figure(figsize=(10, 10))
    plt.imshow(annotated_rgb)
    plt.axis("off")
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    main()
