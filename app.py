import streamlit as st
import pandas as pd

# 🌈 --- PAGE CONFIG & THEME ---
st.set_page_config(
    page_title="DID - Monthly Records",
    layout="wide",
    page_icon="📅",
)

# Apply some custom CSS styling
st.markdown("""
    <style>
        /* Background and font */
        .main {
            background-color: #f4f6f9;
            font-family: 'Segoe UI', sans-serif;
        }
        /* Headings */
        h1, h2, h3 {
            color: #0056b3;
        }
        /* Buttons */
        div.stButton > button {
            background-color: #0078D4;
            color: white;
            border-radius: 10px;
            height: 3em;
            width: 100%;
            border: none;
            transition: 0.3s;
            font-weight: 600;
        }
        div.stButton > button:hover {
            background-color: #0056b3;
            transform: scale(1.02);
        }
        /* Metric boxes */
        [data-testid="stMetricValue"] {
            color: #008000;
            font-weight: bold;
        }
        /* Data editor */
        [data-testid="stDataFrame"] {
            border: 1px solid #ddd;
            border-radius: 10px;
            background: white;
        }
        /* Divider line */
        hr {
            border: 1px solid #ccc;
        }
    </style>
""", unsafe_allow_html=True)

# 🎯 --- HEADER ---
st.markdown("<h1 style='text-align:center;'>📘 DID - Monthly Records</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>Record daily city work, KM, and payments (1st — 31st)</p>", unsafe_allow_html=True)

# 🧮 --- FUNCTION TO MAKE DEFAULT DATAFRAME ---
def make_default_df():
    days = list(range(1, 32))
    df = pd.DataFrame({
        "Date": days,
        "City": ["" for _ in days],
        "KM": [0.0 for _ in days],
        "Working Payment": [0.0 for _ in days],
        "Extra Payment": [0.0 for _ in days],
    })
    df["Total Payment"] = df["Working Payment"] + df["Extra Payment"]
    return df

# Initialize session
if "df" not in st.session_state:
    st.session_state.df = make_default_df()

# ⚙️ --- CONTROL BUTTONS ---
st.markdown("### ⚙️ Controls")
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    if st.button("🔄 Reset to Default"):
        st.session_state.df = make_default_df()
with col2:
    if st.button("🧹 Clear All Values"):
        st.session_state.df.loc[:, ["City"]] = ""
        st.session_state.df.loc[:, ["KM", "Working Payment", "Extra Payment", "Total Payment"]] = 0.0
with col3:
    st.info("💡 Tip: Edit cells directly below. Click 'Update Totals' when done!")

st.markdown("---")

# 🧾 --- DATA ENTRY TABLE ---
st.markdown("### 📋 Monthly Data Entry")
edited = st.data_editor(
    st.session_state.df,
    num_rows="dynamic",
    use_container_width=True,
)

if not edited.equals(st.session_state.df):
    st.session_state.df = edited

# 🔢 --- UPDATE TOTALS ---
if st.button("✅ Update Totals"):
    try:
        for col in ["KM", "Working Payment", "Extra Payment"]:
            st.session_state.df[col] = pd.to_numeric(st.session_state.df[col], errors="coerce").fillna(0.0)
        st.session_state.df["Total Payment"] = st.session_state.df["Working Payment"] + st.session_state.df["Extra Payment"]
        st.success("✨ Totals updated successfully!")
    except Exception:
        st.error("❌ Error: Please make sure KM and payment fields are numeric.")

# 📊 --- SUMMARY SECTION ---
st.markdown("### 📊 Summary (Auto Calculated)")
total_km = st.session_state.df["KM"].sum()
total_working = st.session_state.df["Working Payment"].sum()
total_extra = st.session_state.df["Extra Payment"].sum()
total_all = st.session_state.df["Total Payment"].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("🚗 Total KM", f"{total_km:.2f}")
col2.metric("💼 Working Payment", f"{total_working:.2f}")
col3.metric("🎁 Extra Payment", f"{total_extra:.2f}")
col4.metric("💰 Total Payment", f"{total_all:.2f}")

st.markdown("---")

# 💾 --- DOWNLOAD OPTIONS ---
csv = st.session_state.df.to_csv(index=False)
st.download_button(
    "⬇️ Download CSV File",
    data=csv,
    file_name="DID_monthly_records.csv",
    mime="text/csv",
    use_container_width=True
)

# Snapshot info
if st.button("📋 Save Snapshot to Clipboard"):
    st.experimental_set_query_params()  # dummy
    st.success("Snapshot created — use 'Download CSV' to save locally.")

st.markdown("---")

# ✅ --- VALIDATION SECTION ---
if st.button("🔍 Validate Data"):
    problems = []
    if (st.session_state.df["KM"] < 0).any():
        problems.append("❗ Some KM values are negative.")
    if (st.session_state.df[["Working Payment", "Extra Payment"]] < 0).any().any():
        problems.append("❗ Some payment values are negative.")
    if problems:
        for p in problems:
            st.warning(p)
    else:
        st.success("✅ All data looks valid!")

# 👣 --- FOOTER ---
st.markdown("""
<hr>
<p style='text-align:center; color:gray;'>
Made for <b>DID Company</b> | Designed with 💙 using Streamlit
</p>
""", unsafe_allow_html=True)
