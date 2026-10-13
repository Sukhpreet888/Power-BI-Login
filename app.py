import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Power BI Portal", page_icon="📊", layout="centered")

# Get these from Supabase Dashboard > Project Settings > API Keys.
# Use the Project URL and a publishable/anon key only.
# Do NOT use a service_role or sb_secret key in this app.
# Verify the key below is the publishable/anon key for this same project.
SUPABASE_URL = "https://hwfunijrvzhpsxfbjfvi.supabase.co"
SUPABASE_KEY = "sb_publishable_nOEJ-PLfLkh3JnHXDYyuKA_bz6uRIJz"


def get_client():
    """Create one Supabase client per Streamlit browser session."""
    if (
        not SUPABASE_URL.startswith("https://")
        or "YOUR-PROJECT-REF" in SUPABASE_URL
        or not SUPABASE_KEY
        or "YOUR-" in SUPABASE_KEY
    ):
        st.error(
            "Supabase configuration is missing. Set SUPABASE_URL to your "
            "Project URL (https://<project-ref>.supabase.co) and SUPABASE_KEY "
            "to your publishable/anon key from Supabase Project Settings > API Keys."
        )
        st.stop()

    if "sb" not in st.session_state:
        st.session_state.sb = create_client(SUPABASE_URL, SUPABASE_KEY)

    return st.session_state.sb


def sign_in(email: str, password: str) -> bool:
    sb = get_client()
    try:
        response = sb.auth.sign_in_with_password(
            {"email": email.strip().lower(), "password": password}
        )
        if not response.user:
            return False

        profile_response = (
            sb.table("profiles")
            .select("role")
            .eq("id", response.user.id)
            .single()
            .execute()
        )
        role = profile_response.data["role"]

        report_response = (
            sb.table("reports")
            .select("url")
            .eq("role", role)
            .single()
            .execute()
        )
        report_url = report_response.data["url"]

        st.session_state.update(
            email=response.user.email,
            role=role,
            report_url=report_url,
        )
        return True

    except Exception as exc:
        try:
            sb.auth.sign_out()
        except Exception:
            pass
        # Keep the app usable while providing a useful error for setup issues.
        st.session_state["login_error_detail"] = str(exc)
        return False


def sign_out():
    try:
        if "sb" in st.session_state:
            st.session_state.sb.auth.sign_out()
    except Exception:
        pass
    finally:
        st.session_state.clear()


def login_view():
    st.markdown(
        "<h1 style='text-align:center'>📊 Power BI Portal</h1>",
        unsafe_allow_html=True,
    )
    st.caption("Sign in to access your dashboard")

    with st.form("login"):
        email = st.text_input("Email", autocomplete="username")
        password = st.text_input(
            "Password", type="password", autocomplete="current-password"
        )
        submitted = st.form_submit_button(
            "Sign In", use_container_width=True, type="primary"
        )

    if submitted:
        st.session_state.pop("login_error_detail", None)
        if sign_in(email, password):
            st.rerun()
        else:
            st.error(
                "Sign-in failed. Verify your email and password, and check that "
                "the Supabase user has a profile and a report URL for its role."
            )
            detail = st.session_state.get("login_error_detail")
            if detail:
                with st.expander("Technical details"):
                    st.code(detail)

    st.caption("Authorized access only")


def dashboard_view():
    st.title("📊 Your Dashboard")
    st.write(
        f"Signed in as **{st.session_state.email}** "
        f"({st.session_state.role})"
    )
    st.link_button(
        "Open Power BI report",
        st.session_state.report_url,
        type="primary",
    )
    st.button("Log out", on_click=sign_out)


if "role" in st.session_state and "report_url" in st.session_state:
    dashboard_view()
else:
    login_view()
