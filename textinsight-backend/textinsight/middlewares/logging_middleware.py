import logging
from datetime import datetime
from textinsight.middlewares.base_middleware import BaseMiddleware

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseMiddleware):
    def __call__(self, request):
        try:
            logger.info(f"Request: {request.method} {request.path} at {datetime.now()} by {request.user}")
        except Exception as log_error:
            logger.error(f"Logging error: {log_error}")

        response = self.get_response(request)

        try:
            logger.info(f"Response: {response.status_code} at {datetime.now()} for {request.user}")
        except Exception as log_error:
            logger.error(f"Logging error: {log_error}")

        return response
