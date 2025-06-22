from fastapi import APIRouter, Depends, HTTPException
from beanie import PydanticObjectId
from services.product_solution_service import get_product_solution_service
from schemas.product_solution_schema import ProductSolutionCreate, ProductSolutionResponse, ProductSolutionUpdate
from schemas.base_response import BaseResponse


router = APIRouter(
    prefix="/solutions", 
    tags=["products_solutions"]
)


@router.post("/", response_model=BaseResponse[ProductSolutionResponse] | ProductSolutionResponse)
async def create_solution(
    product: ProductSolutionCreate,
    service = Depends(get_product_solution_service)
):
    product_db = await service.create_solution(product)
    return BaseResponse(
        message="Product solution created successfully",
        status="success",
        data=product_db
    )


@router.get("/{id}", response_model=BaseResponse[ProductSolutionResponse] | ProductSolutionResponse)
async def get_solution(
    id: PydanticObjectId,
    service = Depends(get_product_solution_service)
    ):
    
    product_db = await service.get_solution(id)
    return BaseResponse(
        message="Product solution retrieved successfully",
        status="success",
        data=product_db
    )


@router.get("/", response_model=BaseResponse[list[ProductSolutionResponse]] | list[ProductSolutionResponse])
async def get_all_solutions(
    service = Depends(get_product_solution_service)
):
    product_db = await service.get_all_solutions()
    return BaseResponse(
        message="Product solutions retrieved successfully",
        status="success",
        data=product_db
    )


@router.put("/{id}", response_model=BaseResponse[ProductSolutionResponse] | ProductSolutionResponse)
async def update_solution(
    id: PydanticObjectId, 
    product: ProductSolutionUpdate,
    service = Depends(get_product_solution_service)
    ):

    product_db = await service.update_solution(id, product)
    return BaseResponse(
        message="Product solution updated successfully",
        status="success",
        data=product_db
    )


@router.delete("/{id}", response_model=BaseResponse[ProductSolutionResponse] | ProductSolutionResponse)
async def delete_solution(
    id: PydanticObjectId,
    service = Depends(get_product_solution_service)
    ):
    product_db = await service.delete_solution(id)
    return BaseResponse(
        message="Product solution deleted successfully",
        status="success",
        data=product_db
    )