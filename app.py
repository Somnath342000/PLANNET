import streamlit as st
import pandas as pd

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="PLANET WAR",
    page_icon="🪐",
    layout="wide"
)

st.title("🪐 PLANET WAR")
st.write("Planet Database Search")

# ==========================================
# LOAD EXCEL DATABASE
# ==========================================

@st.cache_data
def load_database():

    df = pd.read_excel("MASTAR PLANNET.xlsx")

    # Remove extra spaces from column names
    df.columns = df.columns.str.strip()

    return df


df = load_database()

# ==========================================
# SIDEBAR FILTER
# ==========================================

st.sidebar.header("🔎 SEARCH FILTER")

# ------------------------------------------
# ZODAIC SIGN
# ------------------------------------------

sign_list = sorted(
    df["ZODAIC SIGN"].dropna().unique().tolist()
)

selected_sign = st.sidebar.selectbox(
    "♈ ZODAIC SIGN",
    ["ALL"] + sign_list
)

# ------------------------------------------
# PLANNET
# ------------------------------------------

planet_list = sorted(
    df["PLANNET"].dropna().unique().tolist()
)

selected_planet = st.sidebar.selectbox(
    "🪐 PLANNET",
    ["ALL"] + planet_list
)

# ------------------------------------------
# HOUSE
# ------------------------------------------

house_list = sorted(
    df["HOUSE"].dropna().unique().tolist()
)

selected_house = st.sidebar.selectbox(
    "🏠 HOUSE",
    ["ALL"] + house_list
)

# ==========================================
# FILTER DATABASE
# ==========================================

result = df.copy()

if selected_sign != "ALL":
    result = result[
        result["ZODAIC SIGN"] == selected_sign
    ]

if selected_planet != "ALL":
    result = result[
        result["PLANNET"] == selected_planet
    ]

if selected_house != "ALL":
    result = result[
        result["HOUSE"] == selected_house
    ]

# ==========================================
# OUTPUT
# ==========================================

st.divider()

st.subheader("🎯 RESULT")

if len(result) == 0:

    st.warning("❌ No matching data found.")

else:

    # Only required columns
    output = result[
        [
            "PLANNET",
            "ZODAIC SIGN",
            "STATE",
            "STATE POINTS",
            "HOUSE",
            "HOUSE POINT",
            "TOTAL BONOUS POINT",
            "DRAW (TBP +50)",
            "WON (TBP+100)"
        ]
    ].copy()

    # --------------------------------------
    # Rename output columns
    # --------------------------------------

    output = output.rename(
        columns={
            "STATE POINTS": "STATE POINT",
            "TOTAL BONOUS POINT": "TOTAL BONUS POINT",
            "DRAW (TBP +50)": "DRAW",
            "WON (TBP+100)": "WON"
        }
    )

    # --------------------------------------
    # Show result
    # --------------------------------------

    st.dataframe(
        output,
        use_container_width=True,
        hide_index=True
    )

    # ======================================
    # SINGLE CARD RESULT
    # ======================================

    if len(result) == 1:

        row = result.iloc[0]

        st.divider()

        st.subheader("🃏 PLANET CARD")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "🪐 PLANNET",
                row["PLANNET"]
            )

        with c2:
            st.metric(
                "♈ SIGN",
                row["ZODAIC SIGN"]
            )

        with c3:
            st.metric(
                "🏠 HOUSE",
                row["HOUSE"]
            )

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "STATE",
                row["STATE"]
            )

        with c2:
            st.metric(
                "STATE POINT",
                row["STATE POINTS"]
            )

        with c3:
            st.metric(
                "HOUSE POINT",
                row["HOUSE POINT"]
            )

        st.divider()

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "⭐ TBP",
                row["TOTAL BONOUS POINT"]
            )

        with c2:
            st.metric(
                "🤝 DRAW",
                row["DRAW (TBP +50)"]
            )

        with c3:
            st.metric(
                "🏆 WON",
                row["WON (TBP+100)"]
            )
