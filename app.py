import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Power BI Portal", page_icon="📊", layout="centered")


def get_client():
    # One client PER browser session. Do not use st.cache_resource here:
    # it would share one logged-in session across every visitor.
    if "sb" not in st.session_state:
        st.session_state.sb = create_client(
            st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"]
        )
    return st.session_state.sb


def sign_in(email: str, password: str) -> bool:
    sb = get_client()
    try:
        res = sb.auth.sign_in_with_password({"email": email.strip().lower(), "password": password})
        role = (
            sb.table("profiles").select("role").eq("id", res.user.id).single().execute().data["role"]
        )
        url = sb.table("reports").select("url").eq("role", role).single().execute().data["url"]
    except Exception:
        sb.auth.sign_out()
        return False
    st.session_state.update(email=res.user.email, role=role, report_url=url)
    return True


def sign_out():
    try:
        get_client().auth.sign_out()
    finally:
        st.session_state.clear()


def login_view():
    st.markdown("<h1 style='text-align:center'>📊 Power BI Portal</h1>", unsafe_allow_html=True)
    st.caption("Sign in to access your dashboard")
    with st.form("login"):
        email = st.text_input("Email", autocomplete="username")
        password = st.text_input("Password", type="password", autocomplete="current-password")
        submitted = st.form_submit_button("Sign In", use_container_width=True, type="primary")
    if submitted:
        if sign_in(email, password):
            st.rerun()
        else:
            st.error("Invalid email or password.")
    st.caption("Authorized access only")


def dashboard_view():
    st.title("📊 Your Dashboard")
    st.write(f"Signed in as **{st.session_state.email}** ({st.session_state.role})")
    st.link_button("Open Power BI report", st.session_state.report_url, type="primary")
    st.button("Log out", on_click=sign_out)


if "role" in st.session_state:
    dashboard_view()
else:
    login_view()
