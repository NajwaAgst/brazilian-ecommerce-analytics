
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Olist Analytics Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# 2. CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.stApp {
    background-color: #F5F7FB;
    color: #17243A;
}

.stApp p,
.stApp label,
.stApp li {
    color: #263449;
}

h1, h2, h3, h4, h5, h6 {
    color: #17243A !important;
    font-weight: 700 !important;
}

[data-testid="stSidebar"] {
    background-color: #17243A;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.04);
}

[data-testid="stMetricLabel"] {
    color: #64748B !important;
}

[data-testid="stMetricValue"] {
    color: #17243A !important;
    font-weight: 800 !important;
}

.main-title {
    font-size: 32px;
    font-weight: 800;
    color: #17243A !important;
    margin-bottom: 5px;
}

.sub-title {
    color: #64748B !important;
    font-size: 14px;
    margin-bottom: 25px;
}

.insight-box {
    background-color: #E8F5F1;
    padding: 17px;
    border-radius: 10px;
    border-left: 4px solid #16866D;
    color: #174D43 !important;
    margin: 12px 0 22px 0;
}

.insight-box * {
    color: #174D43 !important;
}

[data-testid="stDataFrame"] {
    background-color: #FFFFFF;
}

.stSelectbox label,
.stMultiSelect label,
.stSlider label,
[data-testid="stSelectSlider"] label {
    color: #17243A !important;
    font-weight: 600;
}

hr {
    border-color: #E2E8F0 !important;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. LOAD DATA
# =====================================================

BASE_DIR = Path(__file__).resolve().parent


@st.cache_data
def load_data():

    monthly = pd.read_csv(
        BASE_DIR / "monthly_sales.csv"
    )

    rfm = pd.read_csv(
        BASE_DIR / "rfm_scored.csv"
    )

    delivery = pd.read_csv(
        BASE_DIR / "delivery_data.csv"
    )

    # SALES DATA
    monthly["month"] = monthly["month"].astype(str)

    for col in ["total_orders", "total_revenue", "AOV"]:
        monthly[col] = pd.to_numeric(
            monthly[col],
            errors="coerce"
        )

    monthly = monthly.dropna(
        subset=["month", "total_orders", "total_revenue"]
    )

    monthly = monthly.sort_values("month")

    # RFM DATA
    for col in ["Recency", "Frequency", "Monetary"]:
        rfm[col] = pd.to_numeric(
            rfm[col],
            errors="coerce"
        )

    # DELIVERY DATA
    delivery["delivery_duration"] = pd.to_numeric(
        delivery["delivery_duration"],
        errors="coerce"
    )

    if "delay_days" in delivery.columns:
        delivery["delay_days"] = pd.to_numeric(
            delivery["delay_days"],
            errors="coerce"
        )

    delivery["order_purchase_timestamp"] = pd.to_datetime(
        delivery["order_purchase_timestamp"],
        errors="coerce"
    )

    delivery["month"] = (
        delivery["order_purchase_timestamp"]
        .dt.to_period("M")
        .astype(str)
    )

    return monthly, rfm, delivery


try:

    monthly_sales, rfm_scored, delivery_data = load_data()

except Exception as e:

    st.error(f"Gagal membaca dataset: {e}")

    st.info(
        "Pastikan app.py dan ketiga file CSV "
        "berada dalam folder dashboard yang sama."
    )

    st.stop()


# =====================================================
# 4. DATA VALIDATION
# =====================================================

required_sales = [
    "month",
    "total_orders",
    "total_revenue",
    "AOV"
]

required_rfm = [
    "Recency",
    "Frequency",
    "Monetary",
    "Segment"
]

required_delivery = [
    "delivery_duration",
    "delivery_status",
    "order_purchase_timestamp"
]

if not all(col in monthly_sales.columns for col in required_sales):
    st.error("Kolom pada monthly_sales.csv belum lengkap.")
    st.stop()

if not all(col in rfm_scored.columns for col in required_rfm):
    st.error("Kolom pada rfm_scored.csv belum lengkap.")
    st.stop()

if not all(col in delivery_data.columns for col in required_delivery):
    st.error("Kolom pada delivery_data.csv belum lengkap.")
    st.stop()


# =====================================================
# 5. HELPER FUNCTIONS
# =====================================================

def page_header(title, subtitle):

    st.markdown(
        f'<div class="main-title">{title}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="sub-title">{subtitle}</div>',
        unsafe_allow_html=True
    )


def insight(text):

    st.markdown(
        f"""
        <div class="insight-box">
            💡 <b>KEY INSIGHT</b><br>
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )


def metric_card(col, label, value):

    with col:
        st.metric(label, value)


def style_chart(fig, title=None):

    fig.update_layout(

        title=dict(
            text=title if title else "",
            font=dict(
                color="#17243A",
                size=20,
                family="Arial"
            )
        ),

        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",

        font=dict(
            color="#263449",
            family="Arial",
            size=13
        ),

        xaxis=dict(
            title_font=dict(color="#17243A"),
            tickfont=dict(color="#263449"),
            showgrid=False,
            zeroline=False
        ),

        yaxis=dict(
            title_font=dict(color="#17243A"),
            tickfont=dict(color="#263449"),
            gridcolor="#E8EDF3",
            zeroline=False
        ),

        legend=dict(
            font=dict(color="#263449"),
            title_font=dict(color="#17243A")
        ),

        hoverlabel=dict(
            bgcolor="#FFFFFF",
            font=dict(color="#17243A"),
            bordercolor="#D9E2EC"
        ),

        margin=dict(
            l=25,
            r=25,
            t=65,
            b=45
        )
    )

    return fig


def empty_message(data, message):

    if data.empty:
        st.warning(message)
        return True

    return False


# =====================================================
# 6. SIDEBAR NAVIGATION AND GLOBAL FILTER
# =====================================================

st.sidebar.markdown(
    """
    <div style="padding:10px 0;">
        <h1 style="color:white !important;">
            🛒 OLIST
        </h1>
        <p style="color:#AAB8CC !important;">
            E-Commerce Analytics
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "Sales Performance",
        "Customer RFM",
        "Delivery Performance"
    ]
)


# GLOBAL FILTER

st.sidebar.divider()

st.sidebar.markdown("## DATA FILTER")

# PERIOD FILTER

available_months = sorted(
    monthly_sales["month"].dropna().unique().tolist()
)

if len(available_months) >= 2:

    selected_period = st.sidebar.select_slider(
        "Pilih Periode Analisis",
        options=available_months,
        value=(
            available_months[0],
            available_months[-1]
        )
    )

else:

    selected_period = (
        available_months[0],
        available_months[0]
    )

# CUSTOMER SEGMENT FILTER

available_segments = sorted(
    rfm_scored["Segment"].dropna().unique().tolist()
)

selected_segments = st.sidebar.multiselect(
    "Pilih Segmen Pelanggan",
    options=available_segments,
    default=available_segments
)


# =====================================================
# 7. APPLY GLOBAL FILTER
# =====================================================

# SALES FILTER

filtered_sales = monthly_sales[
    monthly_sales["month"].between(
        selected_period[0],
        selected_period[1]
    )
].copy()


# DELIVERY FILTER

filtered_delivery = delivery_data[
    delivery_data["month"].between(
        selected_period[0],
        selected_period[1]
    )
].copy()


# RFM FILTER

filtered_rfm = rfm_scored[
    rfm_scored["Segment"].isin(selected_segments)
].copy()


st.sidebar.divider()

st.sidebar.caption(
    "Periode berlaku untuk Sales dan Delivery. "
    "Filter segmen berlaku untuk Customer RFM. "
    "Data RFM menggunakan snapshot 1 September 2018."
)


st.sidebar.markdown(
    """
    <br>
    <p style="color:#AAB8CC !important;">
        DATA SOURCE
    </p>
    Brazilian E-Commerce Public Dataset by Olist

    <br><br>

    <p style="color:#AAB8CC !important;">
        BUILT WITH
    </p>
    Python · Pandas · Plotly · Streamlit
    """,
    unsafe_allow_html=True
)


# =====================================================
# 8. OVERVIEW PAGE
# =====================================================

if page == "Overview":

    page_header(
        "E-Commerce Performance Dashboard",
        "Business intelligence overview of Olist e-commerce transactions"
    )

    if empty_message(
        filtered_sales,
        "Tidak ada data penjualan pada periode yang dipilih."
    ):
        st.stop()

    # KPI CALCULATIONS

    total_revenue = filtered_sales["total_revenue"].sum()

    total_orders = filtered_sales["total_orders"].sum()

    overall_aov = (
        total_revenue / total_orders
        if total_orders > 0 else 0
    )

    total_customers = len(filtered_rfm)

    delivery_total = len(filtered_delivery)

    on_time_count = (
        filtered_delivery["delivery_status"]
        .eq("On Time")
        .sum()
    )

    on_time_percentage = (
        on_time_count / delivery_total * 100
        if delivery_total > 0 else 0
    )

    # KPI CARDS

    col1, col2, col3, col4 = st.columns(4)

    metric_card(
        col1,
        "TOTAL REVENUE",
        f"R$ {total_revenue:,.2f}"
    )

    metric_card(
        col2,
        "TOTAL ORDERS",
        f"{total_orders:,.0f}"
    )

    metric_card(
        col3,
        "UNIQUE CUSTOMERS",
        f"{total_customers:,}"
    )

    metric_card(
        col4,
        "ON-TIME DELIVERY",
        f"{on_time_percentage:.2f}%"
    )

    st.caption(
        f"Periode: {selected_period[0]} sampai {selected_period[1]} "
        f"| AOV: R$ {overall_aov:,.2f}"
    )

    st.divider()

    # REVENUE TREND

    st.markdown("### 📈 Monthly Revenue Trend")

    fig = px.line(
        filtered_sales,
        x="month",
        y="total_revenue",
        markers=True,
        labels={
            "month": "Month",
            "total_revenue": "Revenue (R$)"
        }
    )

    fig.update_traces(
        line=dict(color="#16866D", width=3),
        marker=dict(size=8)
    )

    fig = style_chart(
        fig,
        "Monthly Revenue Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # SECOND ROW

    col1, col2 = st.columns(2)

    # DELIVERY STATUS

    with col1:

        st.markdown("### 🚚 Delivery Status")

        if not filtered_delivery.empty:

            status_counts = (
                filtered_delivery["delivery_status"]
                .value_counts()
                .reset_index()
            )

            status_counts.columns = [
                "Status",
                "Count"
            ]

            fig_status = px.pie(
                status_counts,
                names="Status",
                values="Count",
                hole=0.55,
                color="Status",
                color_discrete_map={
                    "On Time": "#16866D",
                    "Late": "#E76F51"
                }
            )

            fig_status.update_traces(
                textfont=dict(color="#17243A", size=13)
            )

            fig_status = style_chart(
                fig_status,
                "Delivery Status Distribution"
            )

            st.plotly_chart(
                fig_status,
                use_container_width=True
            )

        else:

            st.info("Tidak ada data pengiriman pada periode ini.")

    # CUSTOMER SEGMENTS

    with col2:

        st.markdown("### 👥 Customer Segments")

        if not filtered_rfm.empty:

            segment_counts = (
                filtered_rfm["Segment"]
                .value_counts()
                .reset_index()
            )

            segment_counts.columns = [
                "Segment",
                "Customers"
            ]

            fig_segment = px.bar(
                segment_counts,
                x="Customers",
                y="Segment",
                orientation="h",
                color="Customers",
                color_continuous_scale="Teal",
                labels={
                    "Customers": "Number of Customers",
                    "Segment": "Customer Segment"
                }
            )

            fig_segment = style_chart(
                fig_segment,
                "Customer Segment Distribution"
            )

            st.plotly_chart(
                fig_segment,
                use_container_width=True
            )

        else:

            st.info("Pilih minimal satu segmen pelanggan.")

    insight(
        "Dashboard menampilkan kondisi penjualan, karakteristik pelanggan, "
        "dan performa pengiriman berdasarkan filter yang dipilih."
    )


# =====================================================
# 9. SALES PERFORMANCE PAGE
# =====================================================

elif page == "Sales Performance":

    page_header(
        "Sales Performance Analysis",
        "Analyze monthly orders, revenue, and average order value"
    )

    if empty_message(
        filtered_sales,
        "Tidak ada data penjualan pada periode yang dipilih."
    ):
        st.stop()

    # KPI

    total_orders = filtered_sales["total_orders"].sum()

    total_revenue = filtered_sales["total_revenue"].sum()

    average_aov = (
        total_revenue / total_orders
        if total_orders > 0 else 0
    )

    col1, col2, col3 = st.columns(3)

    metric_card(
        col1,
        "TOTAL ORDERS",
        f"{total_orders:,.0f}"
    )

    metric_card(
        col2,
        "TOTAL REVENUE",
        f"R$ {total_revenue:,.2f}"
    )

    metric_card(
        col3,
        "AVERAGE ORDER VALUE",
        f"R$ {average_aov:,.2f}"
    )

    st.divider()

    # MONTHLY ORDERS

    st.markdown("### 📦 Monthly Orders")

    fig_orders = px.bar(
        filtered_sales,
        x="month",
        y="total_orders",
        color="total_orders",
        color_continuous_scale="Teal",
        text="total_orders",
        labels={
            "month": "Month",
            "total_orders": "Total Orders"
        }
    )

    fig_orders.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside"
    )

    fig_orders = style_chart(
        fig_orders,
        "Monthly Order Volume"
    )

    st.plotly_chart(
        fig_orders,
        use_container_width=True
    )

    # MONTHLY REVENUE

    st.markdown("### 💰 Monthly Revenue")

    fig_revenue = px.line(
        filtered_sales,
        x="month",
        y="total_revenue",
        markers=True,
        labels={
            "month": "Month",
            "total_revenue": "Revenue (R$)"
        }
    )

    fig_revenue.update_traces(
        line=dict(color="#16866D", width=3),
        marker=dict(size=8)
    )

    fig_revenue = style_chart(
        fig_revenue,
        "Monthly Revenue Trend"
    )

    st.plotly_chart(
        fig_revenue,
        use_container_width=True
    )

    # AOV

    st.markdown("### 🛍️ Average Order Value")

    fig_aov = px.line(
        filtered_sales,
        x="month",
        y="AOV",
        markers=True,
        labels={
            "month": "Month",
            "AOV": "Average Order Value (R$)"
        }
    )

    fig_aov.update_traces(
        line=dict(color="#D99A28", width=3),
        marker=dict(size=8)
    )

    fig_aov = style_chart(
        fig_aov,
        "Monthly Average Order Value"
    )

    st.plotly_chart(
        fig_aov,
        use_container_width=True
    )

    insight(
        "November 2017 recorded the highest monthly order volume "
        "and revenue during the analyzed period."
    )

    with st.expander("View Monthly Sales Data"):

        st.dataframe(
            filtered_sales,
            use_container_width=True,
            hide_index=True
        )


# =====================================================
# 10. CUSTOMER RFM PAGE
# =====================================================

elif page == "Customer RFM":

    page_header(
        "Customer Segmentation Analysis",
        "Understand customer behavior through Recency, Frequency, and Monetary"
    )

    st.caption(
        "Analisis RFM menggunakan riwayat transaksi "
        "1 Januari 2017 – 31 Agustus 2018, "
        "dengan snapshot 1 September 2018."
    )

    if empty_message(
        filtered_rfm,
        "Pilih minimal satu segmen pelanggan pada sidebar."
    ):
        st.stop()

    # KPI

    col1, col2, col3 = st.columns(3)

    metric_card(
        col1,
        "TOTAL CUSTOMERS",
        f"{len(filtered_rfm):,}"
    )

    metric_card(
        col2,
        "AVERAGE RECENCY",
        f"{filtered_rfm['Recency'].mean():.2f} days"
    )

    metric_card(
        col3,
        "AVERAGE MONETARY",
        f"R$ {filtered_rfm['Monetary'].mean():,.2f}"
    )

    st.divider()

    # SEGMENT DISTRIBUTION

    st.markdown("### 👥 Customer Segment Distribution")

    segment_counts = (
        filtered_rfm["Segment"]
        .value_counts()
        .reset_index()
    )

    segment_counts.columns = [
        "Segment",
        "Customers"
    ]

    fig_segment = px.bar(
        segment_counts,
        x="Segment",
        y="Customers",
        color="Customers",
        color_continuous_scale="Teal",
        text="Customers",
        labels={
            "Customers": "Number of Customers",
            "Segment": "Customer Segment"
        }
    )

    fig_segment.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside"
    )

    fig_segment.update_layout(
        xaxis_tickangle=-30
    )

    fig_segment = style_chart(
        fig_segment,
        "Customer Distribution by Segment"
    )

    st.plotly_chart(
        fig_segment,
        use_container_width=True
    )

    # SEGMENT PROFILE

    segment_profile = (
        filtered_rfm.groupby("Segment")
        .agg(
            Avg_Recency=("Recency", "mean"),
            Avg_Frequency=("Frequency", "mean"),
            Avg_Monetary=("Monetary", "mean"),
            Customers=("Segment", "count")
        )
        .reset_index()
    )

    # MONETARY PROFILE

    st.markdown("### 💰 Average Monetary by Segment")

    fig_monetary = px.bar(
        segment_profile.sort_values(
            "Avg_Monetary",
            ascending=False
        ),
        x="Segment",
        y="Avg_Monetary",
        color="Avg_Monetary",
        color_continuous_scale="Teal",
        labels={
            "Avg_Monetary": "Average Monetary (R$)",
            "Segment": "Customer Segment"
        }
    )

    fig_monetary.update_layout(
        xaxis_tickangle=-30
    )

    fig_monetary = style_chart(
        fig_monetary,
        "Average Customer Monetary Value"
    )

    st.plotly_chart(
        fig_monetary,
        use_container_width=True
    )

    # RECENCY AND FREQUENCY

    col1, col2 = st.columns(2)

    with col1:

        fig_recency = px.bar(
            segment_profile.sort_values(
                "Avg_Recency",
                ascending=True
            ),
            x="Segment",
            y="Avg_Recency",
            color="Avg_Recency",
            color_continuous_scale="Teal",
            labels={
                "Avg_Recency": "Average Recency (Days)",
                "Segment": "Customer Segment"
            }
        )

        fig_recency.update_layout(
            xaxis_tickangle=-40
        )

        fig_recency = style_chart(
            fig_recency,
            "Average Recency by Segment"
        )

        st.plotly_chart(
            fig_recency,
            use_container_width=True
        )

    with col2:

        fig_frequency = px.bar(
            segment_profile.sort_values(
                "Avg_Frequency",
                ascending=False
            ),
            x="Segment",
            y="Avg_Frequency",
            color="Avg_Frequency",
            color_continuous_scale="Teal",
            labels={
                "Avg_Frequency": "Average Frequency",
                "Segment": "Customer Segment"
            }
        )

        fig_frequency.update_layout(
            xaxis_tickangle=-40
        )

        fig_frequency = style_chart(
            fig_frequency,
            "Average Frequency by Segment"
        )

        st.plotly_chart(
            fig_frequency,
            use_container_width=True
        )

    # SEGMENT PROFILE TABLE

    st.markdown("### 📋 Customer Segment Profile")

    st.dataframe(
        segment_profile.style.format({
            "Avg_Recency": "{:.2f} days",
            "Avg_Frequency": "{:.2f}",
            "Avg_Monetary": "R$ {:,.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

    insight(
        "Hibernating customers represent the largest segment in the "
        "overall analysis, while High Value Repeat customers represent "
        "a smaller but valuable group. The displayed results follow "
        "the selected segment filter."
    )

    # CUSTOMER DETAIL

    st.markdown("### 🔎 Customer Detail")

    st.dataframe(
        filtered_rfm,
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# 11. DELIVERY PERFORMANCE PAGE
# =====================================================

elif page == "Delivery Performance":

    page_header(
        "Delivery Performance Analysis",
        "Evaluate delivery reliability, duration, and delay patterns"
    )

    if empty_message(
        filtered_delivery,
        "Tidak ada data pengiriman pada periode yang dipilih."
    ):
        st.stop()

    # DELIVERY CALCULATIONS

    delivery_summary = (
        filtered_delivery["delivery_status"]
        .value_counts()
    )

    on_time_count = delivery_summary.get(
        "On Time",
        0
    )

    late_count = delivery_summary.get(
        "Late",
        0
    )

    total_delivery = on_time_count + late_count

    on_time_pct = (
        on_time_count / total_delivery * 100
        if total_delivery > 0 else 0
    )

    late_pct = (
        late_count / total_delivery * 100
        if total_delivery > 0 else 0
    )

    avg_duration = filtered_delivery[
        "delivery_duration"
    ].mean()

    median_duration = filtered_delivery[
        "delivery_duration"
    ].median()

    # KPI

    col1, col2, col3, col4 = st.columns(4)

    metric_card(
        col1,
        "TOTAL DELIVERIES",
        f"{total_delivery:,}"
    )

    metric_card(
        col2,
        "ON-TIME DELIVERY",
        f"{on_time_pct:.2f}%"
    )

    metric_card(
        col3,
        "LATE DELIVERY",
        f"{late_pct:.2f}%"
    )

    metric_card(
        col4,
        "AVERAGE DURATION",
        f"{avg_duration:.2f} days"
    )

    st.divider()

    # DELIVERY VISUALIZATION

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 🚚 Delivery Status")

        status_df = pd.DataFrame({
            "Status": [
                "On Time",
                "Late"
            ],
            "Orders": [
                on_time_count,
                late_count
            ]
        })

        fig_status = px.pie(
            status_df,
            names="Status",
            values="Orders",
            hole=0.55,
            color="Status",
            color_discrete_map={
                "On Time": "#16866D",
                "Late": "#E76F51"
            }
        )

        fig_status.update_traces(
            textfont=dict(color="#17243A", size=13)
        )

        fig_status = style_chart(
            fig_status,
            "On-Time vs Late Deliveries"
        )

        st.plotly_chart(
            fig_status,
            use_container_width=True
        )

    with col2:

        st.markdown("### 📊 Delivery Duration Distribution")

        valid_duration = filtered_delivery.dropna(
            subset=["delivery_duration"]
        )

        if not valid_duration.empty:

            fig_duration = px.histogram(
                valid_duration,
                x="delivery_duration",
                nbins=40,
                color_discrete_sequence=["#16866D"],
                labels={
                    "delivery_duration": "Delivery Duration (Days)",
                    "count": "Number of Orders"
                }
            )

            fig_duration = style_chart(
                fig_duration,
                "Distribution of Delivery Duration"
            )

            st.plotly_chart(
                fig_duration,
                use_container_width=True
            )

        else:

            st.info("Tidak ada data durasi pengiriman yang valid.")

    # DELIVERY SUMMARY

    st.markdown("### ⏱️ Delivery Duration Summary")

    col1, col2, col3 = st.columns(3)

    metric_card(
        col1,
        "AVERAGE DURATION",
        f"{avg_duration:.2f} days"
    )

    metric_card(
        col2,
        "MEDIAN DURATION",
        f"{median_duration:.2f} days"
    )

    if "delay_days" in filtered_delivery.columns:

        late_orders = filtered_delivery[
            filtered_delivery["delivery_status"] == "Late"
        ]

        avg_delay = late_orders["delay_days"].mean()

        metric_card(
            col3,
            "AVERAGE DELAY",
            f"{avg_delay:.2f} days"
            if pd.notna(avg_delay)
            else "N/A"
        )

    else:

        metric_card(
            col3,
            "LATE ORDERS",
            f"{late_count:,}"
        )

    insight(
        "Sebagian besar pesanan berhasil diterima tepat waktu. "
        "Namun, pesanan yang terlambat tetap perlu dievaluasi "
        "untuk meningkatkan kualitas layanan logistik."
    )

    # DELIVERY DATA TABLE

    with st.expander("View Delivery Data"):

        st.dataframe(
            filtered_delivery,
            use_container_width=True,
            hide_index=True
        )


# =====================================================
# 12. FOOTER
# =====================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        padding:15px;
        color:#64748B;
        font-size:12px;
    ">
        <b style="color:#17243A;">
            Olist E-Commerce Analytics Dashboard
        </b>
        <br>
        Nazwa Agustin | Data Analysis Project
        <br>
        Python · Pandas · Plotly · Streamlit
        <br>
        Analysis Period: January 2017 – August 2018
    </div>
    """,
    unsafe_allow_html=True
)
