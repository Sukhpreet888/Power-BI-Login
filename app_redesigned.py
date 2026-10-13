import streamlit as st
from supabase import create_client

st.set_page_config(
    page_title="Power BI Portal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Supabase project settings.
# Use only the publishable/anon key here — never use a service_role/secret key.
SUPABASE_URL = "https://hwfunijrvzhpsxfbjfvi.supabase.co"
SUPABASE_KEY = "sb_publishable_nOEJ-PLfLkh3JnHXDYyuKA_bz6uRIJz"


def inject_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {
            --portal-blue: #3159ed;
            --portal-navy: #192d53;
            --portal-text: #102344;
            --portal-muted: #71809a;
        }

        html, body, [class*="css"], [data-testid="stAppViewContainer"] {
            font-family: 'Inter', sans-serif;
        }

        [data-testid="stAppViewContainer"] {
            background: #f3f6fb;
        }
        [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu, footer {
            visibility: hidden;
            height: 0;
        }
        [data-testid="stMainBlockContainer"] {
            max-width: 100% !important;
            padding: 4.5vh 2.2vw 3vh !important;
        }
        [data-testid="stHorizontalBlock"] {
            gap: 0 !important;
            align-items: stretch !important;
        }
        [data-testid="column"] {
            padding: 0 !important;
            min-width: 0 !important;
        }

        /* Left panel */
        [data-testid="column"]:first-child > div {
            background: #ffffff;
            border: 1px solid #dce4f1;
            border-right: 0;
            border-radius: 26px 0 0 26px;
            min-height: 86vh;
            padding: clamp(34px, 5.5vw, 82px) clamp(30px, 5.7vw, 76px) 44px;
            box-sizing: border-box;
        }

        /* Right panel */
        [data-testid="column"]:nth-child(2) > div {
            min-height: 86vh;
            box-sizing: border-box;
            border: 1px solid #dce4f1;
            border-left: 0;
            border-radius: 0 26px 26px 0;
            overflow: hidden;
            padding: 0 !important;
            background: linear-gradient(145deg, #192b4e 0%, #203f79 66%, #3159ed 100%);
            position: relative;
        }

        .eyebrow {
            color: #3159ed;
            text-transform: uppercase;
            letter-spacing: 3px;
            font-size: 12px;
            line-height: 1.6;
            font-weight: 700;
            margin: 0 0 23px 0;
        }
        .welcome-title {
            color: #102344;
            font-size: clamp(32px, 3vw, 40px);
            line-height: 1.2;
            font-weight: 700;
            letter-spacing: -1.6px;
            margin: 0 0 30px 0;
        }
        .welcome-subtitle {
            color: #71809a;
            font-size: 16px;
            line-height: 1.8;
            margin: 0 0 54px 0;
        }

        [data-testid="stTextInput"] label {
            color: #14233d !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            margin-bottom: 10px !important;
        }
        [data-testid="stTextInput"] input {
            min-height: 54px !important;
            height: 54px !important;
            border: 1px solid #d6dfef !important;
            border-radius: 12px !important;
            background: #fff !important;
            color: #14233d !important;
            padding: 0 16px !important;
            font-size: 15px !important;
            box-shadow: none !important;
        }
        [data-testid="stTextInput"] input:focus {
            border-color: #526fff !important;
            box-shadow: 0 0 0 4px rgba(49, 89, 237, .13) !important;
        }
        [data-testid="stTextInput"] input::placeholder {
            color: #8290a7 !important;
        }
        [data-testid="stForm"] {
            border: 0 !important;
            padding: 0 !important;
        }
        [data-testid="stFormSubmitButton"] button {
            width: 100%;
            min-height: 56px;
            margin-top: 12px;
            border: 0 !important;
            border-radius: 12px !important;
            background: #3159ed !important;
            color: white !important;
            font-size: 16px !important;
            font-weight: 700 !important;
            box-shadow: 0 9px 18px rgba(49, 89, 237, .18);
            transition: transform .15s ease, background .15s ease;
        }
        [data-testid="stFormSubmitButton"] button:hover {
            background: #244be0 !important;
            transform: translateY(-1px);
        }
        [data-testid="stButton"] button {
            border-radius: 10px;
        }
        .admin-note {
            color: #8996ad;
            font-size: 13px;
            line-height: 1.7;
            margin-top: 32px;
        }
        .right-art {
            min-height: calc(86vh - 2px);
            width: 100%;
            position: relative;
            overflow: hidden;
            box-sizing: border-box;
            background:
                radial-gradient(circle at 72% 31%, rgba(72, 105, 177, .43) 0, rgba(72, 105, 177, .34) 10%, transparent 11%),
                linear-gradient(145deg, #192b4e 0%, #203f79 67%, #3159ed 100%);
        }
        .orbit {
            position: absolute;
            width: 500px;
            height: 500px;
            right: -160px;
            top: -125px;
            border: 1px solid rgba(191, 211, 255, .18);
            border-radius: 50%;
            box-shadow: 0 0 0 42px rgba(191, 211, 255, .035),
                        0 0 0 92px rgba(191, 211, 255, .03);
        }
        .orbit:before {
            content: "";
            position: absolute;
            width: 270px;
            height: 270px;
            border-radius: 50%;
            right: 45px;
            top: 125px;
            background: radial-gradient(circle, rgba(74, 108, 184, .35), rgba(74, 108, 184, .04) 70%, transparent 72%);
        }
        .right-copy {
            position: absolute;
            left: clamp(38px, 5vw, 68px);
            right: 38px;
            bottom: clamp(48px, 9vw, 88px);
            color: #fff;
            z-index: 1;
        }
        .right-eyebrow {
            color: #b9ccff;
            text-transform: uppercase;
            letter-spacing: 2.5px;
            font-size: 12px;
            font-weight: 700;
            margin-bottom: 22px;
        }
        .right-title {
            max-width: 440px;
            font-size: clamp(32px, 3.2vw, 43px);
            line-height: 1.23;
            letter-spacing: -1.5px;
            font-weight: 700;
            margin: 0 0 20px 0;
        }
        .right-description {
            max-width: 430px;
            color: #e0e8ff;
            font-size: 16px;
            line-height: 2;
            margin: 0;
        }
        .password-row [data-testid="stTextInput"] {
            margin-bottom: 0;
        }
        .password-row [data-testid="column"]:last-child {
            display: flex;
            align-items: end;
        }
        .password-row [data-testid="column"]:last-child button {
            min-height: 54px;
            margin-bottom: 0;
            color: #3159ed;
            border: 1px solid #d6dfef;
            background: #fff;
            font-weight: 600;
        }

        @media (max-width: 900px) {
            [data-testid="stMainBlockContainer"] {
                padding: 20px 14px !important;
            }
            [data-testid="column"]:first-child > div {
                border: 1px solid #dce4f1;
                border-radius: 22px;
                min-height: auto;
                padding: 36px 28px;
            }
            [data-testid="column"]:nth-child(2) {
                display: none;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


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
            "Project URL and SUPABASE_KEY to your publishable/anon key."
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
    left, right = st.columns([1, 1], gap="small")

    with left:
        st.markdown(
            """
            <div class="eyebrow">Secure reporting workspace</div>
            <h1 class="welcome-title">Welcome back</h1>
            <p class="welcome-subtitle">Sign in to view the dashboards assigned to you.</p>
            """,
            unsafe_allow_html=True,
        )

        if "show_password" not in st.session_state:
            st.session_state.show_password = False

        email = st.text_input(
            "Work email",
            placeholder="you@company.com",
            autocomplete="username",
            key="login_email",
        )

        password_col, toggle_col = st.columns([5, 1], gap="small")
        with password_col:
            password = st.text_input(
                "Password",
                type="default" if st.session_state.show_password else "password",
                autocomplete="current-password",
                key="login_password",
            )
        with toggle_col:
            st.markdown("<div style='height:31px'></div>", unsafe_allow_html=True)
            if st.button(
                "Hide" if st.session_state.show_password else "Show",
                key="toggle_password",
                use_container_width=True,
            ):
                st.session_state.show_password = not st.session_state.show_password
                st.rerun()

        submitted = st.button(
            "Sign in                         →",
            key="sign_in_button",
            use_container_width=True,
            type="primary",
        )

        if submitted:
            st.session_state.pop("login_error_detail", None)
            if sign_in(email, password):
                st.rerun()
            else:
                st.error(
                    "Sign-in failed. Check your email and password, and confirm "
                    "that your Supabase user has a profile and a report URL assigned to its role."
                )
                detail = st.session_state.get("login_error_detail")
                if detail:
                    with st.expander("Technical details"):
                        st.code(detail)

        st.markdown(
            '<div class="admin-note">Access is managed by your portal administrator.</div>',
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            """
            <div class="right-art">
              <div class="orbit"></div>
              <div class="right-copy">
                <div class="right-eyebrow">Your data. Your access.</div>
                <h2 class="right-title">Clarity for every<br>team.</h2>
                <p class="right-description">
                  One secure place for the reports and insights<br>
                  you are authorized to see.
                </p>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def dashboard_view():
    st.markdown(
        """
        <div class="eyebrow">Secure reporting workspace</div>
        <h1 class="welcome-title">Your dashboard</h1>
        """,
        unsafe_allow_html=True,
    )
    st.write(
        f"Signed in as **{st.session_state.email}** "
        f"({st.session_state.role})"
    )
    st.link_button(
        "Open Power BI report  →",
        st.session_state.report_url,
        type="primary",
    )
    st.button("Log out", on_click=sign_out)


inject_styles()

if "role" in st.session_state and "report_url" in st.session_state:
    dashboard_view()
else:
    login_view()
