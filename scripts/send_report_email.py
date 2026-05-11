#!/usr/bin/env python3
import os
import smtplib
from email.message import EmailMessage
from pathlib import Path


def add_attachment(message: EmailMessage, path: Path) -> bool:
    if not path.exists():
        return False

    data = path.read_bytes()
    maintype, subtype = 'application', 'octet-stream'
    if path.suffix.lower() == '.pdf':
        maintype, subtype = 'application', 'pdf'
    elif path.suffix.lower() == '.html':
        maintype, subtype = 'text', 'html'

    message.add_attachment(data, maintype=maintype, subtype=subtype, filename=path.name)
    return True


def main():
    smtp_host = os.environ['SMTP_HOST']
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))
    smtp_user = os.environ['SMTP_USER']
    smtp_password = os.environ['SMTP_PASSWORD']
    mail_to = os.environ['MAIL_TO']
    mail_from = os.environ.get('MAIL_FROM', smtp_user)

    report_pdf = Path(os.environ.get('REPORT_PDF', 'reports/test_report.pdf'))
    report_html = Path(os.environ.get('REPORT_HTML', 'reports/test_report.html'))

    message = EmailMessage()
    message['Subject'] = os.environ.get('MAIL_SUBJECT', 'QA test report')
    message['From'] = mail_from
    message['To'] = mail_to
    message.set_content(
        'The QA pipeline has completed. The generated report is attached.\n'
        f'PDF: {report_pdf}\n'
        f'HTML: {report_html}\n'
    )

    attached_any = False
    attached_any = add_attachment(message, report_pdf) or attached_any
    attached_any = add_attachment(message, report_html) or attached_any

    if not attached_any:
        print('No report files found to attach.')

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(smtp_user, smtp_password)
        server.send_message(message)

    print('Notification email sent to', mail_to)


if __name__ == '__main__':
    main()
