import streamlit as st
import pandas as pd

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="PLANET WAR",
    page_icon="🪐",
    layout="wide"
)

# =====================================================
# TITLE
# =====================================================

st.title("🪐 PLANET WAR")
st.caption("Planet Database Search")


# =====================================================
# LOAD EXCEL DATABASE
# =====================================================

@st.cache_data
def load_database():

    df = pd.read_excel("MASTAR PLANNET.xlsx")

    # Clean column names
    df.columns = (
        df.columns
        .astype(str)
        .str.replace("\n", " ", regex=False)
        .str.replace("\r", " ", regex=False)
        .str.replace("  ", " ", regex=False)
        .str.strip()
    )

    # Clean values
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str).str.strip()

    return df


df = load_database()


# =====================================================
# FIND COLUMN
# =====================================================

def find_column(possible_names):

    for name in possible_names:
        if name in df.columns:
            return name

    return None


planet_col = find_column([
    "PLANNET",
    "PLANET",
    "Planet"
])

sign_col = find_column([
    "ZODAIC SIGN",
    "ZODIAC SIGN",
    "SIGN",
    "Sign"
])

house_col = find_column([
    "HOUSE",
    "House"
])

state_col = find_column([
    "STATE",
    "PLANET SIGN STATE",
    "PLANNET SIGN STATE"
])

state_point_col = find_column([
    "STATE POINTS",
    "STATE POINT"
])

house_point_col = find_column([
    "HOUSE POINT",
    "HOUSE POINTS"
])

tbp_col = find_column([
    "TOTAL BONOUS POINT",
    "TOTAL BONUS POINT",
    "TOTAL BONUS POINTS",
    "TBP"
])

draw_col = find_column([
    "DRAW (TBP +50)",
    "DRAW",
    "DRAW (TBP+50)"
])

won_col = find_column([
    "WON (TBP+100)",
    "WON (TBP +100)",
    "WON",
    "WON (TBP + 100)"
])


# =====================================================
# CHECK REQUIRED COLUMNS
# =====================================================

required = [
    planet_col,
    sign_col,
    house_col,
    state_col,
    state_point_col,
    house_point_col,
    tbp_col,
    draw_col,
    won_col
]

if any(x is None for x in required):

    st.error(
        "Database column configuration problem."
    )

    st.stop()


# =====================================================
# FILTER SECTION
# =====================================================

st.subheader("🔎 SEARCH PLANET")


col1, col2, col3 = st.columns(3)


# =====================================================
# SIGN FILTER
# =====================================================

with col1:

    sign_list = sorted(
        df[sign_col]
        .dropna()
        .unique()
        .tolist()
    )

    selected_sign = st.selectbox(
        "♈ ZODAIC SIGN",
        ["ALL"] + sign_list
    )


# =====================================================
# PLANET FILTER
# =====================================================

with col2:

    planet_list = sorted(
        df[planet_col]
        .dropna()
        .unique()
        .tolist()
    )

    selected_planet = st.selectbox(
        "🪐 PLANNET",
        ["ALL"] + planet_list
    )


# =====================================================
# HOUSE FILTER
# =====================================================

with col3:

    house_list = sorted(
        df[house_col]
        .dropna()
        .unique()
        .tolist()
    )

    selected_house = st.selectbox(
        "🏠 HOUSE",
        ["ALL"] + house_list
    )


# =====================================================
# FILTER DATABASE
# =====================================================

result = df.copy()


if selected_sign != "ALL":

    result = result[
        result[sign_col].astype(str).str.upper()
        == str(selected_sign).upper()
    ]


if selected_planet != "ALL":

    result = result[
        result[planet_col].astype(str).str.upper()
        == str(selected_planet).upper()
    ]


if selected_house != "ALL":

    result = result[
        result[house_col].astype(str)
        == str(selected_house)
    ]


# =====================================================
# RESULT
# =====================================================

st.divider()

if result.empty:

    st.warning(
        "❌ No matching Planet Card found."
    )

elif len(result) > 1:

    st.info(
        f"🔎 {len(result)} matching cards found. "
        "Please select all three filters."
    )

else:

    row = result.iloc[0]

    # =================================================
    # PLANET CARD
    # =================================================

    st.subheader("🃏 PLANET CARD")


    # -------------------------------------------------
    # BASIC INFORMATION
    # -------------------------------------------------

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "🪐 PLANNET",
            str(row[planet_col])
        )

    with c2:

        st.metric(
            "♈ SIGN",
            str(row[sign_col])
        )

    with c3:

        st.metric(
            "🏠 HOUSE",
            str(row[house_col])
        )


    st.divider()


    # -------------------------------------------------
    # STATE INFORMATION
    # -------------------------------------------------

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "STATE",
            str(row[state_col])
        )

    with c2:

        st.metric(
            "STATE POINT",
            row[state_point_col]
        )

    with c3:

        st.metric(
            "HOUSE POINT",
            row[house_point_col]
        )


    st.divider()


    # -------------------------------------------------
    # FINAL RESULT
    # -------------------------------------------------

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "⭐ TBP",
            row[tbp_col]
        )

    with c2:

        st.metric(
            "🤝 DRAW",
            row[draw_col]
        )

    with c3:

        st.metric(
            "🏆 WON",
            row[won_col]
        )
