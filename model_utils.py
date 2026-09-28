import json
import numpy as np
import tensorflow as tf
from PIL import Image


MODEL_PATH = "model/fungiscan_finetuned.keras"
CLASS_NAMES_PATH = "model/class_names.json"

IMAGE_SIZE = (224, 224)


# ============================================================
# LOAD MODEL
# ============================================================

_model = None
_class_names = None


def load_fungiscan_model():

    global _model
    global _class_names

    if _model is None:
        _model = tf.keras.models.load_model(
            MODEL_PATH
        )

    if _class_names is None:
        with open(
            CLASS_NAMES_PATH,
            "r"
        ) as file:
            _class_names = json.load(file)

    return _model, _class_names


# ============================================================
# FORMAT LABELS
# ============================================================

def format_name(name):

    return (
        name
        .replace("_", " ")
        .strip()
        .title()
    )


# ============================================================
# PREDICT LEAF
# ============================================================

def predict_leaf(image, forced_crop=None):

    model, class_names = load_fungiscan_model()

    # --------------------------------------------------------
    # PREPARE IMAGE
    # --------------------------------------------------------

    if not isinstance(image, Image.Image):
        image = Image.open(image)

    image = image.convert("RGB")
    image = image.resize(IMAGE_SIZE)

    image_array = np.array(
        image,
        dtype=np.float32
    )

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    # --------------------------------------------------------
    # RUN MODEL
    # --------------------------------------------------------

    predictions = model.predict(
        image_array,
        verbose=0
    )[0]

    # ========================================================
    # GROUP PROBABILITIES BY CROP
    # ========================================================

    crop_probabilities = {}

    for index, class_name in enumerate(class_names):

        if "___" not in class_name:
            continue

        crop_raw, condition_raw = class_name.split(
            "___",
            1
        )

        probability = float(
            predictions[index]
        )

        crop_probabilities[crop_raw] = (
            crop_probabilities.get(
                crop_raw,
                0.0
            )
            + probability
        )

    # ========================================================
    # SELECT CROP
    # ========================================================

    crop_source = "AI detected"

    if forced_crop:

        matching_crop = None

        for available_crop in crop_probabilities:

            if (
                format_name(available_crop).lower()
                ==
                forced_crop.strip().lower()
            ):
                matching_crop = available_crop
                break

        if matching_crop is not None:

            predicted_crop_raw = matching_crop
            crop_source = "User confirmed"

        else:

            predicted_crop_raw = max(
                crop_probabilities,
                key=crop_probabilities.get
            )

    else:

        predicted_crop_raw = max(
            crop_probabilities,
            key=crop_probabilities.get
        )

    crop_confidence = (
        crop_probabilities[
            predicted_crop_raw
        ]
        * 100
    )

    # ========================================================
    # FIND CLASSES BELONGING TO SELECTED CROP
    # ========================================================

    crop_class_indices = []

    for index, class_name in enumerate(class_names):

        if class_name.startswith(
            predicted_crop_raw + "___"
        ):
            crop_class_indices.append(index)

    if not crop_class_indices:

        raise ValueError(
            f"No classes found for crop: "
            f"{predicted_crop_raw}"
        )

    # ========================================================
    # SELECT CONDITION WITHIN CROP
    # ========================================================

    best_index = max(
        crop_class_indices,
        key=lambda i: predictions[i]
    )

    predicted_class = class_names[
        best_index
    ]

    crop_raw, condition_raw = predicted_class.split(
        "___",
        1
    )

    # Total probability assigned to this crop
    crop_total = sum(
        float(predictions[i])
        for i in crop_class_indices
    )

    # Normalize disease probabilities within crop
    if crop_total > 0:

        condition_confidence = (
            float(predictions[best_index])
            /
            crop_total
            *
            100
        )

    else:

        condition_confidence = 0.0

    crop = format_name(crop_raw)
    condition = format_name(condition_raw)

    # ========================================================
    # TOP CONDITIONS WITHIN SELECTED CROP
    # ========================================================

    sorted_indices = sorted(
        crop_class_indices,
        key=lambda i: predictions[i],
        reverse=True
    )

    top_predictions = []

    for index in sorted_indices[:3]:

        label = class_names[index]

        top_crop_raw, top_condition_raw = (
            label.split(
                "___",
                1
            )
        )

        if crop_total > 0:

            relative_confidence = (
                float(predictions[index])
                /
                crop_total
                *
                100
            )

        else:

            relative_confidence = 0.0

        top_predictions.append(
            {
                "crop": format_name(
                    top_crop_raw
                ),

                "condition": format_name(
                    top_condition_raw
                ),

                "confidence":
                    relative_confidence
            }
        )

    # ========================================================
    # FINAL CONFIDENCE
    # ========================================================

    # If the user manually confirms the crop,
    # don't penalize the result for AI crop uncertainty.

    if forced_crop and crop_source == "User confirmed":

        overall_confidence = (
            condition_confidence
        )

    else:

        overall_confidence = min(
            crop_confidence,
            condition_confidence
        )

    if overall_confidence >= 80:

        confidence_level = "High"

    elif overall_confidence >= 60:

        confidence_level = "Moderate"

    else:

        confidence_level = "Low"

    # ========================================================
    # RETURN RESULT
    # ========================================================

    return {

        "crop": crop,

        "condition": condition,

        "confidence":
            overall_confidence,

        "crop_confidence":
            crop_confidence,

        "condition_confidence":
            condition_confidence,

        "confidence_level":
            confidence_level,

        "crop_source":
            crop_source,

        "raw_class":
            predicted_class,

        "top_predictions":
            top_predictions
    }