from sqlalchemy.orm import Session

from apps.images.models import Image
from apps.images.schema import ImageSchemaCreate


def get_image(db: Session, image_id: int):
    return db.query(Image).filter(Image.id == image_id).first()


def get_all_approved_images(db: Session):
    return db.query(Image).filter(Image.is_approved==True).all()


def get_all_not_approved_images(db: Session):
    return db.query(Image).filter(Image.is_approved==False).all()


def create_image(db: Session, image: ImageSchemaCreate):
    db_image = Image(
        is_approved=image.is_approved,
        name=image.name,
        filename=image.filename,
        root_path=image.root_path,
        thumbnail_path=image.thumbnail_path
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image
