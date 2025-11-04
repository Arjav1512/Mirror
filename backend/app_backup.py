"""Main Streamlit application for Mirror."""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go

from database import Database
from sentiment_analyzer import SentimentAnalyzer
from bias_detector import BiasDetector
from visualization import EmotionalTimeline
from summary_generator import WeeklySummaryGenerator
from utils import get_week_start, get_week_range

# Page configuration
st.set_page_config(
    page_title="Mirror - AI-Powered Journal",
    page_icon="🪞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
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

# Custom CSS - Dark Theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp {
        background: #0f172a;
        color: #e2e8f0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Login page */
    .login-container {
        background: #1e293b;
        border-radius: 16px;
        padding: 3rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin: 2rem auto;
        max-width: 500px;
        border: 1px solid #334155;
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }
    
    /* Header styling */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #f1f5f9;
        text-align: center;
        margin-bottom: 0.5rem;
        font-family: 'Inter', sans-serif;
    }
    .tagline {
        text-align: center;
        color: #cbd5e1;
        font-size: 1.1rem;
        margin-bottom: 3rem;
        font-weight: 400;
        line-height: 1.8;
        font-family: 'Inter', sans-serif;
    }
    
    /* Philosophical Quote Box */
    .phil-quote {
        text-align: center;
        color: #cbd5e1;
        font-size: 0.95rem;
        font-style: italic;
        padding: 1.5rem 2rem;
        margin: 2rem auto;
        max-width: 600px;
        border-left: 2px solid #7c3aed;
        background: #1e293b;
        font-family: 'Inter', serif;
        border-radius: 8px;
    }
    
    /* Button styling */
    .stButton>button {
        background: #7c3aed;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.2s;
        font-family: 'Inter', sans-serif;
        width: 100%;
        box-shadow: 0 4px 6px rgba(124, 58, 237, 0.3);
    }
    .stButton>button:hover {
        background: #8b5cf6;
        box-shadow: 0 6px 8px rgba(124, 58, 237, 0.4);
    }
    
    /* Text input styling */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        border: 1px solid #475569;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.2s;
        background-color: #1e293b;
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #7c3aed;
        box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.2);
        outline: none;
    }
    
    /* Text area specific */
    .stTextArea>div>div>textarea {
        min-height: 200px;
        font-family: 'Inter', sans-serif;
        line-height: 1.6;
        font-size: 1rem;
        color: #e2e8f0;
    }
    
    /* Select box styling */
    .stSelectbox>div>div>select {
        border: 1px solid #475569;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        transition: all 0.2s;
        font-family: 'Inter', sans-serif;
        background-color: #1e293b;
        color: #e2e8f0;
    }
    .stSelectbox>div>div>select:focus {
        border-color: #7c3aed;
        box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.2);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: #1e293b;
    }
    [data-testid="stSidebar"] {
        background: #1e293b;
        border-right: 1px solid #334155;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #e2e8f0;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem;
        color: #94a3b8;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: #f1f5f9;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
    }
    h1 {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    h2 {
        font-size: 2rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    h3 {
        font-size: 1.5rem;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        margin-bottom: 2rem;
        border-bottom: 2px solid #334155;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        font-weight: 600;
        border-radius: 0;
        font-size: 0.9rem;
        color: #94a3b8;
        transition: all 0.2s;
        font-family: 'Inter', sans-serif;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #a78bfa;
    }
    .stTabs [aria-selected="true"] {
        background: transparent;
        color: #a78bfa;
        border-bottom: 2px solid #7c3aed;
    }
    
    /* Bias alert styling */
    .bias-alert {
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        background: #422006;
        border-left: 4px solid #fb923c;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .bias-alert strong {
        color: #fbbf24;
        font-size: 1rem;
        display: block;
        margin-bottom: 0.5rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
    }
    
    /* Info/Warning/Success message styling */
    .stAlert {
        border-radius: 8px;
        padding: 1rem 1.5rem;
        border-left: 4px solid;
        background: #1e293b;
    }
    
    /* Divider styling */
    hr {
        margin: 2.5rem 0;
        border: none;
        border-top: 1px solid #334155;
    }
    
    /* Main content background */
    .main {
        background: transparent;
    }
    
    /* Card-like sections */
    .element-container {
        padding: 1.5rem;
        background: #1e293b;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin: 1rem 0;
        border: 1px solid #334155;
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Label styling */
    label {
        font-weight: 600;
        color: #f1f5f9;
        font-size: 0.875rem;
        margin-bottom: 0.5rem;
        display: block;
        font-family: 'Inter', sans-serif;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: #e2e8f0;
        background: #1e293b;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        transition: background-color 0.2s;
        font-family: 'Inter', sans-serif;
        border: 1px solid #334155;
    }
    .streamlit-expanderHeader:hover {
        background: #334155;
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-top-color: #7c3aed;
    }
    
    /* Sentiment card */
    .sentiment-card {
        padding: 1.5rem;
        background: #1e293b;
        border-radius: 12px;
        border-left: 4px solid;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        border: 1px solid #334155;
    }
    
    /* Fix all Streamlit widget containers */
    .stTextInput > div > div,
    .stTextArea > div > div,
    .stSelectbox > div > div,
    .stDateInput > div > div,
    .stTimeInput > div > div {
        background-color: #1e293b;
        border-radius: 8px;
    }
    
    /* Form containers */
    .stForm {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.5rem;
    }
    
    /* Columns consistency */
    .row-widget {
        gap: 1rem;
    }
    
    /* Markdown paragraphs */
    .stMarkdown p {
        color: #cbd5e1;
        line-height: 1.6;
    }
    
    /* Code blocks */
    code {
        background: #0f172a;
        color: #a78bfa;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-family: 'Monaco', 'Courier New', monospace;
    }
    
    pre {
        background: #0f172a;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: #334155;
        color: #e2e8f0;
        border: 1px solid #475569;
    }
    .stDownloadButton > button:hover {
        background: #475569;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border: 1px solid #334155;
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background-color: #7c3aed;
    }
    
    /* Success/Error/Warning/Info messages */
    .stSuccess {
        background-color: #064e3b;
        border-left: 4px solid #10b981;
        color: #d1fae5;
    }
    .stError {
        background-color: #450a0a;
        border-left: 4px solid #ef4444;
        color: #fecaca;
    }
    .stWarning {
        background-color: #422006;
        border-left: 4px solid #f59e0b;
        color: #fde68a;
    }
    .stInfo {
        background-color: #1e3a8a;
        border-left: 4px solid #3b82f6;
        color: #dbeafe;
    }
    
    /* Checkbox and radio */
    .stCheckbox, .stRadio {
        color: #e2e8f0;
    }
    
    /* File uploader */
    .stFileUploader {
        background: #1e293b;
        border: 2px dashed #475569;
        border-radius: 12px;
        padding: 2rem;
    }
    .stFileUploader:hover {
        border-color: #7c3aed;
    }
    
    /* Plotly charts */
    .js-plotly-plot {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Remove default Streamlit padding inconsistencies */
    .block-container {
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    /* Consistent section spacing */
    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)


def login_or_signup():
    """Handle user login/signup with beautiful UI."""
    # Hero section styling with philosophical quote
    import random
    quotes = [
        "\"The unexamined life is not worth living.\" — Socrates",
        "\"Knowing yourself is the beginning of all wisdom.\" — Aristotle",
        "\"The mind is everything. What you think you become.\" — Buddha",
        "\"Man is the measure of all things.\" — Protagoras",
        "\"To know thyself is the beginning of wisdom.\" — Socrates",
        "\"The soul becomes dyed with the color of its thoughts.\" — Marcus Aurelius"
    ]
    daily_quote = random.choice(quotes)
    
    st.markdown(f"""
        <div style="text-align: center; padding: 3rem 2rem 2rem 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1.5rem;">🪞</div>
            <h1 style="font-size: 3rem; font-weight: 300; color: #f1f5f9; margin-bottom: 1rem; font-family: 'Inter', sans-serif; letter-spacing: 0.1em;">
                MIRROR
            </h1>
            <p style="font-size: 0.95rem; color: #cbd5e1; font-weight: 300; line-height: 1.8; max-width: 500px; margin: 0 auto 2rem auto; font-style: italic;">
                A space for self-reflection and philosophical inquiry
            </p>
            <div class="phil-quote">
                {daily_quote}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Center content with columns
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        # Styled container for login form
        st.markdown("""
            <div style="background: #1e293b; border-radius: 8px; padding: 3rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3); margin-bottom: 2rem; border: 1px solid #334155;">
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔐 Sign In", "✨ New User"])
        
        with tab1:
            st.markdown("### Welcome Back")
            st.markdown("<p style='color: #94a3b8; margin-bottom: 2rem;'>Sign in to continue your journey of self-reflection</p>", unsafe_allow_html=True)
            
            email = st.text_input("Email Address", key="login_email", placeholder="your.email@example.com", label_visibility="visible")
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                if st.button("Sign In", type="primary", use_container_width=True):
                    if email:
                        user = st.session_state.db.get_user_by_email(email)
                        if user:
                            st.session_state.user_id = user['id']
                            st.session_state.user_email = user['email']
                            st.rerun()
                        else:
                            st.error("User not found. Please sign up first.")
                    else:
                        st.error("Please enter your email.")
        
        with tab2:
            st.markdown("### Create Your Account")
            st.markdown("<p style='color: #94a3b8; margin-bottom: 2rem;'>Start your self-awareness journey today</p>", unsafe_allow_html=True)
            
            with st.form("quick_signup"):
                new_email = st.text_input("Email Address", key="signup_email", placeholder="your.email@example.com", label_visibility="visible")
                new_name = st.text_input("Name", key="signup_name", placeholder="Your name", label_visibility="visible")
                
                col_sub1, col_sub2, col_sub3 = st.columns([1, 2, 1])
                with col_sub2:
                    submit_signup = st.form_submit_button("Create Account", type="primary", use_container_width=True)
                
                if submit_signup:
                    if new_email and new_name:
                        try:
                            user_id = st.session_state.db.create_user(
                                new_email, 
                                new_name, 
                                {"source": "direct_signup"}
                            )
                            st.session_state.user_id = user_id
                            st.session_state.user_email = new_email
                            st.success("✅ Account created! Redirecting...")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error creating account: {str(e)}")
                    else:
                        st.error("Please fill in all fields.")
            
            st.markdown("---")
            st.markdown("""
                <div style="text-align: center; padding: 1rem; background: #334155; border-radius: 12px; margin-top: 1rem;">
                    <p style="color: #cbd5e1; margin: 0; font-size: 0.9rem;">
                        💡 For a guided onboarding experience, visit the 
                        <a href="http://localhost:5000" style="color: #a78bfa; text-decoration: none; font-weight: 600;">landing page</a>
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)


def main_journal_interface():
    """Main journaling interface."""
    import random
    # Philosophical taglines for rotation
    taglines = [
        "The examined life is the conscious life",
        "Know thyself through reflection",
        "Wisdom begins with self-awareness",
        "Every thought shapes the soul",
        "Consciousness observing consciousness",
        "The mirror reflects what already is"
    ]
    current_tagline = random.choice(taglines)
    
    # Header
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown('<h1 class="main-header">🪞 MIRROR</h1>', unsafe_allow_html=True)
        st.markdown(f'<p class="tagline">{current_tagline}</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 👤 Account")
        user = st.session_state.db.get_user_by_email(st.session_state.user_email)
        if user:
            st.markdown(f"### Welcome, {user['name']}")
            st.markdown(f"<span style='color: #94a3b8; font-size: 0.9rem;'>{user['email']}</span>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.button("Sign Out", use_container_width=True):
            st.session_state.user_id = None
            st.session_state.user_email = None
            st.rerun()
        
        st.markdown("---")
        
        # Statistics
        st.markdown("## 📊 Statistics")
        entries = st.session_state.db.get_user_entries(st.session_state.user_id)
        st.metric("Total Entries", len(entries))
        
        if entries:
            sentiment_data = st.session_state.db.get_entries_dataframe(st.session_state.user_id)
            if not sentiment_data.empty:
                avg_valence = sentiment_data['valence'].mean()
                valence_color = "#10b981" if avg_valence > 0.1 else "#ef4444" if avg_valence < -0.1 else "#6366f1"
                st.markdown(f'<div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, {valence_color}25 0%, {valence_color}10 100%); border-radius: 12px; margin: 1rem 0; border: 1px solid {valence_color}30;"><strong style="color: {valence_color}; font-size: 1.2rem;">{avg_valence:.2f}</strong><br><span style="color: #94a3b8; font-size: 0.85rem;">Avg Emotional Valence</span></div>', unsafe_allow_html=True)
    
    # Check if this is a new user (first time after signup)
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
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["✍️ Write", "📊 Timeline", "📈 Insights", "🎯 Goals"])
    
    # Tab 1: New Entry - Redesigned
    with tab1:
        if is_new_user:
            st.markdown("""<h2 style="font-size: 1.8rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.5rem;">Your First Reflection</h2>""", unsafe_allow_html=True)
            st.markdown("""<p style="color: #94a3b8; font-size: 1rem; margin-bottom: 1.5rem;">Start by writing about how you're feeling right now or what's on your mind</p>""", unsafe_allow_html=True)
        else:
            st.markdown("""<h2 style="font-size: 1.8rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.5rem;">New Entry</h2>""", unsafe_allow_html=True)
            st.markdown("""<p style="color: #94a3b8; font-size: 1rem; margin-bottom: 1.5rem;">Take a moment to reflect and let your thoughts flow</p>""", unsafe_allow_html=True)
        
        # Rotating prompts for inspiration
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
        
        # Show a random prompt
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
        
        # Character count
        char_count = len(entry_text)
        st.markdown(f"""<p style="text-align: right; color: #64748b; font-size: 0.85rem; margin-top: -0.5rem;">{char_count} characters</p>""", unsafe_allow_html=True)
        
        # Improved button layout
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            submit = st.button(
                "🪞 Reflect & Save" if is_new_user else "💾 Save Entry",
                type="primary",
                use_container_width=True,
                help="AI will analyze your emotions and patterns"
            )
        
        if submit and entry_text.strip():
            # Analyze sentiment
            sentiment_result = st.session_state.sentiment_analyzer.analyze(entry_text)
            
            # Save entry
            entry_id = st.session_state.db.add_journal_entry(
                user_id=st.session_state.user_id,
                entry_text=entry_text,
                sentiment_score=sentiment_result['sentiment_score'],
                valence=sentiment_result['valence']
            )
            
            # Detect biases
            biases = st.session_state.bias_detector.detect_all(
                entry_text,
                sentiment_result['valence']
            )
            
            # Save detected biases
            for bias in biases:
                st.session_state.db.add_bias(
                    entry_id=entry_id,
                    bias_type=bias['type'],
                    detected_pattern=bias['pattern'],
                    explanation=bias['explanation']
                )
            
            st.success("✅ Entry saved successfully!")
            
            # Show sentiment in a styled card - minimalist
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
            
            # Show biases
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
            
            # Clear form
            st.rerun()
        elif submit:
            st.error("Please write something before submitting.")
    
    # Tab 2: Timeline - Improved
    with tab2:
        st.markdown("""<h2 style="font-size: 1.8rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.5rem;">Emotional Timeline</h2>""", unsafe_allow_html=True)
        st.markdown("""<p style="color: #94a3b8; font-size: 1rem; margin-bottom: 1.5rem;">Visualize your emotional journey and discover patterns</p>""", unsafe_allow_html=True)
        
        sentiment_data = st.session_state.db.get_entries_dataframe(st.session_state.user_id)
        
        if not sentiment_data.empty:
            # Improved statistics cards
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
            
            # Create timeline with better styling
            st.markdown("""<h3 style="font-size: 1.3rem; font-weight: 600; color: #e2e8f0; margin: 2rem 0 1rem 0;">Your Emotional Journey</h3>""", unsafe_allow_html=True)
            fig = st.session_state.visualizer.create_timeline(sentiment_data)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            # Volatility chart
            if len(sentiment_data) >= 3:
                st.markdown("""<h3 style="font-size: 1.3rem; font-weight: 600; color: #e2e8f0; margin: 2rem 0 1rem 0;">Emotional Stability</h3>""", unsafe_allow_html=True)
                vol_fig = st.session_state.visualizer.create_volatility_chart(sentiment_data)
                st.plotly_chart(vol_fig, use_container_width=True, config={'displayModeBar': False})
        else:
            # Better empty state
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
    
    # Tab 3: Insights - Improved
    with tab3:
        st.markdown("""<h2 style="font-size: 1.8rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.5rem;">AI Insights</h2>""", unsafe_allow_html=True)
        st.markdown("""<p style="color: #94a3b8; font-size: 1rem; margin-bottom: 1.5rem;">Discover patterns, biases, and growth opportunities</p>""", unsafe_allow_html=True)
        
        week_start, week_end = get_week_range()
        
        # Get this week's entries
        entries = st.session_state.db.get_user_entries(st.session_state.user_id)
        week_entries = [
            entry for entry in entries
            if datetime.fromisoformat(entry['timestamp']) >= week_start
        ]
        
        if week_entries:
            sentiment_data = st.session_state.db.get_entries_dataframe(st.session_state.user_id)
            week_sentiment = sentiment_data[
                sentiment_data['timestamp'] >= pd.Timestamp(week_start)
            ]
            
            # Check if summary exists
            existing_summary = st.session_state.db.get_weekly_summary(
                st.session_state.user_id,
                week_start
            )
            
            if existing_summary:
                st.markdown(f"#### Week of {week_start.strftime('%B %d, %Y')}")
                st.markdown("---")
                
                # Summary text in a styled card - minimalist
                st.markdown(f"""
                    <div style="padding: 2rem; background: white; 
                    border-radius: 0; border-left: 3px solid #1a1a1a; margin: 1.5rem 0; line-height: 1.9; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05); font-family: 'Crimson Pro', serif; font-size: 1.05rem; color: #333;">
                    {existing_summary['summary_text'].replace(chr(10), '<br>')}
                    </div>
                """, unsafe_allow_html=True)
                
                if existing_summary.get('themes'):
                    st.markdown("#### 🎯 Key Themes")
                    themes_html = " ".join([f'<span style="display: inline-block; padding: 0.6rem 1.2rem; margin: 0.35rem; background: #1a1a1a; color: white; border-radius: 0; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em;">{theme}</span>' for theme in existing_summary['themes']])
                    st.markdown(themes_html, unsafe_allow_html=True)
                
                if existing_summary.get('emotions'):
                    st.markdown("#### 💭 Emotional Patterns")
                    emotions_html = " ".join([f'<span style="display: inline-block; padding: 0.6rem 1.2rem; margin: 0.35rem; background: #f5f5f5; color: #1a1a1a; border: 1px solid #e5e5e5; border-radius: 0; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em;">{emotion}</span>' for emotion in existing_summary['emotions']])
                    st.markdown(emotions_html, unsafe_allow_html=True)
            else:
                st.info(f"You have {len(week_entries)} entries this week. Generate your weekly summary to discover insights!")
                if st.button("✨ Generate Weekly Summary", type="primary", use_container_width=True):
                    with st.spinner("🔍 Analyzing your week..."):
                        summary_data = st.session_state.summary_generator.generate_summary(
                            week_entries,
                            week_sentiment
                        )
                        
                        # Save summary
                        st.session_state.db.save_weekly_summary(
                            user_id=st.session_state.user_id,
                            week_start=week_start,
                            summary_text=summary_data['summary_text'],
                            themes=summary_data['themes'],
                            emotions=summary_data['emotions']
                        )
                        
                        st.rerun()
        else:
            st.info("📝 No entries this week yet. Start journaling to generate your weekly summary!")
    
    # Tab 4: Goals & Growth
    with tab4:
        st.markdown("""<h2 style="font-size: 1.8rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.5rem;">Goals & Growth</h2>""", unsafe_allow_html=True)
        st.markdown("""<p style="color: #94a3b8; font-size: 1rem; margin-bottom: 1.5rem;">Track your cognitive patterns and personal development</p>""", unsafe_allow_html=True)
        
        entries = st.session_state.db.get_user_entries(st.session_state.user_id)
        
        if entries:
            # Collect all biases
            all_biases = []
            for entry in entries:
                biases = st.session_state.db.get_entry_biases(entry['id'])
                all_biases.extend(biases)
            
            if all_biases:
                # Bias frequency
                st.markdown("#### Bias Frequency Over Time")
                bias_counts = {}
                for bias in all_biases:
                    bias_type = bias['bias_type']
                    bias_counts[bias_type] = bias_counts.get(bias_type, 0) + 1
                
                bias_fig = st.session_state.visualizer.create_bias_frequency_chart(bias_counts)
                st.plotly_chart(bias_fig, use_container_width=True)
                
                st.markdown("---")
                
                # Recent biases
                st.markdown("#### Recent Detections")
                st.markdown("Review recent cognitive patterns detected in your entries:")
                
                recent_entries_with_biases = [
                    entry for entry in entries[:10]
                    if st.session_state.db.get_entry_biases(entry['id'])
                ]
                
                for entry in recent_entries_with_biases[:5]:
                    entry_biases = st.session_state.db.get_entry_biases(entry['id'])
                    if entry_biases:
                        entry_date = datetime.fromisoformat(entry['timestamp']).strftime('%B %d, %Y')
                        with st.expander(f"📅 Entry from {entry_date}"):
                            for bias in entry_biases:
                                st.markdown(f"""
                                    <div class="bias-alert">
                                        <strong>{bias['bias_type']}</strong>
                                        <p style="margin: 0.5rem 0 0 0; color: #78350f;">{bias['explanation']}</p>
                                    </div>
                                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="text-align: center; padding: 3rem 2rem; max-width: 600px; margin: 0 auto;">
                        <span style="font-size: 4rem; margin-bottom: 1.5rem; display: block; opacity: 0.5;">🎯</span>
                        <h3 style="font-size: 1.5rem; font-weight: 600; color: #cbd5e1; margin-bottom: 1rem;">Growing Self-Awareness</h3>
                        <p style="color: #94a3b8; font-size: 1rem; line-height: 1.8;">
                            No patterns detected yet. Keep journaling—the more you write, the more insights you'll discover.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="text-align: center; padding: 4rem 2rem; max-width: 600px; margin: 0 auto;">
                    <span style="font-size: 5rem; margin-bottom: 1.5rem; display: block; opacity: 0.5;">🧠</span>
                    <h3 style="font-size: 1.5rem; font-weight: 600; color: #cbd5e1; margin-bottom: 1rem;">Your Growth Journey</h3>
                    <p style="color: #94a3b8; font-size: 1.1rem; line-height: 1.8; margin-bottom: 2rem;">
                        Start reflecting to unlock cognitive insights.<br>
                        Discover patterns in your thinking and grow your self-awareness.
                    </p>
                    <div style="background: linear-gradient(135deg, #7c3aed15 0%, #a78bfa10 100%); border: 1px solid #7c3aed20; border-radius: 12px; padding: 1.5rem; text-align: left;">
                        <p style="color: #a78bfa; font-weight: 600; margin-bottom: 0.75rem;">What you'll discover:</p>
                        <ul style="color: #cbd5e1; margin-left: 1.5rem; line-height: 1.8;">
                            <li>Cognitive bias patterns</li>
                            <li>Thinking style trends</li>
                            <li>Emotional reasoning detection</li>
                            <li>Growth opportunities</li>
                        </ul>
                    </div>
                </div>
            """, unsafe_allow_html=True)


# Main app logic
def main():
    """Main application entry point."""
    if st.session_state.user_id is None:
        login_or_signup()
    else:
        main_journal_interface()


if __name__ == "__main__":
    main()

