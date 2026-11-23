import controller.py
# main.py
from fastapi import FastAPI
from controller import user_controller, order_controller

def create_app() -> FastAPI:
    app = FastAPI(title="My App")
    
    # Wire up controllers (routers)
    app.include_router(controller.router, prefix="/")
    app.include_router(user_controller.router, prefix="/users")
    app.include_router(order_controller.router, prefix="/orders")
    
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    # Start the server
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
  