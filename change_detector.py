import os
import pandas as pd
import rasterio
import torch
import torch.nn.functional as F
from use_croma import PretrainedCROMA


# Configuration

BASE_DIR = os.path.dirname(__file__)

DATASET_DIR = os.path.join(
    BASE_DIR,
    "data_pipeproctor"
)

METADATA_PATH = os.path.join(
    DATASET_DIR,
    "chips_metadata_v2.csv"
)

CROMA_PATH = os.path.join(
    BASE_DIR,
    "CROMA_base.pt"
)


# Load metadata

df = pd.read_csv(METADATA_PATH)


# Load CROMA 

model = PretrainedCROMA(
    pretrained_path=CROMA_PATH,
    size="base",
    modality="SAR",
    image_resolution=128
)

model.eval()


# Data Preprocessing

def normalize_croma(x):
    """
    Normalize data using the preprocessing code from the original CROMA repository (https://github.com/antofuller/croma).
    """

    x = x.float()

    normalized_channels = []

    for channel in range(x.shape[0]):

        channel_data = x[channel]

        min_value = (
            channel_data.mean()
            - 2 * channel_data.std()
        )

        max_value = (
            channel_data.mean()
            + 2 * channel_data.std()
        )

        normalized = (
            (channel_data - min_value)
            / (max_value - min_value)
        )

        normalized = torch.clamp(
            normalized,
            0,
            1
        )

        normalized_channels.append(
            normalized.unsqueeze(0)
        )

    return torch.cat(
        normalized_channels,
        dim=0
    )


# Load image

def load_image(image_path):
    """
    Load a Sentinel-1 GeoTIFF and prepare it for CROMA.

    Returns:
        Tensor of shape (1, 2, 128, 128)
    """

    with rasterio.open(image_path) as src:
        image = src.read()

    image_tensor = torch.from_numpy(image)

    image_normalized = normalize_croma(
        image_tensor
    )

    # Add batch dimension
    image_tensor = image_normalized.unsqueeze(0)

    return image_tensor.float()


# Generate embeddings

def get_embedding(image):

    with torch.no_grad():
        output = model(image)

    return output["SAR_encodings"]



def calculate_change(embedding_t1, embedding_t2):
    """
    Compute patch-level change using cosine distance.
    """

    similarity = F.cosine_similarity(
        embedding_t1,
        embedding_t2,
        dim=-1
    )

    change = 1 - similarity

    return change


# Find anomaly score

def calculate_anomaly_score(change):
    """
        Compute anomaly score (the formula was derrived from previous experiments on sample data) 
    """

    max_change = change.max().item()
    std_change = change[0].std().item()

    anomaly_score = (
        max_change
        + 2 * std_change
    )

    return anomaly_score


# Get segment metadata

def get_metadata(segment_id):

    row = df[
        df["segment_id"] == segment_id
    ]

    if row.empty:
        raise ValueError(
            f"Segment '{segment_id}' not found in metadata."
        )

    row = row.iloc[0]

    return {f"segment_id: {row['segment_id']},longitude: {float(row['longitude'])},latitude: {float(row['latitude'])}"}



def detect_change(image_t1_path, image_t2_path, segment_id ):
    """
    Compare two images and return an anomaly result.

    Args:
        image_t1_path: Path to the first image.
        image_t2_path: Path to the second image.
        segment_id: Segment identifier from the metadata CSV.
    Returns:
        Dictionary containing anomaly score and coordinates.
    """

    t1 = load_image(image_t1_path)
    t2 = load_image(image_t2_path)

    embedding_t1 = get_embedding(t1)
    embedding_t2 = get_embedding(t2)

    change = calculate_change(
        embedding_t1,
        embedding_t2
    )

    anomaly_score = calculate_anomaly_score(
        change
    )
    max_patch = torch.argmax(change[0]).item()

    # CROMA produces 256 patches = 16 x 16
    patch_row = max_patch // 16
    patch_col = max_patch % 16

    # Get geographic metadata
    metadata = get_metadata(segment_id)

    result = {
        "segment_id": metadata["segment_id"],
        "anomaly_score": float(anomaly_score),
        "longitude": metadata["longitude"],
        "latitude": metadata["latitude"],
        "patch_index": int(max_patch),
        "patch_row": int(patch_row),
        "patch_col": int(patch_col)
    }

    return result