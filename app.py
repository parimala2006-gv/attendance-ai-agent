import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Attendance AI Agent",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Attendance AI Agent")

uploaded_file = st.file_uploader(
    "Upload Attendance Excel File",
    type=["xlsx"]
)

if uploaded_file is not None:

    try:
        df = pd.read_excel(uploaded_file)

        st.subheader("Attendance Data")
        st.dataframe(df)

        required_columns = [
            "Interns_Id",
            "Name",
            "Working_Days",
            "Present_Days"
        ]

        missing_columns = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing_columns:
            st.error(
                f"Missing columns: {missing_columns}"
            )

        else:

            df["Working_Days"] = pd.to_numeric(
                df["Working_Days"],
                errors="coerce"
            )

            df["Present_Days"] = pd.to_numeric(
                df["Present_Days"],
                errors="coerce"
            )

            df["Attendance %"] = (
                df["Present_Days"]
                / df["Working_Days"]
            ) * 100

            st.subheader("Attendance Analysis")

            st.dataframe(df)

            low_attendance = df[
                df["Attendance %"] < 75
            ]

            st.subheader(
                "Employees Below 75% Attendance"
            )

            st.dataframe(low_attendance)

            st.subheader("Summary")

            total_employees = len(df)

            low_count = len(low_attendance)

            average_attendance = round(
                df["Attendance %"].mean(),
                2
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Total Employees",
                    total_employees
                )

            with col2:
                st.metric(
                    "Below 75%",
                    low_count
                )

            with col3:
                st.metric(
                    "Average Attendance %",
                    average_attendance
                )

            st.subheader(
                "Attendance Chart"
            )

            chart_data = df.set_index(
                "Name"
            )["Attendance %"]

            st.bar_chart(chart_data)

            if st.button(
                "Generate AI Report"
            ):

                report = f"""
Attendance Report

Total Employees: {total_employees}

Employees Below 75%:
{low_count}

Average Attendance:
{average_attendance}%

Low Attendance Employees:
"""

                for _, row in low_attendance.iterrows():
                    report += (
                        f"\n{row['Name']} - "
                        f"{row['Attendance %']:.2f}%"
                    )

                st.subheader(
                    "AI Report"
                )

                st.text(report)

    except Exception as e:
        st.error(
            f"Error: {str(e)}"
        )

else:
    st.info(
        "Upload an Excel file to begin."
    )