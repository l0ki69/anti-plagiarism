import textract


class DocumentHandler:

    @classmethod
    def handler(cls, doc_path: str) -> str:
        result_text = textract.process(doc_path).decode('utf-8')
        return result_text