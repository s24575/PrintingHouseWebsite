from enum import StrEnum


class OptionGroupType(StrEnum):
    Select = "select"
    Number = "number"


QUANTITY_OPTION_GROUP_NAME = "ilosc"

UPLOAD_FOLDER = "uploads/"
ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png", "docx"}
