
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="MEDORA | Hospital Management System",
    page_icon="🏥",
    layout="wide"
)

PASSWORD = "demo123"

ACCOUNTS = {
    "Patient": "P1001",
    "Doctor": "DOC001",
    "Lab Technician": "LAB001",
    "Pharmacist": "PHR001",
    "Administration": "ADM001",
    "Hospital Head / Chairperson": "HEAD001",
    "Board Member": "BOARD001"
}

PROFILES = {
    "Patient": ("Arjun Kumar", "Patient"),
    "Doctor": ("Dr. Mehta", "Cardiologist"),
    "Lab Technician": ("Ananya Rao", "Laboratory Technician"),
    "Pharmacist": ("Rahul Verma", "Pharmacist"),
    "Administration": ("Priya Sharma", "Hospital Administrator"),
    "Hospital Head / Chairperson": ("Dr. Reddy", "Hospital Director"),
    "Board Member": ("Vikram Rao", "Board Member")
}


def initial_data():
    return {
        "patients": pd.DataFrame([
            ["P1001", "Arjun Kumar", 34, "Male", "O+", "9876543210", "Cardiology"],
            ["P1002", "Sneha Reddy", 28, "Female", "B+", "9876543211", "General Medicine"],
            ["P1003", "Ravi Teja", 46, "Male", "A+", "9876543212", "Orthopedics"],
            ["P1004", "Anjali Sharma", 52, "Female", "AB+", "9876543213", "Neurology"],
            ["P1005", "Kiran Rao", 39, "Male", "O-", "9876543214", "General Medicine"]
        ], columns=[
            "patient_id", "name", "age", "gender",
            "blood_group", "phone", "department"
        ]),

        "visits": pd.DataFrame([
            ["V1001", "P1001", "Dr. Mehta", date(2026, 11, 2),
             "Chest discomfort", "Under observation", "Open"],
            ["V1002", "P1002", "Dr. Mehta", date(2026, 11, 3),
             "Routine check-up", "Stable", "Completed"],
            ["V1003", "P1003", "Dr. Rao", date(2026, 11, 4),
             "Knee pain", "Review required", "Open"]
        ], columns=[
            "visit_id", "patient_id", "doctor", "visit_date",
            "reason", "diagnosis", "status"
        ]),

        "labs": pd.DataFrame([
            ["T1001", "P1001", "Complete Blood Count",
             date(2026, 11, 2), "Pending", "Pending"],
            ["T1002", "P1001", "Lipid Profile",
             date(2026, 11, 2), "Normal", "Completed"],
            ["T1003", "P1002", "Blood Glucose",
             date(2026, 11, 3), "98 mg/dL", "Completed"],
            ["T1004", "P1003", "Vitamin D",
             date(2026, 11, 4), "Pending", "In Progress"]
        ], columns=[
            "test_id", "patient_id", "test_name",
            "test_date", "result", "status"
        ]),

        "bills": pd.DataFrame([
            ["B1001", "P1001", date(2026, 11, 2), 2500.0, "Unpaid"],
            ["B1002", "P1002", date(2026, 11, 3), 1200.0, "Paid"],
            ["B1003", "P1003", date(2026, 11, 4), 1800.0, "Unpaid"],
            ["B1004", "P1004", date(2026, 11, 5), 3200.0, "Paid"]
        ], columns=[
            "bill_id", "patient_id", "bill_date", "amount", "status"
        ]),

        "medicines": pd.DataFrame([
            ["M1001", "Paracetamol 500 mg", 120, 30, 2.5],
            ["M1002", "Amoxicillin 250 mg", 45, 20, 5.0],
            ["M1003", "Cetirizine 10 mg", 18, 25, 3.0],
            ["M1004", "Omeprazole 20 mg", 60, 20, 4.5]
        ], columns=[
            "medicine_id", "medicine_name", "stock",
            "reorder_level", "unit_price"
        ]),

        "prescriptions": pd.DataFrame([
            ["RX1001", "P1001", "Dr. Mehta",
             "Paracetamol 500 mg", "As directed", date(2026, 11, 2)],
            ["RX1002", "P1002", "Dr. Mehta",
             "Cetirizine 10 mg", "As directed", date(2026, 11, 3)]
        ], columns=[
            "prescription_id", "patient_id", "doctor",
            "medicine", "dosage", "prescription_date"
        ])
    }


def initialize():
    defaults = {
        "logged_in": False,
        "role": None,
        "user_id": None,
        "data": initial_data()
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def new_id(df, prefix, column):
    nums = []

    for item in df[column].astype(str).tolist() if not df.empty else []:
        digits = "".join(c for c in item if c.isdigit())
        if digits:
            nums.append(int(digits))

    return f"{prefix}{max(nums, default=1000) + 1}"


def table(df, empty_text="No records found."):
    if df.empty:
        st.info(empty_text)
    else:
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


def pname(pid):
    df = st.session_state.data["patients"]
    found = df.loc[df.patient_id == pid, "name"]

    return found.iloc[0] if not found.empty else "Unknown patient"


# ---------------- MEDORA VISUAL DESIGN ----------------

def apply_medora_styles():
    st.markdown("""
    <style>
    :root {
        --medora-navy: #123b63;
        --medora-blue: #2878b9;
        --medora-teal: #36a995;
        --medora-bg: #f4f8fd;
    }

    .stApp {
        background: var(--medora-bg);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #123b63, #0d3154);
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    [data-testid="stSidebar"] [data-testid="stButton"] button {
        background: rgba(255,255,255,.12);
        border: 1px solid rgba(255,255,255,.16);
        border-radius: 12px;
    }

    h1, h2, h3 {
        color: #153b63;
    }

    [data-testid="stMetric"] {
        background: white;
        padding: 16px;
        border-radius: 16px;
        border: 1px solid #e2ebf5;
        box-shadow: 0 3px 14px rgba(25,70,110,.05);
    }

    [data-testid="stForm"],
    [data-testid="stDataFrame"] {
        background: white;
        border-radius: 16px;
        padding: 12px;
        border: 1px solid #e2ebf5;
    }

    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2.5rem;
    }

    div.stButton > button {
        border-radius: 12px;
        border: 1px solid #d7e5f3;
        font-weight: 600;
        min-height: 42px;
    }

    div.stButton > button[kind="primary"] {
        background: #164b78;
        border-color: #164b78;
    }

    .medora-hero {
        background: linear-gradient(110deg, #dceeff, #eff7ff 58%, #d7edff);
        border: 1px solid #d4e7fb;
        border-radius: 24px;
        padding: 28px 30px;
        margin: 4px 0 20px 0;
        color: #123b63;
    }

    .medora-hero .eyebrow {
        color: #477294;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1.5px;
    }

    .medora-hero h1 {
        margin: 5px 0;
        font-size: 34px;
        color: #123b63;
    }

    .medora-hero p {
        margin: 0;
        font-size: 16px;
        color: #456783;
    }

    .medora-card {
        background: white;
        border: 1px solid #e1eaf4;
        border-radius: 18px;
        padding: 18px;
        min-height: 118px;
        box-shadow: 0 4px 16px rgba(25,70,110,.045);
        margin-bottom: 12px;
    }

    .medora-card h4 {
        color: #163d63;
        margin: 7px 0 4px 0;
        font-size: 17px;
    }

    .medora-card p {
        color: #61778d;
        margin: 0;
        font-size: 13px;
    }

    .medora-icon {
        font-size: 25px;
    }

    .medora-appointment {
        background: linear-gradient(120deg, white, #f0f7ff);
        border: 1px solid #d8e8f8;
        border-radius: 18px;
        padding: 19px;
        min-height: 130px;
        margin-bottom: 14px;
    }

    .medora-status {
        background: linear-gradient(120deg, #e2f5ed, #f1fbf6);
        border: 1px solid #d2eee1;
        border-radius: 18px;
        padding: 19px;
        min-height: 130px;
        margin-bottom: 14px;
    }

    .medora-journey {
        border-radius: 16px;
        padding: 16px;
        min-height: 145px;
        margin-bottom: 10px;
        border: 1px solid rgba(30,70,110,.06);
    }

    .medora-journey h4 {
        margin: 8px 0 5px 0;
        font-size: 15px;
        color: #183b5b;
    }

    .medora-journey p {
        margin: 0;
        font-size: 12px;
        color: #536b82;
    }

    .medora-section-title {
        color: #153b63;
        font-size: 21px;
        font-weight: 750;
        margin: 16px 0 10px 0;
    }

    .medora-assistant {
        background: linear-gradient(135deg, #eaf4ff, #f5f9ff);
        border: 1px solid #d7e8fb;
        border-radius: 18px;
        padding: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- LOGIN PAGE ----------------

def login_screen():
    # MEDORA premium home / login page
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: #f3f7fc;
    }
    [data-testid="stHeader"] {
        background: transparent;
    }
    .medora-hero {
        background: linear-gradient(140deg, #102b50 0%, #174d78 65%, #147d89 100%);
        padding: 48px 38px;
        border-radius: 22px;
        color: white;
        min-height: 470px;
        box-shadow: 0 14px 35px rgba(18, 47, 79, 0.14);
    }
    .medora-brand {
        font-size: 30px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 48px;
    }
    .medora-tag {
        color: #9de6e2;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .medora-heading {
        font-size: 39px;
        line-height: 1.2;
        font-weight: 750;
        margin: 15px 0;
    }
    .medora-description {
        color: #dceaf5;
        font-size: 16px;
        line-height: 1.7;
        max-width: 440px;
    }
    .medora-feature {
        margin-top: 27px;
        padding: 13px 15px;
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 12px;
        color: #f1f8ff;
        background: rgba(255,255,255,0.07);
        font-size: 14px;
    }
    .medora-login-heading {
        color: #142e4d;
        font-size: 29px;
        font-weight: 750;
        margin-top: 18px;
    }
    .medora-login-sub {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 20px;
    }
    div[data-testid="stForm"] {
        background: white;
        border: 1px solid #e1eaf3;
        border-radius: 18px;
        padding: 25px;
        box-shadow: 0 12px 32px rgba(25, 55, 85, 0.07);
    }
    div[data-testid="stForm"] button {
        background: #126b83;
        color: white;
        border: none;
        border-radius: 9px;
        min-height: 45px;
        font-weight: 650;
    }
    div[data-testid="stForm"] button:hover {
        background: #0e5269;
        color: white;
    }
    .medora-footer {
        color: #8493a5;
        text-align: center;
        font-size: 12px;
        padding: 28px 0 5px;
    }
    </style>
    """, unsafe_allow_html=True)

    left, right = st.columns([1.15, 0.85], gap="large")

    with left:
        st.markdown("""
        <div class="medora-hero">
            <div class="medora-brand">✚ MEDORA</div>
            <div class="medora-tag">Connected healthcare management</div>
            <div class="medora-heading">
                Better care.<br>Smarter management.
            </div>
            <div class="medora-description">
                One connected platform for patient care, clinical
                operations and hospital management.
            </div>
            <div class="medora-feature">✦ &nbsp; Patient-centred healthcare experience</div>
            <div class="medora-feature">✦ &nbsp; Connected clinical departments</div>
            <div class="medora-feature">✦ &nbsp; Smarter hospital operations</div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown('<div class="medora-login-heading">Welcome to MEDORA</div>',
                    unsafe_allow_html=True)
        st.markdown(
            '<div class="medora-login-sub">Sign in to access your workspace.</div>',
            unsafe_allow_html=True
        )

        with st.form("login_form"):
            role = st.selectbox("Select your role", list(ACCOUNTS))
            user_id = st.text_input("User ID", placeholder="Enter your assigned ID")
            password = st.text_input("Password", type="password",
                                     placeholder="Enter your password")

            submitted = st.form_submit_button("Sign in  →",
                                              use_container_width=True)

        if submitted:
            if (user_id.strip().upper() == ACCOUNTS[role]
                    and password == PASSWORD):
                st.session_state.logged_in = True
                st.session_state.role = role
                st.session_state.user_id = ACCOUNTS[role]
                st.rerun()
            else:
                st.error("Incorrect role, User ID, or password.")

        st.markdown("""
        <div style="color:#8493a5;font-size:12px;text-align:center;
                    margin-top:16px;">
            Secure workspace access for authorised users
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="medora-footer">
        © 2026 MEDORA Healthcare Technologies
        &nbsp; • &nbsp; Hospital Management System
    </div>
    """, unsafe_allow_html=True)

def sidebar():

    role = st.session_state.role
    display_name, designation = PROFILES[role]

    with st.sidebar:

        st.title("🏥 MEDORA")
        st.caption("Hospital Management System")

        st.divider()

        st.write(f"**Name:** {display_name}")
        st.write(f"**Role:** {role}")
        st.write(f"**ID:** {st.session_state.user_id}")

        if st.button("Logout", use_container_width=True):

            st.session_state.logged_in = False
            st.session_state.role = None
            st.session_state.user_id = None

            st.rerun()


# ---------------- PATIENT DASHBOARD ----------------

def patient_dashboard():

    d = st.session_state.data
    pid = st.session_state.user_id

    profile = d["patients"].loc[
        d["patients"].patient_id == pid
    ]

    if profile.empty:
        st.warning("No patient record is linked to this account.")
        return

    patient = profile.iloc[0]
    name = patient["name"]

    st.markdown(f"""
    <div class="medora-hero">
        <div class="eyebrow">WELCOME TO MEDORA</div>
        <h1>Hello, {name}! 👋</h1>
        <p>Your health information, appointments and reports — all in one place.</p>
    </div>
    """, unsafe_allow_html=True)

    visits = d["visits"].loc[
        d["visits"].patient_id == pid
    ].copy()

    labs = d["labs"].loc[
        d["labs"].patient_id == pid
    ].copy()

    bills = d["bills"].loc[
        d["bills"].patient_id == pid
    ].copy()

    prescriptions = d["prescriptions"].loc[
        d["prescriptions"].patient_id == pid
    ].copy()

    upcoming = visits.loc[
        visits["visit_date"] >= date.today()
    ].sort_values("visit_date")

    # APPOINTMENT AND HEALTH RECORD CARDS

    appt_col, status_col = st.columns([1.55, 1])

    with appt_col:

        if not upcoming.empty:

            appt = upcoming.iloc[0]

            st.markdown(f"""
            <div class="medora-appointment">
                <div style="font-size:13px;color:#477294;font-weight:700;">
                    📅 YOUR NEXT APPOINTMENT
                </div>
                <div style="font-size:23px;font-weight:800;color:#153b63;margin:9px 0 4px;">
                    {appt['visit_date'].strftime('%d %B %Y')}
                </div>
                <div style="color:#526d84;">
                    {appt['doctor']} · {appt['reason'] or 'Consultation'}
                </div>
            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown("""
            <div class="medora-appointment">
                <div style="font-size:13px;color:#477294;font-weight:700;">
                    📅 YOUR NEXT APPOINTMENT
                </div>
                <div style="font-size:21px;font-weight:800;color:#153b63;margin:9px 0 4px;">
                    No appointment scheduled
                </div>
                <div style="color:#526d84;">
                    Please contact hospital administration to book a visit.
                </div>
            </div>
            """, unsafe_allow_html=True)

    with status_col:

        pending_reports = (
            int((labs["status"] != "Completed").sum())
            if not labs.empty else 0
        )

        unpaid_bills = (
            int((bills["status"] == "Unpaid").sum())
            if not bills.empty else 0
        )

        st.markdown(f"""
        <div class="medora-status">
            <div style="font-size:13px;color:#36745f;font-weight:700;">
                💚 YOUR HEALTH RECORDS
            </div>
            <div style="font-size:21px;font-weight:800;color:#205b49;margin:9px 0 4px;">
                Your records are here
            </div>
            <div style="color:#527568;">
                {len(labs)} lab test(s) · {pending_reports} awaiting completion · {unpaid_bills} unpaid bill(s)
            </div>
        </div>
        """, unsafe_allow_html=True)

    # QUICK ACCESS

    st.markdown(
        '<div class="medora-section-title">✨ Quick Access</div>',
        unsafe_allow_html=True
    )

    if "patient_section" not in st.session_state:
        st.session_state.patient_section = "Home"

    shortcuts = [
        ("📄", "My Reports", "View your test results", "Reports"),
        ("💊", "My Medicines", "Check your prescriptions", "Medicines"),
        ("🗓️", "My Appointments", "See your hospital visits", "Appointments"),
        ("🧾", "My Bills", "Review payments and bills", "Bills"),
        ("👤", "My Health Details", "View your personal details", "Health Details")
    ]

    shortcut_cols = st.columns(5)

    for col, (emoji, title, desc, section) in zip(shortcut_cols, shortcuts):

        with col:

            st.markdown(f"""
            <div class="medora-card" style="min-height:112px;">
                <div class="medora-icon">{emoji}</div>
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(
                "Open",
                key=f"patient_open_{section}",
                use_container_width=True
            ):
                st.session_state.patient_section = section
                st.rerun()

    # MY HEALTH JOURNEY - SEPARATE CARDS, NO CONNECTING LINES

    st.markdown(
        '<div class="medora-section-title">⭐ My Health Journey</div>',
        unsafe_allow_html=True
    )

    events = []

    if not visits.empty:

        row = visits.sort_values(
            "visit_date", ascending=False
        ).iloc[0]

        events.append((
            "🩺", "Appointment",
            str(row["status"]),
            row["visit_date"].strftime("%d %b %Y"),
            "#e4f5ed"
        ))

    if not labs.empty:

        row = labs.sort_values(
            "test_date", ascending=False
        ).iloc[0]

        events.append((
            "🧪", "Lab Test",
            str(row["status"]),
            row["test_date"].strftime("%d %b %Y"),
            "#e7f2ff"
        ))

        if row["status"] == "Completed":

            events.append((
                "📄", "Report Available",
                str(row["test_name"]),
                row["test_date"].strftime("%d %b %Y"),
                "#f0eaff"
            ))

    if not prescriptions.empty:

        row = prescriptions.sort_values(
            "prescription_date", ascending=False
        ).iloc[0]

        events.append((
            "💊", "Prescription Updated",
            str(row["medicine"]),
            row["prescription_date"].strftime("%d %b %Y"),
            "#fff0e4"
        ))

    if not upcoming.empty:

        row = upcoming.iloc[0]

        events.append((
            "📅", "Next Appointment",
            str(row["doctor"]),
            row["visit_date"].strftime("%d %b %Y"),
            "#e7f2ff"
        ))

    if events:

        journey_cols = st.columns(min(5, len(events)))

        for i, event in enumerate(events[:5]):

            emoji, title, detail, event_date, bg = event

            with journey_cols[i]:

                st.markdown(f"""
                <div class="medora-journey" style="background:{bg};">
                    <div style="font-size:25px;">{emoji}</div>
                    <h4>{title}</h4>
                    <p>{detail}</p>
                    <p style="margin-top:8px;font-weight:700;">
                        {event_date}
                    </p>
                </div>
                """, unsafe_allow_html=True)

    else:
        st.info("Your health activities will appear here when records are added.")

    # MEDORA ASSISTANT

    st.markdown(
        '<div class="medora-section-title">💬 MEDORA Assistant</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="medora-assistant">
        <div style="font-size:18px;font-weight:750;color:#173d63;">
            Need help understanding your health information?
        </div>
        <div style="color:#58718a;margin-top:5px;">
            You can ask about reports, appointments or prescriptions in simple language.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.caption(
        "Chatbot integration will be added as part of the next development task."
    )

    # SELECTED PATIENT SECTION

    section = st.session_state.patient_section

    if section != "Home":

        st.markdown(
            f'<div class="medora-section-title">{section}</div>',
            unsafe_allow_html=True
        )

        if section == "Reports":
            table(labs, "No lab reports are available yet.")

        elif section == "Medicines":
            table(prescriptions, "No prescriptions are available yet.")

        elif section == "Appointments":
            table(visits, "No appointments or visits are available yet.")

        elif section == "Bills":

            bill_view = bills.copy()

            if not bill_view.empty:
                bill_view["amount"] = bill_view["amount"].map(
                    lambda x: f"₹{x:,.2f}"
                )

            table(bill_view, "No bills are available yet.")

        elif section == "Health Details":

            details = profile[
                [
                    "patient_id", "name", "age",
                    "gender", "blood_group", "department"
                ]
            ]

            table(details)

        if st.button(
            "← Back to Patient Home",
            key="patient_back_home"
        ):
            st.session_state.patient_section = "Home"
            st.rerun()

# ---------------- DOCTOR DASHBOARD ----------------

def doctor_dashboard():
    import streamlit as st

    d = st.session_state.data

    # ---------- DOCTOR DASHBOARD STYLING ----------
    st.markdown("""
    <style>
    .doctor-hero {
        background: linear-gradient(120deg, #102D50, #176B87);
        padding: 30px 32px;
        border-radius: 18px;
        color: white;
        margin-bottom: 25px;
    }
    .doctor-hero h1 {
        color: white;
        font-size: 30px;
        margin-bottom: 8px;
    }
    .doctor-hero p {
        color: #E1F3FA;
        font-size: 15px;
        margin-bottom: 0;
    }
    .doctor-card {
        background: white;
        border: 1px solid #E5EDF4;
        border-radius: 15px;
        padding: 20px;
        min-height: 125px;
        box-shadow: 0 3px 12px rgba(20,50,80,0.05);
    }
    .doctor-card-label {
        color: #64748B;
        font-size: 14px;
        margin-bottom: 12px;
    }
    .doctor-card-value {
        color: #153653;
        font-size: 30px;
        font-weight: 700;
    }
    .doctor-card-icon {
        font-size: 22px;
        margin-bottom: 8px;
    }
    .doctor-section {
        color: #163653;
        font-size: 21px;
        font-weight: 700;
        margin: 22px 0 12px 0;
    }
    div[data-testid="stTabs"] button {
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------- WELCOME BANNER ----------
    st.markdown("""
    <div class="doctor-hero">
        <h1>Welcome, Dr. Mehta! 👋</h1>
        <p>Your clinical workspace — manage patients, appointments,
        laboratory reports and treatment updates.</p>
    </div>
    """, unsafe_allow_html=True)

    # ---------- SUMMARY METRICS ----------
    total_patients = len(d["patients"])
    total_visits = len(d["visits"])
    open_visits = int((d["visits"]["status"] == "Open").sum())
    total_labs = len(d["labs"])

    metrics = [
        ("👥", "Total Patients", total_patients),
        ("📅", "Total Visits", total_visits),
        ("⏳", "Open Visits", open_visits),
        ("🧪", "Lab Reports", total_labs)
    ]

    cols = st.columns(4)

    for col, (icon, label, value) in zip(cols, metrics):
        with col:
            st.markdown(f"""
            <div class="doctor-card">
                <div class="doctor-card-icon">{icon}</div>
                <div class="doctor-card-label">{label}</div>
                <div class="doctor-card-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    # ---------- QUICK ACCESS ----------
    st.markdown('<div class="doctor-section">Quick Access</div>',
                unsafe_allow_html=True)

    quick = st.columns(4)

    shortcuts = [
        ("👤", "Patient Records", "View patient information"),
        ("📋", "Visit History", "Review previous visits"),
        ("🔬", "Lab Reports", "Check test results"),
        ("📝", "Diagnosis", "Update treatment details")
    ]

    for col, (icon, title, desc) in zip(quick, shortcuts):
        with col:
            st.markdown(f"""
            <div class="doctor-card">
                <div class="doctor-card-icon">{icon}</div>
                <b style="color:#183B59;">{title}</b>
                <p style="color:#64748B;font-size:13px;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    # ---------- WORKSPACE ----------
    st.markdown('<div class="doctor-section">Clinical Workspace</div>',
                unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "👥 Patient Records",
        "📋 Visit History",
        "🧪 Laboratory Reports",
        "📝 Update Diagnosis"
    ])

    with tab1:
        st.subheader("Patient Records")
        search = st.text_input("Search patients by name or Patient ID",
                               key="doctor_patient_search")

        patients = d["patients"].copy()

        if search:
            mask = patients.astype(str).apply(
                lambda col: col.str.contains(search, case=False, na=False)
            ).any(axis=1)
            patients = patients[mask]

        table(patients)

    with tab2:
        st.subheader("Patient Visit History")

        visits = d["visits"].copy()
        if not visits.empty:
            visits["patient_name"] = visits["patient_id"].apply(pname)

        table(visits)

    with tab3:
        st.subheader("Laboratory Reports")

        labs = d["labs"].copy()
        if not labs.empty:
            labs["patient_name"] = labs["patient_id"].apply(pname)

        table(labs)

    with tab4:
        st.subheader("Update Diagnosis and Visit Status")

        if not d["visits"].empty:
            with st.form("doctor_update_form"):
                vid = st.selectbox(
                    "Select Visit ID",
                    d["visits"]["visit_id"].tolist()
                )

                diagnosis = st.text_area("Diagnosis / Clinical Notes")

                status = st.selectbox(
                    "Visit Status",
                    ["Open", "Under observation", "Completed"]
                )

                save = st.form_submit_button(
                    "Save Visit Update",
                    use_container_width=True
                )

            if save:
                idx = d["visits"].index[
                    d["visits"]["visit_id"] == vid
                ][0]

                d["visits"].loc[idx, ["diagnosis", "status"]] = [
                    diagnosis.strip(), status
                ]

                st.success(f"Visit {vid} updated successfully!")
                st.rerun()
        else:
            st.info("No visits are currently available.")

# ---------------- LAB TECHNICIAN ----------------

def lab_dashboard():

    st.title("Laboratory Technician Dashboard")

    d = st.session_state.data

    cols = st.columns(4)

    values = [
        ("Total Tests", len(d["labs"])),
        ("Pending", int((d["labs"].status == "Pending").sum())),
        ("In Progress", int((d["labs"].status == "In Progress").sum())),
        ("Completed", int((d["labs"].status == "Completed").sum()))
    ]

    for col, (label, value) in zip(cols, values):
        col.metric(label, value)

    st.subheader("Laboratory Test Records")

    view = d["labs"].copy()
    view["patient_name"] = view.patient_id.apply(pname)

    table(view)

    st.subheader("Update Test Result")

    if not d["labs"].empty:

        with st.form("lab_result_form"):

            tid = st.selectbox(
                "Test ID",
                d["labs"].test_id.tolist()
            )

            result = st.text_input("Test Result")

            status = st.selectbox(
                "Status",
                ["Pending", "In Progress", "Completed"]
            )

            save = st.form_submit_button("Save Test Update")

        if save:

            idx = d["labs"].index[
                d["labs"].test_id == tid
            ][0]

            d["labs"].loc[
                idx, ["result", "status"]
            ] = [result.strip() or "Pending", status]

            st.success(f"Test {tid} updated.")
            st.rerun()


# ---------------- PHARMACY ----------------

def pharmacist_dashboard():

    st.title("Pharmacy Dashboard")

    d = st.session_state.data
    meds = d["medicines"]

    low = meds.loc[
        meds.stock <= meds.reorder_level
    ]

    cols = st.columns(3)

    values = [
        ("Medicines", len(meds)),
        ("Low Stock Items", len(low)),
        ("Total Units", int(meds.stock.sum()))
    ]

    for col, (label, value) in zip(cols, values):
        col.metric(label, value)

    st.subheader("Medicine Inventory")
    table(meds)

    st.subheader("Low Stock Alerts")
    table(low, "No medicines are below their reorder level.")

    st.subheader("Add Medicine Stock")

    with st.form("pharmacy_stock_form"):

        mid = st.selectbox(
            "Medicine",
            meds.medicine_id.tolist()
        )

        quantity = st.number_input(
            "Units to add",
            min_value=1,
            step=1
        )

        save = st.form_submit_button("Add Stock")

    if save:

        idx = meds.index[
            meds.medicine_id == mid
        ][0]

        d["medicines"].loc[idx, "stock"] += int(quantity)

        st.success("Stock updated.")
        st.rerun()

    st.subheader("Prescriptions")

    rx = d["prescriptions"].copy()

    if not rx.empty:
        rx["patient_name"] = rx.patient_id.apply(pname)

    table(rx)


# ---------------- ADMINISTRATION ----------------

def administration_dashboard():

    st.title("Administration Dashboard")

    d = st.session_state.data

    cols = st.columns(4)

    values = [
        ("Patients", len(d["patients"])),
        ("Visits", len(d["visits"])),
        ("Bills", len(d["bills"])),
        ("Unpaid Bills", int((d["bills"].status == "Unpaid").sum()))
    ]

    for col, (label, value) in zip(cols, values):
        col.metric(label, value)

    # PATIENT REGISTRATION

    st.subheader("Patient Registration")

    with st.form("register_patient_form", clear_on_submit=True):

        name = st.text_input("Patient Name")

        age = st.number_input(
            "Age",
            min_value=0,
            max_value=120,
            step=1
        )

        gender = st.selectbox(
            "Gender",
            ["Female", "Male", "Other"]
        )

        blood = st.selectbox(
            "Blood Group",
            ["Unknown", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        )

        phone = st.text_input("Phone Number")

        dept = st.selectbox(
            "Department",
            [
                "General Medicine",
                "Cardiology",
                "Orthopedics",
                "Neurology",
                "Pediatrics",
                "Other"
            ]
        )

        register = st.form_submit_button("Register Patient")

    if register:

        if not name.strip():
            st.error("Enter the patient's name.")

        else:

            pid = new_id(
                d["patients"],
                "P",
                "patient_id"
            )

            row = pd.DataFrame(
                [[pid, name.strip(), int(age), gender, blood, phone.strip(), dept]],
                columns=d["patients"].columns
            )

            d["patients"] = pd.concat(
                [d["patients"], row],
                ignore_index=True
            )

            st.success(f"Patient registered. New Patient ID: {pid}")
            st.rerun()

    # CREATE VISIT

    st.subheader("Create Visit")

    with st.form("create_visit_form", clear_on_submit=True):

        pid = st.selectbox(
            "Patient",
            d["patients"].patient_id.tolist(),
            format_func=lambda x: f"{x} - {pname(x)}"
        )

        doctor = st.selectbox(
            "Doctor",
            ["Dr. Mehta", "Dr. Rao", "Dr. Sharma"]
        )

        visit_date = st.date_input(
            "Visit Date",
            value=date.today()
        )

        reason = st.text_input("Reason for Visit")

        create_visit = st.form_submit_button("Create Visit")

    if create_visit:

        vid = new_id(d["visits"], "V", "visit_id")

        row = pd.DataFrame(
            [[vid, pid, doctor, visit_date, reason.strip(),
              "Not yet diagnosed", "Open"]],
            columns=d["visits"].columns
        )

        d["visits"] = pd.concat(
            [d["visits"], row],
            ignore_index=True
        )

        st.success(f"Visit created: {vid}")
        st.rerun()

    # CREATE BILL

    st.subheader("Create Bill")

    with st.form("create_bill_form", clear_on_submit=True):

        bill_pid = st.selectbox(
            "Bill for Patient",
            d["patients"].patient_id.tolist(),
            format_func=lambda x: f"{x} - {pname(x)}"
        )

        amount = st.number_input(
            "Bill Amount (₹)",
            min_value=0.0,
            step=100.0
        )

        payment = st.selectbox(
            "Payment Status",
            ["Unpaid", "Paid"]
        )

        create_bill = st.form_submit_button("Create Bill")

    if create_bill:

        if amount <= 0:
            st.error("Bill amount must be greater than zero.")

        else:

            bid = new_id(d["bills"], "B", "bill_id")

            row = pd.DataFrame(
                [[bid, bill_pid, date.today(), float(amount), payment]],
                columns=d["bills"].columns
            )

            d["bills"] = pd.concat(
                [d["bills"], row],
                ignore_index=True
            )

            st.success(f"Bill created: {bid}")
            st.rerun()

    st.subheader("Patient Directory")
    table(d["patients"])

    st.subheader("Visit Register")
    table(d["visits"])

    st.subheader("Billing Register")
    table(d["bills"])


# ---------------- MANAGEMENT DASHBOARDS ----------------

def management_dashboard(is_board=False):

    d = st.session_state.data

    if is_board:
        st.title("Board Member Dashboard")
    else:
        st.title("Hospital Head Dashboard")

    total = float(d["bills"].amount.sum())
    paid = float(
        d["bills"].loc[
            d["bills"].status == "Paid", "amount"
        ].sum()
    )

    unpaid = float(
        d["bills"].loc[
            d["bills"].status == "Unpaid", "amount"
        ].sum()
    )

    cols = st.columns(4)

    values = [
        ("Patients", len(d["patients"])),
        ("Visits", len(d["visits"])),
        ("Lab Tests", len(d["labs"])),
        ("Total Billed", f"₹{total:,.2f}")
    ]

    for col, (label, value) in zip(cols, values):
        col.metric(label, value)

    st.subheader("Patients by Department")

    if not d["patients"].empty:
        st.bar_chart(
            d["patients"].department.value_counts()
        )

    col1, col2 = st.columns(2)

    col1.metric("Paid Revenue", f"₹{paid:,.2f}")
    col2.metric("Outstanding Amount", f"₹{unpaid:,.2f}")

    st.subheader("Financial Summary")

    st.bar_chart(
        pd.DataFrame(
            {"Amount (₹)": [paid, unpaid]},
            index=["Paid", "Unpaid"]
        )
    )

    st.subheader("Recent Visits")
    table(d["visits"].tail(10))

    st.subheader("Laboratory Status")

    if not d["labs"].empty:
        st.bar_chart(d["labs"].status.value_counts())

    if not is_board:
        st.subheader("Medicine Inventory")
        table(d["medicines"])

    else:
        st.write(f"**Total billed:** ₹{total:,.2f}")
        st.write(f"**Collected:** ₹{paid:,.2f}")
        st.write(f"**Outstanding:** ₹{unpaid:,.2f}")


# ---------------- MAIN APPLICATION ----------------

def main():

    initialize()

    # LOGIN SCREEN ONLY BEFORE AUTHENTICATION

    if not st.session_state.logged_in:

        login_screen()
        return

    # DASHBOARD ONLY AFTER SUCCESSFUL LOGIN

    sidebar()

    role = st.session_state.role

    display_name, designation = PROFILES[role]

    st.markdown(f"### Welcome, {display_name}!")

    st.caption(
        f"{designation} | MEDORA Hospital Management System | {date.today().isoformat()}"
    )

    st.divider()

    if role == "Patient":
        patient_dashboard()

    elif role == "Doctor":
        doctor_dashboard()

    elif role == "Lab Technician":
        lab_dashboard()

    elif role == "Pharmacist":
        pharmacist_dashboard()

    elif role == "Administration":
        administration_dashboard()

    elif role == "Hospital Head / Chairperson":
        management_dashboard(is_board=False)

    elif role == "Board Member":
        management_dashboard(is_board=True)


if __name__ == "__main__":
    initialize()

def main():

    initialize()

    if not st.session_state.logged_in:
        login_screen()
        return

    apply_medora_styles()
    sidebar()

    role = st.session_state.role

    display_name, designation = PROFILES[role]

    if role != "Patient":

        st.markdown(f"### Welcome, {display_name}!")

        st.caption(
            f"{designation} | MEDORA Hospital Management System | {date.today().isoformat()}"
        )

        st.divider()

    if role == "Patient":
        patient_dashboard()

    elif role == "Doctor":
        doctor_dashboard()

    elif role == "Lab Technician":
        lab_dashboard()

    elif role == "Pharmacist":
        pharmacist_dashboard()

    elif role == "Administration":
        administration_dashboard()

    elif role == "Hospital Head / Chairperson":
        management_dashboard(is_board=False)

    elif role == "Board Member":
        management_dashboard(is_board=True)


if __name__ == "__main__":
    initialize()
    main()

