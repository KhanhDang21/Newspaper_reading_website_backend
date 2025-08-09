from fastapi import APIRouter, Depends, HTTPException
from beanie import PydanticObjectId
from services.newspaper_publisher_service import NewspaperPublisherServiceFactory
from schemas.newspaper_publisher_schema import NewspaperPublisherCreate, NewspaperPublisherUpdate, NewspaperPublisherResponse
from schemas.base_response import BaseResponse
from services.newspaper_publisher_service import get_newspaper_publisher_service

router = APIRouter(
    prefix="/news-papers",
    tags=["news-papers-publisher"]
)

@router.post("/", response_model=BaseResponse[NewspaperPublisherResponse] | NewspaperPublisherResponse)
async def create_newspaper(
    newspaper: NewspaperPublisherCreate,
    service=Depends(get_newspaper_publisher_service)
):
    db_newspaper = await service.create_newspaper(newspaper)
    if db_newspaper is None:
        raise HTTPException(status_code=400, detail="Newspaper creation failed")
    return BaseResponse(
        message="Newspaper created successfully",
        status="success",
        data=db_newspaper,
    )

@router.get("/{id}", response_model=BaseResponse[NewspaperPublisherResponse] | NewspaperPublisherResponse)
async def get_newspaper(
    id: PydanticObjectId,
    service=Depends(get_newspaper_publisher_service)
):
    db_newspaper = await service.get_newspaper(id)
    if db_newspaper is None:
        raise HTTPException(status_code=404, detail="Newspaper not found")
    return BaseResponse(
        message="Newspaper retrieved successfully",
        status="success",
        data=db_newspaper
    )

@router.get("/", response_model=BaseResponse[list[NewspaperPublisherResponse]] | list[NewspaperPublisherResponse])
async def get_all_newspapers(
    service=Depends(get_newspaper_publisher_service)
):
    db_newspapers = await service.get_all_newspapers()
    return BaseResponse(
        message="Newspapers retrieved successfully",
        status="success",
        data=db_newspapers
    )

@router.put("/{id}", response_model=BaseResponse[NewspaperPublisherResponse] | NewspaperPublisherResponse)
async def update_newspaper(
    id: PydanticObjectId,
    newspaper: NewspaperPublisherUpdate,
    service=Depends(get_newspaper_publisher_service)
):
    db_newspaper = await service.update_newspaper(id, newspaper)
    if db_newspaper is None:
        raise HTTPException(status_code=404, detail="Newspaper not found")
    return BaseResponse(
        message="Newspaper updated successfully",
        status="success",
        data=db_newspaper
    )

@router.delete("/{id}", response_model=BaseResponse[NewspaperPublisherResponse] | NewspaperPublisherResponse)
async def delete_newspaper(id: PydanticObjectId, service=Depends(get_newspaper_publisher_service)):
    db_newspaper = await service.delete_newspaper(id)
    if db_newspaper is None:
        raise HTTPException(status_code=404, detail="Newspaper not found")
    return BaseResponse(
        message="Newspaper deleted successfully",
        status="success",
        data=db_newspaper
    )
