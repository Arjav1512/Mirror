"""Enhanced cognitive bias detection with improved pattern matching."""
import re
from typing import List, Dict, Tuple
from collections import Counter


class EnhancedBiasDetector:
    """Detect cognitive biases with improved accuracy and context awareness."""

    def __init__(self):
        """Initialize bias detection patterns."""
        self.setup_patterns()
        self.setup_contextual_modifiers()

    def setup_patterns(self):
        """Setup comprehensive regex patterns for bias detection."""

        self.catastrophizing_patterns = [
            (r'\b(always|never|everything|nothing|everyone|no one)\b.{0,30}(terrible|awful|horrible|worst|disaster|ruined|catastrophe)', 0.9),
            (r'\b(can\'t|cannot|couldn\'t|won\'t|wouldn\'t)\b.{0,20}(anything|ever|survive|cope|handle)', 0.8),
            (r'\b(end|over|finished|done for|hopeless|doomed|destroyed)\b', 0.7),
            (r'\b(completely|totally|utterly|absolutely)\s+(ruined|destroyed|hopeless|terrible)', 0.85),
        ]

        self.black_white_patterns = [
            (r'\b(all or nothing|black and white|either.*or)\b', 0.9),
            (r'\b(always|never|every|all|none|no one|everyone|everything|nothing)\b', 0.6),
            (r'\b(perfect|flawless|terrible|awful|complete failure|total success)\b', 0.75),
            (r'\b(completely|totally|absolutely|entirely)\s+(wrong|right|bad|good|true|false)', 0.8),
            (r'\b(must be|has to be|cannot be)\b.{0,20}\b(one|the only)', 0.7),
        ]

        self.emotional_reasoning_patterns = [
            (r'\b(i feel|feeling).{0,30}(therefore|so|which means|this means|proves|shows)', 0.85),
            (r'\b(because i feel|since i feel).{0,30}(it is|it must|that means)', 0.9),
            (r'\b(feels like).{0,30}(is|are|must be)', 0.75),
            (r'\b(my gut|intuition|feeling)\s+(tells me|says).{0,30}(so|therefore)', 0.7),
        ]

        self.fortune_telling_patterns = [
            (r'\b(will definitely|going to|gonna|certain to).{0,40}(fail|bad|terrible|wrong|disaster)', 0.85),
            (r'\b(i know|i\'m sure|certain).{0,30}(will|going to).{0,30}(bad|fail|wrong|terrible)', 0.8),
            (r'\b(it\'s going to|things will|this will).{0,30}(go wrong|fail|end badly|be terrible)', 0.9),
            (r'\b(no way|impossible).{0,30}(work out|succeed|be good|turn out well)', 0.75),
        ]

        self.overgeneralization_patterns = [
            (r'\b(always|never|every time|whenever|constantly|invariably)\b.{0,30}(happens|happened|occurs)', 0.85),
            (r'\b(this always|that never|it always|they always|he always|she always)\b', 0.8),
            (r'\b(everyone|no one|everybody|nobody|all).{0,20}(are|is|do|does|think|believe)', 0.75),
            (r'\b(once|one time|single).{0,40}(always|never|every)', 0.9),
        ]

        self.personalization_patterns = [
            (r'\b(it\'s all my fault|all because of me|i\'m to blame)', 0.9),
            (r'\b(must be something wrong with me|what did i do|why me)', 0.8),
            (r'\b(taking it personally|directed at me|about me)', 0.7),
        ]

        self.mind_reading_patterns = [
            (r'\b(i know what they\'re thinking|i can tell they|they must think)', 0.85),
            (r'\b(they probably|they\'re probably|i bet they).{0,30}(think|believe|feel)', 0.75),
            (r'\b(obviously thinks|clearly believes|definitely feels)', 0.8),
        ]

    def setup_contextual_modifiers(self):
        """Setup words that modify bias detection confidence."""
        self.negations = {'not', 'no', 'never', 'neither', 'nor', "n't", 'barely', 'hardly'}
        self.qualifiers = {'maybe', 'perhaps', 'possibly', 'sometimes', 'often', 'usually', 'might', 'could'}

    def detect_all(self, text: str, sentiment_valence: float) -> List[Dict]:
        """
        Detect all cognitive biases with confidence scores.

        Args:
            text: Journal entry text
            sentiment_valence: Sentiment valence score (-1 to 1)

        Returns:
            List of detected biases with type, pattern, explanation, and confidence
        """
        if not text or not text.strip():
            return []

        text_lower = text.lower()
        detected_biases = []
        seen_types = set()

        bias_checks = [
            ('Catastrophizing', self.catastrophizing_patterns, sentiment_valence < -0.15),
            ('Black-and-white Thinking', self.black_white_patterns, True),
            ('Emotional Reasoning', self.emotional_reasoning_patterns, True),
            ('Fortune Telling', self.fortune_telling_patterns, sentiment_valence < -0.1),
            ('Overgeneralization', self.overgeneralization_patterns, True),
            ('Personalization', self.personalization_patterns, sentiment_valence < -0.1),
            ('Mind Reading', self.mind_reading_patterns, True),
        ]

        for bias_type, patterns, condition in bias_checks:
            if not condition:
                continue

            if bias_type in seen_types:
                continue

            max_confidence = 0.0
            best_match = None

            for pattern, base_confidence in patterns:
                matches = list(re.finditer(pattern, text_lower, re.IGNORECASE))
                if matches:
                    for match in matches:
                        confidence = self._calculate_confidence(
                            text_lower,
                            match,
                            base_confidence
                        )

                        if confidence > max_confidence:
                            max_confidence = confidence
                            best_match = match

            if best_match and max_confidence >= 0.5:
                detected_biases.append({
                    'type': bias_type,
                    'pattern': self._extract_match(text, best_match),
                    'explanation': self._get_explanation(bias_type),
                    'confidence': round(max_confidence, 2)
                })
                seen_types.add(bias_type)

        detected_biases.sort(key=lambda x: x['confidence'], reverse=True)

        return detected_biases[:5]

    def _calculate_confidence(
        self,
        text: str,
        match: re.Match,
        base_confidence: float
    ) -> float:
        """Calculate confidence score based on context."""
        confidence = base_confidence

        context_start = max(0, match.start() - 50)
        context_end = min(len(text), match.end() + 50)
        context = text[context_start:context_end]
        context_words = set(context.split())

        has_negation = any(neg in context_words for neg in self.negations)
        if has_negation:
            confidence *= 0.7

        has_qualifier = any(qual in context_words for qual in self.qualifiers)
        if has_qualifier:
            confidence *= 0.85

        return confidence

    def _extract_match(self, text: str, match: re.Match, context_chars: int = 80) -> str:
        """Extract matching text with context."""
        start = max(0, match.start() - context_chars // 2)
        end = min(len(text), match.end() + context_chars // 2)

        excerpt = text[start:end].strip()

        if start > 0:
            excerpt = '...' + excerpt
        if end < len(text):
            excerpt = excerpt + '...'

        return excerpt

    def _get_explanation(self, bias_type: str) -> str:
        """Get detailed explanation for each bias type."""
        explanations = {
            'Catastrophizing': 'You may be magnifying negative events and imagining the worst possible outcomes. Try to consider more balanced perspectives and realistic probabilities.',
            'Black-and-white Thinking': 'You may be seeing situations in extremes without recognizing the nuances or middle ground. Reality often exists on a spectrum rather than in absolutes.',
            'Emotional Reasoning': 'You may be treating your feelings as facts, assuming that because you feel a certain way, it must reflect reality. Emotions are valid but not always accurate indicators of truth.',
            'Fortune Telling': 'You may be predicting negative outcomes without sufficient evidence. Consider alternative scenarios and remember that the future is uncertain.',
            'Overgeneralization': 'You may be drawing broad conclusions from single incidents or limited evidence. One experience doesn\'t define a universal pattern.',
            'Personalization': 'You may be taking excessive responsibility for events outside your control or assuming things are about you when they may not be.',
            'Mind Reading': 'You may be assuming you know what others think or feel without concrete evidence. Consider asking rather than assuming.'
        }
        return explanations.get(bias_type, 'Cognitive bias detected.')

    def get_bias_frequency(self, biases_list: List[Dict]) -> Dict[str, int]:
        """Get frequency of each bias type."""
        counter = Counter([bias['type'] for bias in biases_list])
        return dict(counter)

    def get_bias_trends(self, biases_over_time: List[Tuple[str, List[Dict]]]) -> Dict:
        """Analyze bias trends over time."""
        if not biases_over_time:
            return {}

        all_types = set()
        for _, biases in biases_over_time:
            all_types.update([b['type'] for b in biases])

        trends = {}
        for bias_type in all_types:
            occurrences = []
            for date, biases in biases_over_time:
                count = sum(1 for b in biases if b['type'] == bias_type)
                occurrences.append(count)

            trends[bias_type] = {
                'total': sum(occurrences),
                'average': sum(occurrences) / len(occurrences) if occurrences else 0,
                'trend': 'increasing' if len(occurrences) >= 2 and occurrences[-1] > occurrences[0] else 'decreasing' if len(occurrences) >= 2 else 'stable'
            }

        return trends
