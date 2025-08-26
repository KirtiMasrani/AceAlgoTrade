from typing import Optional

import requests
from requests import Response
from requests.exceptions import RequestException
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from .rate_limiter import RateLimiter


@retry(
    reraise=True,
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type(RequestException),
)
def request(
    method: str,
    url: str,
    *,
    provider: Optional[str] = None,
    rate_limiter: Optional[RateLimiter] = None,
    **kwargs,
) -> Response:
    """Perform an HTTP request with retry/backoff and optional throttling."""
    if provider and rate_limiter:
        rate_limiter.throttle(provider)
    resp = requests.request(method, url, timeout=10, **kwargs)
    resp.raise_for_status()
    return resp
