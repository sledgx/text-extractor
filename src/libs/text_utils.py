from langdetect import detect


class TextUtils:

    @staticmethod
    def isEmpty(text: str) -> bool:
        return not (text and text.strip())

    @staticmethod
    def detectLanguage(text: str) -> str:
        if not TextUtils.isEmpty(text):
            return detect(text)
        else:
            return None
