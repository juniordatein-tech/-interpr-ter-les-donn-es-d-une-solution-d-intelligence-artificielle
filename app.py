import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib


# =========================
# Données intégrées
# =========================
leads = pd.DataFrame({
    "lead_id": [201,202,203,204,205,206,207,208,209,210],
    "channel": ["Emailing","Google Ads","LinkedIn Ads","Emailing","Google Ads",
                "LinkedIn Ads","Emailing","Google Ads","LinkedIn Ads","Emailing"],
    "device": ["Desktop","Mobile","Desktop","Mobile","Tablet",
               "Desktop","Mobile","Desktop","Mobile","Desktop"]
})

crm = pd.DataFrame({
    "lead_id": [201,202,203,204,205,206,207,208,209,210],
    "status": ["MQL","SQL","Client","MQL","SQL",
               "Client","MQL","SQL","Client","MQL"]
})

campaign = pd.DataFrame([
    {"channel":"Emailing","cost":1500,"impressions":60000,"clicks":1800,"conversions":150},
    {"channel":"Google Ads","cost":4200,"impressions":120000,"clicks":3200,"conversions":260},
    {"channel":"LinkedIn Ads","cost":3800,"impressions":50000,"clicks":1100,"conversions":95}
])

# =========================
# KPI
# =========================
campaign["CTR"] = campaign["clicks"] / campaign["impressions"]
campaign["conversion_rate"] = campaign["conversions"] / campaign["clicks"]
campaign["CPL"] = campaign["cost"] / campaign["conversions"]

total_leads = len(leads)
avg_cpl = campaign["CPL"].mean()
avg_ctr = campaign["CTR"].mean()
avg_conv = campaign["conversion_rate"].mean()
client_rate = (crm["status"] == "Client").mean()

# =========================
# Dashboard
# =========================
st.title("📊 Dashboard Marketing & Leads – Octobre 2025")

# KPI
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Leads", total_leads)
col2.metric("CPL moyen (€)", round(avg_cpl,2))
col3.metric("CTR moyen", f"{avg_ctr:.2%}")
col4.metric("Taux conversion", f"{avg_conv:.2%}")
col5.metric("% Clients", f"{client_rate:.2%}")

st.divider()

# =========================
# Visualisations
# =========================

# 1. Leads par canal
st.subheader("Répartition des leads par canal")
leads["channel"].value_counts().plot(kind="bar")
st.pyplot(plt.gcf())
plt.clf()

# 2. CPL par canal
st.subheader("Rentabilité par canal (CPL)")
campaign.set_index("channel")["CPL"].plot(kind="bar")
st.pyplot(plt.gcf())
plt.clf()

# 3. Tunnel CRM
st.subheader("Tunnel de conversion CRM")
crm["status"].value_counts().plot(kind="bar")
st.pyplot(plt.gcf())
plt.clf()

# 4. Canal × Statut
st.subheader("Qualification des leads par canal")
merged = pd.merge(leads, crm, on="lead_id")
pivot = pd.crosstab(merged["channel"], merged["status"], normalize="index")
sns.heatmap(pivot, annot=True, cmap="Blues")
st.pyplot(plt.gcf())
plt.clf()

# 5. Device × Clients
st.subheader("Conversion Client par device")
pivot_device = pd.crosstab(merged["device"], merged["status"], normalize="index")
pivot_device["Client"].plot(kind="bar")
st.pyplot(plt.gcf())
plt.clf()
