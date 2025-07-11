"""
Advanced Error Analysis for GlassDesk
AI-powered error pattern detection and analysis
"""

import logging
import json
import re
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from .user_communication import user_comm
from .logging_config import log_api_error


class AdvancedErrorAnalyzer:
    """AI-powered error analysis and pattern detection"""

    def __init__(self):
        self.logger = logging.getLogger("glassdesk.error_analyzer")
        self.error_patterns = defaultdict(list)
        self.error_frequencies = Counter()
        self.performance_metrics = {}
        self.security_incidents = []
        self.user_comm = user_comm

    def analyze_error_patterns(self, log_file: str = "glassdesk.log") -> Dict[str, Any]:
        """Analyze error patterns from log files"""
        try:
            self.logger.info("Starting advanced error pattern analysis")
            
            patterns = {
                "oauth_errors": self._detect_oauth_patterns(log_file),
                "api_errors": self._detect_api_patterns(log_file),
                "database_errors": self._detect_database_patterns(log_file),
                "performance_issues": self._detect_performance_issues(log_file),
                "security_concerns": self._detect_security_issues(log_file),
                "user_experience_issues": self._detect_ux_issues(log_file)
            }
            
            # Generate insights
            insights = self._generate_error_insights(patterns)
            
            # Update error frequencies
            self._update_error_frequencies(patterns)
            
            return {
                "patterns": patterns,
                "insights": insights,
                "recommendations": self._generate_recommendations(patterns),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            log_api_error("analyze_error_patterns", e, {"log_file": log_file})
            return {"error": f"Analysis failed: {str(e)}"}

    def _detect_oauth_patterns(self, log_file: str) -> Dict[str, Any]:
        """Detect OAuth-related error patterns"""
        patterns = {
            "token_expirations": 0,
            "invalid_grants": 0,
            "permission_denied": 0,
            "rate_limiting": 0,
            "connection_failures": 0
        }
        
        try:
            with open(log_file, 'r') as f:
                for line in f:
                    if "oauth" in line.lower() or "token" in line.lower():
                        if "expired" in line.lower() or "invalid_grant" in line.lower():
                            patterns["token_expirations"] += 1
                        elif "permission" in line.lower() or "denied" in line.lower():
                            patterns["permission_denied"] += 1
                        elif "rate" in line.lower() or "429" in line:
                            patterns["rate_limiting"] += 1
                        elif "connection" in line.lower():
                            patterns["connection_failures"] += 1
        except FileNotFoundError:
            self.logger.warning(f"Log file {log_file} not found")
            
        return patterns

    def _detect_api_patterns(self, log_file: str) -> Dict[str, Any]:
        """Detect API-related error patterns"""
        patterns = {
            "timeout_errors": 0,
            "server_errors": 0,
            "client_errors": 0,
            "network_errors": 0,
            "malformed_responses": 0
        }
        
        try:
            with open(log_file, 'r') as f:
                for line in f:
                    if "api" in line.lower():
                        if "timeout" in line.lower():
                            patterns["timeout_errors"] += 1
                        elif "500" in line or "server" in line.lower():
                            patterns["server_errors"] += 1
                        elif "400" in line or "client" in line.lower():
                            patterns["client_errors"] += 1
                        elif "network" in line.lower():
                            patterns["network_errors"] += 1
                        elif "json" in line.lower() or "malformed" in line.lower():
                            patterns["malformed_responses"] += 1
        except FileNotFoundError:
            self.logger.warning(f"Log file {log_file} not found")
            
        return patterns

    def _detect_database_patterns(self, log_file: str) -> Dict[str, Any]:
        """Detect database-related error patterns"""
        patterns = {
            "connection_failures": 0,
            "timeout_errors": 0,
            "permission_errors": 0,
            "constraint_violations": 0,
            "deadlock_errors": 0
        }
        
        try:
            with open(log_file, 'r') as f:
                for line in f:
                    if "database" in line.lower() or "db" in line.lower():
                        if "connection" in line.lower():
                            patterns["connection_failures"] += 1
                        elif "timeout" in line.lower():
                            patterns["timeout_errors"] += 1
                        elif "permission" in line.lower():
                            patterns["permission_errors"] += 1
                        elif "constraint" in line.lower():
                            patterns["constraint_violations"] += 1
                        elif "deadlock" in line.lower():
                            patterns["deadlock_errors"] += 1
        except FileNotFoundError:
            self.logger.warning(f"Log file {log_file} not found")
            
        return patterns

    def _detect_performance_issues(self, log_file: str) -> Dict[str, Any]:
        """Detect performance-related issues"""
        issues = {
            "slow_queries": 0,
            "memory_usage": 0,
            "cpu_usage": 0,
            "response_time_issues": 0,
            "resource_exhaustion": 0
        }
        
        try:
            with open(log_file, 'r') as f:
                for line in f:
                    if "performance" in line.lower() or "slow" in line.lower():
                        if "query" in line.lower():
                            issues["slow_queries"] += 1
                        elif "memory" in line.lower():
                            issues["memory_usage"] += 1
                        elif "cpu" in line.lower():
                            issues["cpu_usage"] += 1
                        elif "response" in line.lower() and "time" in line.lower():
                            issues["response_time_issues"] += 1
                        elif "resource" in line.lower():
                            issues["resource_exhaustion"] += 1
        except FileNotFoundError:
            self.logger.warning(f"Log file {log_file} not found")
            
        return issues

    def _detect_security_issues(self, log_file: str) -> Dict[str, Any]:
        """Detect security-related issues"""
        issues = {
            "authentication_failures": 0,
            "authorization_errors": 0,
            "token_leaks": 0,
            "suspicious_activity": 0,
            "data_exposure": 0
        }
        
        try:
            with open(log_file, 'r') as f:
                for line in f:
                    if "security" in line.lower() or "auth" in line.lower():
                        if "authentication" in line.lower():
                            issues["authentication_failures"] += 1
                        elif "authorization" in line.lower():
                            issues["authorization_errors"] += 1
                        elif "token" in line.lower() and "leak" in line.lower():
                            issues["token_leaks"] += 1
                        elif "suspicious" in line.lower():
                            issues["suspicious_activity"] += 1
                        elif "exposure" in line.lower():
                            issues["data_exposure"] += 1
        except FileNotFoundError:
            self.logger.warning(f"Log file {log_file} not found")
            
        return issues

    def _detect_ux_issues(self, log_file: str) -> Dict[str, Any]:
        """Detect user experience issues"""
        issues = {
            "error_messages_shown": 0,
            "timeout_experiences": 0,
            "confusing_responses": 0,
            "missing_data": 0,
            "slow_interactions": 0
        }
        
        try:
            with open(log_file, 'r') as f:
                for line in f:
                    if "user" in line.lower() or "ux" in line.lower():
                        if "error" in line.lower() and "message" in line.lower():
                            issues["error_messages_shown"] += 1
                        elif "timeout" in line.lower():
                            issues["timeout_experiences"] += 1
                        elif "confusing" in line.lower():
                            issues["confusing_responses"] += 1
                        elif "missing" in line.lower() and "data" in line.lower():
                            issues["missing_data"] += 1
                        elif "slow" in line.lower():
                            issues["slow_interactions"] += 1
        except FileNotFoundError:
            self.logger.warning(f"Log file {log_file} not found")
            
        return issues

    def _generate_error_insights(self, patterns: Dict[str, Any]) -> List[str]:
        """Generate insights from error patterns"""
        insights = []
        
        # OAuth insights
        oauth_patterns = patterns.get("oauth_errors", {})
        if oauth_patterns.get("token_expirations", 0) > 5:
            insights.append("High token expiration rate detected - consider implementing automatic refresh")
        if oauth_patterns.get("rate_limiting", 0) > 3:
            insights.append("API rate limiting frequent - implement better request batching")
            
        # API insights
        api_patterns = patterns.get("api_errors", {})
        if api_patterns.get("timeout_errors", 0) > 10:
            insights.append("Frequent API timeouts - consider increasing timeout values")
        if api_patterns.get("server_errors", 0) > 5:
            insights.append("Server errors detected - monitor external API health")
            
        # Database insights
        db_patterns = patterns.get("database_errors", {})
        if db_patterns.get("connection_failures", 0) > 3:
            insights.append("Database connection issues - check connection pool settings")
        if db_patterns.get("deadlock_errors", 0) > 0:
            insights.append("Database deadlocks detected - review transaction patterns")
            
        # Performance insights
        perf_issues = patterns.get("performance_issues", {})
        if perf_issues.get("slow_queries", 0) > 5:
            insights.append("Slow queries detected - consider query optimization")
        if perf_issues.get("memory_usage", 0) > 3:
            insights.append("High memory usage - monitor resource consumption")
            
        # Security insights
        security_issues = patterns.get("security_concerns", {})
        if security_issues.get("authentication_failures", 0) > 10:
            insights.append("High authentication failure rate - review OAuth implementation")
        if security_issues.get("token_leaks", 0) > 0:
            insights.append("Potential token leaks detected - immediate security review required")
            
        # UX insights
        ux_issues = patterns.get("user_experience_issues", {})
        if ux_issues.get("error_messages_shown", 0) > 20:
            insights.append("Too many error messages shown to users - improve error handling")
        if ux_issues.get("timeout_experiences", 0) > 5:
            insights.append("Users experiencing timeouts - optimize response times")
            
        return insights

    def _generate_recommendations(self, patterns: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # OAuth recommendations
        oauth_patterns = patterns.get("oauth_errors", {})
        if oauth_patterns.get("token_expirations", 0) > 5:
            recommendations.append("Implement automatic token refresh with exponential backoff")
        if oauth_patterns.get("rate_limiting", 0) > 3:
            recommendations.append("Add request queuing and rate limit handling")
            
        # API recommendations
        api_patterns = patterns.get("api_errors", {})
        if api_patterns.get("timeout_errors", 0) > 10:
            recommendations.append("Increase API timeout values and implement retry logic")
        if api_patterns.get("server_errors", 0) > 5:
            recommendations.append("Add circuit breaker pattern for external APIs")
            
        # Database recommendations
        db_patterns = patterns.get("database_errors", {})
        if db_patterns.get("connection_failures", 0) > 3:
            recommendations.append("Implement connection pooling and health checks")
        if db_patterns.get("deadlock_errors", 0) > 0:
            recommendations.append("Review transaction isolation levels and query patterns")
            
        # Performance recommendations
        perf_issues = patterns.get("performance_issues", {})
        if perf_issues.get("slow_queries", 0) > 5:
            recommendations.append("Add database query monitoring and optimization")
        if perf_issues.get("memory_usage", 0) > 3:
            recommendations.append("Implement memory monitoring and garbage collection")
            
        # Security recommendations
        security_issues = patterns.get("security_concerns", {})
        if security_issues.get("authentication_failures", 0) > 10:
            recommendations.append("Review OAuth implementation and add security monitoring")
        if security_issues.get("token_leaks", 0) > 0:
            recommendations.append("Immediate security audit and token encryption review")
            
        # UX recommendations
        ux_issues = patterns.get("user_experience_issues", {})
        if ux_issues.get("error_messages_shown", 0) > 20:
            recommendations.append("Improve error handling and user communication")
        if ux_issues.get("timeout_experiences", 0) > 5:
            recommendations.append("Optimize response times and add progress indicators")
            
        return recommendations

    def _update_error_frequencies(self, patterns: Dict[str, Any]):
        """Update error frequency tracking"""
        for category, pattern_data in patterns.items():
            for error_type, count in pattern_data.items():
                self.error_frequencies[f"{category}_{error_type}"] += count

    def get_error_summary(self) -> Dict[str, Any]:
        """Get a summary of current error patterns"""
        return {
            "total_errors": sum(self.error_frequencies.values()),
            "most_common_errors": self.error_frequencies.most_common(5),
            "error_categories": dict(self.error_frequencies),
            "last_analysis": datetime.now().isoformat()
        }

    def detect_anomalies(self) -> List[str]:
        """Detect unusual error patterns"""
        anomalies = []
        
        # Check for sudden spikes in error rates
        recent_errors = sum(self.error_frequencies.values())
        if recent_errors > 50:  # Threshold for anomaly
            anomalies.append("Unusually high error rate detected")
            
        # Check for specific error patterns
        if self.error_frequencies.get("oauth_errors_token_expirations", 0) > 10:
            anomalies.append("High token expiration rate - possible OAuth configuration issue")
            
        if self.error_frequencies.get("security_concerns_token_leaks", 0) > 0:
            anomalies.append("CRITICAL: Potential security breach detected")
            
        return anomalies


# Global error analyzer instance
error_analyzer = AdvancedErrorAnalyzer() 