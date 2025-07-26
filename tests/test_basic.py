"""
Basic tests for Crystal HR Automation package.
"""
import os
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from rajnish_dc_crystal.core import CrystalHRAutomation
from rajnish_dc_crystal.emailer import EmailNotifier
from rajnish_dc_crystal.config import load_config, create_default_config, get_default_config_path

def test_email_notifier_initialization():
    """Test EmailNotifier initialization."""
    notifier = EmailNotifier(
        gmail_user="test@example.com",
        gmail_app_password="testpass",
        recipient_email="recipient@example.com"
    )
    
    assert notifier.gmail_user == "test@example.com"
    assert notifier.gmail_app_password == "testpass"
    assert notifier.recipient_email == "recipient@example.com"

@patch('smtplib.SMTP')
def test_email_send_success(mock_smtp):
    """Test successful email sending."""
    notifier = EmailNotifier(
        gmail_user="test@example.com",
        gmail_app_password="testpass",
        recipient_email="recipient@example.com"
    )
    
    # Mock SMTP server
    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server
    
    # Test sending email
    result = notifier.send_email("Test Subject", "Test Body")
    
    assert result is True
    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once_with("test@example.com", "testpass")
    assert mock_server.send_message.called

def test_config_default_path():
    """Test default config path generation."""
    path = get_default_config_path()
    assert ".config/crystal_hr/config.json" in str(path)

def test_create_default_config(tmp_path):
    """Test creation of default config file."""
    
    # Create a temporary config file path
    config_path = tmp_path / "config.json"
    
    # Create default config
    config = create_default_config(config_path)
    
    # Check if file was created
    assert config_path.exists()
    
    # Check if config has expected structure
    assert "hr_system" in config
    assert "email" in config
    assert "behavior" in config
    assert "username" in config["hr_system"]

@patch('rajnish_dc_crystal.core.requests.Session')
def test_crystal_hr_login_success(mock_session):
    """Test successful login to Crystal HR."""
    # Setup mock session
    mock_response = MagicMock()
    mock_response.text = "Welcome, Test User"
    mock_session.return_value.post.return_value = mock_response
    
    # Initialize and test login
    hr = CrystalHRAutomation()
    result = hr.login("testuser", "testpass")
    
    assert result is True
    assert hr.logged_in is True

@patch('rajnish_dc_crystal.core.requests.Session')
def test_crystal_hr_punch_in(mock_session):
    """Test punch in functionality."""
    # Setup mock session
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"msg": "Success: Punch In recorded"}
    mock_session.return_value.post.return_value = mock_response
    
    # Initialize and test punch in
    hr = CrystalHRAutomation()
    hr.logged_in = True  # Pretend we're logged in
    result = hr.punch("in")
    
    assert result is True

if __name__ == "__main__":
    pytest.main(["-v", "test_basic.py"])
