import numpy as np

def preprocess_patient_data(raw: dict) -> np.ndarray:
    """Convert raw patient dict into feature array for the 6KB model.
    Expected keys: "age", "hearing_loss_duration", "implant_type".
    The model expects three numeric features: age, duration, and a numeric code for implant type.
    """
    # Numeric features
    age = float(raw.get("age", 0))
    hearing_loss_duration = float(raw.get("hearing_loss_duration", 0))

    # Encode implant_type as a single numeric value (type_a=0, type_b=1, type_c=2)
    implant_raw = raw.get("implant_type", "type_a").lower()
    mapping = {"type_a": 0, "type_b": 1, "type_c": 2}
    implant_code = float(mapping.get(implant_raw, 0))

    # Return as (1, 3) array matching model training
    X = np.array([[age, hearing_loss_duration, implant_code]])
    return X
