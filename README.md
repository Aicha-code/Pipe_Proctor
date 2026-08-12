# Satellite-Based Monitoring of the Niger-Benin Oil Pipeline

## Overview

This project develops an intelligent satellite-based monitoring system for the **Niger-Benin Export Pipeline (NBEP)**, Africa's longest crude oil pipeline at approximately **1,950 km** (2,389 km by GIS route measurement). The pipeline connects the Agadem oil field in southeastern Niger to the Port Seme Terminal on the Atlantic coast of Benin, operated by the China National Petroleum Corporation (CNPC) and the West African Pipeline Company (WAPCO). It has been operational since March 2024 with a capacity of 90,000 barrels per day.

The goal is to use **Sentinel-1 SAR imagery** processed into a training dataset for a **computer vision model** capable of detecting pipeline anomalies (leaks, spills, unauthorized construction, vegetation clearing, etc.).

## Pipeline Corridor Segmentation Strategy

The pipeline route (sourced from the [Global Energy Monitor](https://www.gem.wiki/Niger%E2%80%93Benin_Oil_Pipeline), ProjectID: P1328) is divided into:

| Parameter | Value |
|---|---|
| Segment length | **1 km** |
| Buffer (each side) | **500 m** |
| Total corridor width | **1,000 m** |
| Total segments | **2,389** |
| Geohash precision | **8** (~20 m) |

Each segment is a 1 km slice of the pipeline centerline with a 500 m buffer on both sides, creating a 1 km x 1 km AOI (area of interest) that serves as the footprint for satellite image acquisition.

## Segment Attributes

Every segment in the dataset contains the following fields:

| Field | Description | Example |
|---|---|---|
| `segment_id` | Unique identifier | `SEG_0001` |
| `latitude` | Center latitude of the segment | `6.369446` |
| `longitude` | Center longitude of the segment | `2.624158` |
| `geohash` | Spatial index (precision 8, ~20 m) | `s11u5xwb` |
| `start_chainage_km` | Distance from pipeline origin (Agadem) | `0.0` |
| `end_chainage_km` | Distance from pipeline origin (Agadem) | `1.0` |
| `length_km` | Actual segment length | `1.0` |
| `status` | Pipeline operational status | `operational` |

## Project Structure

```
Satellite-Based-Monitoring-of-Niger-Benin-Oil-Pipeline/
├── data/
│   ├── raw/                    # Source pipeline GeoJSON
│   ├── processed/              # Cleaned pipeline & training dataset manifest
│   ├── segments/               # Segments CSV & GeoJSON
│   ├── manifests/              # Sentinel-1 product catalog
│   ├── dataset/                # Train/val/test splits
│   ├── sentinel1_images/        # Downloaded S1 GRD products (gitignored)
│   └── training_chips/          # Preprocessed image chips (gitignored)
├── scripts/
│   ├── 01_pipeline_segmentation.py
│   ├── 02_sentinel1_data_acquisition.py
│   ├── 03_preprocess_sentinel1.py
│   └── 04_prepare_training_dataset.py
├── models/                    # Model code (to be added)
├── notebooks/                 # Jupyter notebooks (to be added)
├── docs/
├── .gitignore
├── requirements.txt
└── README.md
```

## Workflow

### Step 1: Pipeline Segmentation

```bash
python scripts/01_pipeline_segmentation.py
```

- Loads the Niger-Benin pipeline GeoJSON (GEM ProjectID: P1328)
- Densifies the line geometry to ~100 m intervals
- Splits into 1 km segments
- Creates 500 m buffer on each side
- Computes segment attributes (geohash, chainage, center coordinates)
- **Outputs:** `data/segments/segments.csv`, `data/segments/segments.geojson`, `data/segments/segment_buffers.geojson`

### Step 2: Sentinel-1 Data Acquisition

```bash
export COPERNICUS_USERNAME="your_username"
export COPERNICUS_PASSWORD="your_password"
python scripts/02_sentinel1_data_acquisition.py
```

- Queries the Copernicus Data Space Ecosystem (CDSE) for Sentinel-1 GRD products
- Searches for IW mode, VV+VH dual polarisation imagery
- Builds a catalog manifest mapping each segment to available products
- **Outputs:** `data/manifests/sentinel1_catalog.csv`, `data/processed/training_dataset.csv`

### Step 3: Sentinel-1 Preprocessing

```bash
python scripts/03_preprocess_sentinel1.py
```

Preprocessing pipeline (SNAP GPT):
1. Apply Orbit File (Sentinel Precise)
2. Remove GRD Border Noise
3. Radiometric Calibration (Sigma0, VV + VH)
4. Linear to dB
5. Terrain Correction (Range-Doppler, SRTM 3Sec DEM)
6. Reproject to EPSG:4326
7. Clip to segment 500 m buffer AOI
8. Export as GeoTIFF (LZW compressed, 10 m resolution)

**Outputs:** `data/training_chips/SEG_XXXX/SEG_XXXX_YYYYMMDD.tif`

### Step 4: Training Dataset Preparation

```bash
python scripts/04_prepare_training_dataset.py
```

- Splits segments into train (70%) / val (15%) / test (15%)
- Creates YOLO-compatible dataset configuration
- Initializes all segments as unlabeled (annotation required)
- **Outputs:** `data/dataset/` with train/val/test CSVs and `dataset.yaml`

## Data Sources

| Source | Description | Link |
|---|---|---|
| Global Energy Monitor | Pipeline route geometry (ProjectID: P1328) | [GEM Wiki](https://www.gem.wiki/Niger%E2%80%93Benin_Oil_Pipeline) |
| Copernicus Sentinel-1 | SAR satellite imagery (IW GRD, VV+VH) | [CDSE](https://dataspace.copernicus.eu/) |
| SRTM | Digital Elevation Model for terrain correction | [NASA SRTM](https://www.earthdata.nasa.gov/srtm) |

## Sentinel-1 Acquisition Parameters

| Parameter | Value |
|---|---|
| Platform | Sentinel-1A / Sentinel-1B |
| Product type | GRD (Ground Range Detected) |
| Sensor mode | IW (Interferometric Wide Swath) |
| Polarisation | Dual VV + VH |
| Resolution | ~10 m (range x azimuth) |
| Swath width | ~250 km |
| Revisit time | 12 days (single satellite) / 6 days (S1A + S1B) |

## Labels & Anomaly Detection

The model is designed to detect:
- **Oil leaks/spills** (surface changes detectable by SAR)
- **Unauthorized construction** near the pipeline ROW
- **Vegetation clearing** along the corridor
- **Soil disturbance** and excavation activity
- **Standing water** (potential flooding or leak pooling)

Label classes:
| Class ID | Name | Description |
|---|---|---|
| 0 | Normal | No anomaly detected |
| 1 | Anomaly | Leak, spill, or unauthorized activity detected |
| -1 | Unlabeled | Requires manual annotation |

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install SNAP for Sentinel-1 preprocessing (optional, for step 3)
# Download from: https://step.esa.int/main/download/
```

## Requirements

- Python 3.9+
- geopandas, shapely, pygeohash, geopy
- sentinelsat (for Copernicus API access)
- rasterio (for image processing)
- SNAP (ESA Sentinel Application Platform, for SAR preprocessing)
- PyTorch or TensorFlow (for model training)

## License

This project is for academic and research purposes.

## References

- [Global Energy Monitor - Niger-Benin Oil Pipeline](https://www.gem.wiki/Niger%E2%80%93Benin_Oil_Pipeline)
- [Global Oil Infrastructure Tracker](https://globalenergymonitor.org/projects/global-oil-infrastructure-tracker/)
- [Copernicus Sentinel-1 Mission](https://sentinel.esa.int/web/sentinel/missions/sentinel-1)
- [Wikipedia - Niger-Benin Oil Pipeline](https://en.wikipedia.org/wiki/Niger%E2%80%93Benin_Oil_Pipeline)
