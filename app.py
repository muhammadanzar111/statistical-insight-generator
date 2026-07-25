import streamlit as st
import stats_engine as se
import ai_narrator as ai

# Page configuration
st.set_page_config(page_title="Statistical Insight Generator", page_icon="📊", layout="wide")

st.title("📊 Statistical Insight Engine")

# Sidebar Data Inputs
st.sidebar.header("Data Settings")
dataset_label = st.sidebar.text_input("Dataset Name", value="Sales Data")
input_method = st.sidebar.radio("Input Method", ["Paste Numbers", "Upload CSV"])

numbers_list = []

if input_method == "Paste Numbers":
    raw_input = st.text_area("Enter numbers separated by commas", "120, 135, 128, 142, 110, 350, 125, 130")
    if raw_input:
        try:
            numbers_list = [float(x.strip()) for x in raw_input.split(",") if x.strip()]
        except ValueError:
            st.error("Please enter valid numbers separated by commas.")

# Process Data & Display Output
if st.button("Generate Analysis"):
    if not numbers_list:
        st.warning("Please provide data before generating analysis.")
    else:
        # Compute core statistics
        stats = se.calculate_summary_statistics(numbers_list)

        # Layout columns
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📈 Statistical Metrics")
            st.metric("Sample Size (N)", stats["count"])
            st.metric("Mean", stats["mean"])
            st.metric("Median", stats["median"])
            st.metric("Std Dev", stats["std_dev"])
            st.metric("Min / Max", f"{stats['min']} / {stats['max']}")
            st.write(f"**Outliers:** {stats['outliers']}")

        with col2:
            st.subheader("💡 Executive Insights")
            insights = ai.generate_statistical_insights(stats, dataset_label)
            st.write(insights)