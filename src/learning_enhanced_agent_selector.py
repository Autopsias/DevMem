"""Learning-Enhanced Agent Selector for Claude Code Agent Framework.

Integrates learning capabilities with the existing agent selection system
to improve accuracy while maintaining performance and reliability.
"""

import time
import logging
from typing import Dict, List, Tuple, Optional, NamedTuple
from dataclasses import dataclass

# Import learning components
try:
    from .enhanced_pattern_learning_engine import EnhancedPatternLearningEngine
    from .enhanced_success_pattern_recorder import EnhancedSuccessPatternRecorder
    from .anthropic_guidelines_validator import AnthropicGuidelinesValidator, ValidationResult
except ImportError:
    # Fallback imports for testing
    EnhancedPatternLearningEngine = None
    EnhancedSuccessPatternRecorder = None
    AnthropicGuidelinesValidator = None
    ValidationResult = None

# Import existing agent selector if available
try:
    from .agent_selector import EnhancedAgentSelector, PatternSuccessMetrics
    AGENT_SELECTOR_AVAILABLE = True
except ImportError:
    AGENT_SELECTOR_AVAILABLE = False
    # Create minimal classes for standalone operation
    class PatternSuccessMetrics(NamedTuple):
        accuracy: float
        response_time: float
        context_preservation: float
        coordination_success: float
        confidence: float
        timestamp: float

logger = logging.getLogger(__name__)


@dataclass
class AgentSelectionResult:
    """Result of agent selection with learning enhancement."""
    agent_name: str
    confidence_score: float
    reasoning: str
    learning_applied: bool = False
    learning_confidence_boost: float = 0.0
    validation_result: Optional[ValidationResult] = None
    selection_time_ms: float = 0.0
    fallback_used: bool = False


class LearningEnhancedAgentSelector:
    """Agent selector with learning capabilities for improved accuracy."""
    
    def __init__(self, coordination_hub_path: Optional[str] = None):
        """Initialize learning-enhanced agent selector."""
        self.coordination_hub_path = coordination_hub_path
        
        # Initialize learning components with error handling
        self.learning_engine = None
        self.pattern_recorder = None
        self.guidelines_validator = None
        self.fallback_selector = None
        
        self._initialize_learning_components()
        self._initialize_fallback_selector()
        
        # Performance tracking
        self.selection_history = []
        self.learning_stats = {
            'total_selections': 0,
            'learning_enhanced_selections': 0,
            'fallback_selections': 0,
            'avg_confidence_improvement': 0.0,
            'learning_overhead_ms': 0.0
        }
    
    def _initialize_learning_components(self):
        """Initialize learning components with graceful fallback."""
        try:
            if EnhancedPatternLearningEngine:
                self.learning_engine = EnhancedPatternLearningEngine(self.coordination_hub_path)
                logger.info(f"Initialized learning engine with {len(self.learning_engine.agent_profiles)} agent profiles")
            
            if EnhancedSuccessPatternRecorder:
                self.pattern_recorder = EnhancedSuccessPatternRecorder(self.coordination_hub_path)
                logger.info("Initialized success pattern recorder")
            
            if AnthropicGuidelinesValidator:
                self.guidelines_validator = AnthropicGuidelinesValidator()
                logger.info("Initialized Anthropic guidelines validator")
                
        except Exception as e:
            logger.warning(f"Failed to initialize learning components: {e}")
            logger.info("Will use fallback selection without learning enhancement")
    
    def _initialize_fallback_selector(self):
        """Initialize fallback agent selector."""
        if AGENT_SELECTOR_AVAILABLE:
            try:
                self.fallback_selector = EnhancedAgentSelector()
                logger.info("Initialized fallback agent selector")
            except Exception as e:
                logger.warning(f"Failed to initialize fallback selector: {e}")
    
    def select_agent(self, query: str, context: Optional[Dict] = None) -> AgentSelectionResult:
        """Select agent with learning enhancement and fallback."""
        start_time = time.time()
        self.learning_stats['total_selections'] += 1
        
        try:
            # Try learning-enhanced selection first
            if self.learning_engine:
                result = self._learning_enhanced_selection(query, context)
                if result:
                    result.selection_time_ms = (time.time() - start_time) * 1000
                    self.learning_stats['learning_enhanced_selections'] += 1
                    self._update_learning_stats(result)
                    return result
            
            # Fallback to standard selection
            return self._fallback_selection(query, context, start_time)
            
        except Exception as e:
            logger.error(f"Agent selection failed: {e}")
            return self._emergency_fallback(query, start_time)
    
    def _learning_enhanced_selection(self, query: str, context: Optional[Dict] = None) -> Optional[AgentSelectionResult]:
        """Perform learning-enhanced agent selection."""
        try:
            # Get enhanced suggestion from learning engine
            learning_start = time.time()
            suggestion = self.learning_engine.get_enhanced_agent_suggestion(query)
            learning_time = (time.time() - learning_start) * 1000
            
            self.learning_stats['learning_overhead_ms'] += learning_time
            
            if suggestion:
                agent_name, confidence = suggestion
                
                # Apply learning confidence boost
                original_confidence = confidence
                
                # Boost confidence based on agent profile match
                profile = self.learning_engine.get_agent_profile(agent_name)
                if profile:
                    specialization_boost = profile.specialization_score * 0.1
                    confidence = min(1.0, confidence + specialization_boost)
                
                learning_boost = confidence - original_confidence
                
                # Validate against Anthropic guidelines if validator available
                validation_result = None
                if self.guidelines_validator:
                    pattern = {
                        'pattern_key': f'enhanced_selection:{agent_name}',
                        'agent': agent_name,
                        'confidence': confidence,
                        'keywords': self.pattern_recorder._extract_query_keywords(query) if self.pattern_recorder else []
                    }
                    validation_result = self.guidelines_validator.validate_learning_pattern(pattern)
                    
                    # Reduce confidence if not compliant
                    if not validation_result.is_compliant:
                        confidence *= 0.8
                
                # Generate reasoning
                reasoning = f"Learning-enhanced selection based on agent description matching (confidence: {original_confidence:.3f}"
                if learning_boost > 0:
                    reasoning += f", boosted by {learning_boost:.3f} due to specialization"
                if validation_result and not validation_result.is_compliant:
                    reasoning += ", reduced due to compliance issues"
                reasoning += ")"
                
                return AgentSelectionResult(
                    agent_name=agent_name,
                    confidence_score=confidence,
                    reasoning=reasoning,
                    learning_applied=True,
                    learning_confidence_boost=learning_boost,
                    validation_result=validation_result,
                    fallback_used=False
                )
            
        except Exception as e:
            logger.warning(f"Learning-enhanced selection failed: {e}")
        
        return None
    
    def _fallback_selection(self, query: str, context: Optional[Dict], start_time: float) -> AgentSelectionResult:
        """Fallback to standard agent selection."""
        self.learning_stats['fallback_selections'] += 1
        
        if self.fallback_selector:
            try:
                result = self.fallback_selector.select_agent(query)
                return AgentSelectionResult(
                    agent_name=result.agent_name,
                    confidence_score=result.confidence_score,
                    reasoning=f"Fallback selection: {result.reasoning}",
                    learning_applied=False,
                    selection_time_ms=(time.time() - start_time) * 1000,
                    fallback_used=True
                )
            except Exception as e:
                logger.error(f"Fallback selector failed: {e}")
        
        # Simple keyword-based fallback
        return self._simple_keyword_selection(query, start_time)
    
    def _simple_keyword_selection(self, query: str, start_time: float) -> AgentSelectionResult:
        """Simple keyword-based agent selection as last resort."""
        query_lower = query.lower()
        
        # Simple keyword mapping
        keyword_agents = {
            'test': 'test-specialist',
            'pytest': 'test-specialist',
            'docker': 'infrastructure-engineer',
            'container': 'infrastructure-engineer',
            'security': 'security-enforcer',
            'performance': 'performance-optimizer',
            'documentation': 'documentation-enhancer'
        }
        
        for keyword, agent in keyword_agents.items():
            if keyword in query_lower:
                return AgentSelectionResult(
                    agent_name=agent,
                    confidence_score=0.6,  # Conservative confidence
                    reasoning=f"Simple keyword-based selection for '{keyword}'",
                    learning_applied=False,
                    selection_time_ms=(time.time() - start_time) * 1000,
                    fallback_used=True
                )
        
        # Ultimate fallback
        return AgentSelectionResult(
            agent_name='intelligent-enhancer',
            confidence_score=0.5,
            reasoning="Default fallback to intelligent-enhancer",
            learning_applied=False,
            selection_time_ms=(time.time() - start_time) * 1000,
            fallback_used=True
        )
    
    def _emergency_fallback(self, query: str, start_time: float) -> AgentSelectionResult:
        """Emergency fallback when everything fails."""
        return AgentSelectionResult(
            agent_name='intelligent-enhancer',
            confidence_score=0.4,
            reasoning="Emergency fallback - all selection methods failed",
            learning_applied=False,
            selection_time_ms=(time.time() - start_time) * 1000,
            fallback_used=True
        )
    
    def record_selection_feedback(self, query: str, selected_agent: str, 
                                confidence: float, success: bool = True,
                                user_feedback: Optional[bool] = None) -> bool:
        """Record feedback for learning improvement."""
        if not self.pattern_recorder or not success:
            return False
            
        try:
            success_metrics = {
                'confidence': confidence,
                'indicators': ['successful_selection'] if success else ['failed_selection']
            }
            
            if user_feedback is not None:
                success_metrics['user_feedback'] = user_feedback
            
            return self.pattern_recorder.record_successful_usage(query, selected_agent, success_metrics)
            
        except Exception as e:
            logger.error(f"Failed to record selection feedback: {e}")
            return False
    
    def _update_learning_stats(self, result: AgentSelectionResult):
        """Update learning statistics."""
        if result.learning_applied and result.learning_confidence_boost > 0:
            current_avg = self.learning_stats['avg_confidence_improvement']
            total_enhanced = self.learning_stats['learning_enhanced_selections']
            
            # Update running average
            new_avg = ((current_avg * (total_enhanced - 1)) + result.learning_confidence_boost) / total_enhanced
            self.learning_stats['avg_confidence_improvement'] = new_avg
    
    def get_selection_stats(self) -> Dict[str, any]:
        """Get selection statistics including learning performance."""
        stats = self.learning_stats.copy()
        
        # Add performance metrics
        if stats['total_selections'] > 0:
            stats['learning_usage_rate'] = stats['learning_enhanced_selections'] / stats['total_selections']
            stats['fallback_rate'] = stats['fallback_selections'] / stats['total_selections']
        else:
            stats['learning_usage_rate'] = 0.0
            stats['fallback_rate'] = 0.0
        
        # Add learning engine stats if available
        if self.learning_engine:
            enhancement_stats = self.learning_engine.get_learning_enhancement_stats()
            stats['learning_engine_stats'] = enhancement_stats
        
        # Add validation stats if available
        if self.guidelines_validator:
            stats['anthropic_compliance_thresholds'] = self.guidelines_validator.get_compliance_thresholds()
        
        return stats
    
    def get_agent_profiles(self) -> Dict[str, any]:
        """Get loaded agent profiles information."""
        if self.learning_engine:
            return {
                'profiles_loaded': len(self.learning_engine.agent_profiles),
                'profiles': {name: {
                    'keywords': profile.keywords,
                    'capabilities': profile.capabilities[:3],  # First 3 capabilities
                    'specialization_score': profile.specialization_score
                } for name, profile in self.learning_engine.agent_profiles.items()}
            }
        return {'profiles_loaded': 0, 'profiles': {}}
    
    def validate_learning_system(self) -> Dict[str, any]:
        """Validate the learning system components."""
        validation = {
            'learning_engine_available': self.learning_engine is not None,
            'pattern_recorder_available': self.pattern_recorder is not None,
            'guidelines_validator_available': self.guidelines_validator is not None,
            'fallback_selector_available': self.fallback_selector is not None,
            'coordination_hub_valid': False,
            'agent_profiles_loaded': 0
        }
        
        # Validate coordination hub
        if self.pattern_recorder:
            validation['coordination_hub_valid'] = self.pattern_recorder.validate_coordination_hub_format()
        
        # Count loaded agent profiles
        if self.learning_engine:
            validation['agent_profiles_loaded'] = len(self.learning_engine.agent_profiles)
        
        # Overall system health
        validation['system_health'] = (
            validation['learning_engine_available'] and
            validation['pattern_recorder_available'] and
            validation['coordination_hub_valid'] and
            validation['agent_profiles_loaded'] > 0
        )
        
        return validation
    
    def test_learning_accuracy(self, test_cases: List[Tuple[str, str]]) -> Dict[str, float]:
        """Test learning system accuracy against known correct selections."""
        if not test_cases:
            return {
                'accuracy': 0.0, 
                'total_tests': 0, 
                'correct_selections': 0, 
                'accuracy_percentage': 0.0
            }
        
        if not self.learning_engine:
            # Still test basic selection accuracy even without learning
            correct = 0
            total = len(test_cases)
            
            for query, expected_agent in test_cases:
                result = self.select_agent(query)
                if result.agent_name == expected_agent:
                    correct += 1
            
            accuracy = correct / total if total > 0 else 0.0
            
            return {
                'accuracy': accuracy,
                'correct_selections': correct,
                'total_tests': total,
                'accuracy_percentage': accuracy * 100
            }
        
        correct = 0
        total = len(test_cases)
        
        for query, expected_agent in test_cases:
            result = self.select_agent(query)
            if result.agent_name == expected_agent:
                correct += 1
                # Record as successful for learning
                self.record_selection_feedback(query, result.agent_name, result.confidence_score, True)
        
        accuracy = correct / total if total > 0 else 0.0
        
        return {
            'accuracy': accuracy,
            'correct_selections': correct,
            'total_tests': total,
            'accuracy_percentage': accuracy * 100
        }
