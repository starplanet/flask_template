import logging
import smtplib
from email.policy import SMTP
from email.message import EmailMessage
from email.utils import make_msgid

from proj.utils.html import is_html
from proj.config import CONF

logger = logging.getLogger(__name__)


class EmailProvider(object):
    def __init__(self, host, port, username, password, use_ssl, use_tls, fromname=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_ssl = use_ssl
        self.use_tls = use_tls
        self.fromname = fromname


class SMTPMailer(object):
    def __init__(self, email_provider):
        """
        :type email_provider: hamlet.models.EmailProvider
        """
        self.email_provider = email_provider

    def send(self, subject, content, recipients):
        message = self._new_message(subject, content, recipients)
        return self._send_message(message)

    def _new_message(self, subject, content, recipients):
        msg = EmailMessage(policy=SMTP)
        msg['Subject'] = subject
        msg['From'] = self.email_provider.fromname
        msg['To'] = ', '.join(recipients)
        if is_html(content):
            msg.add_alternative(content, subtype='html')
        else:
            msg.set_content(content)
        msg['Message-ID'] = make_msgid()
        return msg

    def _send_message(self, message):
        if self.email_provider.use_ssl:
            host = smtplib.SMTP_SSL(self.email_provider.host, self.email_provider.port)
        else:
            host = smtplib.SMTP(self.email_provider.host, self.email_provider.port)

        if self.email_provider.use_tls:
            host.starttls()

        host.login(self.email_provider.username, self.email_provider.password)
        host.send_message(message)
        host.quit()


def _send_to_with_email(email, subject, content, quiet=True):
    smtp_config = CONF.SMTP
    provider = EmailProvider(**smtp_config)
    mailer = SMTPMailer(provider)
    try:
        receivers = [email]
        if email != CONF.DEV_EMAIL:
            receivers.append(CONF.DEV_EMAIL)
        mailer.send(subject, content, receivers)
    except Exception as e:
        if quiet:
            logger.exception('send mail failed')
        else:
            raise e
    return receivers


def send_task_status_email(status, msg, email, quiet=True):
    subject = 'Task status: {}'.format(status)
    content = 'Task status: {}. Message: {}'.format(status, msg)
    return _send_to_with_email(email, subject, content, quiet)
