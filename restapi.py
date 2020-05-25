import logging
from json import JSONDecodeError

from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse as Response
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from uvicorn.main import run
from tortoise.contrib.starlette import register_tortoise

from models import Sources
from models import Binaries

logging.basicConfig(level=logging.DEBUG)
app = Starlette()


@app.route("/", methods=["GET"])
async def hello(_: Request) -> Response:
    return Response({"meta on ubuntu": ["binary pkgs", "source pkgs"]})


@app.route("/source/package/names", methods=["GET"])
async def sources_list_names(request: Request) -> Response:
    sources = await Sources.all()
    return Response({"names": [str(source) for source in sources]})


@app.route("/binary/package/names", methods=["GET"])
async def sources_list_names(request: Request) -> Response:
    binaries = await Binaries.all()
    return Response({"names": [str(b) for b in binaries]})


register_tortoise(
    app, db_url="sqlite://packages.db", modules={"models": ["models"]},
)

if __name__ == "__main__":
    run(app)
