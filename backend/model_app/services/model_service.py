from __future__ import annotations

import os

try:
    import pandas as pd
except ImportError:  # pragma: no cover
    pd = None

try:
    import rasterio
except ImportError:  # pragma: no cover
    rasterio = None

try:
    import torch
    import torch.nn.functional as F
except ImportError:  # pragma: no cover
    torch = None
    F = None

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.getenv("CROMA_MODEL_PATH", os.path.join(BASE_DIR, "models", "CROMA_base.pt"))
METADATA_PATH = os.getenv("PIPEPROCTOR_METADATA_PATH", os.path.join(BASE_DIR, "data", "chips_metadata_v2.csv"))

model = None


class InvalidImageError(ValueError):
    """A supplied chip is not something the encoder can read.

    Separate from the plain ValueError raised for an unknown segment so the API
    can tell a bad upload (client error) from a missing record (404).
    """

def _load_metadata():
    if pd is None:
        raise ImportError("pandas is required for model metadata loading.")
    return pd.read_csv(METADATA_PATH)


def _get_model():
    global model

    if model is not None:
        return model

    if torch is None:
        raise ImportError("torch is required to run the change detection model.")

    try:
        from use_croma import PretrainedCROMA
    except ImportError as exc:
        raise ImportError(
            "The CROMA model dependency is missing. Install the model package or provide the required encoder implementation."
        ) from exc

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"CROMA model file not found at: {MODEL_PATH}")

    model = PretrainedCROMA(
        pretrained_path=MODEL_PATH,
        size="base",
        modality="SAR",
        image_resolution=128,
    )
    model.eval()
    return model


def normalize_croma(x: torch.Tensor) -> torch.Tensor:
    """Normalize a SAR chip using the same logic as the research pipeline."""
    if torch is None:
        raise ImportError("torch is required to run the change detection model.")

    x = x.float()
    normalized_channels = []

    for channel in range(x.shape[0]):
        channel_data = x[channel]
        min_value = channel_data.mean() - 2 * channel_data.std()
        max_value = channel_data.mean() + 2 * channel_data.std()
        normalized = (channel_data - min_value) / (max_value - min_value)
        normalized = torch.clamp(normalized, 0, 1)
        normalized_channels.append(normalized.unsqueeze(0))

    return torch.cat(normalized_channels, dim=0)


def load_image(image_path: str) -> torch.Tensor:
    """Load a GeoTIFF SAR chip and convert it into CROMA-ready input."""
    if rasterio is None:
        raise ImportError("rasterio is required to read the SAR TIFF files.")

    with rasterio.open(image_path) as src:
        image = src.read()

    if image.shape[0] != 2:
        raise InvalidImageError(
            f"Image must contain exactly 2 SAR bands (VV and VH), not {image.shape[0]}."
        )

    if image.shape[1:] != (128, 128):
        height, width = image.shape[1], image.shape[2]
        raise InvalidImageError(
            f"Image must be 128 x 128 px to match the encoder, not {width} x {height}."
        )

    image_tensor = torch.from_numpy(image)
    image_normalized = normalize_croma(image_tensor)
    return image_normalized.unsqueeze(0).float()


def get_embedding(image_tensor: torch.Tensor):
    """Run an image through the CROMA SAR encoder."""
    model_instance = _get_model()
    with torch.no_grad():
        output = model_instance(image_tensor)
    return output["SAR_encodings"]


def calculate_change(embedding_t1, embedding_t2):
    """Compute patch-level change by cosine similarity."""
    similarity = F.cosine_similarity(embedding_t1, embedding_t2, dim=-1)
    return 1 - similarity


def calculate_anomaly_score(change):
    """Compute an experimental anomaly score from the change tensor."""
    max_change = change.max().item()
    std_change = change[0].std().item()
    return max_change + 2 * std_change


def get_metadata(segment_id: str):
    """Look up geographic coordinates from metadata."""
    df = _load_metadata()
    row = df[df["segment_id"] == segment_id]

    if row.empty:
        raise ValueError(f"Segment '{segment_id}' not found in metadata.")

    row = row.iloc[0]
    return {
        "segment_id": str(row["segment_id"]),
        "longitude": float(row["longitude"]),
        "latitude": float(row["latitude"]),
    }


def detect_change(image_t1_path: str, image_t2_path: str, segment_id: str):
    """Run the full inference pipeline for a reference/current SAR pair."""
    t1 = load_image(image_t1_path)
    t2 = load_image(image_t2_path)

    embedding_t1 = get_embedding(t1)
    embedding_t2 = get_embedding(t2)

    change = calculate_change(embedding_t1, embedding_t2)
    anomaly_score = calculate_anomaly_score(change)

    max_patch = torch.argmax(change[0]).item()
    patch_row = max_patch // 16
    patch_col = max_patch % 16

    metadata = get_metadata(segment_id)

    return {
        "segment_id": metadata["segment_id"],
        "anomaly_score": float(anomaly_score),
        "longitude": metadata["longitude"],
        "latitude": metadata["latitude"],
        "patch_index": int(max_patch),
        "patch_row": int(patch_row),
        "patch_col": int(patch_col),
    }