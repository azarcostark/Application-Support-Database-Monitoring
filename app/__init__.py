import time

from flask import Flask, request

from utils.logger import get_logger


logger = get_logger("api")


def create_app():
    app = Flask(__name__)

    @app.before_request
    def start_timer():
        request.start_time = time.perf_counter()

    @app.after_request
    def log_request(response):
        start_time = getattr(request, "start_time", None)

        if start_time is not None:
            response_time = time.perf_counter() - start_time
        else:
            response_time = 0.0

        logger.info(
            "%s %s | status=%s | response_time=%.4fs",
            request.method,
            request.path,
            response.status_code,
            response_time,
        )

        return response

    from app.routes import register_routes
    register_routes(app)

    return app