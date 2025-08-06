"""
Token Usage Estimation System for Agent Coordination Performance

Provides accurate token counting and cost prediction for Claude Code
agent coordination to prevent budget overruns and optimize resource usage.
"""

import re
import json
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False


class ModelType(Enum):
    """Supported Claude model types with token pricing."""
    CLAUDE_3_HAIKU = "claude-3-haiku-20240307"
    CLAUDE_3_SONNET = "claude-3-sonnet-20240229"
    CLAUDE_3_OPUS = "claude-3-opus-20240229"
    CLAUDE_3_5_SONNET = "claude-3-5-sonnet-20241022"
    
    @property
    def input_cost_per_1k(self) -> float:
        """Cost per 1K input tokens in USD."""
        costs = {
            self.CLAUDE_3_HAIKU: 0.00025,
            self.CLAUDE_3_SONNET: 0.003,
            self.CLAUDE_3_OPUS: 0.015,
            self.CLAUDE_3_5_SONNET: 0.003,
        }
        return costs[self]
    
    @property
    def output_cost_per_1k(self) -> float:
        """Cost per 1K output tokens in USD."""
        costs = {
            self.CLAUDE_3_HAIKU: 0.00125,
            self.CLAUDE_3_SONNET: 0.015,
            self.CLAUDE_3_OPUS: 0.075,
            self.CLAUDE_3_5_SONNET: 0.015,
        }
        return costs[self]


class PromptType(Enum):
    """Types of prompts for different coordination patterns."""
    AGENT_COORDINATION = "agent_coordination"
    SEQUENTIAL_FLOW = "sequential_flow"
    PARALLEL_EXECUTION = "parallel_execution"
    CONTEXT_ACCUMULATION = "context_accumulation"
    META_ORCHESTRATION = "meta_orchestration"
    SIMPLE_TASK = "simple_task"


@dataclass
class TokenUsage:
    """Represents token usage for a request."""
    input_tokens: int
    output_tokens: int
    total_tokens: int
    model_type: ModelType
    prompt_type: PromptType
    timestamp: datetime
    
    @property
    def input_cost(self) -> float:
        """Calculate input cost in USD."""
        return (self.input_tokens / 1000) * self.model_type.input_cost_per_1k
    
    @property
    def output_cost(self) -> float:
        """Calculate output cost in USD."""
        return (self.output_tokens / 1000) * self.model_type.output_cost_per_1k
    
    @property
    def total_cost(self) -> float:
        """Calculate total cost in USD."""
        return self.input_cost + self.output_cost


@dataclass
class UsageStats:
    """Statistics for token usage over time."""
    total_requests: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost: float = 0.0
    average_tokens_per_request: float = 0.0
    average_cost_per_request: float = 0.0
    
    def update(self, usage: TokenUsage) -> None:
        """Update stats with new usage data."""
        self.total_requests += 1
        self.total_input_tokens += usage.input_tokens
        self.total_output_tokens += usage.output_tokens
        self.total_cost += usage.total_cost
        
        self.average_tokens_per_request = (
            (self.total_input_tokens + self.total_output_tokens) / self.total_requests
        )
        self.average_cost_per_request = self.total_cost / self.total_requests


class TokenEstimator:
    """
    Estimates token usage for different types of prompts and coordination patterns.
    
    Uses tiktoken for accurate token counting and provides cost estimation
    based on Claude model pricing.
    """
    
    def __init__(self):
        """Initialize token estimator."""
        # Use cl100k_base encoding as approximation for Claude models
        if TIKTOKEN_AVAILABLE:
            try:
                self.encoding = tiktoken.get_encoding("cl100k_base")
            except Exception:
                self.encoding = None
        else:
            self.encoding = None
        
        # Prompt complexity multipliers for different coordination types
        self.complexity_multipliers = {
            PromptType.SIMPLE_TASK: 1.0,
            PromptType.AGENT_COORDINATION: 1.3,
            PromptType.SEQUENTIAL_FLOW: 1.5,
            PromptType.PARALLEL_EXECUTION: 1.8,
            PromptType.CONTEXT_ACCUMULATION: 2.0,
            PromptType.META_ORCHESTRATION: 2.5,
        }
        
        # Average response length multipliers by prompt type
        self.response_multipliers = {
            PromptType.SIMPLE_TASK: 0.8,
            PromptType.AGENT_COORDINATION: 1.2,
            PromptType.SEQUENTIAL_FLOW: 1.0,
            PromptType.PARALLEL_EXECUTION: 1.5,
            PromptType.CONTEXT_ACCUMULATION: 1.3,
            PromptType.META_ORCHESTRATION: 1.8,
        }
    
    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for text (alias for count_tokens).
        
        Args:
            text: Text to count tokens for
            
        Returns:
            Number of tokens
        """
        return self.count_tokens(text)
    
    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text.
        
        Args:
            text: Text to count tokens for
            
        Returns:
            Number of tokens
        """
        if not text:
            return 0
        
        if self.encoding:
            try:
                return len(self.encoding.encode(text))
            except Exception:
                pass
        
        # Fallback to word-based estimation (rough approximation)
        words = len(text.split())
        # Approximate token-to-word ratio for English
        return int(words * 1.3)
    
    def estimate_prompt_tokens(self, 
                             prompt: str,
                             prompt_type: PromptType = PromptType.SIMPLE_TASK,
                             context_size: int = 0) -> int:
        """
        Estimate input tokens for a prompt including coordination overhead.
        
        Args:
            prompt: The prompt text
            prompt_type: Type of coordination prompt
            context_size: Size of additional context in tokens
            
        Returns:
            Estimated input token count
        """
        base_tokens = self.count_tokens(prompt)
        multiplier = self.complexity_multipliers.get(prompt_type, 1.0)
        
        # Add context and apply complexity multiplier
        estimated_tokens = int((base_tokens + context_size) * multiplier)
        
        return estimated_tokens
    
    def estimate_response_tokens(self,
                               input_tokens: int,
                               prompt_type: PromptType = PromptType.SIMPLE_TASK) -> int:
        """
        Estimate output tokens based on input size and prompt type.
        
        Args:
            input_tokens: Number of input tokens
            prompt_type: Type of coordination prompt
            
        Returns:
            Estimated output token count
        """
        # Base response is typically 10-30% of input for most tasks
        base_ratio = 0.2
        
        # Apply prompt-type specific multiplier
        multiplier = self.response_multipliers.get(prompt_type, 1.0)
        
        estimated_tokens = int(input_tokens * base_ratio * multiplier)
        
        # Set reasonable bounds
        min_tokens = 50  # Minimum response
        max_tokens = 4000  # Maximum typical response
        
        return max(min_tokens, min(estimated_tokens, max_tokens))
    
    def estimate_coordination_cost(self,
                                 prompt: str,
                                 model_type: ModelType = ModelType.CLAUDE_3_5_SONNET,
                                 prompt_type: PromptType = PromptType.AGENT_COORDINATION,
                                 agent_count: int = 1,
                                 context_tokens: int = 0) -> Dict[str, Any]:
        """
        Estimate cost for agent coordination request.
        
        Args:
            prompt: The coordination prompt
            model_type: Claude model type
            prompt_type: Type of coordination
            agent_count: Number of agents involved
            context_tokens: Additional context tokens
            
        Returns:
            Cost estimation breakdown
        """
        # Estimate tokens for single agent
        input_tokens = self.estimate_prompt_tokens(prompt, prompt_type, context_tokens)
        output_tokens = self.estimate_response_tokens(input_tokens, prompt_type)
        
        # Account for multiple agents in coordination
        if agent_count > 1:
            # Sequential coordination: multiply by agent count
            if prompt_type in [PromptType.SEQUENTIAL_FLOW, PromptType.META_ORCHESTRATION]:
                input_tokens *= agent_count
                output_tokens *= agent_count
            # Parallel coordination: higher input overhead, similar output per agent
            elif prompt_type == PromptType.PARALLEL_EXECUTION:
                input_tokens = int(input_tokens * (1 + agent_count * 0.3))
                output_tokens *= agent_count
        
        # Calculate costs
        input_cost = (input_tokens / 1000) * model_type.input_cost_per_1k
        output_cost = (output_tokens / 1000) * model_type.output_cost_per_1k
        total_cost = input_cost + output_cost
        
        return {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "input_cost_usd": round(input_cost, 6),
            "output_cost_usd": round(output_cost, 6),
            "total_cost_usd": round(total_cost, 6),
            "model_type": model_type.value,
            "prompt_type": prompt_type.value,
            "agent_count": agent_count
        }
    
    def estimate_batch_coordination_cost(self,
                                       coordination_requests: List[Dict[str, Any]],
                                       model_type: ModelType = ModelType.CLAUDE_3_5_SONNET) -> Dict[str, Any]:
        """
        Estimate cost for batch of coordination requests.
        
        Args:
            coordination_requests: List of coordination request specs
            model_type: Claude model type
            
        Returns:
            Batch cost estimation
        """
        total_input_tokens = 0
        total_output_tokens = 0
        total_cost = 0.0
        request_estimates = []
        
        for request in coordination_requests:
            estimate = self.estimate_coordination_cost(
                prompt=request.get("prompt", ""),
                model_type=model_type,
                prompt_type=PromptType(request.get("prompt_type", "simple_task")),
                agent_count=request.get("agent_count", 1),
                context_tokens=request.get("context_tokens", 0)
            )
            
            total_input_tokens += estimate["input_tokens"]
            total_output_tokens += estimate["output_tokens"]
            total_cost += estimate["total_cost_usd"]
            request_estimates.append(estimate)
        
        return {
            "batch_summary": {
                "total_requests": len(coordination_requests),
                "total_input_tokens": total_input_tokens,
                "total_output_tokens": total_output_tokens,
                "total_tokens": total_input_tokens + total_output_tokens,
                "total_cost_usd": round(total_cost, 6),
                "average_cost_per_request": round(total_cost / len(coordination_requests), 6) if coordination_requests else 0
            },
            "individual_estimates": request_estimates
        }


class TokenUsageTracker:
    """
    Tracks real-time token usage and provides budget monitoring.
    
    Features:
    - Real-time usage tracking
    - Budget threshold warnings  
    - Usage history and reporting
    - Cost analysis by prompt type and agent
    """
    
    def __init__(self, 
                 daily_budget_usd: float = 10.0,
                 warning_threshold: float = 0.8):
        """
        Initialize usage tracker.
        
        Args:
            daily_budget_usd: Daily budget limit in USD
            warning_threshold: Warning threshold as fraction of budget (0.8 = 80%)
        """
        self.daily_budget_usd = daily_budget_usd
        self.warning_threshold = warning_threshold
        
        self.usage_history: List[TokenUsage] = []
        self.daily_stats: Dict[str, UsageStats] = {}  # date -> stats
        self._lock = threading.RLock()
        
        # Persistent storage
        self.storage_dir = Path.home() / ".claude" / "usage"
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.usage_file = self.storage_dir / "token_usage.json"
        
        # Load existing usage data
        self._load_usage_history()
        
        # Warning callbacks
        self.warning_callbacks: List[callable] = []
    
    def track_usage(self, 
                   input_tokens: int,
                   output_tokens: int,
                   model_type: ModelType,
                   prompt_type: PromptType = PromptType.SIMPLE_TASK) -> TokenUsage:
        """
        Track token usage for a request.
        
        Args:
            input_tokens: Input tokens used
            output_tokens: Output tokens generated
            model_type: Model type used
            prompt_type: Type of prompt
            
        Returns:
            TokenUsage record
        """
        usage = TokenUsage(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            model_type=model_type,
            prompt_type=prompt_type,
            timestamp=datetime.now()
        )
        
        with self._lock:
            self.usage_history.append(usage)
            
            # Update daily stats
            date_key = usage.timestamp.strftime("%Y-%m-%d")
            if date_key not in self.daily_stats:
                self.daily_stats[date_key] = UsageStats()
            
            self.daily_stats[date_key].update(usage)
            
            # Check budget warnings
            self._check_budget_warnings(date_key)
            
            # Persist usage data
            self._save_usage_history()
        
        return usage
    
    def _check_budget_warnings(self, date_key: str) -> None:
        """Check if budget thresholds are exceeded."""
        daily_cost = self.daily_stats[date_key].total_cost
        threshold_cost = self.daily_budget_usd * self.warning_threshold
        
        if daily_cost >= threshold_cost:
            warning_msg = f"Token usage warning: ${daily_cost:.4f} / ${self.daily_budget_usd:.2f} daily budget ({(daily_cost/self.daily_budget_usd)*100:.1f}%)"
            
            # Trigger warning callbacks
            for callback in self.warning_callbacks:
                try:
                    callback(warning_msg, daily_cost, self.daily_budget_usd)
                except Exception as e:
                    print(f"Warning callback error: {e}")
            
            # Print warning
            print(f"🚨 {warning_msg}")
    
    def add_warning_callback(self, callback: callable) -> None:
        """Add callback function for budget warnings."""
        self.warning_callbacks.append(callback)
    
    def get_daily_usage(self, date: Optional[datetime] = None) -> Optional[UsageStats]:
        """
        Get usage statistics for specific date.
        
        Args:
            date: Date to get stats for (defaults to today)
            
        Returns:
            Usage statistics or None if no data
        """
        if date is None:
            date = datetime.now()
        
        date_key = date.strftime("%Y-%m-%d")
        return self.daily_stats.get(date_key)
    
    def get_usage_by_prompt_type(self, 
                                days: int = 7) -> Dict[str, UsageStats]:
        """
        Get usage statistics by prompt type for recent days.
        
        Args:
            days: Number of recent days to analyze
            
        Returns:
            Statistics by prompt type
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        stats_by_type: Dict[str, UsageStats] = {}
        
        with self._lock:
            for usage in self.usage_history:
                if usage.timestamp >= cutoff_date:
                    prompt_type = usage.prompt_type.value
                    
                    if prompt_type not in stats_by_type:
                        stats_by_type[prompt_type] = UsageStats()
                    
                    stats_by_type[prompt_type].update(usage)
        
        return stats_by_type
    
    def get_weekly_report(self) -> Dict[str, Any]:
        """Generate weekly usage report."""
        week_ago = datetime.now() - timedelta(days=7)
        
        with self._lock:
            recent_usage = [
                usage for usage in self.usage_history 
                if usage.timestamp >= week_ago
            ]
        
        if not recent_usage:
            return {"error": "No usage data for the past week"}
        
        # Calculate totals
        total_requests = len(recent_usage)
        total_input_tokens = sum(u.input_tokens for u in recent_usage)
        total_output_tokens = sum(u.output_tokens for u in recent_usage)
        total_cost = sum(u.total_cost for u in recent_usage)
        
        # Group by model type
        by_model = {}
        for usage in recent_usage:
            model = usage.model_type.value
            if model not in by_model:
                by_model[model] = {"requests": 0, "cost": 0.0}
            by_model[model]["requests"] += 1
            by_model[model]["cost"] += usage.total_cost
        
        # Group by prompt type
        by_prompt_type = {}
        for usage in recent_usage:
            ptype = usage.prompt_type.value
            if ptype not in by_prompt_type:
                by_prompt_type[ptype] = {"requests": 0, "cost": 0.0}
            by_prompt_type[ptype]["requests"] += 1
            by_prompt_type[ptype]["cost"] += usage.total_cost
        
        return {
            "period": "past_7_days",
            "summary": {
                "total_requests": total_requests,
                "total_input_tokens": total_input_tokens,
                "total_output_tokens": total_output_tokens,
                "total_tokens": total_input_tokens + total_output_tokens,
                "total_cost_usd": round(total_cost, 6),
                "average_cost_per_request": round(total_cost / total_requests, 6),
                "daily_average_cost": round(total_cost / 7, 6),
                "budget_utilization": round((total_cost / 7) / self.daily_budget_usd * 100, 1)
            },
            "by_model_type": by_model,
            "by_prompt_type": by_prompt_type
        }
    
    def estimate_remaining_budget_requests(self, 
                                         model_type: ModelType = ModelType.CLAUDE_3_5_SONNET,
                                         prompt_type: PromptType = PromptType.AGENT_COORDINATION) -> Dict[str, Any]:
        """
        Estimate how many requests can be made with remaining daily budget.
        
        Args:
            model_type: Model type to estimate for
            prompt_type: Prompt type to estimate for
            
        Returns:
            Budget and request estimations
        """
        today = datetime.now().strftime("%Y-%m-%d")
        daily_stats = self.daily_stats.get(today, UsageStats())
        
        remaining_budget = self.daily_budget_usd - daily_stats.total_cost
        
        if remaining_budget <= 0:
            return {
                "remaining_budget_usd": 0.0,
                "estimated_requests": 0,
                "status": "budget_exceeded"
            }
        
        # Estimate cost per request based on historical data or defaults
        estimator = TokenEstimator()
        sample_prompt = "Coordinate agent analysis task with context processing."
        
        cost_estimate = estimator.estimate_coordination_cost(
            prompt=sample_prompt,
            model_type=model_type,
            prompt_type=prompt_type
        )
        
        cost_per_request = cost_estimate["total_cost_usd"]
        estimated_requests = int(remaining_budget / cost_per_request) if cost_per_request > 0 else 0
        
        return {
            "remaining_budget_usd": round(remaining_budget, 6),
            "estimated_cost_per_request": round(cost_per_request, 6),
            "estimated_requests": estimated_requests,
            "status": "within_budget"
        }
    
    def _save_usage_history(self) -> None:
        """Save usage history to persistent storage."""
        try:
            # Keep only recent history to prevent file from growing too large
            cutoff_date = datetime.now() - timedelta(days=30)
            recent_usage = [
                usage for usage in self.usage_history 
                if usage.timestamp >= cutoff_date
            ]
            
            usage_data = []
            for usage in recent_usage:
                usage_data.append({
                    "input_tokens": usage.input_tokens,
                    "output_tokens": usage.output_tokens,
                    "total_tokens": usage.total_tokens,
                    "model_type": usage.model_type.value,
                    "prompt_type": usage.prompt_type.value,
                    "timestamp": usage.timestamp.isoformat(),
                    "total_cost": usage.total_cost
                })
            
            with open(self.usage_file, 'w') as f:
                json.dump(usage_data, f, indent=2)
                
        except Exception as e:
            print(f"Warning: Failed to save usage history: {e}")
    
    def _load_usage_history(self) -> None:
        """Load usage history from persistent storage."""
        try:
            if not self.usage_file.exists():
                return
            
            with open(self.usage_file) as f:
                usage_data = json.load(f)
            
            for data in usage_data:
                try:
                    usage = TokenUsage(
                        input_tokens=data["input_tokens"],
                        output_tokens=data["output_tokens"],
                        total_tokens=data["total_tokens"],
                        model_type=ModelType(data["model_type"]),
                        prompt_type=PromptType(data["prompt_type"]),
                        timestamp=datetime.fromisoformat(data["timestamp"])
                    )
                    
                    self.usage_history.append(usage)
                    
                    # Update daily stats
                    date_key = usage.timestamp.strftime("%Y-%m-%d")
                    if date_key not in self.daily_stats:
                        self.daily_stats[date_key] = UsageStats()
                    
                    self.daily_stats[date_key].update(usage)
                    
                except (ValueError, KeyError) as e:
                    # Skip malformed entries
                    continue
            
        except Exception as e:
            print(f"Warning: Failed to load usage history: {e}")


# Global instances
_token_estimator: Optional[TokenEstimator] = None
_usage_tracker: Optional[TokenUsageTracker] = None


def get_token_estimator() -> TokenEstimator:
    """Get or create global token estimator."""
    global _token_estimator
    if _token_estimator is None:
        _token_estimator = TokenEstimator()
    return _token_estimator


def get_usage_tracker() -> TokenUsageTracker:
    """Get or create global usage tracker."""
    global _usage_tracker
    if _usage_tracker is None:
        _usage_tracker = TokenUsageTracker()
    return _usage_tracker


def estimate_agent_coordination_cost(prompt: str,
                                   agent_count: int = 1,
                                   model_type: ModelType = ModelType.CLAUDE_3_5_SONNET) -> Dict[str, Any]:
    """
    Convenience function to estimate agent coordination cost.
    
    Args:
        prompt: Coordination prompt
        agent_count: Number of agents involved
        model_type: Claude model type
        
    Returns:
        Cost estimation
    """
    estimator = get_token_estimator()
    return estimator.estimate_coordination_cost(
        prompt=prompt,
        model_type=model_type,
        prompt_type=PromptType.AGENT_COORDINATION,
        agent_count=agent_count
    )


def track_agent_usage(input_tokens: int,
                     output_tokens: int,
                     model_type: ModelType = ModelType.CLAUDE_3_5_SONNET,
                     prompt_type: PromptType = PromptType.AGENT_COORDINATION) -> TokenUsage:
    """
    Convenience function to track agent coordination usage.
    
    Args:
        input_tokens: Input tokens used
        output_tokens: Output tokens generated
        model_type: Model type used
        prompt_type: Type of coordination prompt
        
    Returns:
        TokenUsage record
    """
    tracker = get_usage_tracker()
    return tracker.track_usage(input_tokens, output_tokens, model_type, prompt_type)