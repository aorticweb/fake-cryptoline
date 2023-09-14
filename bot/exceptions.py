from typing import Dict, Optional


class DataSourceException(Exception):
    """Exception during API request to data source api"""

    def __init__(self, status_code: int, resp_text: Optional[str] = ""):
        self.status_code = status_code
        self.resp_text = resp_text


class DataSourceInconsistencyException(Exception):
    """The data returned by the data source api the is not the expected data"""

    def __init__(self, details: Optional[str] = None, extra: Optional[Dict] = None):
        self.details = details
        self.extra = extra
