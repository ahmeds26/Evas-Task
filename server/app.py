from fastapi import FastAPI, Request

from server.routes.items import router as ItemRouter

app = FastAPI()

app.include_router(ItemRouter, tags=["Item"], prefix="/items")


@app.get("/", tags=["Root"])
async def root(request: Request):
    return "Welcome to OLX Scraper Api!"