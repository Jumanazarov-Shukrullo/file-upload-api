from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from api.v1.routers.upload import router as upload_router
from api.v1.routers.auth import router as auth_router

app = FastAPI(title="File Upload API")
app.include_router(upload_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    # Apply BearerAuth to every path
    for path in openapi_schema["paths"].values():
        for op in path.values():
            op.setdefault("security", []).append({"BearerAuth": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=8000)