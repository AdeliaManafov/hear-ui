"""Tests for utility functions."""

from app.utils import (
    EmailData,
    generate_new_account_email,
    generate_password_reset_token,
    generate_reset_password_email,
    send_email,
    verify_password_reset_token,
)


class TestEmailData:
    """Tests for EmailData dataclass."""

    def test_email_data_creation(self):
        """Test EmailData can be created."""
        email = EmailData(html_content="<p>Test</p>", subject="Test Subject")

        assert email.html_content == "<p>Test</p>"
        assert email.subject == "Test Subject"


class TestGenerateResetPasswordEmail:
    """Tests for generate_reset_password_email function."""

    def test_generates_email_data(self):
        """Test it returns EmailData."""
        result = generate_reset_password_email(
            email_to="user@example.com",
            email="user@example.com",
            token="test-token-123",
        )

        assert isinstance(result, EmailData)
        assert "Password recovery" in result.subject
        assert "test-token-123" in result.html_content

    def test_includes_project_name_in_subject(self):
        """Test subject includes project name."""
        result = generate_reset_password_email(
            email_to="test@test.com",
            email="test@test.com",
            token="abc",
        )

        # Subject should contain some project name
        assert len(result.subject) > 0


class TestGenerateNewAccountEmail:
    """Tests for generate_new_account_email function."""

    def test_generates_email_data(self):
        """Test it returns EmailData."""
        result = generate_new_account_email(
            email_to="new@example.com",
            username="newuser",
            password="secret123",
        )

        assert isinstance(result, EmailData)
        assert "newuser" in result.html_content
        assert "secret123" in result.html_content

    def test_includes_username_in_subject(self):
        """Test subject mentions username."""
        result = generate_new_account_email(
            email_to="test@test.com",
            username="testuser",
            password="pass",
        )

        assert "testuser" in result.subject


class TestPasswordResetToken:
    """Tests for password reset token functions."""

    def test_generate_token(self):
        """Test generating a reset token."""
        token = generate_password_reset_token("user@example.com")

        assert isinstance(token, str)
        assert len(token) > 0
        assert "user@example.com" in token

    def test_verify_valid_token(self):
        """Test verifying a valid token."""
        email = "test@example.com"
        token = generate_password_reset_token(email)

        result = verify_password_reset_token(token)

        assert result == email

    def test_verify_invalid_token(self):
        """Test verifying an invalid token returns None."""
        result = verify_password_reset_token("invalid-token")
        assert result is None

    def test_verify_empty_token(self):
        """Test verifying empty token."""
        result = verify_password_reset_token("")
        assert result is None

    def test_verify_none_like_token(self):
        """Test with various invalid inputs."""
        assert verify_password_reset_token("random-string") is None
        assert verify_password_reset_token("demo-token:") == ""


class TestSendEmail:
    """Tests for send_email function."""

    def test_send_email_no_op(self):
        """Test send_email runs without error (archived/no-op)."""
        # Should not raise
        send_email(
            email_to="test@example.com",
            subject="Test",
            html_content="<p>Test</p>",
        )

    def test_send_email_with_empty_values(self):
        """Test send_email with empty values."""
        send_email(email_to="", subject="", html_content="")
