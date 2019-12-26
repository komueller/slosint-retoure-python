from typing import List
import email

from app.aws import s3
from app.infrastructure import constants
from app.infrastructure.errors import (
    MailAttachmentNotFoundError,
    TooManyMailAttachmentsError,
)


def get_first_attachment_from_s3_mail(filename: str):
    print(f"MailService: get bytes from S3 Bucket with filename '{filename}'")

    mail_bytes = s3.get_file(constants.AWS_MAIL_PREFIX + filename)
    if len(mail_bytes) <= 0:
        raise FileNotFoundError(
            f"The file '{filename}' could not be found on the S3 Bucket"
        )

    attachments = get_all_attachments_from_bytes(mail_bytes)

    print(f"Found {len(attachments)} attachments")
    if len(attachments) <= 0:
        raise MailAttachmentNotFoundError(filename)
    if len(attachments) > 1:
        raise TooManyMailAttachmentsError(filename)

    return attachments[0]


def get_all_attachments_from_bytes(mail_bytes) -> List:
    mail = email.message_from_bytes(mail_bytes)

    result = []
    if mail.get_content_maintype() == "multipart":
        for part in mail.walk():
            if (
                part.get_content_maintype() == "multipart"
                or part.get_content_maintype() == "text"
                or part.get("Content-Disposition") == "inline"
                or part.get("Content-Disposition") is None
            ):
                continue

            print(f"Filename of attachment: {part.get_filename()}")
            result.append(part.get_payload(decode=True))
            # result.append(part.as_string())

    return result
