from beanie import PydanticObjectId
from models.tag_model import Tag
from schemas.tag_schema import TagCreate, TagUpdate, TagResponse

class TagServiceFactory:
    @staticmethod
    def create_service():
        return TagService()
    
class TagService:
    async def create_tag(self, request: TagCreate) -> TagResponse:
        try:
            tag = Tag(**request.dict())
            await tag.insert()
            return TagResponse(**tag.dict())
        except Exception as e:
            print(e)
            return None

    async def get_tag(self, id: PydanticObjectId) -> TagResponse:
        try:
            tag = await Tag.get(id)
            if not tag:
                raise Exception("Tag not found")
            return TagResponse(**tag.dict())
        except Exception as e:
            print(e)
            return None

    async def get_all_tags(self) -> list[TagResponse]:
        try:
            return await Tag.find_all().to_list()
        except Exception as e:
            print(e)
            return None

    async def update_tag(self, id: PydanticObjectId, request: TagUpdate) -> TagResponse:
        try:
            tag = await Tag.get(id)
            if not tag:
                raise Exception("Tag not found")
            for key, value in request.dict(exclude_unset=True).items():
                setattr(tag, key, value)
            await tag.save()
            return TagResponse(**tag.dict())
        except Exception as e:
            print(e)
            return None
        
    async def delete_tag(self, id: PydanticObjectId) -> TagResponse:
        try:
            tag = await Tag.get(id)
            if not tag:
                raise Exception("Tag not found")
            await tag.delete()
            return TagResponse(**tag.dict())
        except Exception as e:
            print(e)
            return None
        
def get_tag_service():
    try:
        yield TagServiceFactory.create_service()
    finally:
        pass 