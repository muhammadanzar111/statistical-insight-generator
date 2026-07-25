import streamlit as st
import pandas as pd
from stats_engine import calculate_stats, run_ttest
from ai_narrator import generate_narrative

st.set_page_config(page_title="Statistical Insight Generator", layout="wide")

st.title("📊 Statistical Insight Generator")
st.write("Upload a CSV file or enter numerical data to analyze key descriptive and inferential statistics.")

# Sidebar Data Input Option
st.sidebar.header("Data Input Method")
input_option = st.sidebar.radio("Choose Input Method", ["Manual Input", "CSV Upload"])

data = []

if input_option == "Manual Input":
    user_input = st.text_area("Enter numbers separated by commas (e.g., 12, 15, 18, 22, 30):", "10, 20, 30, 40, 50, 60, 100")
    if user_input:
        try:
            data = [float(x.strip()) for x in user_input.split(",") if x.strip() != ""]
        except ValueError:
            st.error("Please enter valid numerical values separated by commas.")

elif input_option == "CSV Upload":
    uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if numeric_cols:
            selected_col = st.sidebar.selectbox("Select Column to Analyze", numeric_cols)
            data = df[selected_col].dropna().tolist()
        else:
            st.error("No numeric columns found in the uploaded file.")

# Run Analysis if data exists
if data:
    stats = calculate_stats(data)

    st.subheader("📈 Descriptive Statistics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Sample Size (N)", stats["count"])
    col2.metric("Mean", f"{stats['mean']:.2f}")
    col3.metric("Median", f"{stats['median']:.2f}")
    col4.metric("Std Deviation", f"{stats['std']:.2f}")

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Min", f"{stats['min']:.2f}")
    col6.metric("Max", f"{stats['max']:.2f}")
    col7.metric("Range", f"{stats['range']:.2f}")
    col8.metric("IQR", f"{stats['iqr']:.2f}")

    st.divider()

    st.subheader("📝 AI Narrative Insight")
    narrative = generate_narrative(stats)
    st.markdown(narrative)

    st.divider()

    st.subheader("🧪 Hypothesis Testing (One-Sample t-Test)")
    mu_0 = st.number_input("Enter Hypothesized Population Mean (μ₀):", value=0.0)
    if st.button("Run One-Sample t-Test"):
        ttest_res = run_ttest(data, mu_0)
        st.write(f"**t-Statistic:** {ttest_res['t_stat']:.4f}")
        st.write(f"**p-Value:** {ttest_res['p_value']:.4f}")
        st.info(ttest_res["interpretation"])

else:
    st.info("Please enter data or upload a CSV to begin analysis.")