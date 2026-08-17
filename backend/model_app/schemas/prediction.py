from pydantic import BaseModel, Field


class ChangeDetectionResponse(BaseModel):
    segment_id: str = Field(..., description="Unique segment identifier")
    anomaly_score: float = Field(
        ...,
        description="Model anomaly score for the detected change",
        ge=0,
    )
    longitude: float = Field(..., description="Longitude for the segment")
    latitude: float = Field(..., description="Latitude for the segment")
    patch_index: int = Field(
        ...,
        ge=0,
        le=255,
        description="Flattened patch index in the 16x16 patch grid",
    )
    patch_row: int = Field(
        ...,
        ge=0,
        le=15,
        description="Row index of the most changed patch",
    )
    patch_col: int = Field(
        ...,
        ge=0,
        le=15,
        description="Column index of the most changed patch",
    )
