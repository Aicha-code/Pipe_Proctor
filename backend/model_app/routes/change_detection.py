import os
import tempfile

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from model_app.schemas.prediction import ChangeDetectionResponse
from model_app.services import model_service

router = APIRouter(prefix="/api/v1", tags=["change-detection"])

ALLOWED_CONTENT_TYPES = {
    "image/tiff",
    "image/tif",
    "application/octet-stream",
}


@router.post("/change-detection", response_model=ChangeDetectionResponse)
async def change_detection(
    reference_image: UploadFile = File(...),
    current_image: UploadFile = File(...),
    segment_id: str = Form(...),
):
    """Accept two SAR chip images and return the strongest detected change."""

    reference_type = (reference_image.content_type or "").lower()
    current_type = (current_image.content_type or "").lower()

    if reference_type not in {item.lower() for item in ALLOWED_CONTENT_TYPES}:
        raise HTTPException(status_code=400, detail="reference_image must be a TIFF file")

    if current_type not in {item.lower() for item in ALLOWED_CONTENT_TYPES}:
        raise HTTPException(status_code=400, detail="current_image must be a TIFF file")

    temp_files = []

    try:
        with tempfile.NamedTemporaryFile(suffix=".tif", delete=False) as ref_file:
            ref_data = await reference_image.read()
            ref_file.write(ref_data)
            ref_path = ref_file.name
            temp_files.append(ref_path)

        with tempfile.NamedTemporaryFile(suffix=".tif", delete=False) as cur_file:
            cur_data = await current_image.read()
            cur_file.write(cur_data)
            cur_path = cur_file.name
            temp_files.append(cur_path)

        result = model_service.detect_change(
            image_t1_path=ref_path,
            image_t2_path=cur_path,
            segment_id=segment_id,
        )

        return ChangeDetectionResponse(**result)

    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Model execution failed: {str(exc)}") from exc

    finally:
        for file_path in temp_files:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except OSError:
                    pass