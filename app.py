import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go

# ============================================================================
# CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Customer churn dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# STYLES
# ============================================================================

st.markdown(
    """
    <style>
    :root {
        color-scheme: dark;
    }
    html, body, [data-testid="stAppViewContainer"] {
        background: #0b1220 !important;
        color: #e2e8f0 !important;
    }
    #MainMenu, footer, header[data-testid="stHeader"], div[data-testid="stToolbar"] {
        visibility: hidden !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 1.5rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 1600px;
    }
    .css-18e3th9, .css-10trblm, .css-1avcm0n, .css-1d391kg, .css-1lcbmhc, .css-1v3fvcr, .css-1e5imcs {
        background-color: #0f172a !important;
        padding-top: 0rem !important;
    }
    .stTabs [role="tablist"] {
        background: rgba(15, 23, 42, 0.95);
        border-radius: 24px;
        padding: 4px;
        margin: 0 0 24px 0 !important;
        box-shadow: 0 18px 45px rgba(0, 0, 0, 0.35);
        backdrop-filter: blur(20px);
    }
    [role="tab"] {
        border-radius: 16px !important;
        padding: 0.9rem 1.25rem !important;
        margin: 0 0.2rem !important;
        color: #94a3b8 !important;
        background: transparent !important;
        border: 1px solid transparent !important;
        transition: all 0.2s ease;
    }
    [role="tab"][aria-selected="true"] {
        color: #e2e8f0 !important;
        background: rgba(255, 255, 255, 0.08) !important;
        border-color: rgba(255, 255, 255, 0.14) !important;
    }
    .stButton>button {
        background-color: #2563eb !important;
        color: white !important;
        border-radius: 0.75rem !important;
        border: none !important;
        padding: 0.75rem 1rem !important;
    }
    .stButton>button:hover {
        background-color: #1d4ed8 !important;
    }
    .stAlert {
        background-color: #111827 !important;
        color: #e2e8f0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================================
# LOAD MODEL AND DATA
# ============================================================================

@st.cache_resource
def load_model_and_columns():
    try:
        model = joblib.load("churn_model.pkl")
        columns = joblib.load("model_columns.pkl")
        return model, columns
    except FileNotFoundError:
        st.error("Model artifact missing. Add churn_model.pkl and model_columns.pkl to the app folder.")
        st.stop()

@st.cache_data
def load_sample_data():
    np.random.seed(42)
    n = 1000
    return pd.DataFrame({
        "Churn": np.random.choice([0, 1], n, p=[0.73, 0.27]),
        "Contract": np.random.choice(["Month-to-month", "One year", "Two year"], n),
        "PaymentMethod": np.random.choice(["Electronic check", "Mailed check", "Bank transfer", "Credit card"], n),
        "MonthlyCharges": np.random.uniform(20, 120, n),
        "tenure": np.random.randint(1, 73, n),
        "InternetService": np.random.choice(["Fiber optic", "DSL", "No"], n),
    })

model, model_columns = load_model_and_columns()
sample_df = load_sample_data()

# ============================================================================
# HELPERS
# ============================================================================

def risk_label(prob: float) -> tuple[str, str]:
    if prob >= 0.70:
        return "High", "#ef4444"
    if prob >= 0.40:
        return "Medium", "#f59e0b"
    return "Low", "#22c55e"


def build_feature_vector(payload: dict, columns: list[str]) -> pd.DataFrame:
    record = pd.DataFrame(np.zeros((1, len(columns))), columns=columns)
    for key, value in payload.items():
        if key in columns:
            record.at[0, key] = float(value)
    return record


def metrics_row():
    cols = st.columns(4, gap="large")
    metrics = [
        ("Accuracy", "78.04%"),
        ("Precision", "58%"),
        ("Recall", "61%"),
        ("F1 score", "60%"),
    ]
    for column, (label, value) in zip(cols, metrics):
        column.markdown(
            f"""
            <div class='kpi-card'>
                <div class='kpi-card-title'>{label}</div>
                <div class='kpi-card-value'>{value}</div>
                <div class='kpi-card-label'>High-confidence model performance presented clearly.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def style_plotly(fig):
    fig.update_layout(template="plotly_dark", paper_bgcolor="#0b1220", plot_bgcolor="#0b1220")
    return fig


def create_performance_comparison_chart():
    metrics = [
        {"metric": "Accuracy", "value": 78.04, "color": "#38bdf8"},
        {"metric": "Precision", "value": 58.00, "color": "#f59e0b"},
        {"metric": "Recall", "value": 61.00, "color": "#22c55e"},
        {"metric": "F1 Score", "value": 60.00, "color": "#a855f7"},
    ]
    df = pd.DataFrame(metrics)
    fig = px.bar(
        df,
        x="value",
        y="metric",
        orientation="h",
        text="value",
        color="metric",
        color_discrete_map={
            "Accuracy": "#38bdf8",
            "Precision": "#f59e0b",
            "Recall": "#22c55e",
            "F1 Score": "#a855f7",
        },
        title="Model performance comparison",
        labels={"value": "Score (%)", "metric": "Metric"},
    )
    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        hovertemplate="%{y}: %{x:.1f}%<extra></extra>",
        marker_line_color="#111827",
        marker_line_width=1.5,
    )
    fig.update_layout(
        yaxis=dict(autorange="reversed", showgrid=False, tickfont=dict(color="#cbd5e1", size=13)),
        xaxis=dict(range=[0, 100], showgrid=True, gridcolor="rgba(148, 163, 184, 0.12)", tickvals=[0, 20, 40, 60, 80, 100], tickfont=dict(color="#94a3b8")),
        plot_bgcolor="#0b1220",
        paper_bgcolor="#0b1220",
        margin=dict(t=50, b=30, l=90, r=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
        hoverlabel=dict(bgcolor="#111827", font_color="#ffffff"),
    )
    return fig


# Top navigation tabs will be rendered in the main layout.

def render_home():
    st.markdown("# Customer Churn Dashboard")
    st.markdown("#### Minimal retention analytics for telecom users.")
    st.markdown("---")
    metrics_row()

    performance_fig = create_performance_comparison_chart()
    style_plotly(performance_fig)
    st.plotly_chart(performance_fig, width='stretch')

    st.markdown("---")
    c1, c2, c3 = st.columns(3, gap="large")
    c1.markdown(
        """
        <div class='kpi-card'>
            <div class='kpi-card-title'>Customer sample</div>
            <div class='kpi-card-value'>1000</div>
            <div class='kpi-card-label'>Dataset segment for current analytics.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c2.markdown(
        """
        <div class='kpi-card'>
            <div class='kpi-card-title'>Churn rate</div>
            <div class='kpi-card-value'>27%</div>
            <div class='kpi-card-label'>Current retention performance.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c3.markdown(
        """
        <div class='kpi-card'>
            <div class='kpi-card-title'>Deployment status</div>
            <div class='kpi-card-value'>Streamlit Cloud</div>
            <div class='kpi-card-label'>Production-ready deployment target.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_prediction():
    st.markdown("# Customer Prediction")
    st.markdown("#### Enter customer details to score churn risk.")
    st.markdown("---")

    with st.expander("Customer details", expanded=True):
        left, right = st.columns(2)
        with left:
            gender = st.selectbox("Gender", ["Male", "Female"])
            senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"])
            partner = st.selectbox("Partner", ["Yes", "No"])
            dependents = st.selectbox("Dependents", ["Yes", "No"])
            phone_service = st.selectbox("Phone Service", ["Yes", "No"])
            multiple_lines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
            internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        with right:
            online_security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
            online_backup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
            device_protection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
            tech_support = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
            streaming_tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
            streaming_movies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])

    with st.expander("Billing & contract", expanded=True):
        b1, b2, b3 = st.columns(3)
        with b1:
            contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
            paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
            payment_method = st.selectbox(
                "Payment Method",
                ["Electronic check", "Mailed check", "Bank transfer", "Credit card"],
            )
        with b2:
            tenure = st.slider("Tenure (months)", min_value=0, max_value=72, value=12)
            monthly_charges = st.number_input("Monthly Charges", value=72.0, min_value=0.0, step=0.5, format="%.2f")
        with b3:
            total_charges = st.number_input("Total Charges", value=720.0, min_value=0.0, step=1.0, format="%.2f")
            st.caption("Prediction uses the saved model's numeric inputs.")

    st.markdown("---")
    if st.button("Predict churn", type="primary", use_container_width=True):
        payload = {
            "tenure": tenure,
            "MonthlyCharges": monthly_charges,
            "TotalCharges": total_charges,
        }
        features = build_feature_vector(payload, model_columns)

        try:
            prediction = int(model.predict(features)[0])
            probability = float(model.predict_proba(features)[0][1])
            status, color = risk_label(probability)
            label = "Churn" if prediction == 1 else "No Churn"

            st.markdown("---")
            col1, col2, col3 = st.columns([2, 1, 1])
            col1.metric("Outcome", label)
            col2.metric("Probability", f"{probability:.1%}")
            col3.metric("Risk level", status)

            gauge = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=probability * 100,
                    number={"suffix": "%"},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "bar": {"color": color},
                        "steps": [
                            {"range": [0, 40], "color": "#16a34a"},
                            {"range": [40, 70], "color": "#f59e0b"},
                            {"range": [70, 100], "color": "#ef4444"},
                        ],
                    },
                )
            )
            style_plotly(gauge).update_layout(height=360, margin={"t": 10, "b": 10, "l": 10, "r": 10})
            st.plotly_chart(gauge, width='stretch')

            st.markdown("### Recommendation")
            if prediction == 1:
                st.markdown(
                    """
                    - Initiate retention outreach immediately
                    - Offer a contract incentive or discount
                    - Review service satisfaction and billing
                    """
                )
            else:
                st.markdown(
                    """
                    - Maintain engagement with loyalty messaging
                    - Promote value add-ons
                    - Monitor satisfaction proactively
                    """
                )

        except Exception as error:
            st.error(f"Prediction failed: {error}")


def render_dashboard():
    st.markdown("# Analytics Dashboard")
    st.markdown("#### Interactive churn insights and feature impact.")
    st.markdown("---")
    metrics_row()
    st.markdown("---")

    left, right = st.columns(2)
    with left:
        churn_data = sample_df['Churn'].value_counts().rename({0: 'Retained', 1: 'Churned'})
        pie = px.pie(
            names=churn_data.index,
            values=churn_data.values,
            title='Churn distribution',
            color=churn_data.index,
            color_discrete_map={'Retained': '#22c55e', 'Churned': '#ef4444'},
        )
        style_plotly(pie)
        st.plotly_chart(pie, width='stretch')
    with right:
        contract_churn = pd.crosstab(sample_df['Contract'], sample_df['Churn'])
        bar = px.bar(
            contract_churn,
            barmode='group',
            title='Contract vs churn',
            labels={'value': 'Customers', 'Contract': 'Contract'},
        )
        style_plotly(bar)
        st.plotly_chart(bar, width='stretch')

    bottom_left, bottom_right = st.columns(2)
    with bottom_left:
        payment_churn = pd.crosstab(sample_df['PaymentMethod'], sample_df['Churn'])
        bar = px.bar(
            payment_churn,
            barmode='group',
            title='Payment method vs churn',
            labels={'value': 'Customers', 'PaymentMethod': 'Payment Method'},
        )
        style_plotly(bar)
        st.plotly_chart(bar, width='stretch')
    with bottom_right:
        hist = px.histogram(
            sample_df,
            x='MonthlyCharges',
            color='Churn',
            barmode='overlay',
            title='Monthly charges distribution',
            color_discrete_map={0: '#22c55e', 1: '#ef4444'},
        )
        style_plotly(hist)
        st.plotly_chart(hist, width='stretch')

    st.markdown("---")
    importance = pd.DataFrame({
        'feature': model_columns,
        'importance': model.feature_importances_.tolist(),
    }).sort_values('importance', ascending=True)
    fig = px.bar(
        importance,
        x='importance',
        y='feature',
        orientation='h',
        title='Feature importance',
        color='importance',
        color_continuous_scale='viridis',
    )
    style_plotly(fig).update_layout(margin={'t': 30, 'b': 20}, showlegend=False)
    st.plotly_chart(fig, width='stretch')


def render_insights():
    st.markdown("# Business Insights")
    st.markdown("#### Focused retention recommendations.")
    st.markdown("---")
    st.write("**Top churn drivers**")
    st.write("- Tenure: the shortest-tenure customers are the most likely to churn")
    st.write("- MonthlyCharges: higher monthly spend is associated with churn risk")
    st.write("- TotalCharges: long-term customers need value reinforcement")
    st.markdown("---")
    st.write("**Key insights**")
    st.write("- Month-to-month contracts show the highest churn pressure")
    st.write("- Electronic check payment increases churn likelihood")
    st.write("- Bundles and support services help stabilize retention")
    st.markdown("---")
    st.write("**Recommendations**")
    st.write("- Incentivize longer contract commitments")
    st.write("- Promote automatic payment enrollment")
    st.write("- Offer targeted retention incentives for high spend customers")


def render_about():
    st.markdown("# About Project")
    st.markdown("#### Production-ready churn forecasting using saved ML artifacts.")
    st.markdown("---")
    st.write("- Dataset: telecom churn sample")
    st.write("- Model: Random Forest classifier")
    st.write("- Training: SMOTE to balance churn cases")
    st.write("- Deployment: Streamlit Cloud compatible")

# ============================================================================
# MAIN
# ============================================================================

tabs = st.tabs(["🏠 Home", "🔮 Prediction", "📈 Analytics", "💡 Insights", "ℹ️ About"])
with tabs[0]:
    render_home()
with tabs[1]:
    render_prediction()
with tabs[2]:
    render_dashboard()
with tabs[3]:
    render_insights()
with tabs[4]:
    render_about()
