import streamlit as st
import pandas as pd
import sqlite3

# --- Page configuration (sets browser tab title/icon and layout) ---
st.set_page_config(
    page_title="My Data Dashboard",
    page_icon="📊",
    layout="wide"
)

# --- Function: load and clean the uploaded CSV ---
def load_and_clean(file):
    try:
        df = pd.read_csv(file)
    except Exception as e:
        st.error(f"❌ Couldn't read that file. Make sure it's a valid CSV. ({e})")
        return None

    if df.empty:
        st.warning("⚠️ That CSV file has no rows in it. Try a different file.")
        return None

    if "salary" in df.columns:
        df["salary"] = df["salary"].fillna(df["salary"].mean())
    if "hire_date" in df.columns:
        df["hire_date"] = pd.to_datetime(df["hire_date"], errors="coerce")
    return df

# --- Function: save the cleaned data into a SQLite database file ---
def save_to_db(df):
    conn = sqlite3.connect("dashboard.db")
    df.to_sql("data", conn, if_exists="replace", index=False)
    conn.close()

# --- Function: load the most recently saved data from the database ---
def load_from_db():
    conn = sqlite3.connect("dashboard.db")
    try:
        df = pd.read_sql("SELECT * FROM data", conn)
    except Exception:
        df = None
    conn.close()
    return df

# --- App title ---
st.title("📊 My First Data Dashboard")
st.write("Upload a CSV file to see a summary and a chart.")

st.divider()

# --- File upload widget ---
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = load_and_clean(uploaded_file)
    if df is not None:
        save_to_db(df)
        st.success("✅ Data saved! It will still be here next time you open the app.")
else:
    df = load_from_db()
    if df is not None:
        st.info("📂 Showing previously saved data. Upload a new file above to replace it.")

if df is not None:
    # --- Sidebar filters (interactivity) ---
    st.sidebar.header("🔧 Filters")

    if "department" in df.columns:
        departments = ["All"] + sorted(df["department"].unique().tolist())
        selected_dept = st.sidebar.selectbox("Filter by department", departments)

        if selected_dept != "All":
            df = df[df["department"] == selected_dept]

    # --- Data preview ---
    st.subheader("🔍 Preview of your data")
    st.dataframe(df, width="stretch")

    # --- Download button for the (filtered, cleaned) data ---
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download this data as CSV",
        data=csv_data,
        file_name="filtered_data.csv",
        mime="text/csv"
    )

    st.divider()

    # --- Summary stats (updates automatically based on the filter above) ---
    st.subheader("📈 Summary Stats")
    col1, col2, col3 = st.columns(3)
    col1.metric("Employees", len(df))

    if "salary" in df.columns:
        col2.metric("Average Salary", f"${df['salary'].mean():,.0f}")
        col3.metric("Highest Salary", f"${df['salary'].max():,.0f}")

    st.divider()

    # --- Chart: let the user pick which numeric column to visualize ---
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if "department" in df.columns and numeric_cols:
        st.subheader("📊 Chart by Department")
        chart_column = st.selectbox("Choose a column to chart", numeric_cols)

        chart_data = df.groupby("department")[chart_column].mean().sort_values(ascending=False)
        st.bar_chart(chart_data)
else:
    st.info("👆 Upload a CSV file above to get started.")