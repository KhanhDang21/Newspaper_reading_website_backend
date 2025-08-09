from beanie import PydanticObjectId
from schemas.newspaper_publisher_schema import NewspaperPublisherCreate, NewspaperPublisherUpdate, NewspaperPublisherResponse
from models.newspaper_publisher_model import NewspaperPublisher

class NewspaperPublisherServiceFactory:
    @staticmethod
    def create_service():
        return NewspaperPublisherService()

class NewspaperPublisherService:
    async def create_newspaper(self, request: NewspaperPublisherCreate) -> NewspaperPublisherResponse:
        try:
            newspaper = NewspaperPublisher(**request.dict())
            await newspaper.insert()
            return NewspaperPublisherResponse(**newspaper.dict())
        except Exception as e:
            print(e)
            return None

    async def get_newspaper(self, id: PydanticObjectId) -> NewspaperPublisherResponse:
        try:
            newspaper = await NewspaperPublisher.get(id)
            if not newspaper:
                raise Exception("Newspaper not found")
            return NewspaperPublisherResponse(**newspaper.dict())
        except Exception as e:
            print(e)
            return None

    async def get_all_newspapers(self) -> list[NewspaperPublisherResponse]:
        try:
            return await NewspaperPublisher.find_all().to_list()
        except Exception as e:
            print(e)
            return None

    async def update_newspaper(self, id: PydanticObjectId, request: NewspaperPublisherUpdate) -> NewspaperPublisherResponse:
        try:
            newspaper = await NewspaperPublisher.get(id)
            if not newspaper:
                raise Exception("Newspaper not found")
            for key, value in request.dict(exclude_unset=True).items():
                setattr(newspaper, key, value)
            await newspaper.save()
            return NewspaperPublisherResponse(**newspaper.dict())
        except Exception as e:
            print(e)
            return None

    async def delete_newspaper(self, id: PydanticObjectId) -> NewspaperPublisherResponse:
        try:
            newspaper = await NewspaperPublisher.get(id)
            if not newspaper:
                raise Exception("Newspaper not found")
            await newspaper.delete()
            return NewspaperPublisherResponse(**newspaper.dict())
        except Exception as e:
            print(e)
            return None

def get_newspaper_publisher_service():
    try:
        yield NewspaperPublisherServiceFactory.create_service()
    finally:
        pass