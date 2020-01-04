import sys
import traceback
from typing import Dict

from app.services import mail_service
from app.services.excel_to_model_converter import ExcelToModelConverter
from app.services.model_to_xml_converter import ModelToXmlConverter
from app.aws import sns


def lambda_handler(event: Dict, *args) -> str:
    print("Starting program")

    try:
        message_id = event["Records"][0]["ses"]["mail"]["messageId"]
        start_convert(message_id)
    except Exception:
        error = f"\nThe following error occurred:\n{traceback.format_exc()}\n"
        print(error)
        return error

    success_message = "Execution was successful"
    print(success_message)
    return success_message


def start_convert(message_id: str):
    file = mail_service.get_first_attachment_from_s3_mail(message_id)
    retoure_models = ExcelToModelConverter().convert(file)
    xml = ModelToXmlConverter().convert(retoure_models)

    print("\nGenerated xml:\n" + "\n\n".join(xml))
    [sns.publish(retoure) for retoure in xml]


if __name__ == "__main__":
    with open(sys.argv[1], "rb") as f:
        attachments = mail_service.get_all_attachments_from_bytes(f.read())

    print(f"Found {len(attachments)} attachments")

    retoure_models = ExcelToModelConverter().convert(attachments[0])
    xml = ModelToXmlConverter().convert(retoure_models)

    print("\nGenerated xml:\n" + "\n\n".join(xml))
