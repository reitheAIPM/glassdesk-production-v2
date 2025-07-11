"""
Configuration management for GlassDesk
Handles loading of environment variables and JSON configuration files
"""

import os
import json
import logging
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ConfigManager:
    """Manages application configuration from environment variables and JSON files"""
    
    def __init__(self, config_file_path: str = None):
        self.config_file_path = config_file_path or "config/config_example.json"
        self.config = {}
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from JSON file and environment variables"""
        try:
            # Load JSON configuration
            if os.path.exists(self.config_file_path):
                with open(self.config_file_path, 'r') as f:
                    self.config = json.load(f)
                logging.info(f"Configuration loaded from {self.config_file_path}")
            else:
                logging.warning(f"Config file {self.config_file_path} not found, using defaults")
                self.config = self.get_default_config()
            
            # Override with environment variables
            self._load_env_overrides()
            
        except Exception as e:
            logging.error(f"Error loading configuration: {str(e)}")
            self.config = self.get_default_config()
    
    def _load_env_overrides(self) -> None:
        """Override config with environment variables"""
        env_mappings = {
            'GOOGLE_CLIENT_ID': ('gmail', 'client_id'),
            'GOOGLE_CLIENT_SECRET': ('gmail', 'client_secret'),
            'ZOOM_JWT_TOKEN': ('zoom', 'jwt_token'),
            'ZOOM_API_KEY': ('zoom', 'api_key'),
            'ZOOM_API_SECRET': ('zoom', 'api_secret'),
            'ASANA_PAT': ('asana', 'personal_access_token'),
        }
        
        for env_var, config_path in env_mappings.items():
            env_value = os.getenv(env_var)
            if env_value:
                section, key = config_path
                if section not in self.config:
                    self.config[section] = {}
                self.config[section][key] = env_value
    
    def get_default_config(self) -> Dict[str, Any]:
        """Return default configuration structure"""
        return {
            'development': {
                'use_mock_data': True,
                'mock_data_path': './mock_data/'
            },
            'gmail': {
                'client_id': 'YOUR_GOOGLE_CLIENT_ID',
                'client_secret': 'YOUR_GOOGLE_CLIENT_SECRET',
                'redirect_uri': 'http://localhost:5000/oauth2callback'
            },
            'zoom': {
                'jwt_token': 'YOUR_ZOOM_JWT_TOKEN',
                'api_key': 'YOUR_ZOOM_API_KEY',
                'api_secret': 'YOUR_ZOOM_API_SECRET'
            },
            'asana': {
                'personal_access_token': 'YOUR_ASANA_PAT'
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (supports nested keys like 'gmail.client_id')"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """Get entire configuration section"""
        return self.config.get(section, {})
    
    def validate_config(self) -> bool:
        """Validate that required configuration is present"""
        required_sections = ['gmail', 'zoom', 'asana']
        
        for section in required_sections:
            if section not in self.config:
                logging.error(f"Missing required configuration section: {section}")
                return False
        
        return True
    
    def should_use_mock_data(self) -> bool:
        """Check if mock data should be used based on configuration"""
        # Check environment variable first
        env_mock_data = os.getenv('USE_MOCK_DATA', '').lower()
        if env_mock_data in ['true', '1', 'yes']:
            return True
        elif env_mock_data in ['false', '0', 'no']:
            return False
        
        # Fall back to config file setting
        return self.get('development.use_mock_data', True)
    
    def get_mock_data_path(self) -> str:
        """Get the path to mock data directory"""
        return self.get('development.mock_data_path', './mock_data/')

# Global config instance
config_manager = ConfigManager() 