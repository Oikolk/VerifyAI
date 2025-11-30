import streamlit as st

def init_session_state():
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'cache' not in st.session_state:
        st.session_state.cache = {}

def check_cache(claim):
    """
    Checks if the claim exists in the session cache.
    Simple exact match for now. In a real app, we might use semantic similarity.
    """
    return st.session_state.cache.get(claim.strip().lower())

def update_cache(claim, result):
    """
    Updates the session cache with the new result.
    """
    st.session_state.cache[claim.strip().lower()] = result

def add_to_history(claim, result):
    """
    Adds the verification result to the history.
    """
    st.session_state.history.insert(0, {"claim": claim, "result": result})
