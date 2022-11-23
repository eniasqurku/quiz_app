from django.core.mail import EmailMessage


def send_invitation_email(email: str, quiz_id: int):
    mail_to = [email]
    body = f"""
        You are invited to participate in the quiz with id {quiz_id}
    """
    email = EmailMessage(subject=f"Quiz invitation", body=body, to=mail_to)

    email.send()


def send_score_email(email: str, data: tuple):
    mail_to = [email]
    body = f"""
        The score for quiz {data[0]} is {data[1]}
    """
    email = EmailMessage(subject=f"Quiz Score", body=body, to=mail_to)

    email.send()
