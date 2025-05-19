import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import io

st.title("📊 Basic Statistics and Distribution Analysis")

st.sidebar.header("Settings")

# Text input in sidebar
user_input = st.sidebar.text_area(
    "Paste your data here (value, category):",
    height=200,
    placeholder="Example:\n175,uomo\n168,donna\n182,uomo\n160,donna"
)

if user_input:
    try:
        data = pd.read_csv(io.StringIO(user_input), header=None, names=["Valore", "Categoria"])

        if data.shape[1] != 2:
            st.error("Data must have exactly two columns.")
        else:
            st.subheader("🔍 Data Preview")
            st.dataframe(data)

            # CSV download
            csv = data.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download CSV", csv, "input_data.csv", "text/csv")

            categorie_uniche = data["Categoria"].unique().tolist()
            categorie_scelte = st.sidebar.multiselect("Select two or more categories:", categorie_uniche)

            if len(categorie_scelte) >= 2:
                dati_filtrati = data[data["Categoria"].isin(categorie_scelte)]

                st.subheader("📈 Summary Statistics")
                statistiche = dati_filtrati.groupby("Categoria")["Valore"].agg(["count", "mean", "std", "min", "max"])
                st.dataframe(statistiche)

                # A/B Test (t-test)
                if len(categorie_scelte) == 2:
                    g1 = dati_filtrati[dati_filtrati["Categoria"] == categorie_scelte[0]]["Valore"]
                    g2 = dati_filtrati[dati_filtrati["Categoria"] == categorie_scelte[1]]["Valore"]
                    t_stat, p_val = stats.ttest_ind(g1, g2, equal_var=False)
                    st.markdown("### 🧪 A/B Test (t-test)")
                    st.write(f"t-statistic: `{t_stat:.4f}`")
                    st.write(f"p-value: `{p_val:.4f}`")
                    if p_val < 0.05:
                        st.success("Significant difference (p < 0.05)")
                    else:
                        st.info("No significant difference (p ≥ 0.05)")

                # ANOVA
                if len(categorie_scelte) > 2:
                    gruppi = [group["Valore"].values for _, group in dati_filtrati.groupby("Categoria")]
                    f_stat, p_val = stats.f_oneway(*gruppi)
                    st.markdown("### 🧪 ANOVA")
                    st.write(f"F-statistic: `{f_stat:.4f}`")
                    st.write(f"p-value: `{p_val:.4f}`")
                    if p_val < 0.05:
                        st.success("At least one group is significantly different (p < 0.05)")
                    else:
                        st.info("No significant difference between groups (p ≥ 0.05)")

                # Distribution plots
                st.subheader("📊 Distribution Plots")
                for cat in categorie_scelte:
                    subset = dati_filtrati[dati_filtrati["Categoria"] == cat]["Valore"]
                    fig, ax = plt.subplots()
                    sns.histplot(subset, kde=True, ax=ax)
                    ax.set_title(f"Distribution for {cat}")
                    st.pyplot(fig)

                # Shapiro-Wilk test
                st.subheader("🔬 Normality Test (Shapiro-Wilk)")
                for cat in categorie_scelte:
                    subset = dati_filtrati[dati_filtrati["Categoria"] == cat]["Valore"]
                    stat, p = stats.shapiro(subset)
                    st.write(f"**{cat}** → W = `{stat:.4f}`, p = `{p:.4f}`")
                    if p > 0.05:
                        st.success("Looks like a normal distribution (p > 0.05)")
                    else:
                        st.warning("Not normally distributed (p ≤ 0.05)")

            else:
                st.info("Please select at least two categories from the sidebar.")

    except Exception as e:
        st.error(f"Error reading input: {e}")
