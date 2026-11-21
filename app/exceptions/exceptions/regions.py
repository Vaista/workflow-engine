from app.exceptions.exceptions.base import AppException


class InvalidRegionCodeException(AppException):
    
    def __init__(self, region_codes: list[str]):
        self.region_codes = sorted(region_codes)

class RegionNotFoundException(AppException):
    def __init__(self, region_code: str):
        self.region_code = region_code
