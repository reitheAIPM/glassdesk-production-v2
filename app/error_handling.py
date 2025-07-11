import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename="glassdesk.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def safe_api_call(func, *args, **kwargs):
    """Wrapper to handle API call errors gracefully."""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logging.error(f"Error in function {func.__name__}: {str(e)}")
        return None


def validate_data(data, required_keys):
    """Ensure all required keys exist in the data."""
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        logging.warning(f"Missing keys in data: {missing_keys}")
    return not missing_keys
