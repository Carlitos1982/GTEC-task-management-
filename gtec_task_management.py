
import streamlit as st
import pandas as pd
import os
from datetime import datetime
from PIL import Image

# ---------- CONFIG ----------

# CSV file path
CSV_FILE = 'gtec_tasks.csv'

# Load existing data or create empty DataFrame
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        df = pd.DataFrame(columns=[
            'Task ID', 'Requester', 'Request Date', 'Proposed Deadline', 'Department', 'Description',
            'Hours Estimated', 'Direct Release', 'GTEC User', 'GTEC Deadline', 'Status',
            'Completion Date', 'Rework Needed', 'Rework Type', 'Rework Hours',
            'Rework Status', 'Final Approval'
        ])
        df.to_csv(CSV_FILE, index=False)
        return df

# Save DataFrame to CSV
def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# ---------- PAGE CONFIG ----------

st.set_page_config(page_title="GTEC Task Management", layout="wide")

# Load logo
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Flowserve_logo.svg/2560px-Flowserve_logo.svg.png", width=200)

st.title("GTEC Task Management")

# Load data
df = load_data()

# ---------- ADD NEW TASK ----------

st.header("➕ Add New Task")

with st.form("add_task_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        task_id = st.text_input("Task ID")
        requester = st.selectbox("Requester", ["Mario R.", "John S.", "Anna P.", "Luca F.", "Giulia B."])
        request_date = st.date_input("Request Date", value=datetime.today())
        proposed_deadline = st.date_input("Proposed Deadline")
        department = st.text_input("Department")

    with col2:
        description = st.text_area("Description")
        hours_estimated = st.number_input("Hours Estimated", min_value=0.0)
        direct_release = st.radio("Direct Release?", ["Yes", "No"])
        gtec_user = st.text_input("GTEC User")
        gtec_deadline = st.date_input("GTEC Deadline")

    with col3:
        status = st.selectbox("Status", ["Not yet started", "On hold", "In progress", "Completed"])
        completion_date = st.date_input("Completion Date", value=datetime(1900, 1, 1))
        rework_needed = st.radio("Rework Needed?", ["No", "Yes"])
        rework_type = st.selectbox("Rework Type", ["", "Minor", "Major"])
        rework_hours = st.number_input("Rework Hours", min_value=0.0)
        rework_status = st.selectbox("Rework Status", ["", "Not yet started", "In progress", "Completed"])
        final_approval = st.selectbox("Final Approval", ["", "OK", "Rework Needed"])

    submitted = st.form_submit_button("Add Task")

    if submitted:
        new_row = pd.DataFrame([{
            'Task ID': task_id,
            'Requester': requester,
            'Request Date': request_date,
            'Proposed Deadline': proposed_deadline,
            'Department': department,
            'Description': description,
            'Hours Estimated': hours_estimated,
            'Direct Release': direct_release,
            'GTEC User': gtec_user,
            'GTEC Deadline': gtec_deadline,
            'Status': status,
            'Completion Date': "" if completion_date == datetime(1900,1,1) else completion_date,
            'Rework Needed': rework_needed,
            'Rework Type': rework_type,
            'Rework Hours': rework_hours,
            'Rework Status': rework_status,
            'Final Approval': final_approval
        }])

        df = pd.concat([df, new_row], ignore_index=True)
        save_data(df)
        st.success(f"✅ Task {task_id} added successfully!")
