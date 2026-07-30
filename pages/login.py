import streamlit as st

from utils.auth import authenticate_user, create_user, init_auth_state


init_auth_state()

st.markdown('<div class="login-page-v3"></div>', unsafe_allow_html=True)

left_col, right_col = st.columns([1.08, 0.92], gap="large")

with left_col:
    st.markdown(
        """
        <div class="login-visual-card">
            <div class="login-brand-lock">
                <div class="brand-shield">CS</div>
                <div>
                    <div class="brand-title">Cyber<span>Shield</span></div>
                    <div class="brand-subtitle">FORENSICS</div>
                </div>
            </div>
            <p class="login-lead">
                AI-powered cyber investigation, threat detection, evidence reporting,
                and forensic intelligence in one secure command center.
            </p>
            <div class="login-feature-cloud">
                <span>Threat Detection</span>
                <span>AI Analysis</span>
                <span>Evidence Reporting</span>
                <span>Network Monitoring</span>
            </div>
            <div class="login-compliance-row">
                <span>SOC 2 Ready</span>
                <span>ISO 27001 Aligned</span>
                <span>24/7 Monitoring</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right_col:
    st.markdown(
        """
        <div class="login-panel-heading">
            <h1>Welcome Back</h1>
            <p>Secure access to your CyberShield Forensics dashboard.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    login_tab, register_tab = st.tabs(["Secure Login", "Create Account"])

    with login_tab:
        with st.form("login_form"):
            username = st.text_input("Username", key="login_username", placeholder="Enter username")
            password = st.text_input("Password", type="password", key="login_password", placeholder="Enter password")
            remember = st.checkbox("Remember me", value=True)
            submitted = st.form_submit_button("Secure Login", use_container_width=True)

        if submitted:
            ok, user = authenticate_user(username, password)
            if ok:
                st.session_state["logged_in"] = True
                st.session_state["user"] = user
                st.session_state["remember_me"] = remember
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid username or password")

    with register_tab:
        with st.form("register_form"):
            full_name = st.text_input("Full Name", placeholder="Enter full name")
            new_username = st.text_input("New Username", placeholder="Create username")
            new_password = st.text_input("New Password", type="password", placeholder="Minimum 6 characters")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
            created = st.form_submit_button("Create Account", use_container_width=True)

        if created:
            if new_password != confirm_password:
                st.error("Passwords do not match.")
            else:
                ok, message = create_user(new_username, new_password, full_name)
                if ok:
                    st.success(message)
                else:
                    st.error(message)

    st.markdown(
        """
        <div class="login-security-row">
            <div><strong>Encryption</strong><span>Protected access</span></div>
            <div><strong>AI Monitor</strong><span>Threat-aware</span></div>
            <div><strong>Auth</strong><span>Local secure login</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
