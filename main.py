from ui import run_app
from router import route_request
from models import get_models


if __name__ == "__main__":
    run_app(route_request, get_models)