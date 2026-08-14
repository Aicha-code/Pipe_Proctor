# CROMA Change Detection

This repository contains the current CROMA-based change detection pipeline and the Sentinel-1 dataset used for SAR anomaly analysis.

## Repository structure

```text
Project/
├── change_detector.py
├── use_croma.py                # temporary CROMA wrapper/model integration
├── CROMA_base.pt               # pretrained CROMA weights
├── data_pipeproctor/
│   ├── chips_metadata_v2.csv
│   └── imagery/
│       └── chips_v2/
├── Model_test01.py
├── experiment.py
├── requirements.txt
├── readme.md
└── Model/
```

> **Branch note:** `use_croma.py` and `CROMA_base.pt` are included in this branch for convenience during backend integration and testing. They are not intended to be merged into `main`. The final project should obtain the CROMA implementation and pretrained weights from the original CROMA repository.

## Files

- `change_detector.py` - main change detection module
- `use_croma.py` - CROMA model integration based on https://github.com/antofuller/croma
- `CROMA_base.pt` - pretrained CROMA weights from the same repository
- `data_pipeproctor/` - Sentinel-1 imagery and metadata
- `Model_test01.py` - evaluation script comparing original and simulated images at different change levels
- `experiment.py` - experiment and model-run utilities

## Dataset

The dataset contains:

- 20 Sentinel-1 SAR image chips
- Image size: 128 × 128
- 2 SAR channels: VV and VH
- Metadata in `chips_metadata_v2.csv`

The metadata contains the geographic coordinates associated
with each segment.

## Change detection model

The detector performs the following steps:

1. Loads two Sentinel-1 images.
2. Applies CROMA preprocessing.
3. Generates SAR embeddings using pretrained CROMA.
4. Computes cosine distance between matching patches.
5. Identifies the most changed patch.
6. Computes an anomaly score.

Current anomaly score formula:

```python
anomaly_score = max_change + 2 * std(change)
```

## Output

The detector returns a JSON-like dictionary structured as:

```python
{
    "segment_id": "...",
    "anomaly_score": ...,
    "longitude": ...,
    "latitude": ...,
    "patch_index": ...,
    "patch_row": ...,
    "patch_col": ...
}
```

## Installation
1. Clone the repository and switch to this branch.

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Ensure that `CROMA_base.pt` is present in the project root.

### Input

`detect_change()` function expects:

- `image_t1_path` - path to the reference/previous Sentinel-1 GeoTIFF
- `image_t2_path` - path to the new/current Sentinel-1 GeoTIFF
- `segment_id` - segment identifier corresponding to the image metadata

Both images should be:

- GeoTIFF (`.tif`)
- 128 × 128 pixels
- 2 SAR channels
- Channel 0: VV
- Channel 1: VH

The images are loaded using `rasterio` and normalized inside `change_detector.py`.

Example:

```python
result = detect_change(
    image_t1_path="path/to/t1.tif",
    image_t2_path="path/to/t2.tif",
    segment_id="P1328_SEG_0001"
)
```
## Metadata

Geographic information is retrieved from `chips_metadata_v2.csv`.

The detector uses the provided `segment_id` to find the corresponding:

- latitude
- longitude

in the metadata file.

The `segment_id` therefore needs to correspond to an entry in the metadata CSV.

### Patch-level change detection

CROMA produces 256 spatial patches for a 128 × 128 image, corresponding to a 16 × 16 patch grid.

The detector identifies the patch with the highest change score.

- `patch_index` - flattened patch index from 0 to 255
- `patch_row` - row of the most changed patch in the 16 × 16 grid
- `patch_col` - column of the most changed patch in the 16 × 16 grid

The patch coordinates describe the location of the most changed region within the image chip. They are separate from the geographic latitude and longitude of the segment.

### Response schema

The API should return the same structure as the model output:

```json
{
  "segment_id": "P1328_SEG_0001",
  "anomaly_score": 0.842,
  "longitude": 2.624158,
  "latitude": 6.369446,
  "patch_index": 102,
  "patch_row": 6,
  "patch_col": 6
}
```

### Integration notes

- Validate input image shape and dtype before calling the model.
- Consider storing metadata such as `segment_id`, longitude, latitude, and patch coordinates alongside the result for downstream workflows.


## Current limitations

1. The current dataset contains images from the same acquisition date that is why The T2 images used during initial experiments were synthetically generated.

2. Because of that, The anomaly score has only been evaluated on simulated changes and has not yet been calibrated on real change/no-change pairs.

3. The current anomaly score formula is experimental and should not yet be inerpreted as a calibrated probability of infrastructure damage or anomaly.

## Summary

This repository provides the CROMA-based change detection logic. To integrate it with the FATS API, expose a small FastAPI service that accepts two SAR images, calls `detect_change()`, and returns the JSON anomaly result for each request.