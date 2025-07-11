"""
Production Monitoring for GlassDesk
Real-time monitoring and alerting for production systems
"""

import logging
import time
import psutil
import threading
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
from .user_communication import user_comm
from .logging_config import log_api_error
from .advanced_error_analysis import error_analyzer


class ProductionMonitor:
    """Production monitoring and alerting system"""

    def __init__(self):
        self.logger = logging.getLogger("glassdesk.monitor")
        self.metrics = defaultdict(list)
        self.alerts = []
        self.performance_thresholds = {
            "cpu_usage": 80.0,
            "memory_usage": 85.0,
            "response_time": 5.0,
            "error_rate": 5.0,
            "api_timeout": 10.0
        }
        self.security_thresholds = {
            "auth_failures": 10,
            "suspicious_requests": 5,
            "token_exposures": 1
        }
        self.monitoring_active = False
        self.user_comm = user_comm

    def start_monitoring(self):
        """Start continuous monitoring"""
        if self.monitoring_active:
            self.logger.warning("Monitoring already active")
            return

        self.monitoring_active = True
        self.logger.info("Starting production monitoring")

        # Start monitoring threads
        threading.Thread(target=self._monitor_system_resources, daemon=True).start()
        threading.Thread(target=self._monitor_application_health, daemon=True).start()
        threading.Thread(target=self._monitor_security_events, daemon=True).start()
        threading.Thread(target=self._monitor_user_experience, daemon=True).start()

    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.monitoring_active = False
        self.logger.info("Stopping production monitoring")

    def _monitor_system_resources(self):
        """Monitor system resource usage"""
        while self.monitoring_active:
            try:
                # CPU usage
                cpu_percent = psutil.cpu_percent(interval=1)
                self._record_metric("cpu_usage", cpu_percent)

                # Memory usage
                memory = psutil.virtual_memory()
                self._record_metric("memory_usage", memory.percent)

                # Disk usage
                disk = psutil.disk_usage('/')
                self._record_metric("disk_usage", (disk.used / disk.total) * 100)

                # Network I/O
                network = psutil.net_io_counters()
                self._record_metric("network_bytes_sent", network.bytes_sent)
                self._record_metric("network_bytes_recv", network.bytes_recv)

                # Check thresholds
                if cpu_percent > self.performance_thresholds["cpu_usage"]:
                    self._create_alert("high_cpu_usage", f"CPU usage at {cpu_percent}%")

                if memory.percent > self.performance_thresholds["memory_usage"]:
                    self._create_alert("high_memory_usage", f"Memory usage at {memory.percent}%")

                time.sleep(30)  # Check every 30 seconds

            except Exception as e:
                log_api_error("monitor_system_resources", e, {})
                time.sleep(60)  # Wait longer on error

    def _monitor_application_health(self):
        """Monitor application health metrics"""
        while self.monitoring_active:
            try:
                # Check database connectivity
                db_health = self._check_database_health()
                self._record_metric("database_health", 1 if db_health else 0)

                # Check API endpoints
                api_health = self._check_api_health()
                self._record_metric("api_health", 1 if api_health else 0)

                # Check OAuth tokens
                oauth_health = self._check_oauth_health()
                self._record_metric("oauth_health", 1 if oauth_health else 0)

                # Check error rates
                error_rate = self._calculate_error_rate()
                self._record_metric("error_rate", error_rate)

                if error_rate > self.performance_thresholds["error_rate"]:
                    self._create_alert("high_error_rate", f"Error rate at {error_rate}%")

                time.sleep(60)  # Check every minute

            except Exception as e:
                log_api_error("monitor_application_health", e, {})
                time.sleep(120)  # Wait longer on error

    def _monitor_security_events(self):
        """Monitor security-related events"""
        while self.monitoring_active:
            try:
                # Check for authentication failures
                auth_failures = self._count_auth_failures()
                self._record_metric("auth_failures", auth_failures)

                # Check for suspicious activity
                suspicious_activity = self._detect_suspicious_activity()
                self._record_metric("suspicious_activity", suspicious_activity)

                # Check for token exposures
                token_exposures = self._detect_token_exposures()
                self._record_metric("token_exposures", token_exposures)

                # Create security alerts
                if auth_failures > self.security_thresholds["auth_failures"]:
                    self._create_alert("high_auth_failures", f"{auth_failures} authentication failures")

                if suspicious_activity > self.security_thresholds["suspicious_requests"]:
                    self._create_alert("suspicious_activity", f"{suspicious_activity} suspicious requests detected")

                if token_exposures > self.security_thresholds["token_exposures"]:
                    self._create_alert("token_exposure", "CRITICAL: Token exposure detected")

                time.sleep(120)  # Check every 2 minutes

            except Exception as e:
                log_api_error("monitor_security_events", e, {})
                time.sleep(300)  # Wait longer on error

    def _monitor_user_experience(self):
        """Monitor user experience metrics"""
        while self.monitoring_active:
            try:
                # Response time monitoring
                response_time = self._measure_response_time()
                self._record_metric("response_time", response_time)

                # User interaction tracking
                user_interactions = self._count_user_interactions()
                self._record_metric("user_interactions", user_interactions)

                # Error message frequency
                error_messages = self._count_error_messages()
                self._record_metric("error_messages_shown", error_messages)

                # Timeout experiences
                timeout_experiences = self._count_timeout_experiences()
                self._record_metric("timeout_experiences", timeout_experiences)

                # Create UX alerts
                if response_time > self.performance_thresholds["response_time"]:
                    self._create_alert("slow_response_time", f"Response time at {response_time}s")

                if error_messages > 20:
                    self._create_alert("too_many_errors", f"{error_messages} error messages shown to users")

                if timeout_experiences > 5:
                    self._create_alert("timeout_experiences", f"{timeout_experiences} timeout experiences")

                time.sleep(60)  # Check every minute

            except Exception as e:
                log_api_error("monitor_user_experience", e, {})
                time.sleep(120)  # Wait longer on error

    def _check_database_health(self) -> bool:
        """Check database connectivity"""
        try:
            from database.database_schema import get_database_connection
            conn = get_database_connection()
            if conn:
                conn.close()
                return True
            return False
        except Exception as e:
            self.logger.error(f"Database health check failed: {str(e)}")
            return False

    def _check_api_health(self) -> bool:
        """Check API endpoint health"""
        try:
            # This would check actual API endpoints
            # For now, return True as placeholder
            return True
        except Exception as e:
            self.logger.error(f"API health check failed: {str(e)}")
            return False

    def _check_oauth_health(self) -> bool:
        """Check OAuth token health"""
        try:
            # This would check OAuth token validity
            # For now, return True as placeholder
            return True
        except Exception as e:
            self.logger.error(f"OAuth health check failed: {str(e)}")
            return False

    def _calculate_error_rate(self) -> float:
        """Calculate current error rate"""
        try:
            # Analyze recent logs for error rate
            analysis = error_analyzer.analyze_error_patterns()
            total_errors = sum(analysis.get("patterns", {}).get("api_errors", {}).values())
            total_requests = 100  # Placeholder - would be actual request count
            
            if total_requests > 0:
                return (total_errors / total_requests) * 100
            return 0.0
        except Exception as e:
            self.logger.error(f"Error rate calculation failed: {str(e)}")
            return 0.0

    def _count_auth_failures(self) -> int:
        """Count recent authentication failures"""
        try:
            analysis = error_analyzer.analyze_error_patterns()
            security_issues = analysis.get("patterns", {}).get("security_concerns", {})
            return security_issues.get("authentication_failures", 0)
        except Exception as e:
            self.logger.error(f"Auth failure count failed: {str(e)}")
            return 0

    def _detect_suspicious_activity(self) -> int:
        """Detect suspicious activity patterns"""
        try:
            analysis = error_analyzer.analyze_error_patterns()
            security_issues = analysis.get("patterns", {}).get("security_concerns", {})
            return security_issues.get("suspicious_activity", 0)
        except Exception as e:
            self.logger.error(f"Suspicious activity detection failed: {str(e)}")
            return 0

    def _detect_token_exposures(self) -> int:
        """Detect potential token exposures"""
        try:
            analysis = error_analyzer.analyze_error_patterns()
            security_issues = analysis.get("patterns", {}).get("security_concerns", {})
            return security_issues.get("token_leaks", 0)
        except Exception as e:
            self.logger.error(f"Token exposure detection failed: {str(e)}")
            return 0

    def _measure_response_time(self) -> float:
        """Measure average response time"""
        try:
            # This would measure actual response times
            # For now, return a placeholder value
            return 1.5  # seconds
        except Exception as e:
            self.logger.error(f"Response time measurement failed: {str(e)}")
            return 0.0

    def _count_user_interactions(self) -> int:
        """Count recent user interactions"""
        try:
            # This would count actual user interactions
            # For now, return a placeholder value
            return 25
        except Exception as e:
            self.logger.error(f"User interaction count failed: {str(e)}")
            return 0

    def _count_error_messages(self) -> int:
        """Count error messages shown to users"""
        try:
            analysis = error_analyzer.analyze_error_patterns()
            ux_issues = analysis.get("patterns", {}).get("user_experience_issues", {})
            return ux_issues.get("error_messages_shown", 0)
        except Exception as e:
            self.logger.error(f"Error message count failed: {str(e)}")
            return 0

    def _count_timeout_experiences(self) -> int:
        """Count timeout experiences"""
        try:
            analysis = error_analyzer.analyze_error_patterns()
            ux_issues = analysis.get("patterns", {}).get("user_experience_issues", {})
            return ux_issues.get("timeout_experiences", 0)
        except Exception as e:
            self.logger.error(f"Timeout experience count failed: {str(e)}")
            return 0

    def _record_metric(self, metric_name: str, value: float):
        """Record a metric with timestamp"""
        timestamp = datetime.now()
        self.metrics[metric_name].append({
            "value": value,
            "timestamp": timestamp,
            "timestamp_str": timestamp.isoformat()
        })

        # Keep only last 1000 measurements per metric
        if len(self.metrics[metric_name]) > 1000:
            self.metrics[metric_name] = self.metrics[metric_name][-1000:]

    def _create_alert(self, alert_type: str, message: str):
        """Create and log an alert"""
        alert = {
            "type": alert_type,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "severity": self._determine_severity(alert_type)
        }

        self.alerts.append(alert)
        self.logger.warning(f"ALERT: {alert_type} - {message}")

        # Notify user for critical alerts
        if alert["severity"] == "critical":
            self.user_comm.notify_user(f"System alert: {message}", "warning")

        # Keep only last 100 alerts
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]

    def _determine_severity(self, alert_type: str) -> str:
        """Determine alert severity"""
        critical_alerts = ["token_exposure", "security_breach", "system_failure"]
        warning_alerts = ["high_cpu_usage", "high_memory_usage", "high_error_rate"]
        
        if alert_type in critical_alerts:
            return "critical"
        elif alert_type in warning_alerts:
            return "warning"
        else:
            return "info"

    def get_monitoring_summary(self) -> Dict[str, Any]:
        """Get a summary of current monitoring status"""
        try:
            # Calculate current metrics
            current_metrics = {}
            for metric_name, measurements in self.metrics.items():
                if measurements:
                    current_metrics[metric_name] = measurements[-1]["value"]

            # Get recent alerts
            recent_alerts = self.alerts[-10:] if self.alerts else []

            # Get system status
            system_status = {
                "cpu_usage": psutil.cpu_percent(),
                "memory_usage": psutil.virtual_memory().percent,
                "disk_usage": (psutil.disk_usage('/').used / psutil.disk_usage('/').total) * 100
            }

            return {
                "monitoring_active": self.monitoring_active,
                "current_metrics": current_metrics,
                "recent_alerts": recent_alerts,
                "system_status": system_status,
                "performance_thresholds": self.performance_thresholds,
                "security_thresholds": self.security_thresholds,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            log_api_error("get_monitoring_summary", e, {})
            return {"error": f"Monitoring summary failed: {str(e)}"}

    def get_performance_report(self) -> Dict[str, Any]:
        """Get a detailed performance report"""
        try:
            # Calculate performance metrics
            performance_data = {}
            for metric_name, measurements in self.metrics.items():
                if measurements:
                    values = [m["value"] for m in measurements[-100:]]  # Last 100 measurements
                    performance_data[metric_name] = {
                        "current": values[-1] if values else 0,
                        "average": sum(values) / len(values) if values else 0,
                        "min": min(values) if values else 0,
                        "max": max(values) if values else 0,
                        "trend": "increasing" if len(values) > 1 and values[-1] > values[-2] else "stable"
                    }

            return {
                "performance_metrics": performance_data,
                "alerts_summary": {
                    "total_alerts": len(self.alerts),
                    "critical_alerts": len([a for a in self.alerts if a["severity"] == "critical"]),
                    "warning_alerts": len([a for a in self.alerts if a["severity"] == "warning"]),
                    "info_alerts": len([a for a in self.alerts if a["severity"] == "info"])
                },
                "recommendations": self._generate_performance_recommendations(performance_data),
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            log_api_error("get_performance_report", e, {})
            return {"error": f"Performance report failed: {str(e)}"}

    def _generate_performance_recommendations(self, performance_data: Dict[str, Any]) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []

        # CPU recommendations
        cpu_data = performance_data.get("cpu_usage", {})
        if cpu_data.get("current", 0) > 70:
            recommendations.append("High CPU usage detected - consider optimizing resource-intensive operations")

        # Memory recommendations
        memory_data = performance_data.get("memory_usage", {})
        if memory_data.get("current", 0) > 80:
            recommendations.append("High memory usage detected - consider implementing memory cleanup")

        # Response time recommendations
        response_data = performance_data.get("response_time", {})
        if response_data.get("current", 0) > 3:
            recommendations.append("Slow response times detected - optimize API calls and database queries")

        # Error rate recommendations
        error_data = performance_data.get("error_rate", {})
        if error_data.get("current", 0) > 5:
            recommendations.append("High error rate detected - review error handling and API integrations")

        return recommendations


# Global production monitor instance
production_monitor = ProductionMonitor() 