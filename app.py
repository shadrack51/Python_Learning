import streamlit as st
import pandas as pd
import sqlite3


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Employee Analytics Dashboard",
    page_icon="👥",
    layout="wide"
)


# ---------------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------------

DB_NAME = "employees.db"


def load_employee_data():
    conn = sqlite3.connect(DB_NAME)

    try:
        df = pd.read_sql(
            "SELECT * FROM employees",
            conn
        )
    except Exception as e:
        st.error(f"Could not load employee data: {e}")
        df = pd.DataFrame()

    conn.close()

    return df


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = load_employee_data()


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("👥 Employee Analytics Dashboard")

st.write(
    "Explore employee data, salaries, departments, and workforce statistics."
)

st.divider()


# ---------------------------------------------------------
# CHECK DATABASE
# ---------------------------------------------------------

if df.empty:

    st.warning(
        "No employee data was found in the database."
    )

    st.stop()


# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------

st.sidebar.header("🔍 Filters")


# Department filter

if "department" in df.columns:

    departments = sorted(
        df["department"].dropna().unique().tolist()
    )

    selected_department = st.sidebar.multiselect(
        "Department",
        departments,
        default=departments
    )

    filtered_df = df[
        df["department"].isin(selected_department)
    ]

else:

    filtered_df = df.copy()


# Search employee

if "name" in filtered_df.columns:

    search = st.sidebar.text_input(
        "Search employee"
    )

    if search:

        filtered_df = filtered_df[
            filtered_df["name"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]


# ---------------------------------------------------------
# KEY METRICS
# ---------------------------------------------------------

st.subheader("📊 Workforce Overview")


col1, col2, col3, col4 = st.columns(4)


# Employee count

col1.metric(
    "Employees",
    len(filtered_df)
)


# Average salary

if "salary" in filtered_df.columns:

    average_salary = filtered_df["salary"].mean()

    col2.metric(
        "Average Salary",
        f"${average_salary:,.0f}"
    )


# Highest salary

if "salary" in filtered_df.columns:

    highest_salary = filtered_df["salary"].max()

    col3.metric(
        "Highest Salary",
        f"${highest_salary:,.0f}"
    )


# Lowest salary

if "salary" in filtered_df.columns:

    lowest_salary = filtered_df["salary"].min()

    col4.metric(
        "Lowest Salary",
        f"${lowest_salary:,.0f}"
    )


st.divider()


# ---------------------------------------------------------
# SALARY BY DEPARTMENT
# ---------------------------------------------------------

if "department" in filtered_df.columns and "salary" in filtered_df.columns:

    st.subheader("💰 Average Salary by Department")

    salary_by_department = (
        filtered_df
        .groupby("department")["salary"]
        .mean()
        .sort_values(ascending=False)
    )

    st.bar_chart(
        salary_by_department
    )


st.divider()


# ---------------------------------------------------------
# EMPLOYEE COUNT BY DEPARTMENT
# ---------------------------------------------------------

if "department" in filtered_df.columns:

    st.subheader("👥 Employees by Department")

    employees_by_department = (
        filtered_df["department"]
        .value_counts()
    )

    st.bar_chart(
        employees_by_department
    )


st.divider()


# ---------------------------------------------------------
# EMPLOYEE DATA
# ---------------------------------------------------------

st.subheader("📋 Employee Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)


# ---------------------------------------------------------
# DOWNLOAD DATA
# ---------------------------------------------------------

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="⬇️ Download filtered employee data",
    data=csv_data,
    file_name="employee_data.csv",
    mime="text/csv"
)