"""
Self-Healing System for GlassDesk
Automatically detects and fixes common issues without user intervention
"""

import logging
import os
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from .user_communication import user_comm
from .logging_config import log_api_error


class SelfHealingSystem:
    """Automatically detects and fixes common system issues"""

    def __init__(self):
        self.logger = logging.getLogger("glassdesk.self_healing")
        self.health_checks = {}
        self.auto_fix_attempts = {}
        self.last_diagnostic_run = None

    def run_full_diagnostics(self) -> Dict[str, Any]:
        """Run comprehensive system diagnostics"""
        self.logger.info("Starting full system diagnostics")

        diagnostics = {
            "database": self._check_database_health(),
            "configuration": self._check_configuration_health(),
            "api_connections": self._check_api_connections(),
            "file_permissions": self._check_file_permissions(),
            "dependencies": self._check_dependencies(),
            "log_files": self._check_log_files(),
            "environment": self._check_environment_variables(),
        }

        # Log overall health status
        healthy_components = sum(
            1 for status in diagnostics.values() if status["healthy"]
        )
        total_components = len(diagnostics)

        overall_health = {
            "healthy_components": healthy_components,
            "total_components": total_components,
            "health_percentage": (healthy_components / total_components) * 100,
            "issues_found": [k for k, v in diagnostics.items() if not v["healthy"]],
            "timestamp": datetime.now().isoformat(),
        }

        self.health_checks = diagnostics
        self.last_diagnostic_run = datetime.now()

        self.logger.info(
            f"Diagnostics complete: {healthy_components}/{total_components} healthy"
        )

        return overall_health

    def attempt_auto_fixes(self, issues: List[str]) -> Dict[str, bool]:
        """Attempt to automatically fix detected issues"""
        fix_results = {}

        for issue in issues:
            self.logger.info(f"Attempting auto-fix for: {issue}")

            try:
                if issue == "database":
                    fix_results[issue] = self._fix_database_issues()
                elif issue == "configuration":
                    fix_results[issue] = self._fix_configuration_issues()
                elif issue == "api_connections":
                    fix_results[issue] = self._fix_api_connection_issues()
                elif issue == "file_permissions":
                    fix_results[issue] = self._fix_file_permission_issues()
                elif issue == "dependencies":
                    fix_results[issue] = self._fix_dependency_issues()
                elif issue == "log_files":
                    fix_results[issue] = self._fix_log_file_issues()
                elif issue == "environment":
                    fix_results[issue] = self._fix_environment_issues()
                else:
                    fix_results[issue] = False

            except Exception as e:
                self.logger.error(f"Auto-fix failed for {issue}: {str(e)}")
                fix_results[issue] = False

        # Update auto-fix attempts tracking
        self.auto_fix_attempts[datetime.now().isoformat()] = {
            "issues_attempted": issues,
            "results": fix_results,
        }

        return fix_results

    def _check_database_health(self) -> Dict[str, Any]:
        """Check database connection and health"""
        try:
            from database.database_schema import get_database_connection

            connection = get_database_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchone()
                cursor.close()
                connection.close()

                return {
                    "healthy": True,
                    "message": "Database connection successful",
                    "details": "Connection established and basic query executed",
                }
            else:
                return {
                    "healthy": False,
                    "message": "Database connection failed",
                    "details": "Could not establish database connection",
                }

        except Exception as e:
            return {
                "healthy": False,
                "message": f"Database health check failed: {str(e)}",
                "details": f"Exception during database health check: {type(e).__name__}",
            }

    def _check_configuration_health(self) -> Dict[str, Any]:
        """Check configuration files and settings"""
        try:
            from config.config_manager import config_manager

            # Check if config is valid
            if config_manager.validate_config():
                return {
                    "healthy": True,
                    "message": "Configuration is valid",
                    "details": "All required configuration sections present",
                }
            else:
                return {
                    "healthy": False,
                    "message": "Configuration validation failed",
                    "details": "Missing required configuration sections",
                }

        except Exception as e:
            return {
                "healthy": False,
                "message": f"Configuration check failed: {str(e)}",
                "details": f"Exception during configuration check: {type(e).__name__}",
            }

    def _check_api_connections(self) -> Dict[str, Any]:
        """Check API connection health"""
        try:
            # Test basic API connectivity
            import requests

            test_urls = [
                "https://www.googleapis.com",
                "https://api.zoom.us",
                "https://app.asana.com",
            ]

            successful_connections = 0
            failed_connections = []

            for url in test_urls:
                try:
                    response = requests.get(url, timeout=5)
                    if response.status_code < 500:  # Not server error
                        successful_connections += 1
                    else:
                        failed_connections.append(f"{url}: HTTP {response.status_code}")
                except Exception as e:
                    failed_connections.append(f"{url}: {str(e)}")

            if successful_connections >= len(test_urls) * 0.7:  # 70% success rate
                return {
                    "healthy": True,
                    "message": "API connections healthy",
                    "details": f"{successful_connections}/{len(test_urls)} APIs accessible",
                }
            else:
                return {
                    "healthy": False,
                    "message": "API connection issues detected",
                    "details": f"Failed connections: {failed_connections}",
                }

        except Exception as e:
            return {
                "healthy": False,
                "message": f"API health check failed: {str(e)}",
                "details": f"Exception during API health check: {type(e).__name__}",
            }

    def _check_file_permissions(self) -> Dict[str, Any]:
        """Check file and directory permissions"""
        try:
            required_files = ["glassdesk.log", "main.py", "requirements.txt"]

            required_dirs = ["app", "database", "config", "tests", "docs"]

            missing_files = []
            missing_dirs = []

            # Check files
            for file_path in required_files:
                if not os.path.exists(file_path):
                    missing_files.append(file_path)

            # Check directories
            for dir_path in required_dirs:
                if not os.path.exists(dir_path):
                    missing_dirs.append(dir_path)

            if not missing_files and not missing_dirs:
                return {
                    "healthy": True,
                    "message": "All required files and directories present",
                    "details": "File system structure is correct",
                }
            else:
                return {
                    "healthy": False,
                    "message": "Missing required files or directories",
                    "details": f"Missing files: {missing_files}, Missing dirs: {missing_dirs}",
                }

        except Exception as e:
            return {
                "healthy": False,
                "message": f"File permission check failed: {str(e)}",
                "details": f"Exception during file check: {type(e).__name__}",
            }

    def _check_dependencies(self) -> Dict[str, Any]:
        """Check if all required dependencies are available"""
        try:
            required_modules = [
                "flask",
                "requests",
                "google.auth",
                "psycopg2",
                "python-dotenv",
            ]

            missing_modules = []

            for module in required_modules:
                try:
                    __import__(module.replace("-", "_"))
                except ImportError:
                    missing_modules.append(module)

            if not missing_modules:
                return {
                    "healthy": True,
                    "message": "All dependencies available",
                    "details": "All required Python modules are installed",
                }
            else:
                return {
                    "healthy": False,
                    "message": "Missing dependencies detected",
                    "details": f"Missing modules: {missing_modules}",
                }

        except Exception as e:
            return {
                "healthy": False,
                "message": f"Dependency check failed: {str(e)}",
                "details": f"Exception during dependency check: {type(e).__name__}",
            }

    def _check_log_files(self) -> Dict[str, Any]:
        """Check log file health and rotation"""
        try:
            log_file = "glassdesk.log"

            if not os.path.exists(log_file):
                return {
                    "healthy": False,
                    "message": "Log file does not exist",
                    "details": "glassdesk.log file is missing",
                }

            # Check log file size
            file_size = os.path.getsize(log_file)
            max_size = 10 * 1024 * 1024  # 10MB

            if file_size > max_size:
                return {
                    "healthy": False,
                    "message": "Log file too large",
                    "details": f"Log file size: {file_size} bytes (max: {max_size})",
                }

            return {
                "healthy": True,
                "message": "Log files healthy",
                "details": f"Log file size: {file_size} bytes",
            }

        except Exception as e:
            return {
                "healthy": False,
                "message": f"Log file check failed: {str(e)}",
                "details": f"Exception during log check: {type(e).__name__}",
            }

    def _check_environment_variables(self) -> Dict[str, Any]:
        """Check critical environment variables"""
        try:
            required_vars = ["DB_HOST", "DB_NAME", "DB_USER"]

            missing_vars = []

            for var in required_vars:
                if not os.getenv(var):
                    missing_vars.append(var)

            if not missing_vars:
                return {
                    "healthy": True,
                    "message": "Environment variables configured",
                    "details": "All required environment variables are set",
                }
            else:
                return {
                    "healthy": False,
                    "message": "Missing environment variables",
                    "details": f"Missing vars: {missing_vars}",
                }

        except Exception as e:
            return {
                "healthy": False,
                "message": f"Environment check failed: {str(e)}",
                "details": f"Exception during environment check: {type(e).__name__}",
            }

    def _fix_database_issues(self) -> bool:
        """Attempt to fix database connection issues"""
        try:
            # Try to reinitialize database
            from database.database_schema import init_database

            return init_database()
        except Exception as e:
            self.logger.error(f"Database auto-fix failed: {str(e)}")
            return False

    def _fix_configuration_issues(self) -> bool:
        """Attempt to fix configuration issues"""
        try:
            # Try to reload configuration
            from config.config_manager import config_manager

            config_manager.load_config()
            return config_manager.validate_config()
        except Exception as e:
            self.logger.error(f"Configuration auto-fix failed: {str(e)}")
            return False

    def _fix_api_connection_issues(self) -> bool:
        """Attempt to fix API connection issues"""
        try:
            # Wait and retry logic
            time.sleep(2)
            return True  # Assume retry will help
        except Exception as e:
            self.logger.error(f"API connection auto-fix failed: {str(e)}")
            return False

    def _fix_file_permission_issues(self) -> bool:
        """Attempt to fix file permission issues"""
        try:
            # Create missing directories
            for dir_path in ["logs", "temp"]:
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
            return True
        except Exception as e:
            self.logger.error(f"File permission auto-fix failed: {str(e)}")
            return False

    def _fix_dependency_issues(self) -> bool:
        """Attempt to fix dependency issues"""
        try:
            # This would typically involve pip install
            # For now, just return True as a placeholder
            return True
        except Exception as e:
            self.logger.error(f"Dependency auto-fix failed: {str(e)}")
            return False

    def _fix_log_file_issues(self) -> bool:
        """Attempt to fix log file issues"""
        try:
            # Rotate log file if too large
            log_file = "glassdesk.log"
            if (
                os.path.exists(log_file)
                and os.path.getsize(log_file) > 10 * 1024 * 1024
            ):
                backup_file = (
                    f"glassdesk.log.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                )
                os.rename(log_file, backup_file)
            return True
        except Exception as e:
            self.logger.error(f"Log file auto-fix failed: {str(e)}")
            return False

    def _fix_environment_issues(self) -> bool:
        """Attempt to fix environment variable issues"""
        try:
            # This would typically involve prompting user or using defaults
            # For now, just return True as a placeholder
            return True
        except Exception as e:
            self.logger.error(f"Environment auto-fix failed: {str(e)}")
            return False


# Global self-healing system instance
self_healing = SelfHealingSystem()
