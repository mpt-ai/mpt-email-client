import os
import requests
import concurrent.futures
from .check import check_type

MPT_EMAIL_APIKEY = os.environ.get('MPT_EMAIL_APIKEY', None)
MPT_EMAIL_URI = os.environ.get('MPT_EMAIL_URI', None)

DEFAULT_TIMEOUT = 30


def _send_mail(args):
    data = {
        "subject": args.get('subject'),
        "message": args.get('message'),
        "email": args.get('email'),
    }

    cc = args.get('cc') or []
    if cc:
        data["cc"] = ", ".join(cc)

    try:
        r = requests.post(
            f"{args.get('host')}/mail/api/emailMessage/",
            headers={
                "Authorization": f"Api-Key {args.get('api_key')}"
            },
            data=data,
            files=args.get('files'),
            verify=args.get('ssl_verify'),
            timeout=args.get('timeout'),
        )
    except requests.RequestException as e:
        return False, f"failed to reach {args.get('host')}: {e}"

    if r.status_code == 201:
        return True, f"email sent to {args.get('email')} successfully"

    try:
        detail = r.json()
    except ValueError:
        detail = r.text

    if r.status_code in (400, 401, 403):
        return False, detail
    return False, f"{detail}\nsomething went wrong ({r.status_code})"


def sendEmail(
        subject=None,
        message=None,
        emails=None,
        cc=None,
        attachments=None,
        host=MPT_EMAIL_URI,
        api_key=MPT_EMAIL_APIKEY,
        ssl_verify=True,
        timeout=DEFAULT_TIMEOUT,
):
    if host is None or api_key is None:
        raise ValueError("please input `host` and `api_key` or set env `MPT_EMAIL_APIKEY` and `MPT_EMAIL_URI`")

    check_type(variable=subject, variableName="subject", dtype=str)
    check_type(variable=message, variableName="message", dtype=str)
    check_type(variable=emails, variableName="emails", dtype=list, child=str)

    cc = cc or []
    attachments = attachments or []
    check_type(variable=cc, variableName="cc", dtype=list, child=str)
    check_type(variable=attachments, variableName="attachments", dtype=list, child=str)

    # Read each attachment into memory once so the bytes can be shared safely
    # across the per-recipient requests. A shared open file handle would be
    # drained by the first request, leaving empty attachments for the rest.
    files = []
    for path in attachments:
        with open(path, 'rb') as fp:
            files.append(("attachments", (os.path.basename(path), fp.read())))

    datas = [{
        'subject': subject,
        'message': message,
        'email': email,
        'cc': cc,
        'files': files,
        'host': host,
        'api_key': api_key,
        'ssl_verify': ssl_verify,
        'timeout': timeout,
    } for email in emails]

    result = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(_send_mail, arg) for arg in datas]

        # Iterate over the future objects as they complete
        for future in concurrent.futures.as_completed(futures):
            result.append(future.result())
    return result
