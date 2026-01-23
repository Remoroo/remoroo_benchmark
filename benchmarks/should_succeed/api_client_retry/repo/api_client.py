"""API client that needs retry logic."""

import time
from typing import Optional, Dict, Any

# Simulated server state (fails first 2 requests, then succeeds)
_request_count = 0

def _simulated_api_call(endpoint: str) -> Dict[str, Any]:
    """Simulate an API that fails transiently then succeeds.
    
    This simulates a flaky server that:
    - Returns 503 on first request
    - Returns 502 on second request  
    - Returns 200 with data on third request
    """
    global _request_count
    _request_count += 1
    
    if _request_count == 1:
        return {"status": 503, "error": "Service Unavailable"}
    elif _request_count == 2:
        return {"status": 502, "error": "Bad Gateway"}
    else:
        return {"status": 200, "data": {"message": "Success!", "value": 42}}


class APIError(Exception):
    """Exception raised for API errors."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error {status_code}: {message}")


class APIClient:
    """A simple API client.
    
    BUG: No retry logic! Fails immediately on transient errors.
    
    GOAL: Implement retry with exponential backoff:
    - Retry up to 3 times on transient errors (500, 502, 503, 504)
    - Wait 1s before first retry, 2s before second, 4s before third
    - Raise APIError if all retries fail
    """
    
    def __init__(self, base_url: str = "https://api.example.com"):
        self.base_url = base_url
        self.request_count = 0
    
    def fetch_data(self, endpoint: str) -> Dict[str, Any]:
        """Fetch data from an API endpoint.
        
        BUG: No retry logic - fails immediately on any error.
        
        TODO: Add retry with exponential backoff:
        - max_retries = 3
        - transient_errors = [500, 502, 503, 504]
        - delays = [1, 2, 4] seconds (exponential backoff)
        """
        self.request_count += 1
        
        # Make the API call (simulated)
        response = _simulated_api_call(endpoint)
        
        # BUG: No retry on transient errors!
        if response["status"] != 200:
            raise APIError(response["status"], response.get("error", "Unknown error"))
        
        return response["data"]


def main():
    """Test the API client retry logic."""
    global _request_count
    _request_count = 0  # Reset for test
    
    client = APIClient()
    
    print("Testing API client with flaky server simulation")
    print("Server will fail first 2 requests, then succeed")
    print()
    
    start_time = time.time()
    
    try:
        result = client.fetch_data("/data")
        elapsed = time.time() - start_time
        
        print(f"Result: {result}")
        print(f"Total requests made: {_request_count}")
        print(f"Time elapsed: {elapsed:.1f}s")
        
        # Verify retry worked correctly
        retry_works = (
            result.get("value") == 42 and  # Got correct data
            _request_count == 3 and         # Made exactly 3 requests (2 failures + 1 success)
            elapsed >= 2.5                  # Waited for retries (1s + 2s minimum)
        )
        
        print(f"\nretry_works: {retry_works}")
        
        if retry_works:
            print("SUCCESS: Retry logic with exponential backoff works!")
        else:
            if _request_count < 3:
                print("FAILED: Not enough retry attempts")
            elif elapsed < 2.5:
                print("FAILED: Didn't wait for exponential backoff delays")
            else:
                print("FAILED: Unexpected result")
                
    except APIError as e:
        print(f"FAILED: API call raised error without retry: {e}")
        print(f"retry_works: false")


if __name__ == "__main__":
    main()

