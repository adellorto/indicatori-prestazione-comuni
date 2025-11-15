import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configurazione pagina
st.set_page_config(
    page_title="Indicatori di Prestazione Comunale",
    page_icon="🏛️",
    layout="wide"
)

# Titolo
st.title("🏛️ Dashboard Indicatori di Prestazione Comunale")
st.markdown("Basato su UNI/PdR 5:2013 - Framework di Prestazione per Amministrazioni Locali Italiane")

# Crea cartella data se non esiste
os.makedirs("data", exist_ok=True)

# Definizione categorie indicatori e relativi codici
INDICATORI_GOVERNO = {
    "G.1": "Autonomia Finanziaria",
    "G.2": "Velocità di Riscossione Annua",
    "G.3": "Efficacia di Gestione del Bilancio",
    "G.4": "Efficacia di Gestione dei Residui",
    "G.5": "Propensione all'Investimento",
    "G.6": "Pressione Tributaria per Abitante",
    "G.7": "Rispetto del Patto di Stabilità",
    "G.8": "Capacità di Ascolto dei Cittadini",
    "G.9": "Orientamento all'Innovazione",
    "G.10": "Orientamento alla Gestione per Processi",
    "G.11": "Stabilità del Fondo Cassa",
    "G.12": "Coefficiente di Spesa per OOPP"
}

INDICATORI_OPERATIVI = {
    "O.1": "Rispetto dei Tempi di Rilascio Documenti",
    "O.2": "Rispetto dei Tempi di Trattamento Pratiche",
    "O.3": "Accessibilità ai Servizi",
    "O.4": "Assenza di Barriere Architettoniche",
    "O.5": "Tempo Medio di Attesa allo Sportello",
    "O.6": "Soddisfazione Generale dei Cittadini",
    "O.7": "Rispetto dei Tempi di Realizzazione OOPP",
    "O.8": "Tempo di Intervento su Manutenzione",
    "O.9": "Conservazione Patrimonio e Verde Pubblico",
    "O.10": "Disponibilità Servizi Sociali",
    "O.11": "Disponibilità Servizi Culturali/Tempo Libero",
    "O.12": "Efficacia Servizi Educativi",
    "O.13": "Soddisfazione Servizi Scolastici",
    "O.14": "Sicurezza Cittadini - Reati contro il Patrimonio",
    "O.15": "Sicurezza Cittadini - Reati contro le Persone",
    "O.16": "Sicurezza Cittadini - Disponibilità Agenti",
    "O.17": "Sicurezza Cittadini - Servizio Emergenze",
    "O.18": "Sicurezza Cittadini - Incidenza Furti",
    "O.19": "Violazione Norme Amministrative",
    "O.20": "Sviluppo Economico - Tasso Nascita Imprese",
    "O.21": "Sfruttamento Territoriale",
    "O.22": "Efficienza Rete Idrica",
    "O.23": "Classe Energetica dell'Amministrazione",
    "O.24": "Sostenibilità Ambientale",
    "O.25": "Efficienza Raccolta Rifiuti"
}

INDICATORI_SUPPORTO = {
    "S.1": "Tempo Medio Formazione Atti Interni",
    "S.2": "Rispetto Tempi Emissione Atti Interni",
    "S.3": "Funzionamento Protocollo in Entrata",
    "S.4": "Funzionamento Protocollo in Uscita",
    "S.5": "Grado di Dematerializzazione Documenti",
    "S.6": "Copertura Sistema Customer Satisfaction",
    "S.7": "Livello Struttura IT - PC/Tablet",
    "S.8": "Livello Struttura IT - Accesso Internet",
    "S.9": "Tempo Medio Risposta Reclami",
    "S.10": "Livello Attivazione Partnership",
    "S.11": "Qualità Sito Web - Frequenza Aggiornamento",
    "S.12": "Qualità Sito Web - Accessibilità",
    "S.13": "Qualità Sito Web - Usabilità",
    "S.14": "Rispetto Tempi Pagamento Fornitori",
    "S.15": "Copertura Servizi Online",
    "S.16": "Utilizzo Servizi Online",
    "S.17": "Copertura Carta dei Servizi",
    "S.18": "Livello Partecipazione Cittadini",
    "S.19": "Presenza Personale in Servizio",
    "S.20": "Attenzione Formazione - Tempo Dedicato",
    "S.21": "Attenzione Formazione - Corsi Realizzati",
    "S.22": "Tasso Turnover Personale",
    "S.23": "Sicurezza Luoghi di Lavoro"
}

TUTTI_INDICATORI = {**INDICATORI_GOVERNO, **INDICATORI_OPERATIVI, **INDICATORI_SUPPORTO}

# Sidebar per navigazione
st.sidebar.title("Navigazione")
pagina = st.sidebar.radio("Scegli una pagina:", ["Inserisci Nuovi Dati", "Visualizza Dati Esistenti", "Confronta Comuni"])

# Percorso file CSV
FILE_CSV = "data/indicatori_comuni.csv"

def carica_dati_esistenti():
    """Carica i dati esistenti dei comuni dal CSV"""
    if os.path.exists(FILE_CSV):
        return pd.read_csv(FILE_CSV)
    return pd.DataFrame()

def salva_dati(nuovi_dati):
    """Salva i nuovi dati del comune nel CSV"""
    df = carica_dati_esistenti()
    nuova_riga = pd.DataFrame([nuovi_dati])
    df = pd.concat([df, nuova_riga], ignore_index=True)
    df.to_csv(FILE_CSV, index=False)
    return True

# PAGINA 1: Inserisci Nuovi Dati
if pagina == "Inserisci Nuovi Dati":
    st.header("📝 Inserisci Dati Prestazionali del Comune")

    # Informazioni base del comune
    st.subheader("Informazioni Comune")
    col1, col2 = st.columns(2)

    with col1:
        nome_comune = st.text_input("Nome Comune *", placeholder="es., Comune di Milano")
        provincia = st.text_input("Provincia", placeholder="es., Milano")

    with col2:
        regione = st.text_input("Regione", placeholder="es., Lombardia")
        popolazione = st.number_input("Popolazione", min_value=0, step=1)

    data_inserimento = st.date_input("Data Inserimento", value=datetime.now())
    anno_riferimento = st.number_input("Anno di Riferimento", min_value=2000, max_value=2100, value=2023)

    # Tab per diverse categorie di indicatori
    tab1, tab2, tab3 = st.tabs(["🏛️ Governo (12)", "⚙️ Operativi (25)", "🔧 Supporto (23)"])

    valori_indicatori = {}

    with tab1:
        st.subheader("Indicatori di Governo (G.1 - G.12)")
        st.markdown("*Questi indicatori misurano i processi di governance, gestione finanziaria e pianificazione strategica.*")

        for codice, nome in INDICATORI_GOVERNO.items():
            valori_indicatori[codice] = st.number_input(
                f"{codice}: {nome}",
                min_value=0.0,
                max_value=100000.0,
                step=0.01,
                format="%.2f",
                key=codice,
                help=f"Inserisci valore per {nome}"
            )

    with tab2:
        st.subheader("Indicatori Operativi (O.1 - O.25)")
        st.markdown("*Questi indicatori misurano l'efficacia dell'erogazione dei servizi e la soddisfazione dei cittadini.*")

        for codice, nome in INDICATORI_OPERATIVI.items():
            valori_indicatori[codice] = st.number_input(
                f"{codice}: {nome}",
                min_value=0.0,
                max_value=100000.0,
                step=0.01,
                format="%.2f",
                key=codice,
                help=f"Inserisci valore per {nome}"
            )

    with tab3:
        st.subheader("Indicatori di Supporto (S.1 - S.23)")
        st.markdown("*Questi indicatori misurano i processi interni, sistemi IT e risorse umane.*")

        for codice, nome in INDICATORI_SUPPORTO.items():
            valori_indicatori[codice] = st.number_input(
                f"{codice}: {nome}",
                min_value=0.0,
                max_value=100000.0,
                step=0.01,
                format="%.2f",
                key=codice,
                help=f"Inserisci valore per {nome}"
            )

    # Pulsante di salvataggio
    st.markdown("---")
    if st.button("💾 Salva Dati Comune", type="primary", use_container_width=True):
        if not nome_comune:
            st.error("❌ Per favore inserisci il nome del comune!")
        else:
            # Prepara dizionario dati
            nuovi_dati = {
                "Comune": nome_comune,
                "Provincia": provincia,
                "Regione": regione,
                "Popolazione": popolazione,
                "Data_Inserimento": data_inserimento.strftime("%Y-%m-%d"),
                "Anno_Riferimento": anno_riferimento,
                **valori_indicatori
            }

            # Salva su CSV
            if salva_dati(nuovi_dati):
                st.success(f"✅ Dati per {nome_comune} salvati con successo!")
            else:
                st.error("❌ Errore nel salvataggio dei dati. Riprova.")

# PAGINA 2: Visualizza Dati Esistenti
elif pagina == "Visualizza Dati Esistenti":
    st.header("📊 Visualizza Dati Comuni Esistenti")

    df = carica_dati_esistenti()

    if df.empty:
        st.info("ℹ️ Nessun dato disponibile. Inserisci prima i dati per i comuni.")
    else:
        st.success(f"Trovati dati per {len(df)} comune/comuni")

        # Opzioni filtro
        st.subheader("Filtra Dati")
        comune_selezionato = st.selectbox(
            "Seleziona Comune",
            options=["Tutti"] + df["Comune"].unique().tolist()
        )

        # Visualizza dati filtrati
        if comune_selezionato != "Tutti":
            df_filtrato = df[df["Comune"] == comune_selezionato]
        else:
            df_filtrato = df

        # Mostra informazioni base
        st.subheader("Informazioni di Base")
        colonne_visualizzate = ["Comune", "Provincia", "Regione", "Popolazione", "Anno_Riferimento", "Data_Inserimento"]
        st.dataframe(df_filtrato[colonne_visualizzate], use_container_width=True)

        # Mostra indicatori per categoria
        st.subheader("Valori Indicatori")

        tab_indicatori1, tab_indicatori2, tab_indicatori3 = st.tabs(["Governo", "Operativi", "Supporto"])

        with tab_indicatori1:
            col_gov = list(INDICATORI_GOVERNO.keys())
            if all(col in df_filtrato.columns for col in col_gov):
                st.dataframe(df_filtrato[["Comune"] + col_gov], use_container_width=True)

        with tab_indicatori2:
            col_op = list(INDICATORI_OPERATIVI.keys())
            if all(col in df_filtrato.columns for col in col_op):
                st.dataframe(df_filtrato[["Comune"] + col_op], use_container_width=True)

        with tab_indicatori3:
            col_sup = list(INDICATORI_SUPPORTO.keys())
            if all(col in df_filtrato.columns for col in col_sup):
                st.dataframe(df_filtrato[["Comune"] + col_sup], use_container_width=True)

        # Opzione download
        st.markdown("---")
        csv = df_filtrato.to_csv(index=False)
        st.download_button(
            label="📥 Scarica Dati come CSV",
            data=csv,
            file_name=f"dati_comuni_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# PAGINA 3: Confronta Comuni
elif pagina == "Confronta Comuni":
    st.header("📈 Confronta Comuni")

    df = carica_dati_esistenti()

    if df.empty:
        st.info("ℹ️ Nessun dato disponibile per il confronto. Inserisci prima i dati di almeno un comune.")
    elif len(df) < 2:
        st.info("ℹ️ Servono almeno 2 comuni per il confronto. Inserisci più dati.")
    else:
        st.subheader("Seleziona Comuni da Confrontare")

        comuni_selezionati = st.multiselect(
            "Scegli i comuni:",
            options=df["Comune"].unique().tolist(),
            default=df["Comune"].unique().tolist()[:2] if len(df) >= 2 else []
        )

        if len(comuni_selezionati) >= 2:
            df_confronto = df[df["Comune"].isin(comuni_selezionati)]

            # Seleziona categoria indicatore da confrontare
            st.subheader("Seleziona Categoria Indicatore")
            categoria = st.selectbox(
                "Scegli categoria:",
                options=["Governo", "Operativi", "Supporto"]
            )

            # Ottieni indicatori per categoria selezionata
            if categoria == "Governo":
                codici_indicatori = list(INDICATORI_GOVERNO.keys())
                nomi_indicatori = INDICATORI_GOVERNO
            elif categoria == "Operativi":
                codici_indicatori = list(INDICATORI_OPERATIVI.keys())
                nomi_indicatori = INDICATORI_OPERATIVI
            else:
                codici_indicatori = list(INDICATORI_SUPPORTO.keys())
                nomi_indicatori = INDICATORI_SUPPORTO

            # Visualizza tabella confronto
            st.subheader(f"Confronto Indicatori {categoria}")

            # Prepara dati confronto
            dati_confronto = df_confronto[["Comune"] + codici_indicatori].set_index("Comune").T
            dati_confronto.index = [f"{codice}: {nomi_indicatori[codice]}" for codice in codici_indicatori]

            st.dataframe(dati_confronto, use_container_width=True)

            # Grafico a barre per confronto indicatore selezionato
            st.subheader("Confronto Visuale")
            indicatore_selezionato = st.selectbox(
                "Seleziona un indicatore da visualizzare:",
                options=codici_indicatori,
                format_func=lambda x: f"{x}: {nomi_indicatori[x]}"
            )

            dati_grafico = df_confronto[["Comune", indicatore_selezionato]].set_index("Comune")
            st.bar_chart(dati_grafico)
        else:
            st.warning("⚠️ Seleziona almeno 2 comuni da confrontare.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8em;'>
    <p>Basato su UNI/PdR 5:2013 - Indicatori di Prestazione per Amministrazioni Locali Italiane</p>
    <p>© 2024 Dashboard Prestazioni Comunali</p>
</div>
""", unsafe_allow_html=True)
