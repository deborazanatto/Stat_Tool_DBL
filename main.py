import io

import pandas as pd
import streamlit as st
from scipy import stats

with st.sidebar:
    with open("images/deepblue.svg") as f:
        image = f.read()
    st.image(image, use_container_width=False)

    st.sidebar.header("Statistics Dashboard")

    # st.sidebar.markdown("")

st.title("Calcolo Statistiche su Dati Categoriali")

st.markdown(
    """
Inserisci i tuoi dati nel box sottostante.  
- Le colonne devono essere separate da **virgola**  
- La **prima colonna** deve contenere i **valori numerici**  
- La **seconda colonna** deve contenere le **categorie**  
"""
)

# Text input
user_input = st.text_area("Inserisci i dati:", height=200, placeholder="Esempio:\n10, A\n20, B\n15, A\n30, C")

if user_input:
    try:
        # Convert string input to a DataFrame
        data = pd.read_csv(io.StringIO(user_input), header=None, names=["Valore", "Categoria"])

        # Check if data is valid
        if data.shape[1] != 2:
            st.error("I dati devono avere esattamente due colonne.")

        else:
            # Visualizza il dataset
            st.subheader("Anteprima dei dati")
            st.dataframe(data)

            # Statistiche di base
            st.subheader("Statistiche per Categoria")
            statistiche = data.groupby("Categoria")["Valore"].agg(["count", "mean", "std", "min", "max"])
            st.dataframe(statistiche)

            # Selezione delle categorie
            categorie_uniche = sorted(data["Categoria"].unique().tolist())
            categorie_scelte = 0

            if len(categorie_uniche) > 2:
                st.subheader("Seleziona le categorie da confrontare")
                categorie_scelte = st.multiselect("", categorie_uniche)

            elif len(categorie_uniche) == 2:
                categorie_scelte = categorie_uniche

            if len(categorie_scelte) >= 2:
                # Filtra i dati per le categorie scelte
                dati_filtrati = data[data["Categoria"].isin(categorie_scelte)]

            elif len(categorie_scelte) == 1:
                st.warning("Seleziona almeno **due categorie** per il confronto.")

            else:
                st.info("Seleziona due o più categorie per calcolare le statistiche.")

            if len(categorie_scelte) >= 2:
                st.subheader("Statistiche Avanzate")

            # A/B Test (solo se 2 gruppi)
            if len(categorie_scelte) == 2:
                gruppo1 = dati_filtrati[data["Categoria"] == categorie_scelte[0]]["Valore"]
                gruppo2 = dati_filtrati[data["Categoria"] == categorie_scelte[1]]["Valore"]

                t_stat, p_val = stats.ttest_ind(gruppo1, gruppo2, equal_var=False)

                st.markdown("**Test A/B (t-test indipendente):**")
                st.write(f"Statistiche t: `{t_stat:.4f}`")
                st.write(f"p-value: `{p_val:.4f}`")

                if p_val < 0.05:
                    st.success("Differenza significativa tra i due gruppi (p < 0.05)")
                else:
                    st.info("Nessuna differenza statisticamente significativa (p ≥ 0.05)")

            # ANOVA (più di 2 gruppi)
            if len(categorie_scelte) > 2:
                gruppi = [group["Valore"].values for _, group in dati_filtrati.groupby("Categoria")]
                f_stat, p_val = stats.f_oneway(*gruppi)

                st.markdown("**ANOVA (analisi della varianza):**")
                st.write(f"F-statistica: `{f_stat:.4f}`")
                st.write(f"p-value: `{p_val:.4f}`")

                if p_val < 0.05:
                    st.success("Almeno un gruppo differisce significativamente dagli altri (p < 0.05)")
                else:
                    st.info("Nessuna differenza significativa tra i gruppi (p ≥ 0.05)")

    except Exception as e:
        st.error(f"Errore nel parsing dei dati: {e}")
