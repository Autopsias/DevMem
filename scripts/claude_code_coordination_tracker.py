#!/usr/bin/env python3
"""
Claude Code Coordination Tracker

Observability and learning system for coordination patterns to enable continuous
improvement and performance optimization.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict


class CoordinationEventType(Enum):
    """Types of coordination events to track."""
    
    START = "start"
    COMPLETE = "complete"
    ERROR = "error"
    TIMEOUT = "timeout"


class PatternType(Enum):
    """Types of coordination patterns identified."""
    
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    BATCH = "batch"
    HYBRID = "hybrid"


@dataclass
class CoordinationEvent:
    """Individual coordination event record."""
    
    event_id: str
    event_type: CoordinationEventType
    timestamp: float
    agent_count: int
    domains: List[str]
    strategy: str
    duration: Optional[float] = None
    success: Optional[bool] = None
    agents_used: Optional[List[str]] = None
    error_message: Optional[str] = None


@dataclass
class CoordinationPattern:
    """Identified coordination pattern with success metrics."""
    
    pattern_id: str
    pattern_type: PatternType
    domains: List[str]
    agent_count: int
    strategy: str
    success_rate: float
    avg_duration: float
    usage_count: int
    last_used: float
    confidence_score: float


@dataclass
class PerformanceInsight:
    """Performance insight and recommendation."""
    
    insight_id: str
    category: str
    description: str
    recommendation: str
    impact_score: float
    confidence: float
    created_at: float
    applies_to: List[str]  # Domains or patterns this applies to


class ClaudeCodeCoordinationTracker:
    """
    Coordination tracking and learning system for Claude Code patterns.
    
    Provides observability, pattern recognition, and performance insights
    for continuous improvement of coordination strategies.
    """
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize coordination tracker.
        
        Args:
            data_dir: Directory for storing tracking data
        """
        self.data_dir = Path(data_dir or ".claude/coordination_data")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Event storage
        self.events: List[CoordinationEvent] = []
        self.patterns: Dict[str, CoordinationPattern] = {}
        self.insights: List[PerformanceInsight] = []
        
        # Analytics cache
        self._analytics_cache: Dict[str, Any] = {}
        self._cache_timestamp: float = 0
        self.CACHE_TTL = 300  # 5 minutes
        
        # Load existing data
        self._load_data()
    
    def start_coordination(
        self, 
        event_id: str, 
        agent_count: int, 
        domains: List[str], 
        strategy: str,
        agents_used: Optional[List[str]] = None
    ) -> None:
        """
        Log the start of a coordination event.
        
        Args:
            event_id: Unique identifier for this coordination
            agent_count: Number of agents being coordinated
            domains: List of domains involved
            strategy: Coordination strategy being used
            agents_used: List of specific agents being used
        """
        event = CoordinationEvent(
            event_id=event_id,
            event_type=CoordinationEventType.START,
            timestamp=time.time(),
            agent_count=agent_count,
            domains=domains.copy(),
            strategy=strategy,
            agents_used=agents_used.copy() if agents_used else None
        )
        
        self.events.append(event)
        self._invalidate_cache()
        self._save_events()
    
    def complete_coordination(
        self, 
        event_id: str, 
        success: bool = True, 
        error_message: Optional[str] = None
    ) -> None:
        """
        Log the completion of a coordination event.
        
        Args:
            event_id: Unique identifier for the coordination
            success: Whether the coordination was successful
            error_message: Error message if coordination failed
        """
        # Find the start event
        start_event = None
        for event in reversed(self.events):
            if event.event_id == event_id and event.event_type == CoordinationEventType.START:
                start_event = event
                break
        
        if not start_event:
            # Log completion event even without start event
            duration = None
        else:
            duration = time.time() - start_event.timestamp
        
        completion_event = CoordinationEvent(
            event_id=event_id,
            event_type=CoordinationEventType.COMPLETE if success else CoordinationEventType.ERROR,
            timestamp=time.time(),
            agent_count=start_event.agent_count if start_event else 0,
            domains=start_event.domains.copy() if start_event else [],
            strategy=start_event.strategy if start_event else "unknown",
            duration=duration,
            success=success,
            agents_used=start_event.agents_used.copy() if start_event and start_event.agents_used else None,
            error_message=error_message
        )
        
        self.events.append(completion_event)
        
        # Learn from this coordination
        if start_event and completion_event.duration is not None:
            self._learn_pattern(start_event, completion_event)
        
        self._invalidate_cache()
        self._save_events()
    
    def _learn_pattern(self, start_event: CoordinationEvent, completion_event: CoordinationEvent) -> None:
        """
        Learn coordination patterns from completed events.
        
        Args:
            start_event: The start event
            completion_event: The completion event
        """
        # Create pattern key
        pattern_key = self._generate_pattern_key(
            start_event.domains, 
            start_event.agent_count, 
            start_event.strategy
        )
        
        # Determine pattern type
        pattern_type = self._classify_pattern_type(start_event.strategy, start_event.agent_count)
        
        # Update or create pattern
        if pattern_key in self.patterns:
            pattern = self.patterns[pattern_key]
            
            # Update metrics
            total_duration = pattern.avg_duration * pattern.usage_count
            pattern.usage_count += 1
            pattern.avg_duration = (total_duration + completion_event.duration) / pattern.usage_count
            
            # Update success rate
            if completion_event.success:
                success_count = int(pattern.success_rate * (pattern.usage_count - 1))
                pattern.success_rate = (success_count + 1) / pattern.usage_count
            else:
                success_count = int(pattern.success_rate * (pattern.usage_count - 1))
                pattern.success_rate = success_count / pattern.usage_count
            
            pattern.last_used = completion_event.timestamp
            
            # Update confidence based on usage count and consistency
            pattern.confidence_score = min(0.95, pattern.usage_count * 0.1 + pattern.success_rate * 0.5)
            
        else:
            # Create new pattern
            pattern = CoordinationPattern(
                pattern_id=pattern_key,
                pattern_type=pattern_type,
                domains=start_event.domains.copy(),
                agent_count=start_event.agent_count,
                strategy=start_event.strategy,
                success_rate=1.0 if completion_event.success else 0.0,
                avg_duration=completion_event.duration,
                usage_count=1,
                last_used=completion_event.timestamp,
                confidence_score=0.3  # Low initial confidence
            )
            
            self.patterns[pattern_key] = pattern
        
        self._save_patterns()
    
    def _generate_pattern_key(self, domains: List[str], agent_count: int, strategy: str) -> str:
        """Generate unique pattern key."""
        sorted_domains = sorted(domains)
        return f"{'+'.join(sorted_domains)}_{agent_count}_{strategy}"
    
    def _classify_pattern_type(self, strategy: str, agent_count: int) -> PatternType:
        """Classify coordination pattern type."""
        if "batch" in strategy.lower():
            return PatternType.BATCH
        elif "parallel" in strategy.lower():
            return PatternType.PARALLEL
        elif agent_count == 1:
            return PatternType.SEQUENTIAL
        else:
            return PatternType.HYBRID
    
    def get_analytics(self) -> Dict[str, Any]:
        """
        Get comprehensive analytics on coordination patterns.
        
        Returns:
            Dictionary with analytics data
        """
        # Check cache
        if time.time() - self._cache_timestamp < self.CACHE_TTL and self._analytics_cache:
            return self._analytics_cache
        
        # Generate fresh analytics
        analytics = self._generate_analytics()
        
        # Cache results
        self._analytics_cache = analytics
        self._cache_timestamp = time.time()
        
        return analytics
    
    def _generate_analytics(self) -> Dict[str, Any]:
        """Generate comprehensive analytics."""
        if not self.events:
            return {"message": "No coordination events recorded"}
        
        # Basic statistics
        total_events = len(self.events)
        completed_events = [e for e in self.events if e.event_type in [CoordinationEventType.COMPLETE, CoordinationEventType.ERROR]]
        successful_events = [e for e in completed_events if e.success]
        
        # Time-based analytics
        recent_events = [e for e in self.events if e.timestamp > time.time() - 3600]  # Last hour
        
        # Domain analytics
        domain_usage = defaultdict(int)
        domain_success = defaultdict(int)
        
        for event in completed_events:
            for domain in event.domains:
                domain_usage[domain] += 1
                if event.success:
                    domain_success[domain] += 1
        
        # Strategy analytics
        strategy_usage = defaultdict(int)
        strategy_success = defaultdict(int)
        strategy_duration = defaultdict(list)
        
        for event in completed_events:
            strategy_usage[event.strategy] += 1
            if event.success:
                strategy_success[event.strategy] += 1
            if event.duration:
                strategy_duration[event.strategy].append(event.duration)
        
        # Pattern analytics
        pattern_stats = []
        for pattern in self.patterns.values():
            pattern_stats.append({
                "pattern_id": pattern.pattern_id,
                "domains": pattern.domains,
                "agent_count": pattern.agent_count,
                "strategy": pattern.strategy,
                "success_rate": round(pattern.success_rate, 3),
                "avg_duration": round(pattern.avg_duration, 2),
                "usage_count": pattern.usage_count,
                "confidence_score": round(pattern.confidence_score, 3)
            })
        
        # Sort patterns by confidence and usage
        pattern_stats.sort(key=lambda x: (x["confidence_score"], x["usage_count"]), reverse=True)
        
        analytics = {
            "summary": {
                "total_events": total_events,
                "completed_coordinations": len(completed_events),
                "successful_coordinations": len(successful_events),
                "success_rate": round(len(successful_events) / len(completed_events), 3) if completed_events else 0,
                "recent_events_1h": len(recent_events),
                "total_patterns_learned": len(self.patterns),
                "last_coordination": datetime.fromtimestamp(max(e.timestamp for e in self.events)).isoformat() if self.events else None
            },
            "domain_analytics": {
                domain: {
                    "usage_count": domain_usage[domain],
                    "success_rate": round(domain_success[domain] / domain_usage[domain], 3) if domain_usage[domain] > 0 else 0
                }
                for domain in sorted(domain_usage.keys())
            },
            "strategy_analytics": {
                strategy: {
                    "usage_count": strategy_usage[strategy],
                    "success_rate": round(strategy_success[strategy] / strategy_usage[strategy], 3) if strategy_usage[strategy] > 0 else 0,
                    "avg_duration": round(sum(strategy_duration[strategy]) / len(strategy_duration[strategy]), 2) if strategy_duration[strategy] else 0
                }
                for strategy in sorted(strategy_usage.keys())
            },
            "top_patterns": pattern_stats[:10],  # Top 10 patterns
            "insights_generated": len(self.insights)
        }
        
        return analytics
    
    def generate_insights(self) -> List[PerformanceInsight]:
        """
        Generate performance insights and recommendations.
        
        Returns:
            List of performance insights
        """
        new_insights = []
        current_time = time.time()
        analytics = self.get_analytics()
        
        # Only try to generate new insights if we have analytics data
        if analytics and not analytics.get("message"):
            # Insight 1: Low success rate patterns
            for pattern in self.patterns.values():
                if pattern.usage_count >= 3 and pattern.success_rate < 0.7:
                    insight = PerformanceInsight(
                        insight_id=f"low_success_{pattern.pattern_id}",
                        category="reliability",
                        description=f"Pattern {pattern.pattern_id} has low success rate ({pattern.success_rate:.1%})",
                        recommendation=f"Consider alternative strategies for {'+'.join(pattern.domains)} coordination with {pattern.agent_count} agents",
                        impact_score=0.8,
                        confidence=pattern.confidence_score,
                        created_at=current_time,
                        applies_to=pattern.domains
                    )
                    new_insights.append(insight)
            
            # Insight 2: High-performing patterns
            high_performers = [p for p in self.patterns.values() if p.success_rate > 0.9 and p.usage_count >= 2]
            if high_performers:
                best_pattern = max(high_performers, key=lambda x: x.success_rate * x.confidence_score)
                insight = PerformanceInsight(
                    insight_id=f"high_performer_{best_pattern.pattern_id}",
                    category="optimization",
                    description=f"Pattern {best_pattern.pattern_id} shows excellent performance ({best_pattern.success_rate:.1%} success)",
                    recommendation=f"Prefer {best_pattern.strategy} strategy for {'+'.join(best_pattern.domains)} coordination",
                    impact_score=0.6,
                    confidence=best_pattern.confidence_score,
                    created_at=current_time,
                    applies_to=best_pattern.domains
                )
                new_insights.append(insight)
            
            # Insight 3: Performance degradation
            recent_patterns = [p for p in self.patterns.values() if p.last_used > current_time - 3600]
            if recent_patterns:
                avg_recent_success = sum(p.success_rate for p in recent_patterns) / len(recent_patterns)
                if avg_recent_success < 0.8:
                    insight = PerformanceInsight(
                        insight_id="recent_degradation",
                        category="monitoring",
                        description=f"Recent coordination success rate is {avg_recent_success:.1%}, below optimal",
                        recommendation="Review recent coordination failures and consider system resource constraints",
                        impact_score=0.9,
                        confidence=0.7,
                        created_at=current_time,
                        applies_to=["all"]
                    )
                    new_insights.append(insight)
            
            # Insight 4: Underutilized strategies
            strategy_stats = analytics.get("strategy_analytics", {})
            total_coordinations = sum(s["usage_count"] for s in strategy_stats.values())
            
            if total_coordinations > 10:
                for strategy, stats in strategy_stats.items():
                    if stats["success_rate"] > 0.85 and stats["usage_count"] / total_coordinations < 0.1:
                        insight = PerformanceInsight(
                            insight_id=f"underutilized_{strategy}",
                            category="optimization",
                            description=f"Strategy '{strategy}' has high success rate ({stats['success_rate']:.1%}) but low usage",
                            recommendation=f"Consider using '{strategy}' strategy more frequently for applicable scenarios",
                            impact_score=0.4,
                            confidence=0.6,
                            created_at=current_time,
                            applies_to=["strategy_selection"]
                        )
                        new_insights.append(insight)
        
        # Add new insights to collection
        self.insights.extend(new_insights)
        
        # Keep only recent insights (last 24 hours) - always do cleanup
        self.insights = [i for i in self.insights if i.created_at > current_time - 86400]
        
        self._save_insights()
        
        return new_insights
    
    def get_pattern_recommendations(self, domains: List[str], agent_count: int) -> Dict[str, Any]:
        """
        Get pattern-based recommendations for coordination.
        
        Args:
            domains: Domains involved in coordination
            agent_count: Number of agents needed
            
        Returns:
            Dictionary with recommendations
        """
        matching_patterns = []
        
        # Find patterns that match domains and agent count
        for pattern in self.patterns.values():
            domain_overlap = set(domains).intersection(set(pattern.domains))
            if domain_overlap and abs(pattern.agent_count - agent_count) <= 2:
                similarity_score = len(domain_overlap) / max(len(domains), len(pattern.domains))
                agent_score = 1.0 - abs(pattern.agent_count - agent_count) / 10.0
                
                matching_patterns.append({
                    "pattern": pattern,
                    "similarity_score": similarity_score,
                    "agent_score": agent_score,
                    "total_score": similarity_score * pattern.confidence_score * agent_score
                })
        
        # Sort by total score
        matching_patterns.sort(key=lambda x: x["total_score"], reverse=True)
        
        recommendations = {
            "recommended_strategy": None,
            "confidence": 0.0,
            "estimated_duration": None,
            "success_probability": 0.0,
            "matching_patterns": len(matching_patterns),
            "alternatives": []
        }
        
        if matching_patterns:
            best_match = matching_patterns[0]
            best_pattern = best_match["pattern"]
            
            recommendations.update({
                "recommended_strategy": best_pattern.strategy,
                "confidence": best_pattern.confidence_score,
                "estimated_duration": best_pattern.avg_duration,
                "success_probability": best_pattern.success_rate,
                "alternatives": [
                    {
                        "strategy": match["pattern"].strategy,
                        "confidence": match["pattern"].confidence_score,
                        "success_rate": match["pattern"].success_rate,
                        "similarity": match["similarity_score"]
                    }
                    for match in matching_patterns[1:3]  # Top 2 alternatives
                ]
            })
        
        return recommendations
    
    def _invalidate_cache(self) -> None:
        """Invalidate analytics cache."""
        self._analytics_cache = {}
        self._cache_timestamp = 0
    
    def _load_data(self) -> None:
        """Load existing tracking data."""
        # Load events
        events_file = self.data_dir / "events.json"
        if events_file.exists():
            try:
                with open(events_file, 'r') as f:
                    events_data = json.load(f)
                    self.events = [
                        CoordinationEvent(
                            event_id=e["event_id"],
                            event_type=CoordinationEventType(e["event_type"]),
                            timestamp=e["timestamp"],
                            agent_count=e["agent_count"],
                            domains=e["domains"],
                            strategy=e["strategy"],
                            duration=e.get("duration"),
                            success=e.get("success"),
                            agents_used=e.get("agents_used"),
                            error_message=e.get("error_message")
                        )
                        for e in events_data
                    ]
            except (json.JSONDecodeError, KeyError):
                self.events = []
        
        # Load patterns
        patterns_file = self.data_dir / "patterns.json"
        if patterns_file.exists():
            try:
                with open(patterns_file, 'r') as f:
                    patterns_data = json.load(f)
                    self.patterns = {
                        pattern_id: CoordinationPattern(
                            pattern_id=p["pattern_id"],
                            pattern_type=PatternType(p["pattern_type"]),
                            domains=p["domains"],
                            agent_count=p["agent_count"],
                            strategy=p["strategy"],
                            success_rate=p["success_rate"],
                            avg_duration=p["avg_duration"],
                            usage_count=p["usage_count"],
                            last_used=p["last_used"],
                            confidence_score=p["confidence_score"]
                        )
                        for pattern_id, p in patterns_data.items()
                    }
            except (json.JSONDecodeError, KeyError):
                self.patterns = {}
        
        # Load insights
        insights_file = self.data_dir / "insights.json"
        if insights_file.exists():
            try:
                with open(insights_file, 'r') as f:
                    insights_data = json.load(f)
                    self.insights = [
                        PerformanceInsight(
                            insight_id=i["insight_id"],
                            category=i["category"],
                            description=i["description"],
                            recommendation=i["recommendation"],
                            impact_score=i["impact_score"],
                            confidence=i["confidence"],
                            created_at=i["created_at"],
                            applies_to=i["applies_to"]
                        )
                        for i in insights_data
                    ]
            except (json.JSONDecodeError, KeyError):
                self.insights = []
    
    def _save_events(self) -> None:
        """Save events to disk."""
        events_file = self.data_dir / "events.json"
        try:
            with open(events_file, 'w') as f:
                events_data = []
                for event in self.events:
                    event_dict = asdict(event)
                    # Convert enum to string for JSON serialization
                    event_dict['event_type'] = event.event_type.value
                    events_data.append(event_dict)
                json.dump(events_data, f, indent=2)
        except IOError:
            pass  # Fail silently
    
    def _save_patterns(self) -> None:
        """Save patterns to disk."""
        patterns_file = self.data_dir / "patterns.json"
        try:
            with open(patterns_file, 'w') as f:
                patterns_data = {}
                for k, pattern in self.patterns.items():
                    pattern_dict = asdict(pattern)
                    # Convert enum to string for JSON serialization
                    pattern_dict['pattern_type'] = pattern.pattern_type.value
                    patterns_data[k] = pattern_dict
                json.dump(patterns_data, f, indent=2)
        except IOError:
            pass  # Fail silently
    
    def _save_insights(self) -> None:
        """Save insights to disk."""
        insights_file = self.data_dir / "insights.json"
        try:
            with open(insights_file, 'w') as f:
                json.dump([asdict(insight) for insight in self.insights], f, indent=2)
        except IOError:
            pass  # Fail silently


# Global instance for system-wide usage
coordination_tracker = ClaudeCodeCoordinationTracker()


def main():
    """Example usage and demonstration."""
    tracker = ClaudeCodeCoordinationTracker()
    
    print("Claude Code Coordination Tracker - Example Usage")
    print("=" * 55)
    
    # Simulate some coordination events
    import uuid
    
    # Example 1: Successful testing coordination
    event_id = str(uuid.uuid4())
    print(f"\nExample 1: Testing Coordination (ID: {event_id[:8]})")
    tracker.start_coordination(event_id, 2, ["testing"], "single_parallel", ["test-specialist", "coverage-optimizer"])
    time.sleep(0.1)  # Simulate work
    tracker.complete_coordination(event_id, success=True)
    
    # Example 2: Complex infrastructure coordination
    event_id = str(uuid.uuid4())
    print(f"Example 2: Infrastructure Coordination (ID: {event_id[:8]})")
    tracker.start_coordination(event_id, 4, ["infrastructure", "security"], "batch_parallel")
    time.sleep(0.2)  # Simulate work
    tracker.complete_coordination(event_id, success=True)
    
    # Example 3: Failed coordination
    event_id = str(uuid.uuid4())
    print(f"Example 3: Failed Coordination (ID: {event_id[:8]})")
    tracker.start_coordination(event_id, 6, ["testing", "performance"], "batch_parallel")
    time.sleep(0.05)  # Simulate quick failure
    tracker.complete_coordination(event_id, success=False, error_message="Timeout occurred")
    
    # Get analytics
    print("\nAnalytics Summary:")
    analytics = tracker.get_analytics()
    print(f"Total Events: {analytics['summary']['total_events']}")
    print(f"Success Rate: {analytics['summary']['success_rate']:.1%}")
    print(f"Patterns Learned: {analytics['summary']['total_patterns_learned']}")
    
    # Generate insights
    print("\nGenerated Insights:")
    insights = tracker.generate_insights()
    for insight in insights:
        print(f"- {insight.category.title()}: {insight.description}")
        print(f"  Recommendation: {insight.recommendation}")
    
    # Get recommendations
    print("\nPattern Recommendations for testing + security (3 agents):")
    recommendations = tracker.get_pattern_recommendations(["testing", "security"], 3)
    if recommendations["recommended_strategy"]:
        print(f"Strategy: {recommendations['recommended_strategy']}")
        print(f"Confidence: {recommendations['confidence']:.2f}")
        print(f"Success Probability: {recommendations['success_probability']:.1%}")
    else:
        print("No matching patterns found")


if __name__ == "__main__":
    main()