"""Tests for database functionality."""

from unittest.mock import MagicMock, patch

from sqlmodel import SQLModel

from app.core import db


class TestInitDb:
    """Test class for init_db function."""

    def test_init_db_creates_tables(self):
        """Test that init_db calls SQLModel.metadata.create_all."""
        with patch.object(SQLModel.metadata, 'create_all') as mock_create_all:
            # pass a dummy session object because the function signature requires it
            db.init_db(MagicMock())
            mock_create_all.assert_called_once()

    def test_init_db_in_testing_mode(self):
        """Test init_db works in testing mode."""
        # Patch settings to simulate testing mode and assert drop_all + create_all
        from unittest.mock import MagicMock as _MM
        with patch('app.core.config.settings', new=_MM(TESTING=True)):
            with patch.object(SQLModel.metadata, 'drop_all') as mock_drop_all, \
                 patch.object(SQLModel.metadata, 'create_all') as mock_create_all:
                db.init_db(MagicMock())
                mock_drop_all.assert_called_once()
                mock_create_all.assert_called_once()
