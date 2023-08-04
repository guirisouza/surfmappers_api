import os
import uuid
from pathlib import Path

from PIL import Image, ImageFile
from starlette.datastructures import UploadFile
from sqlalchemy.orm import Session

from apps.helpers.local_file_manager import save_upload_file_tmp

from apps.images.repository import create_image, get_all_approved_images
from apps.images.schema import ImageSchemaCreate

ImageFile.LOAD_TRUNCATED_IMAGES = True

STATIC_PATH_IMAGES = f"{str(Path(__file__).resolve().parent.parent)}/static/images"

class ImageProc:
    def __init__(self, image: UploadFile):
        self.content_type = str(image.content_type).lower()
        self.input_image_path = save_upload_file_tmp(image)
        self.output_image_path = ""
        self.image_file = Image.open(self.input_image_path)
        self.image_size = self.image_file.size
        self.original_file_name = image.filename.split(".")[0]
        self.new_file_name = str(uuid.uuid4())
        self.original_extension = image.filename.split(".")[-1]
        self.final_name = ""
        self.preserve_original_name: bool = False


class ImageProcessingDomain:
    def __init__(self, image: ImageProc):
        self.image = image

    def _save(self):
        self.image.output_image_path = f"{STATIC_PATH_IMAGES}/{self.image.new_file_name}.png"
        self.image.final_name = f"/static/images/{self.image.new_file_name}.png"
        self.image.image_file.save(self.image.output_image_path)

    def _close_mem(self):
        self.image.image_file.close()
        self.image.input_image_path.unlink()

    def image_save_process_flow(self):
        try:
            self._save()
        except TypeError as ex:
            pass
        finally:
            if self.image.output_image_path:
                self._close_mem()

class ImageDomain():
    def __init__(self, db: Session, image: UploadFile = None):
        if image:
            self.image = ImageProc(image=image)
            self.image_processing_domain = ImageProcessingDomain(image=self.image)
        self.db = db

    def create_image(self):
        try:
            self.image_processing_domain.image_save_process_flow()
            image_schema = ImageSchemaCreate(
                is_approved=True,
                root_path=self.image.final_name,
                filename=self.image.new_file_name,
                name=self.image.original_file_name,
                thumbnail_path=self.image.original_file_name
            )
            image = create_image(db=self.db, image=image_schema)
            return image
        except Exception as ex:
            pass

    def get_images(self):
        approved_images = get_all_approved_images(db=self.db)
        return approved_images


