from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI()
BASE_URL: str = "http://localhost:8000"


class ShortenRequest(BaseModel):
    url: str


@app.post("/url/shorten")
async def url_shorten(request: ShortenRequest):
    """
    Given a URL, generate a short version of the URL that can be later resolved to the originally
    specified URL.
    """
    short_url = "new-short-url"
    return {"short_url": f"{BASE_URL}/r/{short_url}"}


class ResolveRequest(BaseModel):
    short_url: str


@app.get("/r/{short_url}")
async def url_resolve(short_url: str):
    """
    Return a redirect response for a valid shortened URL string.
    If the short URL is unknown, return an HTTP 404 response.
    """
    return RedirectResponse("http://original/url")


@app.get("/")
async def index():
    return "Your URL Shortener is running!"
