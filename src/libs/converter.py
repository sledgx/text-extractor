import textract
from libs.text_utils import TextUtils
from libs.path_utils import PathUtils


class TextExtractor:

    @staticmethod
    def getText(path: str, use_ocr_fallback: bool = True) -> tuple:
        ocr_fallback = False
        ext = PathUtils.getExtension(path)
        text = textract.process(path).decode('utf-8')

        if TextUtils.isEmpty(text) and ext == 'pdf' and use_ocr_fallback:
            ocr_fallback = True
            text = textract.process(path, method='tesseract').decode('utf-8')

        return (text, ocr_fallback)
