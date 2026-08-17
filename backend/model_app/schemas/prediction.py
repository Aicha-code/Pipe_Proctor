from pydantic import BaseModel, Field


class ChangeDetectionResponse(BaseModel):
    """
    Response model for change detection API.
    
    Contains the anomaly detection result with geolocation coordinates
    and patch-level information for visualization on the frontend.
    """

    segment_id: str = Field(
        ...,
        description="Unique segment identifier from the input (e.g., P1328_SEG_0020)",
        example="P1328_SEG_0020",
    )
    anomaly_score: float = Field(
        ...,
        description="Model anomaly score (0.0+). Higher values indicate stronger anomalies. Typical range 0.0-2.0",
        ge=0,
        example=1.1555836200714111,
    )
    longitude: float = Field(
        ...,
        description="Longitude coordinate of the segment (WGS84)",
        example=2.6275,
    )
    latitude: float = Field(
        ...,
        description="Latitude coordinate of the segment (WGS84)",
        example=6.540285,
    )
    patch_index: int = Field(
        ...,
        ge=0,
        le=255,
        description="Flattened patch index (0-255) in the 16x16 patch grid. Calculated as: patch_row * 16 + patch_col",
        example=29,
    )
    patch_row: int = Field(
        ...,
        ge=0,
        le=15,
        description="Row index (0-15) of the most anomalous patch in the 16x16 grid",
        example=1,
    )
    patch_col: int = Field(
        ...,
        ge=0,
        le=15,
        description="Column index (0-15) of the most anomalous patch in the 16x16 grid",
        example=13,
    )

    class Config:
        json_schema_extra = {
            "example": {
                "segment_id": "P1328_SEG_0020",
                "anomaly_score": 1.1555836200714111,
                "longitude": 2.6275,
                "latitude": 6.540285,
                "patch_index": 29,
                "patch_row": 1,
                "patch_col": 13,
            }
        }
