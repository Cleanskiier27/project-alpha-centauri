from litestar import Litestar, get

@get("/")
def hello_world() -> dict[str, str]:
    return {"hello": "world"}

@get("/status")
def get_status() -> dict[str, str]:
    return {"status": "Agent Executive Core Online", "repo": "github.com/cleanskiier27/gates"}

app = Litestar(route_handlers=[hello_world, get_status])
