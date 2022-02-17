import argparse
import dataclasses
import importlib.resources
import os.path
import smtplib
import sys
import typing
from email.message import Message
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import markdown


def main() -> None:
    args = _get_args()
    mail = _make_mail(
        args.sender_address,
        args.recipient_addresses,
        args.subject,
        args.content_file_path,
        args.attachment_file_path,
    )
    _send_mail(
        args.smtp_host_name,
        args.smtp_port_number,
        args.smtp_user_name,
        args.smtp_password,
        mail,
    )


@dataclasses.dataclass
class _Args:
    sender_address: str
    recipient_addresses: list[str]
    subject: str
    content_file_path: str
    smtp_host_name: str
    smtp_port_number: int
    smtp_user_name: str
    smtp_password: typing.Optional[str]
    attachment_file_path: typing.Optional[str]


def _get_args() -> _Args:
    arg_parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    arg_parser.add_argument(
        "sender",
        metavar="FROM",
        help="the sender of the mail",
        nargs=1,
    )
    arg_parser.add_argument(
        "recipients",
        metavar="TO",
        help="the recipients of the mail",
        nargs=1,
    )
    arg_parser.add_argument(
        "subject",
        metavar="SUBJECT",
        help="the subject of the mail",
        nargs=1,
    )
    arg_parser.add_argument(
        "content_file",
        metavar="FILE",
        help="the markdown file as the content of the mail",
        nargs=1,
    )
    arg_parser.add_argument(
        "-H",
        "--smtp-host",
        metavar="HOST",
        help="specify the host of the smtp server",
        default="127.0.0.1",
    )
    arg_parser.add_argument(
        "-p",
        "--smtp-port",
        metavar="PORT",
        help="specify the port of the smtp server",
        default="465",
    )
    arg_parser.add_argument(
        "-u",
        "--smtp-user",
        metavar="USER",
        help="specify the user of smtp server",
    )
    arg_parser.add_argument(
        "-P",
        "--smtp-pass",
        metavar="PASS",
        help="specify the password for the user of smtp server",
    )
    arg_parser.add_argument(
        "-a", "--attachment-file", metavar="FILE", help="specify the attachment file"
    )
    raw_args = arg_parser.parse_args(sys.argv[1:])
    sender_address = raw_args.sender[0]
    recipient_addresses = raw_args.recipients[0].split(",")
    subject = raw_args.subject[0]
    content_file_path = raw_args.content_file[0]
    if content_file_path == "-":
        content_file_path = "/dev/stdin"
    smtp_host_name = raw_args.smtp_host
    smtp_port_number = int(raw_args.smtp_port)
    smtp_user_name = raw_args.smtp_user
    if smtp_user_name is None:
        smtp_user_name = sender_address
    smtp_password = raw_args.smtp_pass
    attachment_file_path = raw_args.attachment_file
    args = _Args(
        sender_address=sender_address,
        recipient_addresses=recipient_addresses,
        subject=subject,
        content_file_path=content_file_path,
        smtp_host_name=smtp_host_name,
        smtp_port_number=smtp_port_number,
        smtp_user_name=smtp_user_name,
        smtp_password=smtp_password,
        attachment_file_path=attachment_file_path,
    )
    return args


def _make_mail(
    sender_address: str,
    recipient_addresses: list[str],
    subject: str,
    content_file_path: str,
    attachment_file_path: typing.Optional[str],
) -> Message:
    with open(content_file_path, "r") as f:
        markdown1 = f.read()
    html = _markdown_2_html(markdown1)
    mail = MIMEText(html, "html")
    mail["From"] = sender_address
    mail["To"] = ", ".join(recipient_addresses)
    mail["Subject"] = subject
    if attachment_file_path is not None:
        mixed = MIMEMultipart("mixed")
        mixed.attach(mail)
        with open(attachment_file_path, "rb") as f:
            attachment = MIMEApplication(f.read(), "octet-stream")
        attachment.add_header(
            "Content-Disposition",
            "attachment",
            filename=os.path.basename(attachment_file_path),
        )
        mixed.attach(attachment)
        mail = mixed
    return mail


def _markdown_2_html(markdown1: str) -> str:
    with (importlib.resources.files("mdmail") / "github-markdown.css").open("r") as f:
        css = f.read()
    html_body = markdown.markdown(markdown1, extensions=["tables"])
    html = """
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
{css}
.markdown-body {{
    box-sizing: border-box;
    min-width: 200px;
    max-width: 980px;
    margin: 0 auto;
    padding: 45px;
}}

@media (max-width: 767px) {{
    .markdown-body {{
        padding: 15px;
    }}
}}
</style>
</head>
<body class="markdown-body">
{html_body}
</body>
</html>
""".format(
        css=css, html_body=html_body
    )
    return html


def _send_mail(
    smtp_host_name: str,
    smtp_port_number: int,
    smtp_user_name: str,
    smtp_password: typing.Optional[str],
    mail: Message,
) -> None:
    smtp = smtplib.SMTP_SSL(smtp_host_name, smtp_port_number)
    if smtp_password is not None:
        smtp.ehlo()
        smtp.login(smtp_user_name, smtp_password)
    smtp.ehlo()
    smtp.send_message(mail)
    smtp.quit()


if __name__ == "__main__":
    main()
