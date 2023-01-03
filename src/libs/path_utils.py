import tempfile
from langdetect import detect


class PathUtils:

    @staticmethod
    def getExtension(path: str) -> str:
        return '.' in path and path.rsplit('.', 1)[1].lower()

    @staticmethod
    def getTempPath() -> str:
        return next(tempfile._get_candidate_names())
