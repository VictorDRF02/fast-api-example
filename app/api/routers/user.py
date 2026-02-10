from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/")
async def read_users():
    pass

@router.get("/{user_id}")
async def read_user(user_id: int):
    pass

@router.post("/")
async def create_user():
    pass

@router.put("/{user_id}")
async def update_user(user_id: int):
    pass

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    pass