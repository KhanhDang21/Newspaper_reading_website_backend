from beanie import PydanticObjectId
from models.product_solution_model import ProductSolution
from schemas.product_solution_schema import ProductSolutionUpdate, ProductSolutionCreate, ProductSolutionResponse


class ProductSolutionServiceFactory:
    @staticmethod
    def create_service():
        return ProductSolutionService()
    

class ProductSolutionService:
    async def create_solution(self, request: ProductSolutionCreate) -> ProductSolutionResponse:
        try:
            solution = ProductSolution(**request.dict())
            await solution.insert()
            return ProductSolutionResponse(**solution.dict())
        
        except Exception as e:
            print(e)
            return None


    async def get_solution(self, id: PydanticObjectId) -> ProductSolutionResponse:
        try:
            solution = await ProductSolution.get(id)
            if not solution:
                raise Exception("Solution not found")
            return ProductSolutionResponse(**solution.dict())
        except Exception as e:
            print(e)
            return None


    async def get_all_solutions(self) -> list[ProductSolutionResponse]:
        try:
            return await ProductSolution.find_all().to_list()
        except Exception as e:
            print(e)
            return None


    async def update_solution(self, id: PydanticObjectId, request: ProductSolutionUpdate) -> ProductSolutionResponse:
        try:
            solution = await ProductSolution.get(id)
            if not solution:
                raise Exception("Solution not found")
            for key, value in request.dict(exclude_unset=True).items():
                setattr(solution, key, value)
            await solution.save()
            return ProductSolutionResponse(**solution.dict())
        except Exception as e:
            print(e)
            return None


    async def delete_solution(self, id: PydanticObjectId) -> ProductSolutionResponse:
        try:
            solution = await ProductSolution.get(id)
            if not solution:
                raise Exception("Solution not found")
            await solution.delete()
            return ProductSolutionResponse(**solution.dict())
        except Exception as e:
            print(e)
            return None


def get_product_solution_service():
    try:
        yield ProductSolutionServiceFactory.create_service()
    finally:
        pass
