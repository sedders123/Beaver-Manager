import sendgrid

key = "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"


sg = sendgrid.SendGridClient(key)


def send_message(recepient, subject, message):
    """
    Sends email to recipent using the ``sendgrid`` module

    Args:
        recepient (str): In form "John Doe <john.doe@example.com>"
        subject (str): Plain text
        message (str): Can use HTML formatting
    """
    message = sendgrid.Mail()
    message.add_to(recepient)
    message.set_from("automated-beavers@sedders123.me")
    message.set_subject("Sending with SendGrid is Fun")
    message.set_html("and easy to do anywhere, even with Python")

    sg.send(message)
