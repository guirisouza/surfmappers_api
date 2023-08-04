from fastapi.routing import APIRouter
from apps import docs, images

api_router = APIRouter()

api_router.include_router(docs.router)

api_router.include_router(
    images.router,
    prefix="/images",
    tags=["images"],
)
