import streamlit as st
import pandas as pd
from datetime import date

from database import (
    insert_patient,
    get_patients,
    update_patient,
    delete_patient
)

from ai_service import predict_health

st.set_page_config(
    page_title="Health Prediction System",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 Health Prediction Application")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Create",
        "View",
        "Update",
        "Delete"
    ]
)

# --------------------------
# CREATE
# --------------------------

if menu == "Create":

    st.header("Add Patient")

    name = st.text_input(
        "Full Name"
    )

    dob = st.date_input(
        "Date of Birth"
    )

    email = st.text_input(
        "Email"
    )

    glucose = st.number_input(
        "Glucose",
        min_value=0.0,
        step=1.0
    )

    haemoglobin = st.number_input(
        "Haemoglobin",
        min_value=0.0,
        step=0.1
    )

    cholesterol = st.number_input(
        "Cholesterol",
        min_value=0.0,
        step=1.0
    )

    if st.button("Predict & Save"):

        if name.strip() == "":
            st.error("Please enter Full Name")

        elif dob > date.today():
            st.error("DOB cannot be a future date")

        elif "@" not in email or "." not in email:
            st.error("Please enter a valid email")

        else:

            remarks = predict_health(
                glucose,
                haemoglobin,
                cholesterol
            )

            insert_patient(
                (
                    name,
                    str(dob),
                    email,
                    glucose,
                    haemoglobin,
                    cholesterol,
                    remarks
                )
            )

            st.success(
                "Patient Saved Successfully"
            )

            st.subheader(
                "AI Prediction"
            )

            st.info(
                remarks
            )

# --------------------------
# VIEW
# --------------------------

elif menu == "View":

    st.header(
        "Patient Records"
    )

    data = get_patients()

    if len(data) == 0:
        st.warning(
            "No records found"
        )

    else:

        df = pd.DataFrame(
            data,
            columns=[
                "ID",
                "Name",
                "DOB",
                "Email",
                "Glucose",
                "Haemoglobin",
                "Cholesterol",
                "Remarks"
            ]
        )

        search = st.text_input(
            "Search by Name"
        )

        if search:
            df = df[
                df["Name"].str.contains(
                    search,
                    case=False
                )
            ]

        st.dataframe(
            df,
            use_container_width=True
        )

        csv = df.to_csv(
            index=False
        )

        st.download_button(
            "Download CSV",
            csv,
            "patients.csv",
            "text/csv"
        )

# --------------------------
# UPDATE
# --------------------------

elif menu == "Update":

    st.header(
        "Update Patient"
    )

    patients = get_patients()

    if len(patients) == 0:

        st.warning(
            "No patients available"
        )

    else:

        patient_ids = [
            row[0]
            for row in patients
        ]

        selected_id = st.selectbox(
            "Select Patient ID",
            patient_ids
        )

        patient = None

        for row in patients:
            if row[0] == selected_id:
                patient = row
                break

        name = st.text_input(
            "Full Name",
            patient[1]
        )

        dob = st.text_input(
            "DOB",
            patient[2]
        )

        email = st.text_input(
            "Email",
            patient[3]
        )

        glucose = st.number_input(
            "Glucose",
            value=float(patient[4])
        )

        haemoglobin = st.number_input(
            "Haemoglobin",
            value=float(patient[5])
        )

        cholesterol = st.number_input(
            "Cholesterol",
            value=float(patient[6])
        )

        if st.button(
            "Update Record"
        ):

            remarks = predict_health(
                glucose,
                haemoglobin,
                cholesterol
            )

            update_patient(
                (
                    name,
                    dob,
                    email,
                    glucose,
                    haemoglobin,
                    cholesterol,
                    remarks,
                    selected_id
                )
            )

            st.success(
                "Patient Updated Successfully"
            )

# --------------------------
# DELETE
# --------------------------

elif menu == "Delete":

    st.header(
        "Delete Patient"
    )

    patients = get_patients()

    if len(patients) == 0:

        st.warning(
            "No patients available"
        )

    else:

        patient_ids = [
            row[0]
            for row in patients
        ]

        selected_id = st.selectbox(
            "Select Patient ID",
            patient_ids
        )

        if st.button(
            "Delete Record"
        ):

            delete_patient(
                selected_id
            )

            st.success(
                "Patient Deleted Successfully"
            )