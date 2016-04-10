"""Module to control email"""
from flask.ext.mail import Message
from beaver_manager import mail
from threading import Thread
from beaver_manager import app
from .decorators import async


@async
def send_async_email(app, msg):
    """
    Function that will asyncrhonusly send an email so that the app doesn't
    hang waiting for the email to be sent

    Args:
        app(app): Flask app instance
        msg (msg): Flask email message instance
    """
    with app.app_context():
        mail.send(msg)


def send_email(subject, recipients, text_body, html_body):
    """
    Sends email to recipent using the flasks email module

    Args:
        subject (str): Plain text
        recepients (str): Reciepent email. Can be list of strings
        text_body (str): Body of message without HTML formatting
        html_body (str): Body of message with HTML formattin
    """
    sender = "beavermanagerautomated@gmail.com"
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(app, msg)
    return True
