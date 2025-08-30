# gtec_manager_mobile.py

import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

st.set_page_config(page_title="GTEC Task Management", layout="centered")
st.markdown(
    '<style>body { zoom: 90%; }</style>',
    unsafe_allow_html=True
)

st.title("🔧 GTEC Task Management")

# Messaggio iniziale per esperienza mobile
st.info("🔄 For best experience, rotate your phone horizontally.")

# Sessione per archiviare i task
if "task_list" not in st.session_state:
    st.session_state.task_list = []

# ---------- FORM PER NUOVO TASK ----------
st.subheader("➕ Add New Task")

with st.form("new_task_form"):
    requester = st.selectbox("Requester", ["Davide", "Marco", "Giulia", "Alessandro"])
    request_date = st.date_input("Request Date", value=datetime.today())
    proposed_deadline = st.date_input("Proposed Deadline")
    department = st.text_input("Department")
    description = st.text_area("Task Description")
    estimated_hours = st.number_input("Estimated Hours", min_value=0.0, step=0.5)
    direct_release = st.radio("Direct Release?", ["Yes", "No"])

    gtec_supervisor = st.text_input("GTEC Supervisor")
    gtec_assignee = st.text_input("GTEC Assignee")
    gtec_deadline = st.date_input("GTEC Deadline")
    status = st.selectbox("Status", ["Not yet started", "In progress", "Completed", "On hold"])
    completion_date = st.date_input("Completion Date", disabled=(status != "Completed"))

    # Campi condizionati
    final_check_ok = None
    rework_needed = None
    rework_type = None
    rework_hours = None
    rework_confirmed = None
    final_approval = None

    if direct_release == "No":
        final_check_ok = st.selectbox("Final Check OK?", ["Pending", "Yes", "No"])
        if final_check_ok == "No":
            rework_needed = "Yes"
            rework_type = st.radio("Rework Type", ["Minor", "Major"])
            rework_hours = st.number_input("Rework Estimated Hours", min_value=0.0, step=0.5)
            rework_confirmed = st.selectbox("Rework Confirmed by GTEC?", ["Pending", "Yes"])
            final_approval = st.selectbox("Final Approval after Rework?", ["Pending", "Yes", "No"])
        else:
            rework_needed = "No"

    submitted = st.form_submit_button("Add Task")

    if submitted:
        new_task = {
            "Task ID": len(st.session_state.task_list) + 1,
            "Requester": requester,
            "Request Date": request_date,
            "Proposed Deadline": proposed_deadline,
            "Department": department,
            "Description": description,
            "Estimated Hours": estimated_hours,
            "Direct Release": direct_release,
            "GTEC Supervisor": gtec_supervisor,
            "GTEC Assignee": gtec_assignee,
            "GTEC Deadline": gtec_deadline,
            "Status": status,
            "Completion Date": completion_date if status == "Completed" else None,
            "Final Check OK": final_check_ok,
            "Rework Needed": rework_needed,
            "Rework Type": rework_type,
            "Rework Hours": rework_hours,
            "Rework Confirmed": rework_confirmed,
            "Final Approval": final_approval
        }
        st.session_state.task_list.append(new_task)
        st.success(f"✅ Task #{new_task['Task ID']} added.")

# ---------- KPI DASHBOARD ----------
st.subheader("📊 KPI Dashboard")

if st.session_state.task_list:
    df = pd.DataFrame(st.session_state.task_list)
    df["Proposed Deadline"] = pd.to_datetime(df["Proposed Deadline"], errors="coerce")
    df["Completion Date"] = pd.to_datetime(df["Completion Date"], errors="coerce")

    total_tasks = len(df)
    completed = df[df["Status"] == "Completed"]
    in_progress = df[df["Status"] == "In progress"]
    on_hold = df[df["Status"] == "On hold"]
    rework = df[df["Rework Needed"] == "Yes"]

    on_time = completed[completed["Completion Date"] <= completed["Proposed Deadline"]]
    late = completed[completed["Completion Date"] > completed["Proposed Deadline"]]

    kpi = {
        "Total Tasks": total_tasks,
        "Completed Tasks": len(completed),
        "In Progress": len(in_progress),
        "On Hold": len(on_hold),
        "Rework Required": len(rework),
        "On Time Completion (%)": round(len(on_time) / len(completed) * 100, 1) if len(completed) else 0.0,
        "Late Completion (%)": round(len(late) / len(completed) * 100, 1) if len(completed) else 0.0,
    }

    kpi_df = pd.DataFrame.from_dict(kpi, orient="index", columns=["Value"])
    kpi_df.reset_index(inplace=True)
    kpi_df.columns = ["KPI", "Value"]
    st.dataframe(kpi_df, use_container_width=True)
else:
    st.info("No tasks yet for KPI calculation.")

# ---------- TABELLA TASK ----------
st.subheader("📋 Task List")

if st.session_state.task_list:
    df_tasks = pd.DataFrame(st.session_state.task_list)
    st.dataframe(df_tasks, use_container_width=True)

    # ---------- DOWNLOAD EXCEL ----------
    def convert_df_to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="GTEC Tasks")
            writer.save()
        return output.getvalue()

    excel_data = convert_df_to_excel(df_tasks)
    st.download_button(
        label="⬇️ Download as Excel",
        data=excel_data,
        file_name="gtec_tasks.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("No tasks added yet.")