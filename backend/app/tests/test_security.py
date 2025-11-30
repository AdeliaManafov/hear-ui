"""Tests for core security functions (password hashing)."""

import pytest
from app.core.security import get_password_hash, verify_password


class TestPasswordHashing:
    """Test password hashing and verification."""

    def test_get_password_hash_returns_string(self):
        """Test that hashing returns a string."""
        password = "test_password_123"
        hashed = get_password_hash(password)
        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_get_password_hash_creates_unique_hashes(self):
        """Test that same password creates different hashes (due to salt)."""
        password = "same_password"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        # bcrypt uses random salt, so hashes should differ
        assert hash1 != hash2

    def test_verify_password_correct(self):
        """Test that correct password verifies successfully."""
        password = "correct_password"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test that incorrect password fails verification."""
        password = "correct_password"
        wrong_password = "wrong_password"
        hashed = get_password_hash(password)
        assert verify_password(wrong_password, hashed) is False

    def test_verify_password_empty_password(self):
        """Test verification with empty password."""
        password = ""
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True
        assert verify_password("not_empty", hashed) is False

    def test_hash_special_characters(self):
        """Test hashing password with special characters."""
        password = "P@$$w0rd!#%&*()[]{}äöü"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True

    def test_hash_long_password(self):
        """Test hashing a very long password."""
        password = "a" * 1000
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True
