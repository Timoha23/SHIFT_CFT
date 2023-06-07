import uvicorn
from fastapi import APIRouter, FastAPI

from api.handlers.salary_handlers import salary_router
from api.handlers.user_handlers import user_router


app = FastAPI(title="Workers salaries")

main_router = APIRouter()

main_router.include_router(user_router, prefix="/users", tags=["users"])
main_router.include_router(salary_router, prefix="/salary", tags=["salaries"])

app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
