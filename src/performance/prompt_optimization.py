"""
Agent Coordination Prompt Optimization System

Analyzes and optimizes agent coordination prompts for improved efficiency
and reduced response time as specified in story acceptance criteria.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

from .token_estimation import TokenEstimator, PromptType, ModelType


class OptimizationLevel(Enum):
    """Levels of prompt optimization."""
    MINIMAL = "minimal"          # Basic cleanup only
    STANDARD = "standard"        # Standard optimization
    AGGRESSIVE = "aggressive"    # Maximum optimization


@dataclass
class PromptAnalysis:
    """Analysis results for a coordination prompt."""
    original_length: int
    optimized_length: int
    token_reduction: int
    verbosity_score: float
    complexity_score: float
    optimization_opportunities: List[str]
    optimized_prompt: str
    performance_impact: Dict[str, float]


class PromptOptimizer:
    """
    Optimizes agent coordination prompts for efficiency and clarity.
    
    Features:
    - Removes unnecessary verbosity
    - Streamlines coordination instructions
    - Maintains semantic meaning
    - Provides performance metrics
    """
    
    def __init__(self):
        """Initialize prompt optimizer."""
        self.token_estimator = TokenEstimator()
        
        # Common verbose patterns to optimize
        self.verbose_patterns = {
            # Redundant phrases
            r'\bplease\s+': '',
            r'\bkindly\s+': '',
            r'\bI\s+would\s+like\s+you\s+to\s+': '',
            r'\bCould\s+you\s+please\s+': '',
            r'\bI\s+need\s+you\s+to\s+': '',
            
            # Redundant coordination phrases
            r'\bFor\s+this\s+task,?\s*': '',
            r'\bIn\s+order\s+to\s+': 'To ',
            r'\bIt\s+is\s+important\s+that\s+': '',
            r'\bMake\s+sure\s+that\s+': 'Ensure ',
            r'\bBe\s+sure\s+to\s+': '',
            
            # Wordy connectors
            r'\bdue\s+to\s+the\s+fact\s+that\b': 'because',
            r'\bin\s+spite\s+of\s+the\s+fact\s+that\b': 'although',
            r'\bfor\s+the\s+purpose\s+of\b': 'to',
            r'\bwith\s+regard\s+to\b': 'regarding',
            r'\bin\s+relation\s+to\b': 'regarding',
            
            # Filler words
            r'\b(very|really|quite|rather|fairly|pretty)\s+': '',
            r'\bactually\s+': '',
            r'\bobviously\s+': '',
            r'\bclearly\s+': '',
            
            # Multiple spaces
            r'\s{2,}': ' ',
        }
        
        # Coordination-specific optimizations
        self.coordination_optimizations = {
            # Agent invocation patterns
            r'Please\s+use\s+the\s+Task\s+tool\s+to\s+launch.*?with\s+the\s+([^.]+)\s+agent': r'Task(\1)',
            r'I\'m\s+going\s+to\s+use\s+the\s+Task\s+tool.*?(\w+-\w+)\s+agent': r'Using Task(\1)',
            r'Let\s+me\s+use\s+the\s+Task\s+tool.*?(\w+-\w+)\s+agent': r'Task(\1)',
            
            # Coordination flow patterns
            r'First,?\s+let\'s\s+': '',
            r'Now,?\s+let\'s\s+': '',
            r'Next,?\s+we\s+need\s+to\s+': '',
            r'After\s+that,?\s+': '',
            r'Finally,?\s+': '',
            
            # Verbose agent descriptions
            r'specialized\s+agent\s+for\s+': 'agent: ',
            r'agent\s+that\s+specializes\s+in\s+': 'agent: ',
            r'expert\s+in\s+': '',
        }
        
        # Critical phrases to preserve (never optimize these)
        self.preserve_patterns = {
            r'CLAUDE_TOOL_PARAMETER_\w+',
            r'@[\w/.]+',  # Memory imports
            r'claude\s+mcp',  # Claude MCP commands
            r'Task\([^)]+\)',  # Task tool calls
            r'AC:\s*\d+',  # Acceptance criteria references
        }
    
    def analyze_prompt(self, prompt: str, prompt_type: PromptType = PromptType.AGENT_COORDINATION) -> PromptAnalysis:
        """
        Analyze prompt for optimization opportunities.
        
        Args:
            prompt: The prompt to analyze
            prompt_type: Type of coordination prompt
            
        Returns:
            Detailed analysis of optimization opportunities
        """
        original_tokens = self.token_estimator.count_tokens(prompt)
        verbosity_score = self._calculate_verbosity_score(prompt)
        complexity_score = self._calculate_complexity_score(prompt)
        
        # Identify optimization opportunities
        opportunities = self._identify_opportunities(prompt)
        
        # Generate optimized version
        optimized_prompt = self.optimize_prompt(prompt, OptimizationLevel.STANDARD)
        optimized_tokens = self.token_estimator.count_tokens(optimized_prompt)
        
        # Calculate performance impact
        performance_impact = self._estimate_performance_impact(
            original_tokens, optimized_tokens, prompt_type
        )
        
        return PromptAnalysis(
            original_length=len(prompt),
            optimized_length=len(optimized_prompt),
            token_reduction=original_tokens - optimized_tokens,
            verbosity_score=verbosity_score,
            complexity_score=complexity_score,
            optimization_opportunities=opportunities,
            optimized_prompt=optimized_prompt,
            performance_impact=performance_impact
        )
    
    def optimize_prompt(self, prompt: str, level: OptimizationLevel = OptimizationLevel.STANDARD) -> str:
        """
        Optimize prompt for efficiency while preserving meaning.
        
        Args:
            prompt: Original prompt
            level: Optimization level
            
        Returns:
            Optimized prompt
        """
        optimized = prompt
        
        # Preserve critical patterns
        preserved_patterns = {}
        for i, pattern in enumerate(self.preserve_patterns):
            matches = re.findall(pattern, optimized, re.IGNORECASE)
            for match in matches:
                placeholder = f"__PRESERVE_{i}_{hash(match)}__"
                preserved_patterns[placeholder] = match
                optimized = optimized.replace(match, placeholder)
        
        # Apply optimizations based on level
        if level in [OptimizationLevel.MINIMAL, OptimizationLevel.STANDARD, OptimizationLevel.AGGRESSIVE]:
            optimized = self._apply_basic_optimizations(optimized)
        
        if level in [OptimizationLevel.STANDARD, OptimizationLevel.AGGRESSIVE]:
            optimized = self._apply_coordination_optimizations(optimized)
        
        if level == OptimizationLevel.AGGRESSIVE:
            optimized = self._apply_aggressive_optimizations(optimized)
        
        # Restore preserved patterns
        for placeholder, original in preserved_patterns.items():
            optimized = optimized.replace(placeholder, original)
        
        # Final cleanup
        optimized = self._final_cleanup(optimized)
        
        return optimized.strip()
    
    def _apply_basic_optimizations(self, prompt: str) -> str:
        """Apply basic verbose pattern removal."""
        optimized = prompt
        
        for pattern, replacement in self.verbose_patterns.items():
            optimized = re.sub(pattern, replacement, optimized, flags=re.IGNORECASE)
        
        return optimized
    
    def _apply_coordination_optimizations(self, prompt: str) -> str:
        """Apply coordination-specific optimizations."""
        optimized = prompt
        
        for pattern, replacement in self.coordination_optimizations.items():
            optimized = re.sub(pattern, replacement, optimized, flags=re.IGNORECASE)
        
        return optimized
    
    def _apply_aggressive_optimizations(self, prompt: str) -> str:
        """Apply aggressive optimizations (more risk of semantic change)."""
        optimized = prompt
        
        # More aggressive patterns
        aggressive_patterns = {
            r'\bI\s+think\s+': '',
            r'\bI\s+believe\s+': '',
            r'\bin\s+my\s+opinion\s+': '',
            r'\bit\s+seems\s+': '',
            r'\bapparently\s+': '',
            r'\bbasically\s+': '',
            r'\bessentially\s+': '',
            
            # Simplify conditional language
            r'\bwould\s+be\s+able\s+to\s+': 'can ',
            r'\bmight\s+be\s+able\s+to\s+': 'could ',
            r'\bshould\s+be\s+able\s+to\s+': 'can ',
            
            # Simplify temporal phrases
            r'\bat\s+this\s+point\s+in\s+time\b': 'now',
            r'\bat\s+the\s+present\s+time\b': 'now',
            r'\bin\s+the\s+near\s+future\b': 'soon',
        }
        
        for pattern, replacement in aggressive_patterns.items():
            optimized = re.sub(pattern, replacement, optimized, flags=re.IGNORECASE)
        
        return optimized
    
    def _final_cleanup(self, prompt: str) -> str:
        """Final cleanup of the optimized prompt."""
        # Remove extra punctuation
        optimized = re.sub(r'[.]{2,}', '.', prompt)
        optimized = re.sub(r'[,]{2,}', ',', optimized)
        
        # Fix spacing around punctuation
        optimized = re.sub(r'\s+([.!?,:;])', r'\1', optimized)
        optimized = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', optimized)
        
        # Normalize whitespace
        optimized = re.sub(r'\s+', ' ', optimized)
        optimized = re.sub(r'\n\s*\n\s*\n+', '\n\n', optimized)
        
        return optimized
    
    def _calculate_verbosity_score(self, prompt: str) -> float:
        """Calculate verbosity score (higher = more verbose)."""
        total_words = len(prompt.split())
        
        if total_words == 0:
            return 0.0
        
        # Count verbose patterns
        verbose_matches = 0
        for pattern in self.verbose_patterns:
            verbose_matches += len(re.findall(pattern, prompt, re.IGNORECASE))
        
        # Count coordination verbosity
        coord_verbose_matches = 0
        for pattern in self.coordination_optimizations:
            coord_verbose_matches += len(re.findall(pattern, prompt, re.IGNORECASE))
        
        verbosity_score = ((verbose_matches + coord_verbose_matches) / total_words) * 100
        return min(verbosity_score, 100.0)  # Cap at 100%
    
    def _calculate_complexity_score(self, prompt: str) -> float:
        """Calculate complexity score (higher = more complex)."""
        words = prompt.split()
        sentences = re.split(r'[.!?]+', prompt)
        
        if not words or not sentences:
            return 0.0
        
        # Average words per sentence
        avg_words_per_sentence = len(words) / len(sentences)
        
        # Count complex constructions
        complex_patterns = [
            r'\bwhich\b', r'\bthat\b', r'\bwhere\b', r'\bwhen\b',
            r'\bhowever\b', r'\bnevertheless\b', r'\bfurthermore\b',
            r'\bmoreover\b', r'\btherefore\b', r'\bconsequently\b'
        ]
        
        complex_matches = sum(
            len(re.findall(pattern, prompt, re.IGNORECASE))
            for pattern in complex_patterns
        )
        
        complexity_ratio = complex_matches / len(words)
        sentence_complexity = min(avg_words_per_sentence / 20, 1.0)  # Normalize to 0-1
        
        return (complexity_ratio + sentence_complexity) * 50  # Scale to 0-100
    
    def _identify_opportunities(self, prompt: str) -> List[str]:
        """Identify specific optimization opportunities."""
        opportunities = []
        
        # Check for verbose patterns
        for pattern in self.verbose_patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                opportunities.append(f"Remove verbose pattern: {pattern[:20]}...")
        
        # Check for coordination verbosity
        for pattern in self.coordination_optimizations:
            if re.search(pattern, prompt, re.IGNORECASE):
                opportunities.append(f"Streamline coordination: {pattern[:20]}...")
        
        # Check sentence length
        sentences = re.split(r'[.!?]+', prompt)
        long_sentences = [s for s in sentences if len(s.split()) > 25]
        if long_sentences:
            opportunities.append(f"Simplify {len(long_sentences)} long sentences")
        
        # Check for repetition
        words = prompt.lower().split()
        word_freq = {}
        for word in words:
            if len(word) > 4:  # Only check longer words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        repeated_words = [word for word, count in word_freq.items() if count > 3]
        if repeated_words:
            opportunities.append(f"Reduce repetition of {len(repeated_words)} words")
        
        return opportunities
    
    def _estimate_performance_impact(self, 
                                   original_tokens: int,
                                   optimized_tokens: int,
                                   prompt_type: PromptType) -> Dict[str, float]:
        """Estimate performance impact of optimization."""
        if original_tokens == 0:
            return {"token_reduction_percent": 0.0, "estimated_time_savings_ms": 0.0, "cost_savings_percent": 0.0}
        
        token_reduction_percent = ((original_tokens - optimized_tokens) / original_tokens) * 100
        
        # Estimate time savings (rough approximation)
        # Assume ~1ms per 10 tokens processing time
        time_savings_ms = (original_tokens - optimized_tokens) * 0.1
        
        # Estimate cost savings (same as token reduction for both input and output)
        cost_savings_percent = token_reduction_percent
        
        return {
            "token_reduction_percent": round(token_reduction_percent, 2),
            "estimated_time_savings_ms": round(time_savings_ms, 2),
            "cost_savings_percent": round(cost_savings_percent, 2)
        }
    
    def batch_optimize_prompts(self, 
                             prompts: Dict[str, str],
                             level: OptimizationLevel = OptimizationLevel.STANDARD) -> Dict[str, PromptAnalysis]:
        """
        Optimize multiple prompts in batch.
        
        Args:
            prompts: Dictionary of prompt_name -> prompt_text
            level: Optimization level to apply
            
        Returns:
            Dictionary of prompt_name -> analysis results
        """
        results = {}
        
        for name, prompt in prompts.items():
            analysis = self.analyze_prompt(prompt)
            analysis.optimized_prompt = self.optimize_prompt(prompt, level)
            
            # Recalculate metrics with the final optimized prompt
            optimized_tokens = self.token_estimator.count_tokens(analysis.optimized_prompt)
            original_tokens = self.token_estimator.count_tokens(prompt)
            
            analysis.token_reduction = original_tokens - optimized_tokens
            analysis.optimized_length = len(analysis.optimized_prompt)
            analysis.performance_impact = self._estimate_performance_impact(
                original_tokens, optimized_tokens, PromptType.AGENT_COORDINATION
            )
            
            results[name] = analysis
        
        return results
    
    def generate_optimization_report(self, 
                                   analyses: Dict[str, PromptAnalysis]) -> Dict[str, Any]:
        """
        Generate comprehensive optimization report.
        
        Args:
            analyses: Dictionary of prompt analyses
            
        Returns:
            Comprehensive optimization report
        """
        if not analyses:
            return {"error": "No analyses provided"}
        
        total_original_tokens = sum(
            self.token_estimator.count_tokens(analysis.optimized_prompt) + analysis.token_reduction
            for analysis in analyses.values()
        )
        
        total_optimized_tokens = sum(
            self.token_estimator.count_tokens(analysis.optimized_prompt)
            for analysis in analyses.values()
        )
        
        total_token_reduction = total_original_tokens - total_optimized_tokens
        
        avg_verbosity = sum(analysis.verbosity_score for analysis in analyses.values()) / len(analyses)
        avg_complexity = sum(analysis.complexity_score for analysis in analyses.values()) / len(analyses)
        
        # Calculate aggregate performance impact
        total_time_savings = sum(
            analysis.performance_impact["estimated_time_savings_ms"]
            for analysis in analyses.values()
        )
        
        overall_reduction_percent = (total_token_reduction / total_original_tokens * 100) if total_original_tokens > 0 else 0
        
        return {
            "summary": {
                "total_prompts_analyzed": len(analyses),
                "total_token_reduction": total_token_reduction,
                "overall_reduction_percent": round(overall_reduction_percent, 2),
                "total_time_savings_ms": round(total_time_savings, 2),
                "average_verbosity_score": round(avg_verbosity, 2),
                "average_complexity_score": round(avg_complexity, 2)
            },
            "by_prompt": {
                name: {
                    "token_reduction": analysis.token_reduction,
                    "length_reduction": analysis.original_length - analysis.optimized_length,
                    "verbosity_score": analysis.verbosity_score,
                    "opportunities_count": len(analysis.optimization_opportunities),
                    "performance_impact": analysis.performance_impact
                }
                for name, analysis in analyses.items()
            },
            "top_opportunities": self._get_top_opportunities(analyses),
            "recommendations": self._generate_recommendations(analyses)
        }
    
    def _get_top_opportunities(self, analyses: Dict[str, PromptAnalysis]) -> List[Dict[str, Any]]:
        """Get top optimization opportunities across all prompts."""
        opportunity_counts = {}
        
        for name, analysis in analyses.items():
            for opportunity in analysis.optimization_opportunities:
                base_opportunity = opportunity.split(':')[0] if ':' in opportunity else opportunity
                if base_opportunity not in opportunity_counts:
                    opportunity_counts[base_opportunity] = {"count": 0, "prompts": []}
                opportunity_counts[base_opportunity]["count"] += 1
                opportunity_counts[base_opportunity]["prompts"].append(name)
        
        # Sort by frequency
        sorted_opportunities = sorted(
            opportunity_counts.items(),
            key=lambda x: x[1]["count"],
            reverse=True
        )
        
        return [
            {
                "opportunity": opp,
                "frequency": data["count"],
                "affected_prompts": data["prompts"][:5]  # Top 5 affected prompts
            }
            for opp, data in sorted_opportunities[:10]  # Top 10 opportunities
        ]
    
    def _generate_recommendations(self, analyses: Dict[str, PromptAnalysis]) -> List[str]:
        """Generate optimization recommendations."""
        recommendations = []
        
        # Check overall verbosity
        high_verbosity_prompts = [
            name for name, analysis in analyses.items()
            if analysis.verbosity_score > 15
        ]
        
        if high_verbosity_prompts:
            recommendations.append(
                f"Focus on reducing verbosity in {len(high_verbosity_prompts)} high-verbosity prompts"
            )
        
        # Check complexity
        high_complexity_prompts = [
            name for name, analysis in analyses.items()
            if analysis.complexity_score > 40
        ]
        
        if high_complexity_prompts:
            recommendations.append(
                f"Simplify sentence structure in {len(high_complexity_prompts)} complex prompts"
            )
        
        # Check token reduction potential
        low_optimization_prompts = [
            name for name, analysis in analyses.items()
            if analysis.performance_impact["token_reduction_percent"] < 10
        ]
        
        if len(low_optimization_prompts) < len(analyses) * 0.3:  # If most prompts show good optimization
            recommendations.append("Apply aggressive optimization to maximize token reduction")
        
        # Check for coordination-specific optimizations
        total_opportunities = sum(
            len(analysis.optimization_opportunities) for analysis in analyses.values()
        )
        
        if total_opportunities > len(analyses) * 2:  # More than 2 opportunities per prompt on average
            recommendations.append("Consider systematic refactoring of coordination patterns")
        
        return recommendations


# Global optimizer instance
_optimizer: Optional[PromptOptimizer] = None


def get_prompt_optimizer() -> PromptOptimizer:
    """Get or create global prompt optimizer."""
    global _optimizer
    if _optimizer is None:
        _optimizer = PromptOptimizer()
    return _optimizer


def optimize_agent_prompt(prompt: str, level: OptimizationLevel = OptimizationLevel.STANDARD) -> str:
    """
    Convenience function to optimize a single agent coordination prompt.
    
    Args:
        prompt: The prompt to optimize
        level: Optimization level
        
    Returns:
        Optimized prompt
    """
    optimizer = get_prompt_optimizer()
    return optimizer.optimize_prompt(prompt, level)


def analyze_agent_prompt_efficiency(prompt: str) -> PromptAnalysis:
    """
    Convenience function to analyze agent prompt efficiency.
    
    Args:
        prompt: The prompt to analyze
        
    Returns:
        Analysis results
    """
    optimizer = get_prompt_optimizer()
    return optimizer.analyze_prompt(prompt)