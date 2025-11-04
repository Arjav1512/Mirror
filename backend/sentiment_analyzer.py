"""Sentiment analysis using TextBlob and VADER."""
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from typing import Dict, Tuple


class SentimentAnalyzer:
    """Combined sentiment analysis using TextBlob and VADER."""
    
    def __init__(self):
        """Initialize sentiment analyzers."""
        self.vader = SentimentIntensityAnalyzer()
    
    def analyze(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment of text using both TextBlob and VADER.
        
        Returns:
            Dictionary with sentiment scores and combined valence.
        """
        # TextBlob analysis
        blob = TextBlob(text)
        textblob_polarity = blob.sentiment.polarity  # -1 to 1
        textblob_subjectivity = blob.sentiment.subjectivity  # 0 to 1
        
        # VADER analysis
        vader_scores = self.vader.polarity_scores(text)
        vader_compound = vader_scores['compound']  # -1 to 1
        
        # Combined valence (weighted average)
        # VADER is better for social media/text, TextBlob for general text
        # Weight: 60% VADER, 40% TextBlob
        combined_valence = (0.6 * vader_compound) + (0.4 * textblob_polarity)
        
        return {
            'textblob_polarity': textblob_polarity,
            'textblob_subjectivity': textblob_subjectivity,
            'vader_compound': vader_compound,
            'vader_pos': vader_scores['pos'],
            'vader_neu': vader_scores['neu'],
            'vader_neg': vader_scores['neg'],
            'sentiment_score': vader_compound,  # Primary score
            'valence': combined_valence  # Combined weighted score
        }
    
    def calculate_rolling_average(self, df: pd.DataFrame, window: int = 7) -> pd.DataFrame:
        """
        Calculate rolling average of sentiment scores.
        
        Args:
            df: DataFrame with 'timestamp' and 'valence' columns
            window: Rolling window size in days
        
        Returns:
            DataFrame with rolling average added
        """
        df = df.copy()
        df.set_index('timestamp', inplace=True)
        df['rolling_avg'] = df['valence'].rolling(window=f'{window}D', min_periods=1).mean()
        df.reset_index(inplace=True)
        return df
    
    def detect_volatility(self, df: pd.DataFrame, threshold: float = 0.5) -> pd.Series:
        """
        Detect high volatility periods in sentiment.
        
        Args:
            df: DataFrame with 'valence' column
            threshold: Standard deviation threshold for volatility
        
        Returns:
            Boolean series indicating volatile periods
        """
        if len(df) < 2:
            return pd.Series([False] * len(df))
        
        rolling_std = df['valence'].rolling(window=7, min_periods=2).std()
        return rolling_std > threshold
    
    def detect_mood_shifts(self, df: pd.DataFrame, 
                          shift_threshold: float = 0.3) -> pd.DataFrame:
        """
        Detect significant mood shifts in sentiment timeline.
        
        Args:
            df: DataFrame with 'timestamp' and 'valence' columns
            shift_threshold: Minimum change to consider a shift
        
        Returns:
            DataFrame with mood shift indicators
        """
        df = df.copy()
        df['shift'] = df['valence'].diff().abs() > shift_threshold
        return df

