# app/utils.py
import requests
import json
import time
from functools import wraps
from .logging_config import logger

def retry_on_failure(max_retries=3, delay=1):
    """Decorator to retry failed API calls"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                    time.sleep(delay * (attempt + 1))  # Exponential backoff
            return None
        return wrapper
    return decorator

def safe_json_parse(response):
    """Safely parse JSON from response with detailed error info"""
    try:
        if not response.text.strip():
            raise ValueError("Empty response")
        
        # Try direct parse
        data = response.json()
        return data, None
    except json.JSONDecodeError as e:
        # Try to fix common JSON issues
        text = response.text.strip()
        
        # Remove BOM if present
        if text.startswith('\ufeff'):
            text = text[1:]
        
        # Try to extract JSON from wrapped response
        if '{' in text and '}' in text:
            start = text.find('{')
            end = text.rfind('}') + 1
            json_str = text[start:end]
            try:
                data = json.loads(json_str)
                return data, "Extracted JSON from wrapped response"
            except:
                pass
        
        # Return error details
        error_info = {
            "error": str(e),
            "status_code": response.status_code,
            "content_type": response.headers.get('content-type'),
            "response_preview": text[:500],
            "response_length": len(text)
        }
        return None, error_info