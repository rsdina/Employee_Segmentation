from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "results" / "employee_segmentation_results.csv"
RECOMMENDATIONS_PATH = ROOT / "results" / "hr_recommendations.csv"

COLORS = {
    "background": "#102E3A",
    "panel": "#173E49",
    "panel_alt": "#204C56",
    "text": "#F3F7F8",
    "muted": "#A9C6CA",
    "cyan": "#18C7C9",
    "coral": "#F5795B",
    "magenta": "#B72D8C",
    "gold": "#F4C95D",
    "mint": "#6CD7B5",
}
SEGMENT_COLORS = {
    "Emerging Talent": COLORS["cyan"],
    "Needs Improvement": COLORS["coral"],
    "Stable Employees": COLORS["magenta"],
}

st.set_page_config(
    page_title="HR Analytics | Workforce Intelligence",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH)
    recommendations = pd.read_csv(RECOMMENDATIONS_PATH)
    return data, recommendations


def format_currency(value):
    return f"${value:,.0f}"


def format_percent(value):
    return f"{value:.1%}"


def style_plot(fig, height=300):
    fig.update_layout(
        height=height,
        margin={"l": 10, "r": 10, "t": 42, "b": 10},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Aptos, Segoe UI, sans-serif", "color": COLORS["text"]},
        title={"font": {"size": 14, "color": COLORS["text"]}},
        legend={"font": {"color": COLORS["muted"]}},
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor="#35616A", tickfont={"color": COLORS["muted"]})
    fig.update_yaxes(showgrid=True, gridcolor="#28535C", zeroline=False, tickfont={"color": COLORS["muted"]})
    return fig


def card(label, value, accent):
    st.markdown(
        f"""
        <div class="metric-card" style="border-top-color:{accent}">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    :root { --bg: #102E3A; --panel: #173E49; --text: #F3F7F8; --muted: #A9C6CA; --cyan: #18C7C9; }
    .stApp { background: var(--bg); color: var(--text); }
    .block-container { padding: 1.35rem 2.3rem 2rem; max-width: 1500px; }
    [data-testid="stSidebar"] { background: #0B2731; border-right: 1px solid #28535C; }
    [data-testid="stSidebar"] > div:first-child { padding: 1.4rem 1rem; }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; letter-spacing: 0; }
    p, div, label, span { font-family: 'DM Sans', sans-serif; letter-spacing: 0; }
    .brand { padding: .5rem .3rem 1.7rem; border-bottom: 1px solid #28535C; margin-bottom: 1.5rem; }
    .brand-title { color: var(--text); font: 700 1.25rem 'Space Grotesk'; letter-spacing: .08em; }
    .brand-subtitle { color: var(--cyan); font-size: .65rem; letter-spacing: .18em; margin-top: .25rem; }
    .metric-card { background: var(--panel); border: 1px solid #2B5962; border-top: 3px solid; border-radius: 7px; padding: 1rem 1.1rem .85rem; min-height: 92px; }
    .metric-label { color: var(--muted); font-size: .72rem; text-transform: uppercase; letter-spacing: .09em; }
    .metric-value { color: var(--text); font: 700 1.75rem 'Space Grotesk'; margin-top: .45rem; }
    .section-title { color: var(--text); font: 600 1rem 'Space Grotesk'; margin: 1.1rem 0 .4rem; }
    .section-caption { color: var(--muted); font-size: .78rem; margin-bottom: .6rem; }
    .insight { background: linear-gradient(135deg, #1B4652, #26394C); border: 1px solid #3B6670; border-left: 3px solid #F5795B; border-radius: 7px; padding: 1rem 1.1rem; min-height: 170px; }
    .insight-kicker { color: #F5795B; font-size: .7rem; font-weight: 700; letter-spacing: .11em; text-transform: uppercase; }
    .insight-title { color: var(--text); font: 600 1.1rem 'Space Grotesk'; margin: .35rem 0 .5rem; }
    .insight-copy { color: var(--muted); font-size: .82rem; line-height: 1.45; }
    .footer-note { color: #71949A; font-size: .72rem; margin-top: 1.5rem; }
    div[data-testid="stMetric"] { background: var(--panel); border: 1px solid #2B5962; border-radius: 7px; padding: .6rem .8rem; }
    div[data-testid="stMetricLabel"] { color: var(--muted); }
    div[data-testid="stMetricValue"] { color: var(--text); }
    .stSelectbox label, .stMultiSelect label, .stSlider label { color: var(--muted) !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

try:
    df, recommendations = load_data()
except FileNotFoundError as error:
    st.error(f"Dashboard data is missing: {error.filename}")
    st.stop()

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-title">HR ANALYTICS</div>
            <div class="brand-subtitle">WORKFORCE INTELLIGENCE</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("### Dashboard")
    page = st.radio("Navigate", ["Overview", "Segment Profile", "Employee Detail"], label_visibility="collapsed")
    st.markdown("### Filters")
    departments = st.multiselect("Department", sorted(df["Department"].dropna().unique()), default=[])
    segments = st.multiselect("Segment", sorted(df["Segment"].dropna().unique()), default=[])
    min_age, max_age = int(df["Age"].min()), int(df["Age"].max())
    age_range = st.slider("Age range", min_age, max_age, (min_age, max_age))
    show_attrition_only = st.toggle("Attrition cases only", value=False)
    if st.button("Reset filters", use_container_width=True):
        st.rerun()
    st.markdown("<div class='footer-note'>Source: employee_segmentation_results.csv<br>Analysis snapshot: 14,999 employees</div>", unsafe_allow_html=True)

filtered = df.copy()
if departments:
    filtered = filtered[filtered["Department"].isin(departments)]
if segments:
    filtered = filtered[filtered["Segment"].isin(segments)]
filtered = filtered[filtered["Age"].between(age_range[0], age_range[1])]
if show_attrition_only:
    filtered = filtered[filtered["Attrition"] == 1]

if filtered.empty:
    st.warning("No employees match the selected filters. Reset the filters to restore the dashboard.")
    st.stop()

employee_count = filtered["EmpId"].nunique()
attrition_rate = filtered["Attrition"].mean()
average_salary = filtered["Annual_Salary"].mean()
average_satisfaction = filtered["Employee_Satisfaction"].mean()

st.markdown(
    "<div style='color:#18C7C9;font-size:.7rem;font-weight:700;letter-spacing:.16em;text-transform:uppercase'>Executive view / workforce pulse</div>",
    unsafe_allow_html=True,
)
st.title("Employee Segmentation Overview")
st.markdown("<div class='section-caption'>A focused view of workforce composition, retention pressure, and the actions most likely to improve employee outcomes.</div>", unsafe_allow_html=True)

if page == "Overview":
    metric_columns = st.columns(4, gap="medium")
    with metric_columns[0]:
        card("Employees in view", f"{employee_count:,}", COLORS["cyan"])
    with metric_columns[1]:
        card("Attrition rate", format_percent(attrition_rate), COLORS["coral"])
    with metric_columns[2]:
        card("Average salary", format_currency(average_salary), COLORS["gold"])
    with metric_columns[3]:
        card("Average satisfaction", f"{average_satisfaction:.2f} / 10", COLORS["magenta"])

    left, middle, right = st.columns([1.1, 1.25, .95], gap="medium")
    with left:
        st.markdown("<div class='section-title'>Segment distribution</div>", unsafe_allow_html=True)
        segment_counts = filtered.groupby("Segment", as_index=False).agg(Employees=("EmpId", "nunique"))
        segment_counts["Color"] = segment_counts["Segment"].map(SEGMENT_COLORS)
        fig = px.pie(segment_counts, names="Segment", values="Employees", hole=.65, color="Segment", color_discrete_map=SEGMENT_COLORS)
        fig.update_traces(textposition="outside", textinfo="percent", marker={"line": {"color": COLORS["background"], "width": 2}})
        st.plotly_chart(style_plot(fig, 295), use_container_width=True, config={"displayModeBar": False})
    with middle:
        st.markdown("<div class='section-title'>Attrition risk by segment</div>", unsafe_allow_html=True)
        risk = filtered.groupby("Segment", as_index=False).agg(Attrition=("Attrition", "mean"), Employees=("EmpId", "nunique"))
        risk = risk.sort_values("Attrition")
        fig = px.bar(risk, x="Attrition", y="Segment", orientation="h", text="Attrition", color="Segment", color_discrete_map=SEGMENT_COLORS)
        fig.update_traces(texttemplate="%{text:.0%}", textposition="outside")
        fig.update_xaxes(tickformat=".0%", range=[0, max(.5, risk["Attrition"].max() * 1.2)])
        fig.update_layout(showlegend=False)
        st.plotly_chart(style_plot(fig, 295), use_container_width=True, config={"displayModeBar": False})
    with right:
        priority = filtered.groupby("Segment").agg(Attrition=("Attrition", "mean"), Overtime=("Overtime_Hours", "mean"), Satisfaction=("Employee_Satisfaction", "mean")).sort_values("Attrition", ascending=False).reset_index().iloc[0]
        segment_recommendation = recommendations[recommendations["Segment"] == priority["Segment"]]
        recommendation = segment_recommendation.iloc[0] if not segment_recommendation.empty else None
        issue = recommendation["Key_Issues"] if recommendation is not None else "Monitor workforce indicators"
        actions = recommendation["Recommended_Actions"] if recommendation is not None else "Review the selected segment profile"
        st.markdown(
            f"<div class='insight'><div class='insight-kicker'>Priority signal</div><div class='insight-title'>{priority['Segment']}</div><div class='insight-copy'><b>{priority['Attrition']:.0%}</b> attrition &nbsp;|&nbsp; <b>{priority['Overtime']:.1f}</b> overtime hours<br><br>{issue}.<br><br>{actions}.</div></div>",
            unsafe_allow_html=True,
        )

    lower_left, lower_right = st.columns([1.25, 1], gap="medium")
    with lower_left:
        st.markdown("<div class='section-title'>Department workforce</div>", unsafe_allow_html=True)
        department_counts = filtered.groupby("Department", as_index=False).agg(Employees=("EmpId", "nunique"), Attrition=("Attrition", "mean"))
        department_counts = department_counts.sort_values("Employees")
        fig = px.bar(department_counts, x="Employees", y="Department", orientation="h", color="Attrition", color_continuous_scale=[COLORS["mint"], COLORS["gold"], COLORS["coral"]])
        fig.update_coloraxes(colorbar_tickformat=".0%", colorbar_title="Attrition")
        st.plotly_chart(style_plot(fig, 350), use_container_width=True, config={"displayModeBar": False})
    with lower_right:
        st.markdown("<div class='section-title'>Workload and performance</div>", unsafe_allow_html=True)
        fig = px.scatter(filtered.sample(min(len(filtered), 3000), random_state=42), x="Overtime_Hours", y="Performance_Rating", size="Employee_Satisfaction", color="Segment", color_discrete_map=SEGMENT_COLORS, hover_data=["Department", "Annual_Salary", "Attrition"], opacity=.7)
        fig.update_layout(showlegend=True, legend_title_text="")
        st.plotly_chart(style_plot(fig, 350), use_container_width=True, config={"displayModeBar": False})

elif page == "Segment Profile":
    st.markdown("<div class='section-title'>Segment comparison</div>", unsafe_allow_html=True)
    profile = filtered.groupby("Segment", as_index=False).agg(
        Employees=("EmpId", "nunique"),
        Attrition=("Attrition", "mean"),
        Salary=("Annual_Salary", "mean"),
        Satisfaction=("Employee_Satisfaction", "mean"),
        Performance=("Performance_Rating", "mean"),
        Overtime=("Overtime_Hours", "mean"),
        Tenure=("Company_Tenure", "mean"),
    )
    st.dataframe(profile.style.format({"Attrition": "{:.1%}", "Salary": "${:,.0f}", "Satisfaction": "{:.2f}", "Performance": "{:.2f}", "Overtime": "{:.1f}", "Tenure": "{:.1f}"}), use_container_width=True, hide_index=True)
    chart_left, chart_right = st.columns(2, gap="medium")
    with chart_left:
        fig = px.bar(profile.sort_values("Salary"), x="Salary", y="Segment", orientation="h", color="Segment", color_discrete_map=SEGMENT_COLORS, title="Average salary")
        st.plotly_chart(style_plot(fig, 350), use_container_width=True, config={"displayModeBar": False})
    with chart_right:
        fig = px.bar(profile.sort_values("Performance"), x="Performance", y="Segment", orientation="h", color="Segment", color_discrete_map=SEGMENT_COLORS, title="Average performance")
        fig.update_xaxes(range=[0, 10])
        st.plotly_chart(style_plot(fig, 350), use_container_width=True, config={"displayModeBar": False})

else:
    st.markdown("<div class='section-title'>Employee detail</div>", unsafe_allow_html=True)
    search = st.text_input("Search employee ID or department", placeholder="Example: 780152 or Sales")
    detail = filtered.copy()
    if search:
        search_text = search.lower()
        detail = detail[detail["EmpId"].astype(str).str.lower().str.contains(search_text) | detail["Department"].str.lower().str.contains(search_text)]
    display_columns = ["EmpId", "Department", "Segment", "Annual_Salary", "Performance_Rating", "Employee_Satisfaction", "Overtime_Hours", "Absenteeism_Days", "Attrition"]
    st.dataframe(detail[display_columns].rename(columns={"EmpId": "Employee ID", "Annual_Salary": "Annual salary", "Performance_Rating": "Performance", "Employee_Satisfaction": "Satisfaction", "Overtime_Hours": "Overtime hours", "Absenteeism_Days": "Absenteeism days"}), use_container_width=True, hide_index=True, height=520)

st.markdown("<div class='footer-note'>HR Analytics | Employee segmentation model snapshot | Use employee-level views only with appropriate access controls.</div>", unsafe_allow_html=True)
