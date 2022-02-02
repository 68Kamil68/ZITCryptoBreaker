from celery import shared_task, Task
import smtplib, ssl

from project.config import settings
from project.utils import get_hash_type, HashTypes, hash_types_functions, WORDLISTS


class SendEmailOnTimeExceedTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        send_email.delay(
            "Hash value not found :(",
            args.get("email"),
            "We couldn't find the value of your hash",
        )


@shared_task
def send_email(subject: str, email_to: str, body: str):
    port = settings.MAIL_PORT
    context = ssl.create_default_context()
    message = "Subject: {}\n\n{}".format(subject, body)

    with smtplib.SMTP_SSL(settings.MAIL_SERVER, port, context=context) as server:
        server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
        server.sendmail(settings.MAIL_USERNAME, email_to, message)


@shared_task(base=SendEmailOnTimeExceedTask, time_limit=600)
def break_hash(hash: str, email: str, wordlist: str | None):
    hash_type = get_hash_type(hash)

    if hash_type == HashTypes.UNSUPPORTED:
        send_email.delay(
            "Unsupported hash type",
            email,
            "The given input has unsupported hashtype",
        )
        return

    hashing_function = hash_types_functions[hash_type]
    if wordlist:
        if wordlist not in WORDLISTS:
            send_email.delay(
                "Wrong wordlist name given",
                email,
                "The given wordlist has not been found on the server",
            )
            return

        with open(f"project/wordlists/{wordlist}.txt", encoding="utf-8") as f:
            for line in f:
                if hash == hashing_function(line.strip().encode("utf-8")).hexdigest():
                    send_email.delay(
                        "Hash value found!",
                        email,
                        f"The given hash {hash} has a value equal to {line} and is of type: {hash_type.value}",
                    )
                    return

    send_email.delay(
        "Hash value not found :(",
        email,
        "We couldn't find the value of your hash",
    )
