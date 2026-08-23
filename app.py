"""
Subscription Auditor
A financial dashboard for tracking, analyzing, and optimizing recurring
digital subscriptions, with an AI-powered advisor built on the Gemini API.
"""

import os
import io
from typing import Optional, Dict, Any, List

import pandas as pd
import streamlit as st

try:
    from google import genai
    from google.genai import types as genai_types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# =============================================================================
# CONSTANTS
# =============================================================================

GEMINI_MODEL = "gemini-2.5-flash"

CATEGORIES = [
    "Entertainment",
    "Music",
    "Productivity",
    "AI",
    "Cloud Storage",
    "News",
    "Gaming",
    "Education",
    "Shopping",
    "Other",
]

REQUIRED_CSV_COLUMNS = ["Service", "Monthly Cost", "Category", "Essential"]

INITIAL_DATA: List[Dict[str, Any]] = [
    {"Service": "Netflix", "Monthly Cost": 649.0, "Category": "Entertainment", "Essential": False},
    {"Service": "Spotify", "Monthly Cost": 119.0, "Category": "Music", "Essential": False},
    {"Service": "Canva", "Monthly Cost": 499.0, "Category": "Productivity", "Essential": True},
    {"Service": "ChatGPT", "Monthly Cost": 1999.0, "Category": "AI", "Essential": True},
    {"Service": "Amazon Prime", "Monthly Cost": 299.0, "Category": "Shopping", "Essential": False},
]

BASE_COLUMNS = ["Service", "Monthly Cost", "Category", "Essential"]


# =============================================================================
# CUSTOM CSS — dark modern fintech theme
# =============================================================================

APP_CSS = """
<style>
:root {
    --bg: #0B0F14;
    --bg-secondary: #111720;
    --card: #151C26;
    --card-hover: #1A2330;
    --border: rgba(255,255,255,0.08);
    --text: #F5F7FA;
    --muted: #9AA6B2;
    --accent: #4F8CFF;
    --accent-soft: rgba(79,140,255,0.14);
    --success: #35D07F;
    --success-soft: rgba(53,208,127,0.14);
    --warning: #F5B942;
    --warning-soft: rgba(245,185,66,0.14);
    --danger: #FF5C6C;
    --danger-soft: rgba(255,92,108,0.14);
}

html, body, [data-testid="stAppViewContainer"], [class*="css"] {
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background: var(--bg);
    color: var(--text);
}

[data-testid="stHeader"] {
    background: rgba(11,15,20,0.0);
}

[data-testid="stSidebar"] {
    background: var(--bg-secondary);
    border-right: 1px solid var(--border);
}

.block-container {
    padding-top: 1.4rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

h1, h2, h3, h4, h5, h6 { color: var(--text) !important; }
p, span, label, div { color: var(--text); }

/* Muted helper text */
.subtext { color: var(--muted); font-size: 0.9rem; margin-top: -0.35rem; }
.section-label {
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-size: 0.72rem;
    color: var(--muted);
    font-weight: 600;
    margin-bottom: 0.15rem;
}

/* Card containers (st.container(border=True)) */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 0.35rem 0.35rem !important;
    transition: background 0.2s ease, border-color 0.2s ease;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
    background: var(--card-hover) !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: transparent;
    padding: 0.2rem 0.1rem;
}
[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-size: 0.72rem !important;
    font-weight: 600;
}
[data-testid="stMetricValue"] {
    color: var(--text) !important;
    font-size: 1.7rem !important;
    font-weight: 700;
}
[data-testid="stMetricDelta"] svg { display: none; }
[data-testid="stMetricDelta"] {
    font-size: 0.8rem !important;
    color: var(--muted) !important;
}

/* Buttons */
.stButton > button {
    background: var(--accent);
    color: #FFFFFF;
    border: 1px solid var(--accent);
    border-radius: 10px;
    font-weight: 600;
    font-size: 0.9rem;
    padding: 0.5rem 1rem;
    transition: filter 0.15s ease, transform 0.05s ease;
}
.stButton > button:hover {
    filter: brightness(1.12);
}
.stButton > button:active {
    transform: translateY(1px);
}
.stDownloadButton > button {
    background: var(--bg-secondary);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 10px;
    font-weight: 600;
}
.stDownloadButton > button:hover {
    background: var(--card-hover);
    border-color: var(--accent);
}

/* Inputs */
input, textarea, .stNumberInput input, .stTextInput input {
    background: var(--bg-secondary) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}
[data-baseweb="select"] > div {
    background: var(--bg-secondary) !important;
    border-color: var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}
.stCheckbox label { color: var(--text) !important; }

/* Slider */
[data-testid="stSlider"] [role="slider"] {
    background: var(--accent) !important;
}

/* Expanders */
[data-testid="stExpander"] {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
}
[data-testid="stExpander"] summary {
    color: var(--text) !important;
    font-weight: 600;
}

/* Tabs */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 4px;
    border-bottom: 1px solid var(--border);
}
[data-testid="stTabs"] button[role="tab"] {
    color: var(--muted);
    font-weight: 600;
    padding: 0.55rem 1rem;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--accent);
    border-bottom: 2px solid var(--accent);
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 10px;
    border: 1px solid var(--border);
}

/* Dividers */
hr { border-color: var(--border) !important; }

/* Data editor */
[data-testid="stDataEditor"] {
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
}

/* Scrollbar */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 6px; }

/* Header */
.app-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 0.6rem 0 1.1rem 0;
}
.app-eyebrow {
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--accent);
    margin-bottom: 0.35rem;
}
.app-title {
    font-size: 2.1rem;
    font-weight: 800;
    color: var(--text);
    margin: 0;
    line-height: 1.15;
}
.app-subtitle {
    color: var(--muted);
    font-size: 0.95rem;
    margin-top: 0.3rem;
    max-width: 560px;
}
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: var(--success-soft);
    color: var(--success);
    border: 1px solid rgba(53,208,127,0.3);
    border-radius: 999px;
    padding: 0.35rem 0.85rem;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    white-space: nowrap;
}
.status-dot {
    width: 7px; height: 7px; border-radius: 50%; background: var(--success);
    box-shadow: 0 0 0 3px var(--success-soft);
}

/* KPI supporting text */
.kpi-context { color: var(--muted); font-size: 0.78rem; margin-top: 0.15rem; }

/* Health badge */
.health-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.3rem 0.8rem;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 0.02em;
}
.health-healthy { background: var(--success-soft); color: var(--success); border: 1px solid rgba(53,208,127,0.3); }
.health-review { background: var(--warning-soft); color: var(--warning); border: 1px solid rgba(245,185,66,0.3); }
.health-critical { background: var(--danger-soft); color: var(--danger); border: 1px solid rgba(255,92,108,0.3); }

/* Mini stat cards */
.mini-stat-label { color: var(--muted); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; }
.mini-stat-value { color: var(--text); font-size: 1.25rem; font-weight: 700; margin-top: 0.2rem; }
.mini-stat-sub { color: var(--muted); font-size: 0.78rem; margin-top: 0.1rem; }

/* AI badge */
.ai-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: var(--accent-soft);
    color: var(--accent);
    border: 1px solid rgba(79,140,255,0.3);
    border-radius: 999px;
    padding: 0.2rem 0.65rem;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    margin-left: 0.5rem;
    vertical-align: middle;
}

/* Savings progress bar */
.savings-bar-track {
    width: 100%;
    height: 10px;
    background: var(--bg-secondary);
    border-radius: 999px;
    overflow: hidden;
    border: 1px solid var(--border);
    margin-top: 0.3rem;
}
.savings-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--accent), var(--success));
    border-radius: 999px;
}

/* Empty state */
.empty-state {
    text-align: center;
    padding: 2.2rem 1rem;
    color: var(--muted);
}
.empty-state-title { color: var(--text); font-size: 1.05rem; font-weight: 700; margin-bottom: 0.3rem; }

/* AI result container */
.ai-result {
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-top: 0.5rem;
}

/* Card header block used inside bordered containers */
.card-title { font-size: 1.05rem; font-weight: 700; color: var(--text); margin-bottom: 0.05rem; }
.card-subtitle { font-size: 0.85rem; color: var(--muted); margin-bottom: 0.6rem; }
</style>
"""


def inject_css() -> None:
    st.markdown(APP_CSS, unsafe_allow_html=True)


# =============================================================================
# SESSION STATE
# =============================================================================

def initialize_session_state() -> None:
    """Initialize all session-state variables needed by the app."""
    if "subscriptions" not in st.session_state:
        st.session_state.subscriptions = pd.DataFrame(INITIAL_DATA, columns=BASE_COLUMNS)

    if "ai_analysis" not in st.session_state:
        st.session_state.ai_analysis = None

    if "confirm_clear_all" not in st.session_state:
        st.session_state.confirm_clear_all = False

    if "confirm_csv_replace" not in st.session_state:
        st.session_state.confirm_csv_replace = False

    if "pending_csv_df" not in st.session_state:
        st.session_state.pending_csv_df = None


# =============================================================================
# DATA SANITIZATION & CALCULATIONS
# =============================================================================

def sanitize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and validate a subscriptions DataFrame, returning a safe copy."""
    if df is None or df.empty:
        return pd.DataFrame(columns=BASE_COLUMNS)

    clean = df.copy()

    for col in BASE_COLUMNS:
        if col not in clean.columns:
            if col == "Monthly Cost":
                clean[col] = 0.0
            elif col == "Essential":
                clean[col] = False
            else:
                clean[col] = ""

    clean["Service"] = clean["Service"].astype(str).str.strip()
    clean = clean[clean["Service"] != ""]
    clean = clean[clean["Service"].str.lower() != "nan"]

    clean["Monthly Cost"] = pd.to_numeric(clean["Monthly Cost"], errors="coerce").fillna(0.0)
    clean["Monthly Cost"] = clean["Monthly Cost"].clip(lower=0.0)

    clean["Category"] = clean["Category"].astype(str).str.strip()
    clean.loc[~clean["Category"].isin(CATEGORIES), "Category"] = "Other"

    clean["Essential"] = clean["Essential"].apply(_to_bool)

    clean = clean[BASE_COLUMNS].reset_index(drop=True)
    return clean


def _to_bool(value: Any) -> bool:
    """Safely coerce a variety of representations to a boolean."""
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)) and not pd.isna(value):
        return bool(value)
    if isinstance(value, str):
        return value.strip().lower() in ("true", "yes", "1", "y")
    return False


def calculate_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """Compute all headline analytics from the subscriptions DataFrame."""
    if df is None or df.empty:
        return {
            "monthly_total": 0.0,
            "annual_total": 0.0,
            "num_subscriptions": 0,
            "avg_monthly_cost": 0.0,
            "highest_monthly_service": None,
            "highest_monthly_cost": 0.0,
            "highest_annual_service": None,
            "highest_annual_cost": 0.0,
            "num_essential": 0,
            "num_discretionary": 0,
            "essential_cost": 0.0,
            "discretionary_cost": 0.0,
            "category_totals": pd.Series(dtype=float),
            "category_pct": pd.Series(dtype=float),
            "top3": pd.DataFrame(columns=["Service", "Annual Cost"]),
            "largest_category": None,
            "largest_category_total": 0.0,
            "discretionary_pct": 0.0,
        }

    working = df.copy()
    working["Annual Cost"] = working["Monthly Cost"] * 12

    monthly_total = float(working["Monthly Cost"].sum())
    annual_total = float(working["Annual Cost"].sum())
    num_subscriptions = int(len(working))
    avg_monthly_cost = float(working["Monthly Cost"].mean()) if num_subscriptions else 0.0

    if num_subscriptions:
        top_monthly_row = working.loc[working["Monthly Cost"].idxmax()]
        highest_monthly_service = top_monthly_row["Service"]
        highest_monthly_cost = float(top_monthly_row["Monthly Cost"])

        top_annual_row = working.loc[working["Annual Cost"].idxmax()]
        highest_annual_service = top_annual_row["Service"]
        highest_annual_cost = float(top_annual_row["Annual Cost"])
    else:
        highest_monthly_service = None
        highest_monthly_cost = 0.0
        highest_annual_service = None
        highest_annual_cost = 0.0

    essential_mask = working["Essential"] == True  # noqa: E712
    num_essential = int(essential_mask.sum())
    num_discretionary = int((~essential_mask).sum())
    essential_cost = float(working.loc[essential_mask, "Monthly Cost"].sum())
    discretionary_cost = float(working.loc[~essential_mask, "Monthly Cost"].sum())
    discretionary_pct = (discretionary_cost / monthly_total * 100) if monthly_total > 0 else 0.0

    category_totals = working.groupby("Category")["Annual Cost"].sum().sort_values(ascending=False)
    category_pct = (category_totals / annual_total * 100) if annual_total > 0 else category_totals * 0

    top3 = working.sort_values("Annual Cost", ascending=False).head(3)[["Service", "Annual Cost"]].reset_index(drop=True)

    largest_category = category_totals.index[0] if not category_totals.empty else None
    largest_category_total = float(category_totals.iloc[0]) if not category_totals.empty else 0.0

    return {
        "monthly_total": monthly_total,
        "annual_total": annual_total,
        "num_subscriptions": num_subscriptions,
        "avg_monthly_cost": avg_monthly_cost,
        "highest_monthly_service": highest_monthly_service,
        "highest_monthly_cost": highest_monthly_cost,
        "highest_annual_service": highest_annual_service,
        "highest_annual_cost": highest_annual_cost,
        "num_essential": num_essential,
        "num_discretionary": num_discretionary,
        "essential_cost": essential_cost,
        "discretionary_cost": discretionary_cost,
        "category_totals": category_totals,
        "category_pct": category_pct,
        "top3": top3,
        "largest_category": largest_category,
        "largest_category_total": largest_category_total,
        "discretionary_pct": discretionary_pct,
    }


def calculate_savings(df: pd.DataFrame, reduction_pct: float) -> Dict[str, float]:
    """
    Deterministic savings simulation.

    Discretionary (non-essential) subscriptions are treated as the pool
    eligible for reduction. The user-selected percentage is applied only
    to that discretionary annual spend, since essential subscriptions are
    assumed to remain untouched.
    """
    if df is None or df.empty:
        return {
            "current_annual": 0.0,
            "projected_annual": 0.0,
            "estimated_savings": 0.0,
            "discretionary_annual": 0.0,
        }

    working = df.copy()
    working["Annual Cost"] = working["Monthly Cost"] * 12

    current_annual = float(working["Annual Cost"].sum())
    discretionary_annual = float(working.loc[working["Essential"] == False, "Annual Cost"].sum())  # noqa: E712

    estimated_savings = discretionary_annual * (reduction_pct / 100.0)
    projected_annual = current_annual - estimated_savings

    return {
        "current_annual": current_annual,
        "projected_annual": projected_annual,
        "estimated_savings": estimated_savings,
        "discretionary_annual": discretionary_annual,
    }


def assess_health(monthly_total: float, discretionary_cost: float, annual_total: float) -> Dict[str, str]:
    """
    Simple, transparent rule-based subscription health assessment.

    Thresholds:
      - Critical: annual total > 60,000 INR
      - Review: discretionary spend is more than 50% of monthly total
      - Healthy: otherwise
    """
    discretionary_ratio = (discretionary_cost / monthly_total * 100) if monthly_total > 0 else 0.0

    if annual_total > 60000:
        status = "Critical"
        reason = f"Annual recurring cost (₹{annual_total:,.0f}) exceeds ₹60,000, a high-spend threshold."
    elif discretionary_ratio > 50:
        status = "Review"
        reason = f"Discretionary (non-essential) subscriptions make up {discretionary_ratio:.0f}% of monthly spending, above the 50% threshold."
    else:
        status = "Healthy"
        reason = "Spending is within reasonable, manageable thresholds based on your current data."

    return {"status": status, "reason": reason}


# =============================================================================
# GEMINI CLIENT
# =============================================================================

def get_gemini_client() -> Optional["genai.Client"]:
    """
    Attempt to construct a Gemini client using Streamlit secrets first,
    falling back to an environment variable. Returns None if unavailable.
    """
    if not GENAI_AVAILABLE:
        return None

    api_key = None
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None

    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return None

    try:
        client = genai.Client(api_key=api_key)
        return client
    except Exception:
        return None


def build_gemini_prompt(df: pd.DataFrame, metrics: Dict[str, Any], savings: Dict[str, float]) -> str:
    """Dynamically construct the user prompt from real subscription data."""
    working = df.copy()
    working["Annual Cost"] = working["Monthly Cost"] * 12

    lines = []
    for _, row in working.iterrows():
        essential_label = "Essential" if row["Essential"] else "Non-essential"
        lines.append(
            f"- {row['Service']} | Category: {row['Category']} | "
            f"Monthly: ₹{row['Monthly Cost']:,.2f} | Annual: ₹{row['Annual Cost']:,.2f} | {essential_label}"
        )
    subscription_data = "\n".join(lines) if lines else "No subscriptions recorded."

    category_lines = []
    for cat, total in metrics["category_totals"].items():
        pct = metrics["category_pct"].get(cat, 0.0)
        category_lines.append(f"- {cat}: ₹{total:,.2f}/year ({pct:.1f}% of total)")
    category_summary = "\n".join(category_lines) if category_lines else "No category data available."

    prompt = f"""
Analyze this user's subscription portfolio and provide a practical, honest cost-optimization review.

FINANCIAL OVERVIEW
Total monthly spending: ₹{metrics['monthly_total']:,.2f}
Total annual spending: ₹{metrics['annual_total']:,.2f}
Number of subscriptions: {metrics['num_subscriptions']}
Average monthly cost per subscription: ₹{metrics['avg_monthly_cost']:,.2f}
Essential subscriptions: {metrics['num_essential']} (₹{metrics['essential_cost']:,.2f}/month)
Discretionary subscriptions: {metrics['num_discretionary']} (₹{metrics['discretionary_cost']:,.2f}/month)
Highest monthly-cost subscription: {metrics['highest_monthly_service']} (₹{metrics['highest_monthly_cost']:,.2f}/month)

SPENDING BY CATEGORY
{category_summary}

INDIVIDUAL SUBSCRIPTIONS
{subscription_data}

CURRENT SAVINGS SIMULATION
Current projected annual cost: ₹{savings['current_annual']:,.2f}
Projected annual cost after simulated reduction: ₹{savings['projected_annual']:,.2f}
Estimated annual savings from simulation: ₹{savings['estimated_savings']:,.2f}

Please structure your response with these exact headings:
1. Overall Financial Diagnosis
2. Biggest Spending Leaks
3. Subscriptions Worth Reconsidering
4. Possible Cheaper Alternatives
5. Estimated Potential Savings
6. 30-Day Action Plan

Use bullet points where helpful. Do not invent exact prices for alternatives unless you are reasonably confident; when uncertain, describe the type of alternative rather than a specific price. Keep the response concise and practical.
""".strip()

    return prompt


def run_gemini_analysis(client: "genai.Client", prompt: str) -> str:
    """Send the constructed prompt to Gemini with a system instruction and return the text response."""
    system_instruction = (
        "You are the 'Subscription Auditor AI', a specialized subscription-cost "
        "optimization advisor. You are not a generic chatbot. Your job is to analyze "
        "recurring digital subscription spending and help the user reduce unnecessary "
        "costs.\n\n"
        "Rules you must follow:\n"
        "- Distinguish essential and discretionary services, and weigh them differently.\n"
        "- Identify expensive subscriptions and overlapping/duplicate services.\n"
        "- Recommend cheaper alternatives only where reasonable, and frame them as suggestions, not facts.\n"
        "- Never claim to have live or real-time pricing. Only reference prices the user provided, "
        "or clearly state when you are estimating.\n"
        "- Do not invent exact prices when uncertain.\n"
        "- Do not recommend cancelling genuinely necessary (essential) services without explaining the tradeoff.\n"
        "- Be concise, practical, and use clear headings and bullet points.\n"
        "- Estimate savings only from the numbers provided or clearly stated assumptions."
    )

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=genai_types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.4,
        ),
    )

    text = getattr(response, "text", None)
    if not text:
        raise ValueError("Gemini returned an empty response.")
    return text


# =============================================================================
# SMALL RENDER HELPERS
# =============================================================================

def _fmt_currency(value: float) -> str:
    return f"₹{value:,.2f}"


def render_header() -> None:
    col_left, col_right = st.columns([4, 1])
    with col_left:
        st.markdown(
            """
            <div class="app-header-inner">
                <div class="app-eyebrow">Financial Control Center</div>
                <div class="app-title">Subscription Auditor</div>
                <div class="app-subtitle">
                    Track recurring expenses, identify spending leaks, and optimize your
                    monthly digital subscriptions.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_right:
        st.markdown(
            """
            <div style="display:flex; justify-content:flex-end; padding-top: 0.9rem;">
                <span class="status-badge"><span class="status-dot"></span>SYSTEM READY</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("<div style='margin-bottom: 0.4rem;'></div>", unsafe_allow_html=True)


def render_empty_state(message_title: str, message_body: str) -> None:
    st.markdown(
        f"""
        <div class="empty-state">
            <div class="empty-state-title">{message_title}</div>
            <div>{message_body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# INPUT FORM
# =============================================================================

def render_input_form() -> None:
    with st.container(border=True):
        st.markdown('<div class="card-title">Add subscription</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-subtitle">Add a recurring service to your portfolio.</div>', unsafe_allow_html=True)

        with st.form("add_subscription_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                service_name = st.text_input("Service")
                monthly_cost = st.number_input("Monthly Cost (INR)", min_value=0.0, step=10.0, format="%.2f")
            with col2:
                category = st.selectbox("Category", CATEGORIES)
                essential = st.checkbox("Essential subscription")

            description = st.text_input("Description (optional)")

            submitted = st.form_submit_button("Add Subscription", use_container_width=True)

            if submitted:
                clean_name = service_name.strip()
                if not clean_name:
                    st.warning("Please enter a subscription name before adding it.")
                elif monthly_cost <= 0:
                    st.warning("Monthly cost must be greater than zero.")
                else:
                    new_row = pd.DataFrame([{
                        "Service": clean_name,
                        "Monthly Cost": float(monthly_cost),
                        "Category": category,
                        "Essential": bool(essential),
                    }])
                    st.session_state.subscriptions = pd.concat(
                        [st.session_state.subscriptions, new_row], ignore_index=True
                    )
                    st.session_state.subscriptions = sanitize_dataframe(st.session_state.subscriptions)
                    st.success(f"Added '{clean_name}' to your subscriptions.")
                    if description.strip():
                        st.caption(f"Note: {description.strip()}")


# =============================================================================
# DATA EDITOR
# =============================================================================

def render_data_editor() -> None:
    with st.container(border=True):
        st.markdown('<div class="card-title">Your subscriptions</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="card-subtitle">Edit prices, categories, and essential status directly below.</div>',
            unsafe_allow_html=True,
        )

        base_df = st.session_state.subscriptions.copy()

        if base_df.empty:
            render_empty_state(
                "No subscriptions yet",
                "Add your first recurring service above to start tracking your spending.",
            )
            return

        display_df = base_df.copy()
        display_df["Annual Cost"] = display_df["Monthly Cost"] * 12
        monthly_total = display_df["Monthly Cost"].sum()
        display_df["Monthly Percentage"] = (
            (display_df["Monthly Cost"] / monthly_total * 100) if monthly_total > 0 else 0.0
        )
        annual_total = display_df["Annual Cost"].sum()
        display_df["Annual Percentage"] = (
            (display_df["Annual Cost"] / annual_total * 100) if annual_total > 0 else 0.0
        )

        edited_df = st.data_editor(
            display_df,
            column_config={
                "Service": st.column_config.TextColumn("Service", required=True),
                "Monthly Cost": st.column_config.NumberColumn("Monthly Cost (₹)", min_value=0.0, format="%.2f"),
                "Category": st.column_config.SelectboxColumn("Category", options=CATEGORIES),
                "Essential": st.column_config.CheckboxColumn("Essential"),
                "Annual Cost": st.column_config.NumberColumn("Annual Cost (₹)", format="%.2f", disabled=True),
                "Monthly Percentage": st.column_config.NumberColumn("Monthly %", format="%.1f%%", disabled=True),
                "Annual Percentage": st.column_config.NumberColumn("Annual %", format="%.1f%%", disabled=True),
            },
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            key="subscription_editor",
        )

        editable_cols = edited_df[BASE_COLUMNS].copy()
        cleaned = sanitize_dataframe(editable_cols)
        st.session_state.subscriptions = cleaned


# =============================================================================
# KPI CARDS
# =============================================================================

def render_kpis(metrics: Dict[str, Any], savings: Dict[str, float]) -> None:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.container(border=True):
            st.metric("Monthly Spend", _fmt_currency(metrics["monthly_total"]))
            st.markdown(
                f'<div class="kpi-context">Across {metrics["num_subscriptions"]} active subscription(s)</div>',
                unsafe_allow_html=True,
            )

    with col2:
        with st.container(border=True):
            st.metric(
                "Annual Spend",
                _fmt_currency(metrics["annual_total"]),
                delta=f"{_fmt_currency(metrics['monthly_total'])} / month",
                delta_color="off",
            )

    with col3:
        with st.container(border=True):
            st.metric("Active Subscriptions", f"{metrics['num_subscriptions']}")
            st.markdown(
                f'<div class="kpi-context">{metrics["num_essential"]} essential · '
                f'{metrics["num_discretionary"]} discretionary</div>',
                unsafe_allow_html=True,
            )

    with col4:
        with st.container(border=True):
            st.metric(
                "Potential Annual Savings",
                _fmt_currency(savings["estimated_savings"]),
                delta="at a 20% reduction target",
                delta_color="normal",
            )


def render_health_card(metrics: Dict[str, Any]) -> None:
    with st.container(border=True):
        st.markdown('<div class="card-title">Subscription Health</div>', unsafe_allow_html=True)

        if metrics["num_subscriptions"] == 0:
            st.markdown('<div class="card-subtitle">Add subscriptions to see your health status.</div>', unsafe_allow_html=True)
            return

        health = assess_health(metrics["monthly_total"], metrics["discretionary_cost"], metrics["annual_total"])
        css_class = {"Healthy": "health-healthy", "Review": "health-review", "Critical": "health-critical"}.get(
            health["status"], "health-healthy"
        )

        st.markdown(
            f'<span class="health-pill {css_class}">{health["status"].upper()}</span>',
            unsafe_allow_html=True,
        )
        st.markdown(f'<div class="kpi-context" style="margin-top:0.5rem;">{health["reason"]}</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="kpi-context" style="margin-top:0.4rem; opacity:0.8;">'
            'This is a simple, rule-based indicator for educational and personal budgeting purposes only. '
            'It does not constitute professional financial advice.</div>',
            unsafe_allow_html=True,
        )


def render_spending_breakdown(metrics: Dict[str, Any]) -> None:
    with st.container(border=True):
        st.markdown('<div class="card-title">Spending Breakdown</div>', unsafe_allow_html=True)

        if metrics["num_subscriptions"] == 0:
            st.markdown('<div class="card-subtitle">Add subscriptions to see a breakdown.</div>', unsafe_allow_html=True)
            return

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown('<div class="mini-stat-label">Top Subscription</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="mini-stat-value">{metrics["highest_monthly_service"]}</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="mini-stat-sub">{_fmt_currency(metrics["highest_monthly_cost"])}/mo</div>',
                unsafe_allow_html=True,
            )
        with c2:
            largest_cat = metrics["largest_category"] or "—"
            st.markdown('<div class="mini-stat-label">Largest Category</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="mini-stat-value">{largest_cat}</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="mini-stat-sub">{_fmt_currency(metrics["largest_category_total"])}/yr</div>',
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown('<div class="mini-stat-label">Avg. Subscription Cost</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="mini-stat-value">{_fmt_currency(metrics["avg_monthly_cost"])}</div>', unsafe_allow_html=True)
            st.markdown('<div class="mini-stat-sub">per month</div>', unsafe_allow_html=True)
        with c4:
            st.markdown('<div class="mini-stat-label">Discretionary Spend</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="mini-stat-value">{metrics["discretionary_pct"]:.0f}%</div>', unsafe_allow_html=True)
            st.markdown('<div class="mini-stat-sub">of monthly total</div>', unsafe_allow_html=True)


# =============================================================================
# CHARTS
# =============================================================================

def render_charts(df: pd.DataFrame, metrics: Dict[str, Any]) -> None:
    if df.empty:
        with st.container(border=True):
            render_empty_state(
                "Nothing to visualize yet",
                "Add a subscription to unlock spending charts and category breakdowns.",
            )
        return

    working = df.copy()
    working["Annual Cost"] = working["Monthly Cost"] * 12

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown('<div class="card-title">Annual Spend by Subscription</div>', unsafe_allow_html=True)
            chart_data = working.set_index("Service")[["Annual Cost"]].sort_values("Annual Cost", ascending=False)
            st.bar_chart(chart_data, height=260)

    with col2:
        with st.container(border=True):
            st.markdown('<div class="card-title">Annual Spend by Category</div>', unsafe_allow_html=True)
            if not metrics["category_totals"].empty:
                st.bar_chart(metrics["category_totals"], height=260)
            else:
                st.markdown('<div class="card-subtitle">No category data available.</div>', unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<div class="card-title">Essential vs. Non-Essential Spending (Annual)</div>', unsafe_allow_html=True)
        essential_vs_discretionary = pd.DataFrame({
            "Type": ["Essential", "Non-Essential"],
            "Annual Cost": [metrics["essential_cost"] * 12, metrics["discretionary_cost"] * 12],
        }).set_index("Type")
        st.bar_chart(essential_vs_discretionary, height=220)


def render_analysis_detail(metrics: Dict[str, Any]) -> None:
    if metrics["num_subscriptions"] == 0:
        return

    with st.expander("Detailed breakdown", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Average monthly cost:** {_fmt_currency(metrics['avg_monthly_cost'])}")
            st.write(f"**Highest monthly subscription:** {metrics['highest_monthly_service']} "
                     f"({_fmt_currency(metrics['highest_monthly_cost'])})")
            st.write(f"**Highest annual subscription:** {metrics['highest_annual_service']} "
                     f"({_fmt_currency(metrics['highest_annual_cost'])})")
        with col2:
            st.write(f"**Essential subscriptions:** {metrics['num_essential']} "
                     f"({_fmt_currency(metrics['essential_cost'])}/month)")
            st.write(f"**Discretionary subscriptions:** {metrics['num_discretionary']} "
                     f"({_fmt_currency(metrics['discretionary_cost'])}/month)")

        if not metrics["category_totals"].empty:
            st.write("**Spending by category:**")
            cat_df = pd.DataFrame({
                "Category": metrics["category_totals"].index,
                "Annual Cost": metrics["category_totals"].values,
                "% of Total": metrics["category_pct"].values,
            })
            st.dataframe(cat_df, use_container_width=True, hide_index=True)

        if not metrics["top3"].empty:
            st.write("**Top 3 subscriptions by annual cost:**")
            st.dataframe(metrics["top3"], use_container_width=True, hide_index=True)


# =============================================================================
# SAVINGS SIMULATOR
# =============================================================================

def render_savings_simulator(df: pd.DataFrame) -> Dict[str, float]:
    with st.container(border=True):
        st.markdown('<div class="card-title">Savings Simulator</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="card-subtitle">See how small reductions in recurring expenses affect your annual spending.</div>',
            unsafe_allow_html=True,
        )

        if df.empty:
            render_empty_state("No data to simulate", "Add subscriptions to run the savings simulator.")
            return calculate_savings(df, 0.0)

        reduction_pct = st.slider("Hypothetical reduction target (%)", min_value=5, max_value=50, value=20, step=5)
        savings = calculate_savings(df, reduction_pct)

        progress_pct = 0.0
        if savings["current_annual"] > 0:
            progress_pct = max(0.0, min(100.0, (savings["projected_annual"] / savings["current_annual"]) * 100))

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Annual Cost", _fmt_currency(savings["current_annual"]))
        with col2:
            st.metric("Projected Annual Cost", _fmt_currency(savings["projected_annual"]))
        with col3:
            st.metric("Estimated Annual Savings", _fmt_currency(savings["estimated_savings"]))

        st.markdown(
            f"""
            <div class="kpi-context">Projected spend as a share of current cost</div>
            <div class="savings-bar-track">
                <div class="savings-bar-fill" style="width:{progress_pct:.1f}%;"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        return savings


# =============================================================================
# AI ADVISOR
# =============================================================================

def render_ai_analysis(df: pd.DataFrame, metrics: Dict[str, Any], savings: Dict[str, float]) -> None:
    with st.container(border=True):
        st.markdown(
            '<div class="card-title">AI Subscription Advisor<span class="ai-badge">GEMINI POWERED</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="card-subtitle">Get a personalized analysis of your recurring spending, '
            'overlapping services, and potential savings.</div>',
            unsafe_allow_html=True,
        )

        client = get_gemini_client()

        if not GENAI_AVAILABLE:
            st.warning(
                "The google-genai package is not installed, so Gemini analysis is unavailable. "
                "Install it with `pip install google-genai` to enable this feature."
            )
        elif client is None:
            st.warning(
                "Gemini analysis is unavailable until a Gemini API key is configured. "
                "Add `GEMINI_API_KEY` to your Streamlit secrets or set it as an environment variable."
            )

        col1, col2 = st.columns([3, 1])
        with col1:
            analyze_clicked = st.button(
                "Analyze My Subscriptions",
                use_container_width=True,
                disabled=(client is None or df.empty),
            )
        with col2:
            clear_clicked = st.button("Clear Analysis", use_container_width=True)

        if clear_clicked:
            st.session_state.ai_analysis = None
            st.info("AI analysis cleared.")

        if analyze_clicked:
            if df.empty:
                st.warning("Add at least one subscription before requesting an analysis.")
            elif client is None:
                st.warning("Gemini analysis is unavailable until a Gemini API key is configured.")
            else:
                with st.spinner("Analyzing your subscriptions with Gemini..."):
                    try:
                        prompt = build_gemini_prompt(df, metrics, savings)
                        result_text = run_gemini_analysis(client, prompt)
                        st.session_state.ai_analysis = result_text
                        st.success("Analysis complete.")
                    except Exception:
                        st.error(
                            "Something went wrong while contacting Gemini. Please check your API key "
                            "and try again in a moment."
                        )

        if st.session_state.ai_analysis:
            st.markdown('<div class="ai-result">', unsafe_allow_html=True)
            st.markdown(st.session_state.ai_analysis)
            st.markdown('</div>', unsafe_allow_html=True)


# =============================================================================
# CSV TOOLS
# =============================================================================

def render_csv_tools(df: pd.DataFrame) -> None:
    col1, col2 = st.columns(2)

    with col1:
        st.caption("Upload a CSV with columns: Service, Monthly Cost, Category, Essential")
        uploaded_file = st.file_uploader("Import subscriptions from CSV", type=["csv"])

        if uploaded_file is not None:
            try:
                new_df = pd.read_csv(uploaded_file)
                missing_cols = [c for c in REQUIRED_CSV_COLUMNS if c not in new_df.columns]
                if missing_cols:
                    st.error(f"CSV is missing required column(s): {', '.join(missing_cols)}")
                else:
                    st.session_state.pending_csv_df = sanitize_dataframe(new_df)
                    st.session_state.confirm_csv_replace = True
            except Exception:
                st.error("Could not read this CSV file. Please check the format and try again.")

        if st.session_state.confirm_csv_replace and st.session_state.pending_csv_df is not None:
            st.warning(
                f"This will replace your current {len(df)} subscription(s) with "
                f"{len(st.session_state.pending_csv_df)} subscription(s) from the uploaded file."
            )
            confirm_col1, confirm_col2 = st.columns(2)
            with confirm_col1:
                if st.button("Confirm Replace", use_container_width=True):
                    st.session_state.subscriptions = st.session_state.pending_csv_df
                    st.session_state.pending_csv_df = None
                    st.session_state.confirm_csv_replace = False
                    st.success("Subscriptions replaced from CSV.")
                    st.rerun()
            with confirm_col2:
                if st.button("Cancel Import", use_container_width=True):
                    st.session_state.pending_csv_df = None
                    st.session_state.confirm_csv_replace = False
                    st.info("CSV import cancelled.")

    with col2:
        st.caption("Download your current subscriptions as a CSV file.")
        if not df.empty:
            csv_buffer = io.StringIO()
            df[BASE_COLUMNS].to_csv(csv_buffer, index=False)
            st.download_button(
                "Download Current Subscriptions (CSV)",
                data=csv_buffer.getvalue(),
                file_name="subscriptions.csv",
                mime="text/csv",
                use_container_width=True,
            )
        else:
            st.info("No subscriptions to export yet.")


# =============================================================================
# RESET / DANGER CONTROLS
# =============================================================================

def render_reset_controls() -> None:
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Reset Demo Data", use_container_width=True):
            st.session_state.subscriptions = pd.DataFrame(INITIAL_DATA, columns=BASE_COLUMNS)
            st.session_state.ai_analysis = None
            st.session_state.confirm_clear_all = False
            st.success("Demo data restored.")
            st.rerun()

    with col2:
        if not st.session_state.confirm_clear_all:
            if st.button("Clear All Subscriptions", use_container_width=True):
                st.session_state.confirm_clear_all = True
        else:
            st.warning("Are you sure? This will remove all subscriptions.")
            confirm_col1, confirm_col2 = st.columns(2)
            with confirm_col1:
                if st.button("Yes, Clear All", use_container_width=True):
                    st.session_state.subscriptions = pd.DataFrame(columns=BASE_COLUMNS)
                    st.session_state.ai_analysis = None
                    st.session_state.confirm_clear_all = False
                    st.success("All subscriptions cleared.")
                    st.rerun()
            with confirm_col2:
                if st.button("Cancel", use_container_width=True):
                    st.session_state.confirm_clear_all = False


def render_footer() -> None:
    st.markdown(
        """
        <div style="text-align:center; padding: 1rem 0 0.4rem 0; color: var(--muted); font-size: 0.82rem;">
            Subscription Auditor · Built with Streamlit and the Gemini API · For educational and personal
            budgeting purposes only. Not professional financial advice.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# MAIN
# =============================================================================

def main() -> None:
    st.set_page_config(
        page_title="Subscription Auditor",
        page_icon="💸",
        layout="wide",
    )

    inject_css()
    initialize_session_state()
    render_header()

    st.session_state.subscriptions = sanitize_dataframe(st.session_state.subscriptions)
    current_df = st.session_state.subscriptions
    is_demo_data = current_df.equals(pd.DataFrame(INITIAL_DATA, columns=BASE_COLUMNS))

    tab_overview, tab_subscriptions, tab_analytics, tab_ai = st.tabs(
        ["Overview", "Subscriptions", "Analytics", "AI Advisor"]
    )

    # ---- OVERVIEW TAB ----
    with tab_overview:
        if is_demo_data:
            st.info("These are example subscriptions to get you started. Edit, delete, or replace them in the Subscriptions tab.")

        metrics = calculate_metrics(current_df)
        kpi_savings = calculate_savings(current_df, 20)
        render_kpis(metrics, kpi_savings)

        st.markdown("<div style='height:0.9rem;'></div>", unsafe_allow_html=True)
        col_health, col_breakdown = st.columns([1, 2])
        with col_health:
            render_health_card(metrics)
        with col_breakdown:
            render_spending_breakdown(metrics)

        st.markdown("<div style='height:0.9rem;'></div>", unsafe_allow_html=True)
        overview_savings = render_savings_simulator(current_df)

    # ---- SUBSCRIPTIONS TAB ----
    with tab_subscriptions:
        render_input_form()
        st.markdown("<div style='height:0.9rem;'></div>", unsafe_allow_html=True)
        render_data_editor()

        st.markdown("<div style='height:0.9rem;'></div>", unsafe_allow_html=True)
        with st.expander("Import / Export Data", expanded=False):
            render_csv_tools(st.session_state.subscriptions)

        with st.expander("Data Controls", expanded=False):
            render_reset_controls()

    # Recompute after any edits made in the Subscriptions tab this run
    current_df = st.session_state.subscriptions
    metrics = calculate_metrics(current_df)

    # ---- ANALYTICS TAB ----
    with tab_analytics:
        render_charts(current_df, metrics)
        st.markdown("<div style='height:0.4rem;'></div>", unsafe_allow_html=True)
        render_analysis_detail(metrics)

    # ---- AI ADVISOR TAB ----
    with tab_ai:
        ai_savings = overview_savings if overview_savings else calculate_savings(current_df, 20)
        render_ai_analysis(current_df, metrics, ai_savings)

    render_footer()


if __name__ == "__main__":
    main()