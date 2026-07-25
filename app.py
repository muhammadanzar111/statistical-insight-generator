import streamlit as st
import pandas as pd
from stats_engine import (
    calculate_stats, run_one_sample_ttest, run_independent_ttest,
    run_paired_ttest, run_one_sample_ztest, run_two_sample_ztest,
    run_anova, run_chi_square, run_correlation, run_levene_test
)
from ai_narrator import generate_narrative

st.set_page_config(page_title="Statistical Insight Suite", layout="wide")
st.title("📊 Complete Statistical & Hypothesis Testing Suite")

st.sidebar.header("Navigation & Settings")
input_option = st.sidebar.radio("Data Input Method", ["Manual Input", "CSV Upload"])

# ---------------------------------------------------------
# MANUAL INPUT MODE
# ---------------------------------------------------------
if input_option == "Manual Input":
    st.sidebar.subheader("Select Test Type")
    test_type = st.sidebar.selectbox("Choose Analysis", [
        "Descriptive Summary & AI Narrative",
        "One-Sample t-Test",
        "Independent Two-Sample t-Test",
        "Paired (Dependent) t-Test",
        "One-Sample Z-Test",
        "Two-Sample Z-Test",
        "One-Way ANOVA",
        "Pearson Correlation",
        "Levene's Variance Test"
    ])

    st.subheader(f"⚙️ Test: {test_type}")

    if test_type == "Descriptive Summary & AI Narrative":
        raw = st.text_area("Enter numbers separated by commas:", "12, 15, 18, 22, 30, 45, 50, 100")
        if raw:
            data = [float(x.strip()) for x in raw.split(",") if x.strip() != ""]
            stats_res = calculate_stats(data)
            
            if stats_res:
                st.subheader("📈 Descriptive Statistics")
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Sample Size (N)", stats_res["count"])
                c2.metric("Mean", f"{stats_res['mean']:.2f}")
                c3.metric("Median", f"{stats_res['median']:.2f}")
                mode_val = f"{stats_res['mode']:.2f}" if isinstance(stats_res['mode'], (int, float)) else stats_res['mode']
                c4.metric("Mode", mode_val)

                c5, c6, c7, c8 = st.columns(4)
                c5.metric("Std Dev", f"{stats_res['std']:.2f}")
                c6.metric("Variance", f"{stats_res['variance']:.2f}")
                c7.metric("Range", f"{stats_res['range']:.2f}")
                c8.metric("IQR", f"{stats_res['iqr']:.2f}")

                st.subheader("📝 AI Narrative Insight")
                st.markdown(generate_narrative(stats_res))

    elif test_type == "One-Sample t-Test":
        raw = st.text_area("Enter Sample Values (comma-separated):", "12, 15, 18, 22, 30, 45")
        mu_0 = st.number_input("Hypothesized Population Mean (μ₀):", value=20.0)
        if st.button("Run One-Sample t-Test") and raw:
            data = [float(x.strip()) for x in raw.split(",") if x.strip() != ""]
            res = run_one_sample_ttest(data, mu_0)
            st.write(f"**t-Statistic:** {res['t_stat']:.4f} | **p-Value:** {res['p_value']:.4f}")
            st.info(res["interpretation"])

    elif test_type == "One-Sample Z-Test":
        raw = st.text_area("Enter Sample Values (comma-separated):", "12, 15, 18, 22, 30, 45")
        mu_0 = st.number_input("Hypothesized Population Mean (μ₀):", value=20.0)
        sigma_input = st.number_input("Population Std Dev (σ) [Optional, 0 = sample std]:", value=0.0)
        sigma = sigma_input if sigma_input > 0 else None
        if st.button("Run One-Sample Z-Test") and raw:
            data = [float(x.strip()) for x in raw.split(",") if x.strip() != ""]
            res = run_one_sample_ztest(data, mu_0, sigma)
            st.write(f"**Z-Statistic:** {res['z_stat']:.4f} | **p-Value:** {res['p_value']:.4f}")
            st.info(res["interpretation"])

    elif test_type in ["Independent Two-Sample t-Test", "Paired (Dependent) t-Test", "Two-Sample Z-Test", "Pearson Correlation", "Levene's Variance Test"]:
        col_a, col_b = st.columns(2)
        with col_a:
            raw_a = st.text_area("Group / Variable A (comma-separated):", "10, 15, 20, 25, 30")
        with col_b:
            raw_b = st.text_area("Group / Variable B (comma-separated):", "12, 18, 22, 28, 35")

        if st.button(f"Run {test_type}") and raw_a and raw_b:
            g1 = [float(x.strip()) for x in raw_a.split(",") if x.strip() != ""]
            g2 = [float(x.strip()) for x in raw_b.split(",") if x.strip() != ""]

            if test_type == "Independent Two-Sample t-Test":
                res = run_independent_ttest(g1, g2)
            elif test_type == "Paired (Dependent) t-Test":
                res = run_paired_ttest(g1, g2)
            elif test_type == "Two-Sample Z-Test":
                res = run_two_sample_ztest(g1, g2)
            elif test_type == "Pearson Correlation":
                res = run_correlation(g1, g2)
                st.write(f"**Pearson r:** {res['corr']:.4f}")
            elif test_type == "Levene's Variance Test":
                res = run_levene_test(g1, g2)

            stat_key = "t_stat" if "t_stat" in res else ("z_stat" if "z_stat" in res else ("stat" if "stat" in res else "corr"))
            st.write(f"**Test Statistic:** {res.get(stat_key, 0.0):.4f} | **p-Value:** {res['p_value']:.4f}")
            st.info(res["interpretation"])

    elif test_type == "One-Way ANOVA":
        raw_g1 = st.text_input("Group 1:", "10, 12, 14, 16")
        raw_g2 = st.text_input("Group 2:", "20, 22, 24, 26")
        raw_g3 = st.text_input("Group 3:", "30, 32, 34, 36")

        if st.button("Run One-Way ANOVA"):
            g1 = [float(x.strip()) for x in raw_g1.split(",") if x.strip() != ""]
            g2 = [float(x.strip()) for x in raw_g2.split(",") if x.strip() != ""]
            g3 = [float(x.strip()) for x in raw_g3.split(",") if x.strip() != ""]
            res = run_anova(g1, g2, g3)
            st.write(f"**F-Statistic:** {res['f_stat']:.4f} | **p-Value:** {res['p_value']:.4f}")
            st.info(res["interpretation"])

# ---------------------------------------------------------
# CSV UPLOAD MODE
# ---------------------------------------------------------
elif input_option == "CSV Upload":
    uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.subheader("📋 Dataset Preview")
        st.dataframe(df.head())

        num_cols = df.select_dtypes(include=['number']).columns.tolist()

        test_type = st.sidebar.selectbox("Select Statistical Test", [
            "Descriptive Summary",
            "One-Sample t-Test",
            "Independent Two-Sample t-Test",
            "Paired (Dependent) t-Test",
            "One-Sample Z-Test",
            "Two-Sample Z-Test",
            "One-Way ANOVA",
            "Chi-Square Test of Independence",
            "Pearson Correlation",
            "Levene's Variance Test"
        ])

        st.divider()
        st.subheader(f"⚙️ Test: {test_type}")

        if test_type == "Descriptive Summary" and num_cols:
            col = st.selectbox("Select Column", num_cols)
            stats_res = calculate_stats(df[col].dropna().tolist())
            if stats_res:
                st.subheader("📈 Descriptive Statistics")
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Sample Size (N)", stats_res["count"])
                c2.metric("Mean", f"{stats_res['mean']:.2f}")
                c3.metric("Median", f"{stats_res['median']:.2f}")
                mode_val = f"{stats_res['mode']:.2f}" if isinstance(stats_res['mode'], (int, float)) else stats_res['mode']
                c4.metric("Mode", mode_val)

                c5, c6, c7, c8 = st.columns(4)
                c5.metric("Std Dev", f"{stats_res['std']:.2f}")
                c6.metric("Variance", f"{stats_res['variance']:.2f}")
                c7.metric("Range", f"{stats_res['range']:.2f}")
                c8.metric("IQR", f"{stats_res['iqr']:.2f}")

                st.subheader("📝 AI Narrative Insight")
                st.markdown(generate_narrative(stats_res))

        elif test_type == "One-Sample t-Test" and num_cols:
            col = st.selectbox("Select Column", num_cols)
            mu_0 = st.number_input("Hypothesized Mean (μ₀)", value=0.0)
            if st.button("Run One-Sample t-Test"):
                res = run_one_sample_ttest(df[col].dropna().tolist(), mu_0)
                st.write(f"**t-Stat:** {res['t_stat']:.4f} | **p-Value:** {res['p_value']:.4f}")
                st.info(res["interpretation"])

        elif test_type == "One-Sample Z-Test" and num_cols:
            col = st.selectbox("Select Column", num_cols)
            mu_0 = st.number_input("Hypothesized Mean (μ₀)", value=0.0)
            sigma_input = st.number_input("Population Std Dev (σ) [Optional, 0 = sample std]:", value=0.0)
            sigma = sigma_input if sigma_input > 0 else None
            if st.button("Run One-Sample Z-Test"):
                res = run_one_sample_ztest(df[col].dropna().tolist(), mu_0, sigma)
                st.write(f"**Z-Stat:** {res['z_stat']:.4f} | **p-Value:** {res['p_value']:.4f}")
                st.info(res["interpretation"])

        elif test_type == "Independent Two-Sample t-Test" and len(num_cols) >= 2:
            col1 = st.selectbox("Group 1 Column", num_cols, index=0)
            col2 = st.selectbox("Group 2 Column", num_cols, index=1)
            if st.button("Run Independent t-Test"):
                res = run_independent_ttest(df[col1].dropna().tolist(), df[col2].dropna().tolist())
                st.write(f"**t-Stat:** {res['t_stat']:.4f} | **p-Value:** {res['p_value']:.4f}")
                st.info(res["interpretation"])

        elif test_type == "Two-Sample Z-Test" and len(num_cols) >= 2:
            col1 = st.selectbox("Group 1 Column", num_cols, index=0)
            col2 = st.selectbox("Group 2 Column", num_cols, index=1)
            if st.button("Run Two-Sample Z-Test"):
                res = run_two_sample_ztest(df[col1].dropna().tolist(), df[col2].dropna().tolist())
                st.write(f"**Z-Stat:** {res['z_stat']:.4f} | **p-Value:** {res['p_value']:.4f}")
                st.info(res["interpretation"])

        elif test_type == "Paired (Dependent) t-Test" and len(num_cols) >= 2:
            col1 = st.selectbox("Condition 1 (Pre)", num_cols, index=0)
            col2 = st.selectbox("Condition 2 (Post)", num_cols, index=1)
            if st.button("Run Paired t-Test"):
                clean_df = df[[col1, col2]].dropna()
                res = run_paired_ttest(clean_df[col1].tolist(), clean_df[col2].tolist())
                st.write(f"**t-Stat:** {res['t_stat']:.4f} | **p-Value:** {res['p_value']:.4f}")
                st.info(res["interpretation"])

        elif test_type == "One-Way ANOVA" and len(num_cols) >= 2:
            selected_cols = st.multiselect("Select 2 or more Numerical Columns", num_cols, default=num_cols[:2])
            if st.button("Run One-Way ANOVA") and len(selected_cols) >= 2:
                groups = [df[c].dropna().tolist() for c in selected_cols]
                res = run_anova(*groups)
                st.write(f"**F-Stat:** {res['f_stat']:.4f} | **p-Value:** {res['p_value']:.4f}")
                st.info(res["interpretation"])

        elif test_type == "Chi-Square Test of Independence":
            all_cols = df.columns.tolist()
            if len(all_cols) >= 2:
                c1 = st.selectbox("Categorical Var 1", all_cols, index=0)
                c2 = st.selectbox("Categorical Var 2", all_cols, index=1)
                if st.button("Run Chi-Square Test"):
                    contingency = pd.crosstab(df[c1], df[c2])
                    st.write("**Contingency Table:**", contingency)
                    res = run_chi_square(contingency)
                    st.write(f"**Chi2-Stat:** {res['chi2_stat']:.4f} | **p-Value:** {res['p_value']:.4f} | **DoF:** {res['dof']}")
                    st.info(res["interpretation"])

        elif test_type == "Pearson Correlation" and len(num_cols) >= 2:
            c1 = st.selectbox("Variable X", num_cols, index=0)
            c2 = st.selectbox("Variable Y", num_cols, index=1)
            if st.button("Run Correlation"):
                clean_df = df[[c1, c2]].dropna()
                res = run_correlation(clean_df[c1].tolist(), clean_df[c2].tolist())
                st.write(f"**Pearson r:** {res['corr']:.4f} | **p-Value:** {res['p_value']:.4f}")
                st.info(res["interpretation"])

        elif test_type == "Levene's Variance Test" and len(num_cols) >= 2:
            selected_cols = st.multiselect("Select Columns to compare Variance", num_cols, default=num_cols[:2])
            if st.button("Run Variance Test") and len(selected_cols) >= 2:
                groups = [df[c].dropna().tolist() for c in selected_cols]
                res = run_levene_test(*groups)
                st.write(f"**Stat:** {res['stat']:.4f} | **p-Value:** {res['p_value']:.4f}")
                st.info(res["interpretation"])
    else:
        st.info("Please upload a CSV file from the sidebar to perform statistical analysis.")