import os
import pandas as pd
import rasterio
import torch
import torch.nn.functional as F
# import matplotlib.pyplot as plt
from use_croma import PretrainedCROMA


""" DATASET """

DATASET_DIR = os.path.join(
    os.path.dirname(__file__),
    "data_pipeproctor"
)

metadata_path = os.path.join(
    DATASET_DIR,
    "chips_metadata_v2.csv"
)

df = pd.read_csv(metadata_path)

# print("Dataset shape:", df.shape)
# print("Columns:", df.columns.tolist())


""" Load the image """

relative_path = df.loc[0, "chip_file"]
latitude = df.loc[0, "latitude"]
longitude = df.loc[0, "longitude"]
segment_id = df.loc[0, "segment_id"]

full_path = os.path.join(
    DATASET_DIR,
    relative_path
)

print(f"Image exists: {'✅' if os.path.exists(full_path) else '❌'}")


with rasterio.open(full_path) as src:

    print("\nImage information:")
    print(f"Width: {src.width}| Height: {src.height} | Bands: {src.count} | Data type: {src.dtypes} | CRS: {src.crs}")

    image = src.read()


print(f"Image shape: {image.shape}| dtype: {image.dtype}| min: {image.min()} | max: {image.max()}")


""" Preprocessing code from the original CROMA repository"""

def normalize_croma(x):

    x = x.float()

    normalized_channels = []

    for channel in range(x.shape[0]):

        channel_data = x[channel]

        min_value = (
            channel_data.mean()
            - 2 * channel_data.std() # we use 2, because the original CROMA code uses 2 standard deviations to define the range for normalization.
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


image_tensor = torch.from_numpy(image)

image_normalized = normalize_croma(image_tensor)

# Add batch dimension
t1 = image_normalized.float().unsqueeze(0)

print(f"\nInput info:\nshape: {t1.shape}, min: {t1.min().item()}, max: {t1.max().item()}")


""" Simulations """

t2_no_change = t1.clone()
 # Simulate a small change 
t2_small = t1.clone()
t2_small[:, :, 50:60, 50:60] += 0.05

# Simulate a medium change
t2_medium = t1.clone()
t2_medium[:, :, 50:60, 50:60] += 0.15

#simulate a big change
t2_large = t1.clone()
t2_large[:, :, 50:70, 50:80] += 0.50


# Keep the ts within CROMA's expected range
t2_small = torch.clamp(t2_small, 0, 1)
t2_medium = torch.clamp(t2_medium, 0, 1)
t2_large = torch.clamp(t2_large, 0, 1)

""" Load CROMA """

model = PretrainedCROMA(pretrained_path="CROMA_base.pt", size="base", modality="SAR", image_resolution=128)

print(f"\nCROMA loaded!\nCROMA input shape: {t1.shape} | min: { t1.min().item()}| max: {t1.max().item()}")

""" Process the images through CROMA """

with torch.no_grad():

    output_t1 = model(t1)

    output_no_change = model(t2_no_change)
    output_small = model(t2_small)
    output_medium = model(t2_medium)
    output_large = model(t2_large)

""" Calculate change """

def get_change(output_t1, output_t2, experiment_name, metadata):

    encoding_t1 = output_t1["SAR_encodings"]
    encoding_t2 = output_t2["SAR_encodings"]

    # Cosine similarity between corresponding spatial patches
    similarity = F.cosine_similarity(
        encoding_t1,
        encoding_t2,
        dim=-1
    )

    # Convert similarity to a change score
    change = 1 - similarity

    # Find the most changed path and compute the Anomaly score

    max_patch = torch.argmax(change[0])
    max_change = change[0, max_patch].item()
    """
        Compute anomaly score (this formula was derrived from various experiments on sample data)
    """
    anomaly_score = (max_change + 2 * change[0].std().item())
    # get the metadata for the experiment
    latitude = metadata["latitude"]
    longitude = metadata["longitude"]
    segment_id = metadata["segment_id"]

    # print statistics of the results
    print("\n")
    print(f"Results for: {experiment_name}")
    print("=" * 20)

    # print(f"Encoding T1 shape: {encoding_t1.shape}")
    # print(f"Encoding T2 shape: {encoding_t2.shape}")

    print(f"Mean change: {change.mean().item():.4f}")
    print(f"Maximum change: {change.max().item():.4f}")
    print(f"Minimum change: {change.min().item():.4f}")

    print("Most changed patch:", max_patch.item())
    print(f"Patch change: {max_change:.6f}")
    print(f"Anomaly score: {anomaly_score:.6f}")

    # patch specific information
    patch_index = max_patch.item()
    
    row = patch_index // 16
    col = patch_index % 16
    
    print(f"Patch at: (row={row}, col={col})")
    print(f"Segment coordinates: ({longitude}, {latitude})")

    result = {
            "segment_id": segment_id,
            "anomaly_score": anomaly_score,
            "longitude": longitude,
            "latitude": latitude,
            "patch_index": patch_index,
            "patch_row": row,
            "patch_col": col
        }
    
    return change, result
    # map the 10 most changed patches to their positions in the 15x15 grid
    # top_k = 10

    # values, indices = torch.topk(change[0], top_k)

    # print("\nTop 10 most changed patches:")

    # for rank, (patch, score) in enumerate(zip(indices, values), start=1):
    #     row = patch.item() // 15
    #     col = patch.item() % 15

    #     print(
    #         f"{rank}. Patch {patch.item():3d} "
    #         f"(row={row}, col={col}) "
    #         f"change={score.item():.6f}"
    #     )
    # return change, result


change_no, result_1 = get_change(
    output_t1,
    output_no_change,
    "No Change",
    {
        "latitude": latitude,
        "longitude": longitude,
        "segment_id": segment_id
    }    
)

change_small, result_2 = get_change(
    output_t1,
    output_small,
    "Small Change",
    {
        "latitude": latitude,
        "longitude": longitude,
        "segment_id": segment_id
    }
)

change_medium, result_3 = get_change(
    output_t1,
    output_medium,
    "Medium Change",
    {
        "latitude": latitude,
        "longitude": longitude,
        "segment_id": segment_id
    }
)

change_large, result_4 = get_change(
    output_t1,
    output_large,
    "Large Change",
    {
        "latitude": latitude,
        "longitude": longitude,
        "segment_id": segment_id
    }
)

results = [
    result_1,
    result_2,
    result_3,
    result_4
]

for result in results:

    print(
        f"Segment: {result['segment_id']} | "
        f"Score: {result['anomaly_score']:.6f} | "
        f"Longitude: {result['longitude']} | "
        f"Latitude: {result['latitude']}"
    )
