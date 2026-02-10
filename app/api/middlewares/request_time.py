import time
from fastapi import Request

async def get_request_time(request: Request, call_next):
    """Middleware to calculate the time taken to process a request and add it to the response headers."""
    # Calculate the time taken to process the request
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # Add the process time to the response headers
    response.headers["X-Process-Time"] = str(process_time)
    print(f"Process Time: {process_time:.4f} seconds")
    return response