"""Main Streamlit application for Mirror - Refactored & Optimized"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from supabase_client import SupabaseDatabase
from enhanced_sentiment import EnhancedSentimentAnalyzer
from enhanced_bias_detector import EnhancedBiasDetector
from visualization import EmotionalTimeline
from summary_generator import WeeklySummaryGenerator
from utils import get_week_start, get_week_range
from auth import verify_auth_token

st.set_page_config(
    page_title="Mirror - AI Journal",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

SHARED_CSS_PATH = Path(__file__).parent.parent / 'shared_styles.css'
try:
    if SHARED_CSS_PATH.exists():
        with open(SHARED_CSS_PATH, 'r') as f:
            shared_css = f.read()
        st.markdown(f'<style>{shared_css}</style>', unsafe_allow_html=True)
except Exception:
    pass

st.markdown("""
    <style>
    .stApp {
        background: #0f172a !important;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

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

    .stSuccess {
        background: linear-gradient(135deg, #064e3b 0%, #065f46 100%);
        border-left: 4px solid #10b981;
        color: #d1fae5;
        padding: 1rem;
        border-radius: 0.75rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }

    .stError {
        background: linear-gradient(135deg, #450a0a 0%, #7f1d1d 100%);
        border-left: 4px solid #ef4444;
        color: #fecaca;
        padding: 1rem;
        border-radius: 0.75rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }

    .stTextArea textarea {
        background-color: #1e293b !important;
        border: 1px solid #475569 !important;
        border-radius: 0.75rem !important;
        color: #f1f5f9 !important;
        font-size: 1rem !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
    }

    .stTextArea textarea:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.2) !important;
    }

    .stTextInput input {
        background-color: #1e293b !important;
        border: 1px solid #475569 !important;
        border-radius: 0.75rem !important;
        color: #f1f5f9 !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stTextInput input:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.2) !important;
    }

    .stButton button {
        background: linear-gradient(135deg, #7c3aed 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 0.75rem !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px rgba(124, 58, 237, 0.3) !important;
    }

    .stButton button:hover {
        background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%) !important;
        box-shadow: 0 6px 12px rgba(124, 58, 237, 0.4) !important;
        transform: translateY(-1px) !important;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #1e293b 0%, #0f172a 100%) !important;
        border-right: 1px solid #334155 !important;
    }

    [data-testid="stMetricValue"] {
        color: #a78bfa !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'db' not in st.session_state:
    st.session_state.db = SupabaseDatabase()
if 'sentiment_analyzer' not in st.session_state:
    st.session_state.sentiment_analyzer = EnhancedSentimentAnalyzer()
if 'bias_detector' not in st.session_state:
    st.session_state.bias_detector = EnhancedBiasDetector()
if 'visualizer' not in st.session_state:
    st.session_state.visualizer = EmotionalTimeline()
if 'summary_generator' not in st.session_state:
    st.session_state.summary_generator = WeeklySummaryGenerator(use_ai=False)


def check_auth_token():
    """Auto-login via JWT token from URL."""
    if st.session_state.user_id is not None:
        return True

    try:
        query_params = st.query_params
        auth_token = None

        if hasattr(query_params, 'get'):
            auth_token = query_params.get('auth_token', None)
        else:
            params_dict = query_params.to_dict() if hasattr(query_params, 'to_dict') else dict(query_params)
            auth_token = params_dict.get('auth_token', [None])[0] if isinstance(params_dict.get('auth_token'), list) else params_dict.get('auth_token', None)

        if auth_token:
            user_data = verify_auth_token(auth_token)

            if user_data:
                st.session_state.user_id = user_data['user_id']
                st.session_state.user_email = user_data['email']
                st.session_state.user_name = user_data['name']

                try:
                    st.query_params.clear()
                except:
                    pass

                return True
            else:
                show_redirect_to_landing()
                return False
        else:
            show_redirect_to_landing()
            return False

    except Exception as e:
        print(f"Auth error: {e}")
        import traceback
        traceback.print_exc()
        show_redirect_to_landing()
        return False


def show_redirect_to_landing():
    """Redirect to landing page."""
    landing_url = os.getenv('LANDING_PAGE_URL', 'http://localhost:5001')

    st.markdown(f"""
        <div style="text-align: center; padding: 5rem 2rem; max-width: 600px; margin: 0 auto;">
            <div style="display: flex; align-items: center; justify-content: center; gap: 1rem; margin-bottom: 2rem;">
                <span style="font-size: 4rem;">🧠</span>
                <h1 style="font-size: 3rem; font-weight: 800; color: #f1f5f9; margin: 0; background: linear-gradient(135deg, #a78bfa 0%, #7c3aed 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    Mirror
                </h1>
            </div>
            <p style="color: #cbd5e1; font-size: 1.2rem; line-height: 1.8; margin-bottom: 1rem;">
                Redirecting you to sign up...
            </p>
            <div style="display: inline-block; margin: 2rem 0;">
                <div style="width: 3rem; height: 3rem; border: 4px solid #334155; border-top-color: #7c3aed; border-radius: 50%; animation: spin 1s linear infinite;"></div>
            </div>
        </div>
        <style>
            @keyframes spin {{
                to {{ transform: rotate(360deg); }}
            }}
        </style>
        <meta http-equiv="refresh" content="1;url={landing_url}">
    """, unsafe_allow_html=True)

    st.stop()


def main_journal_interface():
    """Main dashboard interface."""
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 3rem; padding: 2rem 1rem; background: linear-gradient(135deg, rgba(124, 58, 237, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%); border-radius: 1rem; border: 1px solid rgba(124, 58, 237, 0.2); box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);">
            <div style="display: flex; align-items: center; justify-content: center; gap: 1rem; margin-bottom: 1rem;">
                <span style="font-size: 3.5rem;">🧠</span>
                <h1 style="font-size: 3.5rem; font-weight: 800; color: #f1f5f9; margin: 0; font-family: 'Inter', sans-serif; background: linear-gradient(135deg, #a78bfa 0%, #7c3aed 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    Mirror
                </h1>
            </div>
            <p style="color: #cbd5e1; font-size: 1.1rem; margin: 0; font-family: 'Inter', sans-serif;">
                Welcome back, <strong style="color: #a78bfa;">{st.session_state.user_name}</strong> ✨
            </p>
        </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 1])

    with col_left:
        landing_url = os.getenv('LANDING_PAGE_URL', 'http://localhost:5001')
        st.markdown(f"""
            <a href="{landing_url}" target="_self" style="text-decoration: none;">
                <button style="background: transparent; border: 1px solid #475569; color: #cbd5e1; padding: 0.5rem 1rem; border-radius: 0.5rem; font-family: Inter, sans-serif; font-size: 0.9rem; cursor: pointer;">
                    <span>←</span> Back to Landing
                </button>
            </a>
        """, unsafe_allow_html=True)

    with col_right:
        if st.button("🚪 Sign Out", key="signout", use_container_width=True):
            for key in ['user_id', 'user_email', 'user_name']:
                st.session_state[key] = None
            landing_url = os.getenv('LANDING_PAGE_URL', 'http://localhost:5001')
            st.markdown(f'<meta http-equiv="refresh" content="0;url={landing_url}">', unsafe_allow_html=True)
            st.stop()

    st.markdown("<br>", unsafe_allow_html=True)

    entries = st.session_state.db.get_user_entries(st.session_state.user_id)

    if entries and len(entries) > 0:
        sentiment_data = st.session_state.db.get_entries_dataframe(st.session_state.user_id)
    else:
        sentiment_data = pd.DataFrame()

    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        st.markdown("""<h2 style="font-size: 1.5rem; font-weight: 700; color: #f1f5f9; margin-bottom: 1rem;">📝 Today's Entry</h2>""", unsafe_allow_html=True)

        entry_text = st.text_area(
            "How are you feeling today? What's on your mind?",
            height=250,
            placeholder="Write freely about your thoughts, feelings, or experiences...",
            key="journal_entry"
        )

        char_count = len(entry_text)
        st.markdown(f"""<p style="text-align: right; color: #64748b; font-size: 0.85rem; margin-top: -0.5rem;">{char_count} characters</p>""", unsafe_allow_html=True)

        submit = st.button("💾 Save & Analyze", type="primary", use_container_width=True)

        if submit and entry_text.strip():
            with st.spinner("Analyzing your reflection..."):
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

                st.success(f"✅ Entry saved! Detected {len(biases)} cognitive pattern(s).")
                st.rerun()
        elif submit:
            st.warning("⚠️ Please write something before submitting.")

    with col2:
        st.markdown("""<h2 style="font-size: 1.5rem; font-weight: 700; color: #f1f5f9; margin-bottom: 1rem;">📊 Insights</h2>""", unsafe_allow_html=True)

        if not sentiment_data.empty and 'valence' in sentiment_data.columns and len(sentiment_data) > 0:
            try:
                recent_avg = sentiment_data['valence'].tail(7).mean() if len(sentiment_data) >= 7 else sentiment_data['valence'].mean()

                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #3b82f620 0%, #8b5cf610 100%); padding: 1.5rem; border-radius: 0.75rem; margin-bottom: 1rem; border: 1px solid #3b82f630;">
                        <p style="color: #94a3b8; font-size: 0.85rem; margin: 0 0 0.5rem 0;">7-Day Average</p>
                        <p style="color: #f1f5f9; font-size: 2rem; font-weight: 700; margin: 0;">{recent_avg:.2f}</p>
                        <p style="color: #cbd5e1; font-size: 0.85rem; margin: 0.5rem 0 0 0;">{'Positive trend' if recent_avg > 0 else 'Neutral' if recent_avg == 0 else 'Challenging period'}</p>
                    </div>
                """, unsafe_allow_html=True)

                avg_all = sentiment_data['valence'].mean()
                trend_direction = "Declining" if recent_avg < avg_all - 0.1 else "Improving" if recent_avg > avg_all + 0.1 else "Stable"
                trend_color = "#ef4444" if trend_direction == "Declining" else "#10b981" if trend_direction == "Improving" else "#6366f1"

                st.markdown(f"""
                    <div style="background: #1e293b; padding: 1rem; border-radius: 0.75rem; margin-bottom: 1rem; border: 1px solid #334155;">
                        <p style="color: #94a3b8; font-size: 0.85rem; margin: 0 0 0.5rem 0;">Recent Trend</p>
                        <p style="color: {trend_color}; font-size: 1.2rem; font-weight: 600; margin: 0;">{trend_direction}</p>
                    </div>
                """, unsafe_allow_html=True)

                volatility = sentiment_data['valence'].std()
                volatility_label = "Low volatility" if volatility < 0.3 else "Moderate" if volatility < 0.6 else "High volatility"

                st.markdown(f"""
                    <div style="background: #1e293b; padding: 1rem; border-radius: 0.75rem; border: 1px solid #334155;">
                        <p style="color: #94a3b8; font-size: 0.85rem; margin: 0 0 0.5rem 0;">Volatility</p>
                        <p style="color: #a78bfa; font-size: 1.2rem; font-weight: 600; margin: 0;">{volatility_label}</p>
                    </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.warning(f"Unable to calculate insights: {str(e)}")
        else:
            st.markdown("""
                <div style="background: #1e293b; padding: 2rem; border-radius: 0.75rem; text-align: center; border: 1px solid #334155;">
                    <span style="font-size: 3rem; display: block; margin-bottom: 1rem; opacity: 0.5;">📊</span>
                    <p style="color: #cbd5e1; font-size: 1rem; margin: 0;">Start journaling to see insights</p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""<h2 style="font-size: 1.5rem; font-weight: 700; color: #f1f5f9; margin-bottom: 1rem;">📈 Emotional Timeline</h2>""", unsafe_allow_html=True)

    if not sentiment_data.empty and len(sentiment_data) > 0:
        try:
            st.markdown(f"""<p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 1rem;">{len(sentiment_data)} entries tracked</p>""", unsafe_allow_html=True)
            fig = st.session_state.visualizer.create_timeline(sentiment_data)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        except Exception as e:
            st.error(f"Error creating timeline: {str(e)}")
    else:
        st.info(f"📉 Timeline will appear after your first entry")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<h2 style="font-size: 1.5rem; font-weight: 700; color: #f1f5f9; margin-bottom: 1rem;">🧠 Cognitive Patterns</h2>""", unsafe_allow_html=True)

    if len(entries) > 0:
        try:
            all_biases = []
            for entry in entries:
                try:
                    entry_biases = st.session_state.db.get_entry_biases(entry['id'])
                    all_biases.extend(entry_biases)
                except Exception:
                    pass

            if all_biases and len(all_biases) > 0:
                bias_counts = {}
                for bias in all_biases:
                    bias_type = bias.get('bias_type', 'Unknown')
                    bias_counts[bias_type] = bias_counts.get(bias_type, 0) + 1

                st.markdown(f"""<p style="color: #a78bfa; font-size: 0.9rem; margin-bottom: 1rem;">✓ Found {len(all_biases)} patterns</p>""", unsafe_allow_html=True)

                for bias_type, count in sorted(bias_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                    percentage = (count / len(all_biases)) * 100
                    st.markdown(f"""
                        <div style="background: #1e293b; padding: 1rem 1.5rem; border-radius: 0.75rem; margin-bottom: 0.75rem; border: 1px solid #334155;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <p style="color: #f1f5f9; font-weight: 600; margin: 0; font-size: 1rem;">{bias_type}</p>
                                <p style="color: #a78bfa; font-weight: 700; margin: 0; font-size: 1.1rem;">{percentage:.0f}%</p>
                            </div>
                            <p style="color: #94a3b8; font-size: 0.85rem; margin: 0.5rem 0 0 0;">Detected in {count} entr{'y' if count == 1 else 'ies'}</p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info(f"🧠 No patterns detected yet. Continue journaling!")
        except Exception as e:
            st.error(f"Error analyzing patterns: {str(e)}")
    else:
        st.info("📉 Pattern tracking will appear after your first entry")


def main():
    """Main entry point."""
    if check_auth_token():
        main_journal_interface()


if __name__ == "__main__":
    main()
