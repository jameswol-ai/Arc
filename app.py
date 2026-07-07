import streamlit as st

st.set_page_config(page_title="Arc Studio", page_icon="📐", layout="wide")

st.title("Arc Operating System")
st.markdown("### Integrated Intelligence Dashboard")

# High-level summary of your two engines
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sai Engine (Architectural)")
    st.write("Structural analysis, Eurocode compliance, and building design.")
    if st.button("Open Sai Lab"):
        st.switch_page("pages/01_Sai_Engine.py")

with col2:
    st.subheader("Random Engine (Forex)")
    st.write("Regional financial tracking, hedging, and BoQ indices.")
    if st.button("Open Random Engine"):
        st.switch_page("pages/02_Random_FX.py")
