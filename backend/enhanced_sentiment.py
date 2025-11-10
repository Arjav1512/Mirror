"""Enhanced sentiment analysis with improved accuracy."""
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import re
from typing import Dict, List, Tuple


class EnhancedSentimentAnalyzer:
    """Enhanced sentiment analysis with context awareness and emotion detection."""

    def __init__(self):
        """Initialize sentiment analyzers and emotion lexicons."""
        self.vader = SentimentIntensityAnalyzer()
        self._setup_emotion_lexicons()
        self._setup_intensifiers()

    def _setup_emotion_lexicons(self):
        """Setup emotion-specific word lists for better categorization."""
        self.emotion_words = {
            'joy': ['happy', 'excited', 'joyful', 'delighted', 'thrilled', 'ecstatic',
                   'cheerful', 'pleased', 'content', 'satisfied', 'grateful', 'blessed'],
            'sadness': ['sad', 'unhappy', 'depressed', 'miserable', 'gloomy', 'heartbroken',
                       'disappointed', 'discouraged', 'hopeless', 'lonely', 'empty'],
            'anger': ['angry', 'furious', 'enraged', 'irritated', 'frustrated', 'annoyed',
                     'mad', 'resentful', 'bitter', 'hostile', 'outraged'],
            'fear': ['afraid', 'scared', 'anxious', 'worried', 'nervous', 'terrified',
                    'fearful', 'panicked', 'uneasy', 'apprehensive', 'stressed'],
            'love': ['love', 'adore', 'cherish', 'treasure', 'care', 'affection',
                    'warmth', 'devotion', 'fondness', 'attachment'],
            'surprise': ['surprised', 'shocked', 'amazed', 'astonished', 'stunned',
                        'bewildered', 'startled', 'unexpected']
        }

    def _setup_intensifiers(self):
        """Setup intensifier words that modify sentiment strength."""
        self.intensifiers = {
            'very': 1.3,
            'really': 1.3,
            'extremely': 1.5,
            'incredibly': 1.5,
            'absolutely': 1.4,
            'completely': 1.4,
            'totally': 1.4,
            'utterly': 1.5,
            'so': 1.2,
            'quite': 1.1,
            'rather': 1.1,
            'somewhat': 0.8,
            'slightly': 0.7,
            'barely': 0.6,
            'hardly': 0.6,
            'not': -1.0,
            "n't": -1.0
        }

    def analyze(self, text: str) -> Dict[str, any]:
        """
        Perform comprehensive sentiment analysis.

        Returns:
            Dictionary with sentiment scores, emotions, and confidence metrics.
        """
        if not text or not text.strip():
            return self._empty_result()

        text_lower = text.lower()

        blob = TextBlob(text)
        textblob_polarity = blob.sentiment.polarity
        textblob_subjectivity = blob.sentiment.subjectivity

        vader_scores = self.vader.polarity_scores(text)
        vader_compound = vader_scores['compound']

        emotions = self._detect_emotions(text_lower)
        dominant_emotion = max(emotions.items(), key=lambda x: x[1])[0] if emotions else 'neutral'

        intensity_modifier = self._calculate_intensity(text_lower)

        combined_valence = self._calculate_combined_valence(
            vader_compound,
            textblob_polarity,
            textblob_subjectivity,
            intensity_modifier
        )

        confidence = self._calculate_confidence(
            vader_compound,
            textblob_polarity,
            textblob_subjectivity,
            len(text.split())
        )

        return {
            'textblob_polarity': round(textblob_polarity, 3),
            'textblob_subjectivity': round(textblob_subjectivity, 3),
            'vader_compound': round(vader_compound, 3),
            'vader_pos': round(vader_scores['pos'], 3),
            'vader_neu': round(vader_scores['neu'], 3),
            'vader_neg': round(vader_scores['neg'], 3),
            'sentiment_score': round(vader_compound, 3),
            'valence': round(combined_valence, 3),
            'emotions': emotions,
            'dominant_emotion': dominant_emotion,
            'confidence': round(confidence, 3),
            'word_count': len(text.split())
        }

    def _detect_emotions(self, text: str) -> Dict[str, int]:
        """Detect specific emotions in text."""
        emotions = {}
        words = text.split()

        for emotion, emotion_words in self.emotion_words.items():
            count = sum(1 for word in words if any(ew in word for ew in emotion_words))
            if count > 0:
                emotions[emotion] = count

        return emotions

    def _calculate_intensity(self, text: str) -> float:
        """Calculate intensity modifier based on intensifier words."""
        words = text.split()
        modifier = 1.0
        count = 0

        for word in words:
            for intensifier, multiplier in self.intensifiers.items():
                if intensifier in word:
                    modifier *= multiplier
                    count += 1

        return modifier if count > 0 else 1.0

    def _calculate_combined_valence(
        self,
        vader_compound: float,
        textblob_polarity: float,
        subjectivity: float,
        intensity: float
    ) -> float:
        """
        Calculate combined valence with adaptive weighting.

        Higher subjectivity = trust VADER more (better for emotional text)
        Lower subjectivity = balance both equally
        """
        if subjectivity > 0.6:
            weight_vader = 0.7
            weight_textblob = 0.3
        elif subjectivity < 0.3:
            weight_vader = 0.5
            weight_textblob = 0.5
        else:
            weight_vader = 0.6
            weight_textblob = 0.4

        base_valence = (weight_vader * vader_compound) + (weight_textblob * textblob_polarity)

        valence_with_intensity = base_valence * intensity

        return max(-1.0, min(1.0, valence_with_intensity))

    def _calculate_confidence(
        self,
        vader_compound: float,
        textblob_polarity: float,
        subjectivity: float,
        word_count: int
    ) -> float:
        """
        Calculate confidence in sentiment analysis.

        High confidence when:
        - Both analyzers agree
        - Text is subjective
        - Sufficient word count
        """
        agreement = 1.0 - abs(vader_compound - textblob_polarity) / 2.0

        subjectivity_factor = min(subjectivity * 1.5, 1.0)

        word_factor = min(word_count / 50.0, 1.0)

        confidence = (agreement * 0.5) + (subjectivity_factor * 0.3) + (word_factor * 0.2)

        return max(0.0, min(1.0, confidence))

    def _empty_result(self) -> Dict:
        """Return empty/neutral result for invalid input."""
        return {
            'textblob_polarity': 0.0,
            'textblob_subjectivity': 0.0,
            'vader_compound': 0.0,
            'vader_pos': 0.0,
            'vader_neu': 1.0,
            'vader_neg': 0.0,
            'sentiment_score': 0.0,
            'valence': 0.0,
            'emotions': {},
            'dominant_emotion': 'neutral',
            'confidence': 0.0,
            'word_count': 0
        }

    def calculate_rolling_average(
        self,
        df: pd.DataFrame,
        window: int = 7
    ) -> pd.DataFrame:
        """Calculate rolling average of sentiment scores."""
        if df.empty or 'valence' not in df.columns:
            return df

        df = df.copy()
        df = df.sort_values('timestamp')
        df.set_index('timestamp', inplace=True)
        df['rolling_avg'] = df['valence'].rolling(
            window=f'{window}D',
            min_periods=1
        ).mean()
        df.reset_index(inplace=True)
        return df

    def detect_volatility(
        self,
        df: pd.DataFrame,
        threshold: float = 0.5
    ) -> pd.Series:
        """Detect high volatility periods in sentiment."""
        if df.empty or len(df) < 2 or 'valence' not in df.columns:
            return pd.Series([False] * len(df)) if not df.empty else pd.Series()

        rolling_std = df['valence'].rolling(window=7, min_periods=2).std()
        return rolling_std > threshold

    def detect_mood_shifts(
        self,
        df: pd.DataFrame,
        shift_threshold: float = 0.3
    ) -> pd.DataFrame:
        """Detect significant mood shifts in sentiment timeline."""
        if df.empty or 'valence' not in df.columns:
            return df

        df = df.copy()
        df['shift'] = df['valence'].diff().abs() > shift_threshold
        df['shift_magnitude'] = df['valence'].diff().abs()
        return df
