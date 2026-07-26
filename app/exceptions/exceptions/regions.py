from app.exceptions.exceptions.base import AppException


class InvalidRegionCodeException(AppException):
    
    def __init__(self, region_codes: list[str]):
        self.region_codes = sorted(region_codes)
