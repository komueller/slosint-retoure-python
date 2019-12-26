class MailAttachmentNotFoundError(Exception):
    def __init__(self, mail_id: str):
        super(MailAttachmentNotFoundError, self).__init__(
            f"No attachments found in mail '{mail_id}'"
        )


class TooManyMailAttachmentsError(Exception):
    def __init__(self, mail_id: str):
        super(TooManyMailAttachmentsError, self).__init__(
            f"Mail '{mail_id}' has more than one attachment"
        )
