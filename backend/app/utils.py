import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import emails  # type: ignore
from jinja2 import Template

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class EmailData:
    html_content: str
    subject: str


def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
    template_str = (
        Path(__file__).parent / "email-templates" / "build" / template_name
    ).read_text()
    html_content = Template(template_str).render(context)
    return html_content


def send_email(
    *,
    email_to: str,
    subject: str = "",
    html_content: str = "",
) -> None:
    # Email sending has been archived. In active mode we perform a safe no-op
    # so code that calls `send_email` (e.g. admin test-email endpoint) does not
    # fail in environments without SMTP configuration.
    logger.info(
        "(archived) send_email called — no-op in active code. Subject=%s to=%s",
        subject,
        email_to,
    )



def generate_reset_password_email(email_to: str, email: str, token: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email} (archived)"
    link = f"{settings.FRONTEND_HOST}/reset-password?token={token}"
    html_content = f"<p>Reset link (demo): <a href=\"{link}\">{link}</a></p>"
    return EmailData(html_content=html_content, subject=subject)


def generate_new_account_email(
    email_to: str, username: str, password: str
) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username} (archived)"
    html_content = f"<p>User: {username}<br/>Password: {password}</p>"
    return EmailData(html_content=html_content, subject=subject)


def generate_password_reset_token(email: str) -> str:
    # Produce a simple demo token that can be verified by `verify_password_reset_token`.
    return f"demo-token:{email}"


def verify_password_reset_token(token: str) -> str | None:
    if isinstance(token, str) and token.startswith("demo-token:"):
        return token.split("demo-token:", 1)[1]
    return None
