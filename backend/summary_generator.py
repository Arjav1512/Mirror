"""AI-powered weekly summary generator."""
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from collections import Counter
import pandas as pd

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False


class WeeklySummaryGenerator:
    """Generate AI-powered weekly summaries."""
    
    def __init__(self, use_ai: bool = False):
        """Initialize summary generator."""
        self.use_ai = use_ai and TRANSFORMERS_AVAILABLE
        self.summarizer = None
        
        if self.use_ai:
            try:
                self.summarizer = pipeline(
                    "summarization",
                    model="facebook/bart-large-cnn",
                    device=-1  # CPU
                )
            except Exception:
                self.use_ai = False
    
    def generate_summary(self, entries: List[Dict], 
                        sentiment_data: pd.DataFrame) -> Dict:
        """
        Generate weekly summary from journal entries.
        
        Args:
            entries: List of journal entries (dicts with 'entry_text', 'timestamp')
            sentiment_data: DataFrame with sentiment analysis
        
        Returns:
            Dictionary with summary, themes, and emotions
        """
        if not entries:
            return {
                'summary_text': 'No entries this week to summarize.',
                'themes': [],
                'emotions': []
            }
        
        # Extract themes and emotions
        themes = self._extract_themes(entries)
        emotions = self._analyze_emotions(sentiment_data)
        
        # Generate summary text
        if self.use_ai and self.summarizer:
            summary_text = self._generate_ai_summary(entries, themes, emotions)
        else:
            summary_text = self._generate_rule_based_summary(entries, themes, emotions)
        
        return {
            'summary_text': summary_text,
            'themes': themes,
            'emotions': emotions
        }
    
    def _extract_themes(self, entries: List[Dict]) -> List[str]:
        """Extract common themes from entries."""
        # Simple keyword-based theme extraction
        theme_keywords = {
            'work': ['work', 'job', 'career', 'office', 'boss', 'colleague', 'project'],
            'relationships': ['friend', 'family', 'partner', 'love', 'relationship', 'people'],
            'health': ['health', 'exercise', 'fitness', 'illness', 'pain', 'sleep', 'energy'],
            'goals': ['goal', 'plan', 'future', 'dream', 'want', 'hope', 'aspiration'],
            'challenges': ['difficult', 'hard', 'challenge', 'struggle', 'problem', 'issue'],
            'gratitude': ['thankful', 'grateful', 'appreciate', 'blessed', 'lucky'],
            'stress': ['stress', 'anxious', 'worried', 'overwhelmed', 'pressure'],
            'growth': ['learn', 'grow', 'improve', 'develop', 'progress', 'better']
        }
        
        all_text = ' '.join([entry.get('entry_text', '').lower() for entry in entries])
        
        theme_counts = {}
        for theme, keywords in theme_keywords.items():
            count = sum(1 for keyword in keywords if keyword in all_text)
            if count > 0:
                theme_counts[theme] = count
        
        # Return top 3 themes
        sorted_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)
        return [theme for theme, _ in sorted_themes[:3]]
    
    def _analyze_emotions(self, sentiment_data: pd.DataFrame) -> List[str]:
        """Analyze dominant emotions from sentiment data."""
        if sentiment_data.empty:
            return []
        
        emotions = []
        avg_valence = sentiment_data['valence'].mean()
        
        if avg_valence > 0.3:
            emotions.append('Positive')
        elif avg_valence < -0.3:
            emotions.append('Negative')
        else:
            emotions.append('Neutral')
        
        # Detect volatility
        if len(sentiment_data) > 1:
            volatility = sentiment_data['valence'].std()
            if volatility > 0.4:
                emotions.append('Volatile')
        
        # Trend analysis
        if len(sentiment_data) >= 3:
            recent = sentiment_data['valence'].tail(3).mean()
            earlier = sentiment_data['valence'].head(3).mean()
            if recent > earlier + 0.2:
                emotions.append('Improving')
            elif recent < earlier - 0.2:
                emotions.append('Declining')
        
        return emotions
    
    def _generate_ai_summary(self, entries: List[Dict], 
                            themes: List[str], emotions: List[str]) -> str:
        """Generate summary using AI model."""
        combined_text = ' '.join([entry.get('entry_text', '') for entry in entries])
        
        # Truncate if too long
        max_length = 1000
        if len(combined_text) > max_length:
            combined_text = combined_text[:max_length]
        
        try:
            summary = self.summarizer(
                combined_text,
                max_length=150,
                min_length=50,
                do_sample=False
            )[0]['summary_text']
            
            # Enhance with themes and emotions
            summary += f"\n\nKey themes this week: {', '.join(themes)}."
            if emotions:
                summary += f" Emotional patterns: {', '.join(emotions)}."
            
            return summary
        except Exception:
            # Fallback to rule-based
            return self._generate_rule_based_summary(entries, themes, emotions)
    
    def _generate_rule_based_summary(self, entries: List[Dict],
                                    themes: List[str], emotions: List[str]) -> str:
        """Generate summary using rule-based approach."""
        num_entries = len(entries)
        
        summary_parts = []
        
        # Opening
        summary_parts.append(f"This week, you journaled {num_entries} time{'s' if num_entries != 1 else ''}.")
        
        # Themes
        if themes:
            summary_parts.append(
                f"Your entries frequently touched on: {', '.join(themes)}."
            )
        
        # Emotions
        if emotions:
            dominant_emotion = emotions[0] if emotions else 'Mixed'
            summary_parts.append(
                f"Your emotional landscape was primarily {dominant_emotion.lower()}."
            )
            if len(emotions) > 1:
                summary_parts.append(
                    f"You also experienced {', '.join(emotions[1:]).lower()} patterns."
                )
        
        # Entry highlights (sample sentences)
        if entries:
            summary_parts.append("\nHere's a reflection from your week:")
            # Get a meaningful entry (prefer longer ones)
            sample_entry = max(entries, key=lambda x: len(x.get('entry_text', '')))
            entry_preview = sample_entry.get('entry_text', '')[:200]
            if len(sample_entry.get('entry_text', '')) > 200:
                entry_preview += "..."
            summary_parts.append(f'"{entry_preview}"')
        
        summary_parts.append(
            "\nContinue reflecting to discover deeper patterns in your emotional journey."
        )
        
        return ' '.join(summary_parts)

