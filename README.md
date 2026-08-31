# mpt-email-client

A tiny Python client for sending email (with optional file attachments) through the MPT email service.

## Install
```bash
pip install mptemail
```

## Configuration
Credentials can be passed per call or set once via environment variables (read at import time):

| env var            | description               |
| ------------------ | ------------------------- |
| `MPT_EMAIL_URI`    | email server uri          |
| `MPT_EMAIL_APIKEY` | api key for the service   |

```bash
export MPT_EMAIL_URI="https://email-service.xxx.com"
export MPT_EMAIL_APIKEY="<API_KEY>"
```

> Set at runtime after import? Pass `host` / `api_key` explicitly instead.

## Usage

```python
import mptemail

status = mptemail.sendEmail(
    subject="test",
    message="helloworld",
    emails=["admin@admin.com"],
    cc=["cc@admin.com"],
    attachments=["test.txt"],
    host="https://email-service.xxx.com",
    api_key="<API_KEY>",
    ssl_verify=False,
)
print(status)
```

### Parameters

| parameter   | type      | default             | description                                 |
| ----------- | --------- | ------------------- | ------------------------------------------- |
| subject     | str       | —                   | subject of the email                        |
| message     | str       | —                   | email body, may contain HTML                |
| emails      | List[str] | —                   | recipients (one request per email)          |
| cc          | List[str] | `[]`                | cc recipients                               |
| attachments | List[str] | `[]`                | file paths to attach                        |
| host        | str       | `$MPT_EMAIL_URI`    | email server uri                            |
| api_key     | str       | `$MPT_EMAIL_APIKEY` | api key for the email service               |
| ssl_verify  | bool      | `True`              | verify the server's TLS certificate         |
| timeout     | int       | `30`                | per-request timeout, in seconds             |

`subject`, `message`, and `emails` are required.

## Output

`sendEmail` returns a list of `(success, message)` tuples — one per recipient (order is not guaranteed):

```python
[(True, 'email sent to admin@admin.com successfully')]
```

- **success** — `True` when the server accepted the email (HTTP `201`), otherwise `False`.
- **message** — a string describing the result, or the server's error payload on failure.

## Airflow helpers

`mptemail.utils.airflow_email` builds Airflow alert emails ready to hand to `sendEmail`:

```python
from mptemail.utils.airflow_email import create_notice_email, create_success_email

subject, body = create_notice_email(site_name="prod", context=context)     # task-failure email (with logs)
subject, body = create_success_email(site_name="prod", context=context)    # task-success email
```
