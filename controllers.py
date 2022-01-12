from .common import (
    unauthenticated,
)


@unauthenticated("index", "index.html")
def index():
    return dict()
