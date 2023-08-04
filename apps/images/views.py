import os
from pathlib import Path

from fastapi import APIRouter, File, UploadFile, Request, Depends
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database.get_database import get_db
from apps.images.domain import ImageDomain


BASE_DIR = Path(__file__).resolve().parent

router = APIRouter()

templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))


@router.post("/upload-image", response_class=HTMLResponse)
async def image_upload(
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
    ):

    image_domain = ImageDomain(image=file, db=db)
    image_domain.create_image()


# @router.get("", response_class=HTMLResponse)
# async def list_images(request: Request):
#     return templates.TemplateResponse("list_images.html", {"request": request})


@router.get("", response_class=HTMLResponse)
async def list_images(request: Request, db: Session = Depends(get_db)):
    image_domain = ImageDomain(db=db)
    images = image_domain.get_images()
    return templates.TemplateResponse("list_images.html", {"request": request, "images": images})