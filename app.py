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



#-----শেষ

# =====================================================
# CARD NUMBER SEARCH
# =====================================================

st.divider()

st.subheader("🎴 CARD NUMBER SEARCH")

card_number = st.number_input(
    "Enter Card Number (1 - 108)",
    min_value=1,
    max_value=108,
    value=1,
    step=1
)

search_card = st.button(
    "🔍 SEARCH CARD",
    use_container_width=True
)


# =====================================================
# SEARCH CARD
# =====================================================

if search_card:

    # -------------------------------------------------
    # FIND CARD
    # -------------------------------------------------

    card_result = df[
        pd.to_numeric(
            df["CARD"],
            errors="coerce"
        ) == card_number
    ].copy()


    # -------------------------------------------------
    # CARD NOT FOUND
    # -------------------------------------------------

    if card_result.empty:

        st.error(
            f"❌ Card {card_number} not found."
        )


    # -------------------------------------------------
    # CARD FOUND
    # -------------------------------------------------

    else:

        # =============================================
        # CARD INFORMATION
        # =============================================

        first_row = card_result.iloc[0]

        st.success(
            f"🎴 Card {card_number} Found"
        )


        # ---------------------------------------------
        # CARD / PLANET / SIGN
        # ---------------------------------------------

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "🎴 CARD",
                str(card_number)
            )

        with c2:

            st.metric(
                "🪐 PLANNET",
                str(first_row[planet_col])
            )

        with c3:

            st.metric(
                "♈ SIGN",
                str(first_row[sign_col])
            )


        # ---------------------------------------------
        # STATE / STATE POINT
        # ---------------------------------------------

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "⚡ STATE",
                str(first_row[state_col])
            )

        with c2:

            st.metric(
                "⭐ STATE POINT",
                str(first_row[state_point_col])
            )


        # =============================================
        # PREPARE 12 HOUSE DATA
        # =============================================

        card_result["_HOUSE_SORT"] = pd.to_numeric(
            card_result[house_col],
            errors="coerce"
        )

        # House 1 → 12
        card_result = (
            card_result
            .sort_values(
                "_HOUSE_SORT",
                ascending=True
            )
            .reset_index(drop=True)
        )


        # =============================================
        # TBP RANKING
        # =============================================

        ranking_data = card_result[
            [house_col, tbp_col]
        ].copy()


        # Convert TBP to number
        ranking_data["_TBP_SORT"] = pd.to_numeric(
            ranking_data[tbp_col],
            errors="coerce"
        )


        # ---------------------------------------------
        # RANKING RULE
        #
        # Higher TBP = Better Rank
        #
        # Same TBP:
        # House appearing first gets priority
        # ---------------------------------------------

        ranking_data = (
            ranking_data
            .sort_values(
                by="_TBP_SORT",
                ascending=False,
                kind="stable"
            )
            .reset_index(drop=True)
        )


        # =============================================
        # UNIQUE RANK 1 → 12
        # =============================================

        ranking_data["_RANK"] = range(
            1,
            len(ranking_data) + 1
        )


        # =============================================
        # HOUSE → RANK
        # =============================================

        house_rank = {}

        for _, rank_row in ranking_data.iterrows():

            house_key = str(
                rank_row[house_col]
            )

            house_rank[house_key] = int(
                rank_row["_RANK"]
            )


        # =============================================
        # ORDINAL FUNCTION
        # =============================================

        def ordinal(n):

            if 10 <= n % 100 <= 20:

                suffix = "th"

            else:

                suffix = {
                    1: "st",
                    2: "nd",
                    3: "rd"
                }.get(
                    n % 10,
                    "th"
                )

            return f"{n}{suffix}"


        # =============================================
        # TBP RANKING SUMMARY
        # =============================================

        st.divider()

        st.subheader(
            "🏆 TBP HOUSE RANKING"
        )

        st.caption(
            "Higher TBP = Higher Rank. "
            "If TBP is equal, House order gets priority."
        )


        # Header
        h1, h2 = st.columns(2)

        with h1:
            st.markdown("**HOUSE**")

        with h2:
            st.markdown("**TBP (RANKING)**")


        # ---------------------------------------------
        # Ranking 1 → 12
        # Display House order 1 → 12
        # ---------------------------------------------

        for _, rank_row in card_result.iterrows():

            house = str(
                rank_row[house_col]
            )

            tbp = rank_row[tbp_col]

            rank = house_rank[house]


            c1, c2 = st.columns(2)

            with c1:

                st.write(
                    f"**{ordinal(int(house))} House**"
                )

            with c2:

                st.write(
                    f"**{tbp} "
                    f"({ordinal(rank)})**"
                )


        # =============================================
        # HOUSE DETAILS
        # =============================================

        st.divider()

        st.subheader(
            f"🏠 Card {card_number} — House Details"
        )


        # =============================================
        # 12 HOUSE EXPANDERS
        # =============================================

        for _, house_row in card_result.iterrows():

            house = house_row[house_col]

            house_point = house_row[
                house_point_col
            ]

            tbp = house_row[
                tbp_col
            ]

            draw = house_row[
                draw_col
            ]

            won = house_row[
                won_col
            ]

            rank = house_rank[
                str(house)
            ]


            # -----------------------------------------
            # EXPANDER
            # -----------------------------------------

            with st.expander(
                f"🏠 {ordinal(int(house))} House  | "
                f"TBP: {tbp} | "
                f"🏆 {ordinal(rank)}",
                expanded=False
            ):


                # -------------------------------------
                # HOUSE POINT
                # -------------------------------------

                st.metric(
                    "🏠 HOUSE POINT",
                    str(house_point)
                )


                # -------------------------------------
                # SCORE
                # -------------------------------------

                c1, c2, c3 = st.columns(3)


                with c1:

                    st.metric(
                        "⭐ TBP",
                        str(tbp)
                    )


                with c2:

                    st.metric(
                        "🤝 DRAW",
                        str(draw)
                    )


                with c3:

                    st.metric(
                        "🏆 WON",
                        str(won)
                    )
