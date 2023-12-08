from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import diskcache
import secrets

app = FastAPI()
cache = diskcache.Cache()
BASE_URL: str = "http://localhost:8000"


class ShortenRequest(BaseModel):
    url: str


@app.post("/url/shorten")
async def url_shorten(request: ShortenRequest):
    """
    Given a URL, generate a short version of the URL that can be later resolved to the originally
    specified URL.
    """
    while True:
        # This loop is here since secrets.token_urlsafe might return a key already in the cache.
        # Loop if the first cache.add invocation fails due to a duplicate key.
        with cache.transact():
            short_url = cache.get(request.url)
            if short_url:
                break
            short_url = secrets.token_urlsafe(4)
            if cache.add(short_url, request.url):
                cache.add(request.url, short_url)
                break
    return {"short_url": f"{BASE_URL}/r/{short_url}"}


class ResolveRequest(BaseModel):
    short_url: str


@app.get("/r/{short_url}")
async def url_resolve(short_url: str):
    """
    Return a redirect response for a valid shortened URL string.
    If the short URL is unknown, return an HTTP 404 response.
    """
    original_url = cache.get(short_url)
    if original_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(original_url)


@app.get("/")
async def index():
    return "Your URL Shortener is running!"
