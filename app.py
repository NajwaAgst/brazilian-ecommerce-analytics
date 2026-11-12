
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# 2. CUSTOM CSS
# =====================================================

st.markdown("""
<style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    [data-testid="stSidebar"] {
        background-color: #142536;
    }

    [data-testid="stSidebar"] * {
        color: #F4F7FA;
    }

    .dashboard-subtitle {
        color: #718096;
        font-size: 14px;
        margin-top: -12px;
        margin-bottom: 25px;
    }

    div[data-testid="stMetric"] {
        background-color: #F5F8FC;
        border: 1px solid #E5EAF0;
        padding: 16px;
        border-radius: 12px;
    }

    div[data-testid="stMetricLabel"] {
        color: #64748B;
        font-size: 13px;
    }

    div[data-testid="stMetricValue"] {
        color: #172B4D;
        font-size: 25px;
        font-weight: 700;
    }

    .section-caption {
        color: #718096;
        font-size: 13px;
        margin-top: -10px;
    }

    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. LOAD DATA
# =====================================================

DATA_DIR = Path(__file__).parent / "dashboard_data"


@st.cache_data
def load_data():

    monthly_sales = pd.read_csv(
        DATA_DIR / "monthly_sales.csv"
    )

    rfm = pd.read_csv(
        DATA_DIR / "rfm_data.csv"
    )

    delivery = pd.read_csv(
        DATA_DIR / "delivery_data.csv"
    )

    # Convert date column
    monthly_sales["order_month"] = pd.to_datetime(
        monthly_sales["order_month"],
        errors="coerce"
    )

    # Convert numeric columns
    for col in ["total_orders", "total_revenue", "AOV"]:
        monthly_sales[col] = pd.to_numeric(
            monthly_sales[col],
            errors="coerce"
        )

    for col in ["Recency", "Frequency", "Monetary"]:
        rfm[col] = pd.to_numeric(
            rfm[col],
            errors="coerce"
        )

    for col in ["delivery_duration", "delivery_delay"]:
        delivery[col] = pd.to_numeric(
            delivery[col],
            errors="coerce"
        )

    return monthly_sales, rfm, delivery


try:
    monthly_sales, rfm, delivery = load_data()

except Exception as error:
    st.error(
        "Dataset gagal dibaca. Pastikan ketiga file CSV "
        "tersedia di dalam folder dashboard_data."
    )
    st.exception(error)
    st.stop()


# =====================================================
# 4. DATA VALIDATION
# =====================================================

required_columns = {
    "monthly_sales": [
        "order_month",
        "total_orders",
        "total_revenue",
        "AOV"
    ],
    "rfm": [
        "Recency",
        "Frequency",
        "Monetary"
    ],
    "delivery": [
        "delivery_duration",
        "delivery_delay"
    ]
}

datasets = {
    "monthly_sales": monthly_sales,
    "rfm": rfm,
    "delivery": delivery
}

for dataset_name, columns in required_columns.items():

    missing = [
        col for col in columns
        if col not in datasets[dataset_name].columns
    ]

    if missing:
        st.error(
            f"Kolom {missing} tidak ditemukan pada "
            f"dataset {dataset_name}."
        )
        st.stop()


# =====================================================
# 5. PREPARE DELIVERY STATUS
# =====================================================

# Use existing status column if available.
# Otherwise, derive it from delivery_delay.

if "delivery_status" in delivery.columns:

    delivery["status_clean"] = (
        delivery["delivery_status"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    delivery["status_clean"] = delivery[
        "status_clean"
    ].replace({
        "on time": "On Time",
        "ontime": "On Time",
        "late": "Late"
    })

elif "status" in delivery.columns:

    delivery["status_clean"] = (
        delivery["status"]
        .astype(str)
        .str.strip()
        .str.lower()
        .replace({
            "on time": "On Time",
            "ontime": "On Time",
            "late": "Late"
        })
    )

else:

    delivery["status_clean"] = pd.NA

    valid_delay = delivery["delivery_delay"].notna()

    delivery.loc[
        valid_delay & (delivery["delivery_delay"] <= 0),
        "status_clean"
    ] = "On Time"

    delivery.loc[
        valid_delay & (delivery["delivery_delay"] > 0),
        "status_clean"
    ] = "Late"


# Normalize status labels
delivery["status_clean"] = (
    delivery["status_clean"]
    .astype("string")
    .str.strip()
    .str.lower()
    .map({
        "on time": "On Time",
        "ontime": "On Time",
        "late": "Late"
    })
)


# =====================================================
# 6. CALCULATE KPI
# =====================================================

total_orders = monthly_sales["total_orders"].sum()

total_revenue = monthly_sales["total_revenue"].sum()

aov = (
    total_revenue / total_orders
    if total_orders > 0 else 0
)

total_deliveries = delivery["status_clean"].isin(
    ["On Time", "Late"]
).sum()

on_time_deliveries = (
    delivery["status_clean"] == "On Time"
).sum()

late_deliveries = (
    delivery["status_clean"] == "Late"
).sum()

on_time_rate = (
    on_time_deliveries / total_deliveries * 100
    if total_deliveries > 0 else 0
)

late_rate = (
    late_deliveries / total_deliveries * 100
    if total_deliveries > 0 else 0
)


# =====================================================
# 7. SIDEBAR NAVIGATION
# =====================================================

with st.sidebar:

    st.markdown("# 📊 E-Commerce")
    st.markdown("### Analytics Dashboard")

    st.markdown("---")

    page = st.radio(
        "NAVIGATION",
        [
            "Overview",
            "Customer Analysis",
            "Delivery Analysis"
        ]
    )

    st.markdown("---")

    st.caption("DATASET INFORMATION")
    st.caption("Brazilian E-Commerce Public Dataset")
    st.caption("Source: Olist")
    st.caption("Period: Jan 2017 – Aug 2018")


# =====================================================
# 8. OVERVIEW PAGE
# =====================================================

if page == "Overview":

    st.title("Business Overview")

    st.markdown(
        '<p class="dashboard-subtitle">'
        'A summary of sales performance and business operations '
        'from January 2017 to August 2018.'
        '</p>',
        unsafe_allow_html=True
    )

    # KPI cards
    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "Total Orders",
        f"{total_orders:,.0f}"
    )

    k2.metric(
        "Total Revenue",
        f"R$ {total_revenue:,.2f}"
    )

    k3.metric(
        "Average Order Value",
        f"R$ {aov:,.2f}"
    )

    k4.metric(
        "On-Time Delivery",
        f"{on_time_rate:.2f}%"
    )

    st.markdown("### Sales Performance")

    # Sales charts side by side
    chart1, chart2 = st.columns(2)

    with chart1:

        fig_orders = px.line(
            monthly_sales,
            x="order_month",
            y="total_orders",
            markers=True,
            title="Monthly Order Trend",
            labels={
                "order_month": "Month",
                "total_orders": "Total Orders"
            }
        )

        fig_orders.update_traces(
            line=dict(color="#16A6A0", width=3),
            marker=dict(size=7)
        )

        fig_orders.update_layout(
            height=330,
            margin=dict(l=10, r=10, t=50, b=10),
            hovermode="x unified"
        )

        st.plotly_chart(
            fig_orders,
            use_container_width=True
        )

    with chart2:

        fig_revenue = px.line(
            monthly_sales,
            x="order_month",
            y="total_revenue",
            markers=True,
            title="Monthly Revenue Trend",
            labels={
                "order_month": "Month",
                "total_revenue": "Revenue (R$)"
            }
        )

        fig_revenue.update_traces(
            line=dict(color="#6478D3", width=3),
            marker=dict(size=7)
        )

        fig_revenue.update_layout(
            height=330,
            margin=dict(l=10, r=10, t=50, b=10),
            hovermode="x unified"
        )

        st.plotly_chart(
            fig_revenue,
            use_container_width=True
        )

    # Additional charts
    chart3, chart4 = st.columns(2)

    with chart3:

        fig_aov = px.bar(
            monthly_sales,
            x="order_month",
            y="AOV",
            title="Monthly Average Order Value",
            labels={
                "order_month": "Month",
                "AOV": "AOV (R$)"
            }
        )

        fig_aov.update_traces(
            marker_color="#E5A84B"
        )

        fig_aov.update_layout(
            height=330,
            margin=dict(l=10, r=10, t=50, b=10)
        )

        st.plotly_chart(
            fig_aov,
            use_container_width=True
        )

    with chart4:

        status_data = pd.DataFrame({
            "Delivery Status": ["On Time", "Late"],
            "Total": [
                on_time_deliveries,
                late_deliveries
            ]
        })

        fig_status = px.pie(
            status_data,
            names="Delivery Status",
            values="Total",
            hole=0.55,
            title="Delivery Status Overview",
            color="Delivery Status",
            color_discrete_map={
                "On Time": "#16A6A0",
                "Late": "#E5A84B"
            }
        )

        fig_status.update_layout(
            height=330,
            margin=dict(l=10, r=10, t=50, b=10)
        )

        st.plotly_chart(
            fig_status,
            use_container_width=True
        )

    with st.expander("View Monthly Sales Data"):

        st.dataframe(
            monthly_sales,
            use_container_width=True
        )


# =====================================================
# 9. CUSTOMER ANALYSIS PAGE
# =====================================================

elif page == "Customer Analysis":

    st.title("Customer Behavior Analysis")

    st.markdown(
        '<p class="dashboard-subtitle">'
        'Customer characteristics based on Recency, '
        'Frequency, and Monetary (RFM).'
        '</p>',
        unsafe_allow_html=True
    )

    # Customer KPI
    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Customers",
        f"{len(rfm):,}"
    )

    c2.metric(
        "Average Frequency",
        f"{rfm['Frequency'].mean():.2f}"
    )

    c3.metric(
        "Average Monetary",
        f"R$ {rfm['Monetary'].mean():,.2f}"
    )

    st.markdown("### RFM Distribution")

    # Recency and Frequency
    chart1, chart2 = st.columns(2)

    with chart1:

        fig_recency = px.histogram(
            rfm,
            x="Recency",
            nbins=35,
            title="Recency Distribution",
            labels={
                "Recency": "Recency (Days)"
            },
            color_discrete_sequence=["#16A6A0"]
        )

        fig_recency.update_layout(
            height=350,
            margin=dict(l=10, r=10, t=50, b=10)
        )

        st.plotly_chart(
            fig_recency,
            use_container_width=True
        )

    with chart2:

        frequency_data = (
            rfm["Frequency"]
            .value_counts()
            .sort_index()
            .reset_index()
        )

        frequency_data.columns = [
            "Frequency",
            "Customers"
        ]

        fig_frequency = px.bar(
            frequency_data,
            x="Frequency",
            y="Customers",
            title="Purchase Frequency Distribution",
            labels={
                "Frequency": "Number of Purchases",
                "Customers": "Number of Customers"
            },
            color_discrete_sequence=["#6478D3"]
        )

        fig_frequency.update_layout(
            height=350,
            margin=dict(l=10, r=10, t=50, b=10)
        )

        st.plotly_chart(
            fig_frequency,
            use_container_width=True
        )

    # Monetary chart
    st.markdown("### Customer Spending")

    fig_monetary = px.histogram(
        rfm,
        x="Monetary",
        nbins=40,
        log_x=True,
        title="Monetary Distribution",
        labels={
            "Monetary": "Monetary Value (R$)"
        },
        color_discrete_sequence=["#E5A84B"]
    )

    fig_monetary.update_layout(
        height=350,
        margin=dict(l=10, r=10, t=50, b=10)
    )

    st.plotly_chart(
        fig_monetary,
        use_container_width=True
    )

    # RFM summary
    st.markdown("### RFM Statistical Summary")

    rfm_summary = rfm[
        ["Recency", "Frequency", "Monetary"]
    ].describe().round(2)

    st.dataframe(
        rfm_summary,
        use_container_width=True
    )

    with st.expander("View Customer RFM Data"):

        st.dataframe(
            rfm,
            use_container_width=True
        )


# =====================================================
# 10. DELIVERY ANALYSIS PAGE
# =====================================================

elif page == "Delivery Analysis":

    st.title("Delivery Performance Analysis")

    st.markdown(
        '<p class="dashboard-subtitle">'
        'An evaluation of delivery punctuality, '
        'delivery duration, and delivery delays.'
        '</p>',
        unsafe_allow_html=True
    )

    # Delivery KPI
    d1, d2, d3, d4 = st.columns(4)

    d1.metric(
        "Total Deliveries",
        f"{total_deliveries:,}"
    )

    d2.metric(
        "On-Time Deliveries",
        f"{on_time_deliveries:,}"
    )

    d3.metric(
        "Late Deliveries",
        f"{late_deliveries:,}"
    )

    d4.metric(
        "Late Delivery Rate",
        f"{late_rate:.2f}%"
    )

    st.markdown("### Delivery Status")

    # Status and duration
    chart1, chart2 = st.columns(2)

    with chart1:

        status_data = pd.DataFrame({
            "Delivery Status": ["On Time", "Late"],
            "Total": [
                on_time_deliveries,
                late_deliveries
            ]
        })

        fig_status = px.bar(
            status_data,
            x="Delivery Status",
            y="Total",
            title="On-Time vs Late Deliveries",
            color="Delivery Status",
            color_discrete_map={
                "On Time": "#16A6A0",
                "Late": "#E5A84B"
            },
            text="Total"
        )

        fig_status.update_layout(
            height=350,
            showlegend=False,
            margin=dict(l=10, r=10, t=50, b=10)
        )

        st.plotly_chart(
            fig_status,
            use_container_width=True
        )

    with chart2:

        fig_duration = px.histogram(
            delivery,
            x="delivery_duration",
            nbins=40,
            title="Delivery Duration Distribution",
            labels={
                "delivery_duration": "Delivery Duration (Days)"
            },
            color_discrete_sequence=["#6478D3"]
        )

        fig_duration.update_layout(
            height=350,
            margin=dict(l=10, r=10, t=50, b=10)
        )

        st.plotly_chart(
            fig_duration,
            use_container_width=True
        )

    # Delivery delay
    st.markdown("### Delivery Delay Analysis")

    fig_delay = px.histogram(
        delivery,
        x="delivery_delay",
        nbins=45,
        title="Delivery Delay Distribution",
        labels={
            "delivery_delay": "Difference from Estimated Date (Days)"
        },
        color_discrete_sequence=["#E5A84B"]
    )

    fig_delay.add_vline(
        x=0,
        line_dash="dash",
        line_color="red",
        annotation_text="Estimated Delivery Date"
    )

    fig_delay.update_layout(
        height=350,
        margin=dict(l=10, r=10, t=50, b=10)
    )

    st.plotly_chart(
        fig_delay,
        use_container_width=True
    )

    # Delivery statistics
    st.markdown("### Delivery Statistics")

    delivery_stats = delivery[
        ["delivery_duration", "delivery_delay"]
    ].describe().round(2)

    st.dataframe(
        delivery_stats,
        use_container_width=True
    )

    with st.expander("View Delivery Data"):

        st.dataframe(
            delivery,
            use_container_width=True
        )


# =====================================================
# 11. FOOTER
# =====================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#718096; font-size:12px;">
        E-Commerce Analytics Dashboard |
        Brazilian E-Commerce Public Dataset by Olist<br>
        Analysis Period: January 2017 – August 2018
    </div>
    """,
    unsafe_allow_html=True
)
