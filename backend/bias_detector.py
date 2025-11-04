"""Cognitive bias detection module."""
import re
from typing import List, Dict
from collections import Counter


class BiasDetector:
    """Detect cognitive biases in journal entries."""
    
    def __init__(self):
        """Initialize bias detection patterns."""
        self.setup_patterns()
    
    def setup_patterns(self):
        """Setup regex patterns for bias detection."""
        # Catastrophizing: absolutist language + negative sentiment
        self.catastrophizing_patterns = [
            r'\b(always|never|everything|nothing|everyone|no one)\b.*(terrible|awful|horrible|worst|disaster|ruined)',
            r'\b(can\'t|cannot|couldn\'t|won\'t|wouldn\'t)\b.*(anything|ever|never|always)',
            r'\b(end|over|finished|done for|hopeless)\b'
        ]
        
        # Black-and-white thinking: binary language patterns
        self.black_white_patterns = [
            r'\b(all|none|every|nothing|everything)\b',
            r'\b(either|or).*\b(or|but not)',
            r'\b(perfect|flawless|terrible|awful)\b',
            r'\b(always|never)\b',
            r'\b(completely|totally|absolutely)\s+(wrong|right|bad|good)'
        ]
        
        # Emotional reasoning: feelings as facts
        self.emotional_reasoning_patterns = [
            r'\b(i feel|feels like|i sense).*\b(so|therefore|that means|which means|this proves)',
            r'\b(must be|cannot be|has to be)\b.*\b(because|since|as)\b.*\b(i feel|feeling|emotion)',
            r'\b(i feel|feeling).*\b(it\'s|it is|that\'s|this is|they are|he is|she is)'
        ]
        
        # Fortune telling: unsubstantiated negative predictions
        self.fortune_telling_patterns = [
            r'\b(will|going to|gonna)\b.*\b(bad|terrible|awful|horrible|worst|fail|screw up|mess up)',
            r'\b(it\'s|it is|things are|this will|that will).*\b(going to|about to).*\b(go wrong|fail|collapse|end badly)',
            r'\b(know|certain|sure)\b.*\b(will|going to)\b.*\b(bad|terrible|wrong|fail)'
        ]
        
        # Overgeneralization: isolated incidents as universal patterns
        self.overgeneralization_patterns = [
            r'\b(always|never|every|all|no one|everyone|everything|nothing)\b.*\b(happens|happened|will happen)',
            r'\b(one|once|single|this time).*\b(always|never|every|all)',
            r'\b(every time|whenever|always when|never when)\b',
            r'\b(all|every).*\b(are|is|do|does|have|has)\b.*\b(like|similar to|the same as)\b'
        ]
    
    def detect_all(self, text: str, sentiment_valence: float) -> List[Dict]:
        """
        Detect all cognitive biases in text.
        
        Args:
            text: Journal entry text
            sentiment_valence: Sentiment valence score (-1 to 1)
        
        Returns:
            List of detected biases with type, pattern, and explanation
        """
        text_lower = text.lower()
        detected_biases = []
        
        # Catastrophizing (requires negative sentiment)
        if sentiment_valence < -0.2:
            for pattern in self.catastrophizing_patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    detected_biases.append({
                        'type': 'Catastrophizing',
                        'pattern': self._extract_match(text, pattern),
                        'explanation': 'You may be magnifying negative events and expecting the worst possible outcomes.'
                    })
                    break
        
        # Black-and-white thinking
        matches = sum(1 for pattern in self.black_white_patterns 
                     if re.search(pattern, text_lower, re.IGNORECASE))
        if matches >= 2:  # Need multiple patterns
            detected_biases.append({
                'type': 'Black-and-white Thinking',
                'pattern': 'Binary language patterns detected',
                'explanation': 'You may be thinking in extremes without considering nuances or middle ground.'
            })
        
        # Emotional reasoning
        for pattern in self.emotional_reasoning_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                detected_biases.append({
                    'type': 'Emotional Reasoning',
                    'pattern': self._extract_match(text, pattern),
                    'explanation': 'You may be treating your feelings as facts, assuming that negative emotions reflect reality.'
                })
                break
        
        # Fortune telling
        if sentiment_valence < -0.1:
            for pattern in self.fortune_telling_patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    detected_biases.append({
                        'type': 'Fortune Telling',
                        'pattern': self._extract_match(text, pattern),
                        'explanation': 'You may be predicting negative outcomes without evidence, assuming things will go badly.'
                    })
                    break
        
        # Overgeneralization
        for pattern in self.overgeneralization_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                detected_biases.append({
                    'type': 'Overgeneralization',
                    'pattern': self._extract_match(text, pattern),
                    'explanation': 'You may be treating isolated incidents as universal patterns or rules.'
                })
                break
        
        return detected_biases
    
    def _extract_match(self, text: str, pattern: str, context_words: int = 10) -> str:
        """Extract matching text with context."""
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        if matches:
            match = matches[0]
            start = max(0, match.start() - context_words * 5)
            end = min(len(text), match.end() + context_words * 5)
            return text[start:end].strip()
        return ""
    
    def get_bias_frequency(self, biases_list: List[Dict]) -> Dict[str, int]:
        """Get frequency of each bias type."""
        counter = Counter([bias['type'] for bias in biases_list])
        return dict(counter)

