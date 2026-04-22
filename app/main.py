from fastapi import FastAPI
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.api.routes import auth, users, videos, projects, suppliers, investors, adverts, wallets, settlements, admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

@app.get("/api/health")
def health():
    return {"success": True, "message": f"{settings.APP_NAME} is running"}

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(videos.router, prefix="/api/videos", tags=["videos"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(suppliers.router, prefix="/api/suppliers", tags=["suppliers"])
app.include_router(investors.router, prefix="/api/investors", tags=["investors"])
app.include_router(adverts.router, prefix="/api/adverts", tags=["adverts"])
app.include_router(wallets.router, prefix="/api/wallets", tags=["wallets"])
app.include_router(settlements.router, prefix="/api/settlements", tags=["settlements"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
