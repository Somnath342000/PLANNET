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

st.title("🪐 PLANET WAR")
st.write("Planet Database Search")


# =====================================================
# LOAD EXCEL
# =====================================================

@st.cache_data
def load_database():

    df = pd.read_excel(
        "MASTAR PLANNET.xlsx"
    )

    # Clean column names
    df.columns = (
        df.columns
        .astype(str)
        .str.replace("\n", " ", regex=False)
        .str.replace("\r", " ", regex=False)
        .str.replace("  ", " ", regex=False)
        .str.strip()
    )

    return df


df = load_database()


# =====================================================
# COLUMN CLEANING
# =====================================================

# Remove accidental spaces around values
for col in df.columns:
    if df[col].dtype == "object":
        df[col] = df[col].astype(str).str.strip()


# =====================================================
# SHOW DATABASE COLUMNS
# =====================================================

with st.expander("🔧 Database Columns"):
    st.write(list(df.columns))


# =====================================================
# FIND COLUMN FUNCTION
# =====================================================

def find_column(possible_names):

    for name in possible_names:

        if name in df.columns:
            return name

    return None


# =====================================================
# DETECT REQUIRED COLUMNS
# =====================================================

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
    "STATE POINT",
    "STATE POINTS "
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
# CHECK DATABASE
# =====================================================

required_columns = {
    "PLANNET": planet_col,
    "ZODAIC SIGN": sign_col,
    "HOUSE": house_col,
    "STATE": state_col,
    "STATE POINT": state_point_col,
    "HOUSE POINT": house_point_col,
    "TOTAL BONUS POINT": tbp_col,
    "DRAW": draw_col,
    "WON": won_col
}

missing = [
    name
    for name, column in required_columns.items()
    if column is None
]


if missing:

    st.error(
        "❌ Database-এর নিচের column পাওয়া যাচ্ছে না:"
    )

    for item in missing:
        st.write("•", item)

    st.info(
        "উপরের 'Database Columns' খুলে আপনার Excel-এর actual column names দেখুন।"
    )

    st.stop()


# =====================================================
# SIDEBAR FILTER
# =====================================================

st.header("🔎 SEARCH FILTER")


# -----------------------------
# ZODAIC SIGN
# -----------------------------

sign_list = sorted(
    df[sign_col]
    .dropna()
    .unique()
    .tolist()
)

selected_sign = st.sidebar.selectbox(
    "♈ ZODAIC SIGN",
    ["ALL"] + sign_list
)


# -----------------------------
# PLANNET
# -----------------------------

planet_list = sorted(
    df[planet_col]
    .dropna()
    .unique()
    .tolist()
)

selected_planet = st.sidebar.selectbox(
    "🪐 PLANNET",
    ["ALL"] + planet_list
)


# -----------------------------
# HOUSE
# -----------------------------

house_list = sorted(
    df[house_col]
    .dropna()
    .unique()
    .tolist()
)

selected_house = st.sidebar.selectbox(
    "🏠 HOUSE",
    ["ALL"] + house_list
)


# =====================================================
# APPLY FILTER
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

st.subheader("🎯 RESULT")


if result.empty:

    st.warning(
        "❌ এই combination-এর কোনো data পাওয়া যায়নি।"
    )

else:

    # =================================================
    # OUTPUT TABLE
    # =================================================

    output = pd.DataFrame({

        "PLANNET":
            result[planet_col].values,

        "SIGN":
            result[sign_col].values,

        "STATE":
            result[state_col].values,

        "STATE POINT":
            result[state_point_col].values,

        "HOUSE":
            result[house_col].values,

        "HOUSE POINT":
            result[house_point_col].values,

        "TOTAL BONUS POINT":
            result[tbp_col].values,

        "DRAW":
            result[draw_col].values,

        "WON":
            result[won_col].values
    })


    st.dataframe(
        output,
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# SINGLE CARD
# =====================================================

if len(result) == 1:

    row = result.iloc[0]

    st.divider()

    st.subheader("🃏 PLANET CARD")

    # -----------------------------
    # BASIC
    # -----------------------------

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


    # -----------------------------
    # STATE
    # -----------------------------

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


    # -----------------------------
    # SCORE
    # -----------------------------

    st.divider()

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
