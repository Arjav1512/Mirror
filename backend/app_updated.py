"""Main Streamlit application for Mirror - Unified Authentication Version"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import os
from pathlib import Path

from database import Database
from sentiment_analyzer import SentimentAnalyzer
from bias_detector import BiasDetector
from visualization import EmotionalTimeline
from summary_generator import WeeklySummaryGenerator
from utils import get_week_start, get_week_range
from auth import verify_auth_token

# Page configuration
st.set_page_config(
    page_title="Mirror - AI-Powered Journal",
    page_icon="🪞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load and inject shared styles
SHARED_CSS_PATH = Path(__file__).parent.parent / 'shared_styles.css'
if SHARED_CSS_PATH.exists():
    with open(SHARED_CSS_PATH, 'r') as f:
        shared_css = f.read()
    st.markdown(f'<style>{shared_css}</style>', unsafe_allow_html=True)

# Additional Streamlit-specific overrides
st.markdown("""
    <style>
    /* Streamlit component overrides */
    .stApp {
        background: #0f172a !important;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
        border-bottom: 2px solid #334155;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #94a3b8;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        color: #a78bfa;
        border-bottom: 2px solid #7c3aed;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background-color: #064e3b;
        border-left: 4px solid #10b981;
        color: #d1fae5;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    
    .stError {
        background-color: #450a0a;
        border-left: 4px solid #ef4444;
        color: #fecaca;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'db' not in st.session_state:
    st.session_state.db = Database()
if 'sentiment_analyzer' not in st.session_state:
    st.session_state.sentiment_analyzer = SentimentAnalyzer()
if 'bias_detector' not in st.session_state:
    st.session_state.bias_detector = BiasDetector()
if 'visualizer' not in st.session_state:
    st.session_state.visualizer = EmotionalTimeline()
if 'summary_generator' not in st.session_state:
    st.session_state.summary_generator = WeeklySummaryGenerator(use_ai=False)


def check_auth_token():
    """
    Check for JWT token in URL and auto-login user
    This is the ONLY authentication mechanism - no Streamlit login UI
    """
    if st.session_state.user_id is not None:
        return True
    
    try:
        # Get query parameters
        query_params = st.query_params
        auth_token = query_params.get('auth_token', None)
        
        if auth_token:
            # Verify token
            user_data = verify_auth_token(auth_token)
            
            if user_data:
                # Auto-login user silently
                st.session_state.user_id = user_data['user_id']
                st.session_state.user_email = user_data['email']
                st.session_state.user_name = user_data['name']
                
                # Clear token from URL for security
                st.query_params.clear()
                
                return True
            else:
                st.error("⚠️ Invalid or expired session. Please sign up again.")
                show_redirect_to_landing()
                return False
        else:
            # No token - redirect to landing page
            show_redirect_to_landing()
            return False
            
    except Exception as e:
        print(f"Error checking auth token: {e}")
        show_redirect_to_landing()
        return False


def show_redirect_to_landing():
    """
    Show message and redirect button to landing page
    This replaces the old Streamlit login UI
    """
    landing_url = os.getenv('LANDING_PAGE_URL', 'http://localhost:3000')
    
    st.markdown("""
        <div style="text-align: center; padding: 5rem 2rem; max-width: 600px; margin: 0 auto;">
            <span style="font-size: 5rem; margin-bottom: 2rem; display: block;">🪞</span>
            <h1 style="font-size: 2.5rem; font-weight: 800; color: #f1f5f9; margin-bottom: 1rem;">
                Welcome to Mirror
            </h1>
            <p style="color: #cbd5e1; font-size: 1.2rem; line-height: 1.8; margin-bottom: 2rem;">
                Please sign up or log in to access your journal dashboard.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Go to Sign Up", type="primary", use_container_width=True):
            st.markdown(f'<meta http-equiv="refresh" content="0;url={landing_url}">', unsafe_allow_html=True)
    
    st.stop()


def main_journal_interface():
    """
    Main dashboard interface - only shown to authenticated users
    """
    # Header
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 3rem;">
            <h1 style="font-size: 3rem; font-weight: 800; color: #f1f5f9; margin-bottom: 0.5rem;">
                🪞 Mirror
            </h1>
            <p style="color: #cbd5e1; font-size: 1.1rem;">
                Welcome back, <strong>{st.session_state.user_name}</strong>
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 👤 Profile")
        st.markdown(f"**{st.session_state.user_name}**")
        st.markdown(f"`{st.session_state.user_email}`")
        st.markdown("---")
        
        # Stats
        entries = st.session_state.db.get_user_entries(st.session_state.user_id)
        st.metric("Total Entries", len(entries))
        
        if entries:
            sentiment_data = st.session_state.db.get_entries_dataframe(st.session_state.user_id)
            if not sentiment_data.empty:
                avg_valence = sentiment_data['valence'].mean()
                valence_color = "#10b981" if avg_valence > 0.1 else "#ef4444" if avg_valence < -0.1 else "#6366f1"
                st.markdown(f'<div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, {valence_color}25 0%, {valence_color}10 100%); border-radius: 12px; margin: 1rem 0; border: 1px solid {valence_color}30;"><strong style="color: {valence_color}; font-size: 1.2rem;">{avg_valence:.2f}</strong><br><span style="color: #94a3b8; font-size: 0.85rem;">Avg Emotional Valence</span></div>', unsafe_allow_html=True)
    
    # Check if new user
    entries = st.session_state.db.get_journal_entries(st.session_state.user_id)
    is_new_user = len(entries) == 0
    
    # Welcome screen for new users
    if is_new_user:
        st.markdown("""
            <div style="text-align: center; padding: 3rem 1rem; max-width: 800px; margin: 0 auto;">
                <span style="font-size: 4rem; margin-bottom: 1rem; display: block;">👋</span>
                <h1 style="font-size: 2.5rem; font-weight: 800; color: #f1f5f9; margin-bottom: 1rem;">Welcome to Mirror!</h1>
                <p style="font-size: 1.2rem; color: #cbd5e1; line-height: 1.8; margin-bottom: 2rem;">
                    Your journey to self-awareness starts here. Let's begin with your first reflection.
                </p>
                <div style="background: linear-gradient(135deg, #7c3aed15 0%, #a78bfa10 100%); border: 1px solid #7c3aed30; border-radius: 16px; padding: 2rem; margin: 2rem 0; text-align: left;">
                    <h3 style="color: #a78bfa; margin-bottom: 1rem; font-size: 1.1rem;">💡 Quick Tips:</h3>
                    <ul style="color: #cbd5e1; line-height: 2; margin-left: 1.5rem;">
                        <li>Write freely about your thoughts, feelings, or experiences</li>
                        <li>There's no right or wrong way to journal</li>
                        <li>AI will analyze your emotions and patterns</li>
                        <li>Your entries are private and encrypted</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["✍️ Write", "📊 Timeline", "📈 Insights", "🎯 Goals"])
    
    # Tab 1: Write
    with tab1:
        if is_new_user:
            st.markdown("""<h2 style="font-size: 1.8rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.5rem;">Your First Reflection</h2>""", unsafe_allow_html=True)
            st.markdown("""<p style="color: #94a3b8; font-size: 1rem; margin-bottom: 1.5rem;">Start by writing about how you're feeling right now or what's on your mind</p>""", unsafe_allow_html=True)
        else:
            st.markdown("""<h2 style="font-size: 1.8rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.5rem;">New Entry</h2>""", unsafe_allow_html=True)
            st.markdown("""<p style="color: #94a3b8; font-size: 1rem; margin-bottom: 1.5rem;">Take a moment to reflect and let your thoughts flow</p>""", unsafe_allow_html=True)
        
        # Reflection prompts
        import random
        prompts = [
            "How are you feeling right now? What emotions are present?",
            "What happened today that stood out to you?",
            "What are you grateful for at this moment?",
            "What's been challenging you lately?",
            "Describe a moment from today that made you smile.",
            "What thoughts keep coming back to you?",
            "If today had a color, what would it be and why?",
            "What do you need to let go of?"
        ]
        
        if is_new_user:
            st.markdown(f"""<div style="background: #1e293b; border-left: 3px solid #7c3aed; padding: 1rem 1.5rem; border-radius: 8px; margin-bottom: 1rem;">
                <p style="color: #a78bfa; font-size: 0.9rem; margin: 0;">💭 Reflection Prompt:</p>
                <p style="color: #e2e8f0; margin: 0.5rem 0 0 0; font-size: 1rem;">{random.choice(prompts)}</p>
            </div>""", unsafe_allow_html=True)
        
        entry_text = st.text_area(
            "Your Reflection",
            height=300,
            placeholder="Start writing... Let your thoughts flow naturally. There's no judgment here.",
            label_visibility="collapsed",
            key="journal_entry"
        )
        
        char_count = len(entry_text)
        st.markdown(f"""<p style="text-align: right; color: #64748b; font-size: 0.85rem; margin-top: -0.5rem;">{char_count} characters</p>""", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            submit = st.button(
                "🪞 Reflect & Save" if is_new_user else "💾 Save Entry",
                type="primary",
                use_container_width=True,
                help="AI will analyze your emotions and patterns"
            )
        
        if submit and entry_text.strip():
            sentiment_result = st.session_state.sentiment_analyzer.analyze(entry_text)
            
            entry_id = st.session_state.db.add_journal_entry(
                user_id=st.session_state.user_id,
                entry_text=entry_text,
                sentiment_score=sentiment_result['sentiment_score'],
                valence=sentiment_result['valence']
            )
            
            biases = st.session_state.bias_detector.detect_all(
                entry_text,
                sentiment_result['valence']
            )
            
            for bias in biases:
                st.session_state.db.add_bias(
                    entry_id=entry_id,
                    bias_type=bias['type'],
                    detected_pattern=bias['pattern'],
                    explanation=bias['explanation']
                )
            
            st.success("✅ Entry saved successfully!")
            
            valence = sentiment_result['valence']
            if valence > 0.1:
                sentiment_text = "Positive Energy Detected"
                sentiment_color = "#059669"
            elif valence < -0.1:
                sentiment_text = "Challenging Energy Detected"
                sentiment_color = "#dc2626"
            else:
                sentiment_text = "Neutral Balance Detected"
                sentiment_color = "#a78bfa"
            
            st.markdown(f"""
                <div style="padding: 1.5rem; background: #1e293b; 
                border-radius: 8px; border-left: 4px solid {sentiment_color}; margin: 1.5rem 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3); border: 1px solid #334155;">
                    <strong style="color: {sentiment_color}; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; font-family: 'Inter', sans-serif;">
                        {sentiment_text}
                    </strong>
                    <p style="color: #cbd5e1; margin: 0.75rem 0 0 0; font-size: 0.9rem;">Emotional valence: <strong>{valence:.2f}</strong></p>
                </div>
            """, unsafe_allow_html=True)
            
            if biases:
                st.markdown("### 🧠 Cognitive Patterns Detected")
                st.markdown("These patterns can help you develop greater self-awareness:")
                for bias in biases:
                    st.markdown(f"""
                        <div class="bias-alert">
                            <strong>{bias['type']}</strong>
                            <p style="margin: 0.5rem 0 0 0; color: #fcd34d;">{bias['explanation']}</p>
                        </div>
                    """, unsafe_allow_html=True)
            
            st.rerun()
        elif submit:
            st.error("Please write something before submitting.")
    
    # Tab 2: Timeline
    with tab2:
        st.markdown("""<h2 style="font-size: 1.8rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.5rem;">Emotional Timeline</h2>""", unsafe_allow_html=True)
        st.markdown("""<p style="color: #94a3b8; font-size: 1rem; margin-bottom: 1.5rem;">Visualize your emotional journey and discover patterns</p>""", unsafe_allow_html=True)
        
        sentiment_data = st.session_state.db.get_entries_dataframe(st.session_state.user_id)
        
        if not sentiment_data.empty:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📝 Total Entries", len(sentiment_data), help="Total number of reflections")
            with col2:
                avg = sentiment_data['valence'].mean()
                st.metric("💚 Avg Mood", f"{avg:.2f}", delta="Positive" if avg > 0 else "Neutral" if avg == 0 else "Needs attention", help="Overall emotional valence")
            with col3:
                std = sentiment_data['valence'].std()
                st.metric("📊 Volatility", f"{std:.2f}", help="Emotional consistency (lower = more stable)")
            with col4:
                recent = sentiment_data['valence'].tail(7).mean() if len(sentiment_data) >= 7 else sentiment_data['valence'].mean()
                trend = "↗️" if recent > avg else "↘️" if recent < avg else "→"
                st.metric("📅 Recent Trend", f"{recent:.2f}", delta=trend, help="Last 7 days average")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("""<h3 style="font-size: 1.3rem; font-weight: 600; color: #e2e8f0; margin: 2rem 0 1rem 0;">Your Emotional Journey</h3>""", unsafe_allow_html=True)
            fig = st.session_state.visualizer.create_timeline(sentiment_data)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            if len(sentiment_data) >= 3:
                st.markdown("""<h3 style="font-size: 1.3rem; font-weight: 600; color: #e2e8f0; margin: 2rem 0 1rem 0;">Emotional Stability</h3>""", unsafe_allow_html=True)
                vol_fig = st.session_state.visualizer.create_volatility_chart(sentiment_data)
                st.plotly_chart(vol_fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.markdown("""
                <div style="text-align: center; padding: 4rem 2rem; max-width: 600px; margin: 0 auto;">
                    <span style="font-size: 5rem; margin-bottom: 1.5rem; display: block; opacity: 0.5;">📊</span>
                    <h3 style="font-size: 1.5rem; font-weight: 600; color: #cbd5e1; margin-bottom: 1rem;">Your Timeline Awaits</h3>
                    <p style="color: #94a3b8; font-size: 1.1rem; line-height: 1.8; margin-bottom: 2rem;">
                        Start journaling to visualize your emotional journey.<br>
                        Each entry adds to your unique story.
                    </p>
                    <div style="background: linear-gradient(135deg, #7c3aed15 0%, #a78bfa10 100%); border: 1px solid #7c3aed20; border-radius: 12px; padding: 1.5rem; text-align: left;">
                        <p style="color: #a78bfa; font-weight: 600; margin-bottom: 0.75rem;">What you'll see here:</p>
                        <ul style="color: #cbd5e1; margin-left: 1.5rem; line-height: 1.8;">
                            <li>Interactive emotion charts</li>
                            <li>Pattern recognition over time</li>
                            <li>Mood stability tracking</li>
                            <li>Personalized insights</li>
                        </ul>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    # Tab 3 & 4: Insights and Goals (simplified for brevity)
    with tab3:
        st.markdown("""<h2 style="font-size: 1.8rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.5rem;">AI Insights</h2>""", unsafe_allow_html=True)
        st.markdown("""<p style="color: #94a3b8; font-size: 1rem; margin-bottom: 1.5rem;">Discover patterns, biases, and growth opportunities</p>""", unsafe_allow_html=True)
        st.info("Weekly insights feature - coming soon!")
    
    with tab4:
        st.markdown("""<h2 style="font-size: 1.8rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.5rem;">Goals & Growth</h2>""", unsafe_allow_html=True)
        st.markdown("""<p style="color: #94a3b8; font-size: 1rem; margin-bottom: 1.5rem;">Track your cognitive patterns and personal development</p>""", unsafe_allow_html=True)
        st.info("Goal tracking feature - coming soon!")


def main():
    """Main entry point - check auth first"""
    if check_auth_token():
        main_journal_interface()


if __name__ == "__main__":
    main()
