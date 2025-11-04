"""Visualization module for emotional timeline using Plotly."""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
from typing import Optional


class EmotionalTimeline:
    """Generate interactive emotional timeline visualizations."""
    
    def __init__(self):
        """Initialize visualization settings - dark modern theme matching app UI."""
        self.colors = {
            'positive': '#10b981',     # Green
            'negative': '#ef4444',     # Red
            'neutral': '#a78bfa',      # Light Violet
            'background': '#0f172a',   # Slate-950 (app background)
            'paper': '#1e293b',        # Slate-800 (card background)
            'grid': '#334155',         # Slate-700
            'text': '#f1f5f9',         # Slate-100
            'text_muted': '#cbd5e1',   # Slate-300
            'accent_primary': '#7c3aed',  # Violet-600
            'accent_secondary': '#8b5cf6', # Violet-500
            'gradient_start': 'rgba(124, 58, 237, 0.8)',
            'gradient_end': 'rgba(139, 92, 246, 0.3)'
        }
    
    def create_timeline(self, df: pd.DataFrame, 
                       rolling_window: int = 7) -> go.Figure:
        """
        Create interactive emotional timeline chart.
        
        Args:
            df: DataFrame with 'timestamp' and 'valence' columns
            rolling_window: Days for rolling average
        
        Returns:
            Plotly figure object
        """
        if df.empty or len(df) == 0:
            return self._create_empty_chart()
        
        df = df.copy()
        df = df.sort_values('timestamp')
        
        # Calculate rolling average
        df.set_index('timestamp', inplace=True)
        df['rolling_avg'] = df['valence'].rolling(
            window=f'{rolling_window}D', min_periods=1
        ).mean()
        df.reset_index(inplace=True)
        
        fig = go.Figure()
        
        # Color based on valence
        colors = df['valence'].apply(
            lambda x: self.colors['positive'] if x > 0.1 
            else self.colors['negative'] if x < -0.1 
            else self.colors['neutral']
        )
        
        # Scatter plot for individual entries - Enhanced visual design
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['valence'],
            mode='markers',
            name='Daily Entries',
            marker=dict(
                size=12,
                color=colors,
                opacity=0.8,
                line=dict(width=2, color=self.colors['background']),
                symbol='circle'
            ),
            hovertemplate='<b style="color: #a78bfa;">%{x|%b %d, %Y}</b><br>' +
                         '<b>Emotional Valence:</b> %{y:.2f}<br>' +
                         '<extra></extra>'
        ))
        
        # Rolling average line - Smooth gradient effect
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['rolling_avg'],
            mode='lines',
            name=f'{rolling_window}-Day Trend',
            line=dict(
                color=self.colors['accent_secondary'],
                width=4,
                shape='spline',  # Smooth curves
                smoothing=1.3
            ),
            fill='tozeroy',
            fillcolor=self.colors['gradient_end'],
            hovertemplate='<b style="color: #8b5cf6;">%{x|%b %d, %Y}</b><br>' +
                         '<b>Trend Average:</b> %{y:.2f}<br>' +
                         '<extra></extra>'
        ))
        
        # Zero line (neutral) - Styled for dark theme
        fig.add_hline(
            y=0,
            line_dash="dot",
            line_color=self.colors['grid'],
            line_width=2,
            annotation=dict(
                text="Neutral Baseline",
                font=dict(size=11, color=self.colors['text_muted']),
                bgcolor=self.colors['paper'],
                bordercolor=self.colors['grid'],
                borderwidth=1,
                borderpad=4
            ),
            annotation_position="right"
        )
        
        # Layout - Modern dark theme matching app design
        fig.update_layout(
            title=None,  # Remove title, let app handle it
            xaxis_title=dict(
                text='Timeline',
                font=dict(size=13, color=self.colors['text_muted'], family='Inter')
            ),
            yaxis_title=dict(
                text='Emotional Valence',
                font=dict(size=13, color=self.colors['text_muted'], family='Inter')
            ),
            hovermode='x unified',
            template='plotly_dark',
            plot_bgcolor=self.colors['background'],
            paper_bgcolor=self.colors['background'],
            font=dict(
                family='Inter, -apple-system, sans-serif',
                color=self.colors['text'],
                size=12
            ),
            height=400,
            margin=dict(l=60, r=30, t=20, b=60),
            xaxis=dict(
                gridcolor=self.colors['grid'],
                showgrid=True,
                gridwidth=1,
                zeroline=False,
                color=self.colors['text_muted'],
                tickfont=dict(size=11)
            ),
            yaxis=dict(
                gridcolor=self.colors['grid'],
                showgrid=True,
                gridwidth=1,
                range=[-1.1, 1.1],
                zeroline=False,
                color=self.colors['text_muted'],
                tickfont=dict(size=11)
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5,
                font=dict(size=12, color=self.colors['text']),
                bgcolor='rgba(30, 41, 59, 0.8)',
                bordercolor=self.colors['grid'],
                borderwidth=1
            ),
            hoverlabel=dict(
                bgcolor=self.colors['paper'],
                font_size=13,
                font_family="Inter",
                bordercolor=self.colors['accent_primary']
            )
        )
        
        return fig
    
    def create_volatility_chart(self, df: pd.DataFrame) -> go.Figure:
        """Create volatility visualization."""
        if df.empty or len(df) < 2:
            return self._create_empty_chart()
        
        df = df.copy()
        df = df.sort_values('timestamp')
        df.set_index('timestamp', inplace=True)
        df['volatility'] = df['valence'].rolling(window=7, min_periods=2).std()
        df.reset_index(inplace=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['volatility'],
            fill='tozeroy',
            mode='lines',
            name='Emotional Volatility',
            line=dict(color=self.colors['neutral'], width=2),
            fillcolor='rgba(99, 102, 241, 0.2)'
        ))
        
        fig.update_layout(
            title='Emotional Volatility Over Time',
            xaxis_title='Date',
            yaxis_title='Volatility (Standard Deviation)',
            template='plotly_white',
            height=300,
            margin=dict(l=60, r=40, t=60, b=60)
        )
        
        return fig
    
    def _create_empty_chart(self) -> go.Figure:
        """Create empty chart placeholder."""
        fig = go.Figure()
        fig.add_annotation(
            text="Start journaling to see your emotional timeline",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color='gray')
        )
        fig.update_layout(
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, showticklabels=False),
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=500
        )
        return fig
    
    def create_bias_frequency_chart(self, bias_counts: dict) -> go.Figure:
        """Create chart showing bias frequency."""
        if not bias_counts:
            return self._create_empty_chart()
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(bias_counts.keys()),
                y=list(bias_counts.values()),
                marker_color=self.colors['neutral'],
                text=list(bias_counts.values()),
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title='Cognitive Bias Frequency',
            xaxis_title='Bias Type',
            yaxis_title='Frequency',
            template='plotly_white',
            height=300,
            margin=dict(l=60, r=40, t=60, b=100),
            xaxis=dict(tickangle=-45)
        )
        
        return fig

