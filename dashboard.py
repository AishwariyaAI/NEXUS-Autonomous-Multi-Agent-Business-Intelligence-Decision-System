# ============================================================
# NEXUS CONTROL CENTER
# Autonomous Multi-Agent Business Intelligence & Decision System
# ============================================================

import traceback

import pandas as pd
import streamlit as st

from app.graph.workflow import build_graph

from app.data.analytics import (
    prepare_data,
    calculate_kpis,
    monthly_sales,
    top_products,
    top_countries,
    customer_revenue,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NEXUS Control Center",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0b0f17;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .nexus-title {
        font-size: 46px;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 5px;
    }

    .nexus-subtitle {
        font-size: 18px;
        color: #9ca3af;
        margin-bottom: 35px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "dataset_loaded" not in st.session_state:
    st.session_state.dataset_loaded = False

if "uploaded_df" not in st.session_state:
    st.session_state.uploaded_df = None

if "analytics" not in st.session_state:
    st.session_state.analytics = None

if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

if "nexus_result" not in st.session_state:
    st.session_state.nexus_result = None

if "decision" not in st.session_state:
    st.session_state.decision = "NEED_MORE_RESEARCH"

if "decision_score" not in st.session_state:
    st.session_state.decision_score = 0

if "decision_reason" not in st.session_state:
    st.session_state.decision_reason = ""

if "recommendations" not in st.session_state:
    st.session_state.recommendations = []

if "executive_report" not in st.session_state:
    st.session_state.executive_report = ""


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="nexus-title">
        🧠 NEXUS Control Center
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="nexus-subtitle">
        Autonomous Multi-Agent Business Intelligence & Decision System
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ⚙️ NEXUS System")

    st.success("LangGraph Engine: Online")

    st.success("Multi-Agent System: Online")

    st.success("LLM Provider: Online")

    st.divider()

    st.markdown("## 🤖 Agents")

    st.write("🔎 Market Intelligence")
    st.write("💰 Financial Intelligence")
    st.write("👥 Customer Intelligence")
    st.write("🧠 Business Analyst")
    st.write("🎯 Decision Agent")
    st.write("📄 Executive Reporter")

    st.divider()

    if st.session_state.dataset_loaded:
        st.success("Dataset: Loaded")
    else:
        st.info("Dataset: Waiting")


# ============================================================
# DATASET UPLOAD
# ============================================================

st.header("📂 Business Dataset")

st.write(
    "Upload your own CSV or Excel business dataset "
    "and NEXUS will analyze it."
)

uploaded_file = st.file_uploader(
    "Upload your business dataset",
    type=[
        "csv",
        "xlsx",
        "xls",
    ],
    help="Supported formats: CSV, XLSX and XLS.",
)


# ============================================================
# LOAD DATASET
# ============================================================

if uploaded_file is not None:

    st.markdown(
        f"**Selected file:** `{uploaded_file.name}`"
    )

    load_button = st.button(
        "📥 Load & Analyze Dataset",
        type="primary",
        use_container_width=True,
    )

    if load_button:

        try:

            with st.spinner(
                "Loading and analyzing dataset..."
            ):

                # ------------------------------------------------
                # READ FILE
                # ------------------------------------------------

                file_name = uploaded_file.name.lower()

                if file_name.endswith(".csv"):

                    df = pd.read_csv(
                        uploaded_file
                    )

                elif file_name.endswith(".xlsx"):

                    df = pd.read_excel(
                        uploaded_file
                    )

                elif file_name.endswith(".xls"):

                    df = pd.read_excel(
                        uploaded_file
                    )

                else:

                    st.error(
                        "Unsupported file format."
                    )

                    st.stop()


                # ------------------------------------------------
                # EMPTY DATASET
                # ------------------------------------------------

                if df.empty:

                    st.error(
                        "The uploaded dataset is empty."
                    )

                    st.stop()


                # ------------------------------------------------
                # RAW ROW COUNT
                # ------------------------------------------------

                raw_rows = len(df)


                # ------------------------------------------------
                # REMOVE COMPLETELY EMPTY ROWS
                # ------------------------------------------------

                df = df.dropna(
                    how="all"
                ).copy()


                # ------------------------------------------------
                # PREPARE DATA
                # ------------------------------------------------

                try:

                    prepared_df = prepare_data(
                        df.copy()
                    )

                except Exception:

                    # If uploaded dataset does not match
                    # the default Online Retail structure,
                    # keep the uploaded dataframe.

                    prepared_df = df.copy()


                # ------------------------------------------------
                # SAVE DATAFRAME
                # ------------------------------------------------

                st.session_state.uploaded_df = (
                    prepared_df
                )

                st.session_state.uploaded_file_name = (
                    uploaded_file.name
                )


                # ------------------------------------------------
                # CALCULATE KPIs
                # ------------------------------------------------

                try:

                    kpis = calculate_kpis(
                        prepared_df
                    )

                except Exception:

                    kpis = {}


                # ------------------------------------------------
                # MONTHLY SALES
                # ------------------------------------------------

                try:

                    monthly = monthly_sales(
                        prepared_df
                    )

                except Exception:

                    monthly = {}


                # ------------------------------------------------
                # TOP PRODUCTS
                # ------------------------------------------------

                try:

                    products = top_products(
                        prepared_df
                    )

                except Exception:

                    products = {}


                # ------------------------------------------------
                # TOP COUNTRIES
                # ------------------------------------------------

                try:

                    countries = top_countries(
                        prepared_df
                    )

                except Exception:

                    countries = {}


                # ------------------------------------------------
                # CUSTOMER REVENUE
                # ------------------------------------------------

                try:

                    customers = customer_revenue(
                        prepared_df
                    )

                except Exception:

                    customers = {}


                # ------------------------------------------------
                # CUSTOMER CONCENTRATION
                # ------------------------------------------------

                concentration = {}

                try:

                    from app.data.analytics import (
                        customer_concentration
                    )

                    concentration = (
                        customer_concentration(
                            prepared_df
                        )
                    )

                except Exception:

                    concentration = {}


                # ------------------------------------------------
                # COMPLETE ANALYTICS
                # ------------------------------------------------

                analytics = {

                    "data": prepared_df,

                    "kpis": kpis,

                    "monthly_sales": monthly,

                    "top_products": products,

                    "top_countries": countries,

                    "customer_revenue": customers,

                    "customer_concentration":
                        concentration,

                    "raw_rows": raw_rows,

                    "clean_rows":
                        len(prepared_df),
                }


                # ------------------------------------------------
                # SAVE ANALYTICS
                # ------------------------------------------------

                st.session_state.analytics = (
                    analytics
                )

                st.session_state.dataset_loaded = (
                    True
                )


                # ------------------------------------------------
                # RESET OLD NEXUS RESULTS
                # ------------------------------------------------

                st.session_state.nexus_result = None

                st.session_state.decision = (
                    "NEED_MORE_RESEARCH"
                )

                st.session_state.decision_score = 0

                st.session_state.decision_reason = ""

                st.session_state.recommendations = []

                st.session_state.executive_report = ""


            st.success(
                f"✅ Dataset loaded successfully: "
                f"{uploaded_file.name}"
            )


        except Exception as exc:

            st.session_state.dataset_loaded = False

            st.error(
                f"❌ Unable to process dataset: {exc}"
            )

            with st.expander(
                "Technical details"
            ):

                st.code(
                    traceback.format_exc()
                )


else:

    st.info(
        "📂 Select a CSV or Excel dataset above, "
        "then click **Load & Analyze Dataset**."
    )


# ============================================================
# DATASET INFORMATION
# ============================================================

if st.session_state.dataset_loaded:

    analytics = st.session_state.analytics

    df = st.session_state.uploaded_df


    st.divider()

    st.header(
        "📊 Dataset Information"
    )


    raw_rows = analytics.get(
        "raw_rows",
        len(df),
    )

    clean_rows = analytics.get(
        "clean_rows",
        len(df),
    )

    column_count = len(
        df.columns
    )


    c1, c2, c3 = st.columns(3)


    with c1:

        st.metric(
            "Raw Rows",
            f"{raw_rows:,}",
        )


    with c2:

        st.metric(
            "Clean Rows",
            f"{clean_rows:,}",
        )


    with c3:

        st.metric(
            "Columns",
            f"{column_count:,}",
        )


    # ----------------------------------------------------------
    # COLUMNS
    # ----------------------------------------------------------

    with st.expander(
        "🔍 Detected Dataset Columns"
    ):

        for column in df.columns:

            st.write(
                f"• `{column}`"
            )


    # ----------------------------------------------------------
    # PREVIEW
    # ----------------------------------------------------------

    with st.expander(
        "👀 Preview Uploaded Dataset"
    ):

        st.dataframe(
            df.head(20),
            use_container_width=True,
        )


    # ==========================================================
    # BUSINESS KPIs
    # ==========================================================

    st.divider()

    st.header(
        "📈 Business Intelligence Overview"
    )


    kpis = analytics.get(
        "kpis",
        {}
    )


    total_revenue = kpis.get(
        "total_revenue",
        0,
    )

    total_orders = kpis.get(
        "total_orders",
        0,
    )

    total_customers = kpis.get(
        "total_customers",
        0,
    )

    average_order_value = kpis.get(
        "average_order_value",
        0,
    )


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(
            "Total Revenue",
            f"£{total_revenue:,.2f}",
        )


    with c2:

        st.metric(
            "Total Orders",
            f"{total_orders:,}",
        )


    with c3:

        st.metric(
            "Customers",
            f"{total_customers:,}",
        )


    with c4:

        st.metric(
            "Average Order Value",
            f"£{average_order_value:,.2f}",
        )


    # ==========================================================
    # SALES INTELLIGENCE
    # ==========================================================

    st.header(
        "📉 Sales Intelligence"
    )


    monthly_data = analytics.get(
        "monthly_sales"
    )


    if isinstance(
        monthly_data,
        pd.DataFrame,
    ):

        st.subheader(
            "Monthly Revenue"
        )

        st.line_chart(
            monthly_data,
            use_container_width=True,
        )


    # ==========================================================
    # TOP PRODUCTS AND COUNTRIES
    # ==========================================================

    col1, col2 = st.columns(2)


    with col1:

        st.subheader(
            "🏆 Top Products"
        )

        products = analytics.get(
            "top_products"
        )

        if isinstance(
            products,
            pd.DataFrame,
        ):

            st.dataframe(
                products.head(10),
                use_container_width=True,
            )

        elif products:

            st.write(
                products
            )

        else:

            st.info(
                "Product analytics unavailable."
            )


    with col2:

        st.subheader(
            "🌍 Top Countries"
        )

        countries = analytics.get(
            "top_countries"
        )

        if isinstance(
            countries,
            pd.DataFrame,
        ):

            st.dataframe(
                countries.head(10),
                use_container_width=True,
            )

        elif countries:

            st.write(
                countries
            )

        else:

            st.info(
                "Country analytics unavailable."
            )


# ============================================================
# BUSINESS QUERY
# ============================================================

st.divider()

st.header(
    "💡 Business Intelligence Query"
)


if not st.session_state.dataset_loaded:

    st.warning(
        "⚠️ Load a dataset before running NEXUS analysis."
    )


question = st.text_area(
    "Enter a business problem",
    placeholder=(
        "Example: Analyze the overall business performance, "
        "identify the key drivers of revenue, customer "
        "concentration risks, underperforming areas, and "
        "potential growth opportunities."
    ),
    height=130,
    disabled=not st.session_state.dataset_loaded,
)


# ============================================================
# RUN NEXUS
# ============================================================

run_button = st.button(
    "🚀 Run NEXUS Analysis",
    type="primary",
    use_container_width=True,
    disabled=not st.session_state.dataset_loaded,
)


if run_button:

    if not question.strip():

        st.warning(
            "Please enter a business question."
        )

        st.stop()


    analytics = st.session_state.analytics


    st.divider()

    st.header(
        "⚡ NEXUS Execution"
    )


    progress = st.progress(
        0
    )

    status = st.empty()


    try:

        # ------------------------------------------------------
        # STEP 1
        # ------------------------------------------------------

        status.info(
            "Initializing NEXUS..."
        )

        progress.progress(
            10
        )


        # ------------------------------------------------------
        # STEP 2
        # ------------------------------------------------------

        status.info(
            "Building LangGraph workflow..."
        )

        graph = build_graph()

        progress.progress(
            20
        )


        # ------------------------------------------------------
        # INITIAL STATE
        # ------------------------------------------------------

        initial_state = {

            "query": question,

            "question": question,

            "iteration": 0,

            "uploaded_analytics":
                analytics,

        }


        # ------------------------------------------------------
        # RUN LANGGRAPH
        # ------------------------------------------------------

        status.info(
            "Running NEXUS multi-agent workflow..."
        )


        result = graph.invoke(
            initial_state
        )


        # ======================================================
        # IMPORTANT:
        # SAVE LANGGRAPH RESULT TO SESSION STATE
        # ======================================================

        st.session_state["nexus_result"] = (
            result
        )

        st.session_state["decision"] = (
            result.get(
                "decision",
                "NEED_MORE_RESEARCH"
            )
        )

        st.session_state["decision_score"] = (
            result.get(
                "decision_score",
                0
            )
        )

        st.session_state["decision_reason"] = (
            result.get(
                "decision_reason",
                ""
            )
        )

        st.session_state["recommendations"] = (
            result.get(
                "recommendations",
                []
            )
        )

        st.session_state["executive_report"] = (
            result.get(
                "executive_report",
                ""
            )
        )


        # ------------------------------------------------------
        # FINISH
        # ------------------------------------------------------

        progress.progress(
            100
        )

        status.success(
            "✅ NEXUS analysis completed successfully."
        )


    except Exception as exc:

        progress.empty()

        status.error(
            "❌ NEXUS execution failed."
        )

        st.error(
            str(exc)
        )

        with st.expander(
            "🔧 Technical Details"
        ):

            st.code(
                traceback.format_exc()
            )

        st.stop()


# ============================================================
# RESULTS
# ============================================================

result = st.session_state.get(
    "nexus_result"
)


if result:

    st.divider()

    st.header(
        "🎯 NEXUS Decision Center"
    )


    # ========================================================
    # READ VALUES FROM SESSION STATE
    # ========================================================

    decision = st.session_state.get(
        "decision",
        "NEED_MORE_RESEARCH"
    )

    decision_score = st.session_state.get(
        "decision_score",
        0
    )

    decision_reason = st.session_state.get(
        "decision_reason",
        ""
    )

    recommendations = st.session_state.get(
        "recommendations",
        []
    )

    executive_report = st.session_state.get(
        "executive_report",
        ""
    )

    research_cycles = result.get(
        "iteration",
        0
    )


    # ========================================================
    # DECISION METRICS
    # ========================================================

    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(
            "Research Agents",
            "3",
        )


    with c2:

        st.metric(
            "Decision Score",
            f"{decision_score}/100",
        )


    with c3:

        st.metric(
            "Decision",
            str(decision),
        )


    with c4:

        st.metric(
            "Research Cycles",
            str(
                research_cycles + 1
            ),
        )


    # ========================================================
    # DECISION MESSAGE
    # ========================================================

    if decision == "APPROVE":

        st.success(
            f"✅ Decision APPROVED\n\n"
            f"{decision_reason}"
        )

    elif decision == "APPROVE_WITH_CAUTION":

        st.warning(
            f"⚠️ Decision approved with caution.\n\n"
            f"{decision_reason}"
        )

    elif decision == "NEED_MORE_RESEARCH":

        st.warning(
            f"🔎 Additional research recommended.\n\n"
            f"{decision_reason}"
        )

    elif decision == "REJECT":

        st.error(
            f"❌ Decision rejected.\n\n"
            f"{decision_reason}"
        )

    else:

        st.info(
            f"Decision: {decision}\n\n"
            f"{decision_reason}"
        )


    # ========================================================
    # AGENT INTELLIGENCE
    # ========================================================

    st.divider()

    st.header(
        "🤖 NEXUS Agent Intelligence"
    )


    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "🔎 Market Intelligence",
            "💰 Financial Intelligence",
            "👥 Customer Intelligence",
            "🧠 Business Analysis",
        ]
    )


    # --------------------------------------------------------
    # MARKET
    # --------------------------------------------------------

    with tab1:

        market = result.get(
            "market_analysis",
            ""
        )

        if market:

            st.markdown(
                market
            )

        else:

            st.info(
                "Market analysis not available."
            )


    # --------------------------------------------------------
    # FINANCE
    # --------------------------------------------------------

    with tab2:

        finance = result.get(
            "finance_analysis",
            ""
        )

        if finance:

            st.markdown(
                finance
            )

        else:

            st.info(
                "Financial analysis not available."
            )


    # --------------------------------------------------------
    # CUSTOMER
    # --------------------------------------------------------

    with tab3:

        customer = result.get(
            "customer_analysis",
            ""
        )

        if customer:

            st.markdown(
                customer
            )

        else:

            st.info(
                "Customer analysis not available."
            )


    # --------------------------------------------------------
    # BUSINESS ANALYSIS
    # --------------------------------------------------------

    with tab4:

        business = result.get(
            "business_analysis",
            ""
        )

        if business:

            st.markdown(
                business
            )

        else:

            st.info(
                "Business analysis not available."
            )


    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    st.divider()

    st.header(
        "🎯 Recommended Actions"
    )


    if recommendations:

        for index, recommendation in enumerate(
            recommendations,
            start=1,
        ):

            st.markdown(
                f"### Recommendation {index}"
            )


            # ----------------------------------------------
            # New structured recommendation format
            # ----------------------------------------------

            if isinstance(
                recommendation,
                dict,
            ):

                action = recommendation.get(
                    "action",
                    "No action specified."
                )

                reason = recommendation.get(
                    "reason",
                    ""
                )

                priority = recommendation.get(
                    "priority",
                    "MEDIUM"
                )

                evidence_type = recommendation.get(
                    "evidence_type",
                    "Hypothesis"
                )


                st.markdown(
                    f"**Action:** {action}"
                )

                if reason:

                    st.markdown(
                        f"**Reason:** {reason}"
                    )

                st.markdown(
                    f"**Priority:** {priority}"
                )

                st.markdown(
                    f"**Evidence Type:** {evidence_type}"
                )


            else:

                st.markdown(
                    str(
                        recommendation
                    )
                )


    else:

        st.info(
            "No recommendations returned by the Decision Agent."
        )


    # ========================================================
    # EXECUTIVE REPORT
    # ========================================================

    st.divider()

    st.header(
        "📄 Executive Business Report"
    )


    if executive_report:

        st.markdown(
            executive_report
        )


        st.download_button(
            label="⬇️ Download Executive Report",
            data=executive_report,
            file_name="NEXUS_Executive_Report.md",
            mime="text/markdown",
            use_container_width=True,
        )


    else:

        st.warning(
            "Executive Reporter did not return a report."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "NEXUS — Autonomous Multi-Agent Business Intelligence & Decision System"
)