from app.api.v1.routes import router as v1_router
from app.core import config, tasks
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def get_application() -> FastAPI:
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler("startup", tasks.create_start_app_handler(app))
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))

    app.include_router(v1_router, prefix=config.ROUTER_PREFIX)

    @app.get("/", status_code=200)
    def root():
        return {"Hello": "Mundo!"}

    return app


app = get_application()
