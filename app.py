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
# PLANET WAR IMAGE
# =====================================================

st.image(
    "celestial-synergy-the-transformative-power-of-planetary-aspects-in-vedic-astrology-9910681.png",
    use_container_width=True
)

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

            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
            )

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
# ORDINAL FUNCTION
# =====================================================

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

    # =================================================
    # FIND CARD
    # =================================================

    card_result = df[
        pd.to_numeric(
            df["CARD"],
            errors="coerce"
        ) == card_number
    ].copy()


    # =================================================
    # CARD NOT FOUND
    # =================================================

    if card_result.empty:

        st.error(
            f"❌ Card {card_number} not found."
        )

        st.stop()


    # =================================================
    # CARD FOUND
    # =================================================

    first_row = card_result.iloc[0]


    st.success(
        f"🎴 Card {card_number} Found"
    )


    # =================================================
    # CARD / PLANET / SIGN
    # =================================================

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


    # =================================================
    # STATE / STATE POINT
    # =================================================

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


    # =================================================
    # PREPARE HOUSE DATA
    # =================================================

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


    # =================================================
    # TBP RANKING
    # =================================================

    ranking_data = card_result[
        [house_col, tbp_col]
    ].copy()


    # Convert TBP to numeric
    ranking_data["_TBP_SORT"] = pd.to_numeric(
        ranking_data[tbp_col],
        errors="coerce"
    )


    # =================================================
    # RANKING RULE
    #
    # Higher TBP = Better Rank
    #
    # Same TBP:
    # Earlier House gets priority
    # =================================================

    ranking_data = (
        ranking_data
        .sort_values(
            by="_TBP_SORT",
            ascending=False,
            kind="stable"
        )
        .reset_index(drop=True)
    )


    # =================================================
    # UNIQUE RANK 1 → 12
    # =================================================

    ranking_data["_RANK"] = range(
        1,
        len(ranking_data) + 1
    )


    # =================================================
    # HOUSE → RANK DICTIONARY
    # =================================================

    house_rank = {}


    for _, rank_row in ranking_data.iterrows():

        house_key = str(
            int(rank_row[house_col])
        )

        house_rank[house_key] = int(
            rank_row["_RANK"]
        )


    # =================================================
    # TBP HOUSE RANKING
    # =================================================

    st.divider()

    st.subheader(
        "🏆 TBP HOUSE RANKING"
    )


    st.caption(
        "Higher TBP = Better Rank • "
        "Same TBP = Earlier House gets priority"
    )


    # =================================================
    # CREATE RANKING DATAFRAME
    # =================================================

    ranking_display = pd.DataFrame({

        "HOUSE": [
            f"{ordinal(int(house))} House"
            for house in card_result[house_col]
        ],

        "TBP": [
            tbp
            for tbp in card_result[tbp_col]
        ],

        "RANK": [
            ordinal(
                house_rank[
                    str(int(house))
                ]
            )
            for house in card_result[house_col]
        ]

    })


    # =================================================
    # ADD MEDAL TO TOP 3
    # =================================================

    ranking_display["RANK"] = [

        "🥇 1st"
        if house_rank[str(int(house))] == 1

        else "🥈 2nd"
        if house_rank[str(int(house))] == 2

        else "🥉 3rd"
        if house_rank[str(int(house))] == 3

        else ordinal(
            house_rank[str(int(house))]
        )

        for house in card_result[house_col]
    ]


    # =================================================
    # SHOW RANKING DATAFRAME
    # =================================================

    st.dataframe(
        ranking_display,
        use_container_width=True,
        hide_index=True
    )


    # =================================================
    # HOUSE DETAILS
    # =================================================

    st.divider()

    st.subheader(
        f"🏠 Card {card_number} — House Details"
    )


    # =================================================
    # 12 HOUSE EXPANDERS
    # =================================================

    for _, house_row in card_result.iterrows():

        house = int(
            house_row[house_col]
        )


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


        # ---------------------------------------------
        # RANK ICON
        # ---------------------------------------------

        if rank == 1:

            rank_icon = "🥇"

        elif rank == 2:

            rank_icon = "🥈"

        elif rank == 3:

            rank_icon = "🥉"

        else:

            rank_icon = "🏆"


        # =================================================
        # HOUSE EXPANDER
        # =================================================

        with st.expander(
            f"🏠 {ordinal(house)} House | "
            f"TBP: {tbp} | "
            f"{rank_icon} {ordinal(rank)}",
            expanded=False
        ):


            # -----------------------------------------
            # HOUSE POINT
            # -----------------------------------------

            st.metric(
                "🏠 HOUSE POINT",
                str(house_point)
            )


            # -----------------------------------------
            # SCORE
            # -----------------------------------------

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
# --------2nd ভাগ-------
# =====================================================
# PLANET WAR RESULT
# =====================================================

st.divider()

st.subheader("⚔️ PLANET WAR RESULT")

st.caption(
    "Select two planets to see the Planet War result"
)


# =====================================================
# LOAD RESULT DATABASE
# =====================================================

@st.cache_data
def load_war_result():

    result_df = pd.read_excel(
        "PLANNET WAR RESULT.xlsx",
        sheet_name="RESULT"
    )

    # Clean column names
    result_df.columns = (
        result_df.columns
        .astype(str)
        .str.replace("\n", " ", regex=False)
        .str.strip()
    )

    # Clean values
    for col in result_df.columns:

        if result_df[col].dtype == "object":

            result_df[col] = (
                result_df[col]
                .astype(str)
                .str.strip()
                .str.upper()
            )

    return result_df


war_result = load_war_result()


# =====================================================
# PLANET LIST
# =====================================================

war_planets = sorted(
    set(
        war_result["PLANNET_1"].dropna().tolist()
        +
        war_result["PLANNET_2"].dropna().tolist()
    )
)


# =====================================================
# PLANET SELECTION
# =====================================================

c1, c2 = st.columns(2)


with c1:

    planet_1 = st.selectbox(
        "🪐 PLANET 1",
        war_planets,
        key="war_planet_1"
    )


with c2:

    planet_2 = st.selectbox(
        "🪐 PLANET 2",
        war_planets,
        key="war_planet_2"
    )


# =====================================================
# WAR RESULT BUTTON
# =====================================================

check_war = st.button(
    "⚔️ CHECK WAR RESULT",
    use_container_width=True
)


# =====================================================
# FIND RESULT
# =====================================================

if check_war:

    # Same planet
    if planet_1 == planet_2:

        st.warning(
            "⚠️ Please select two different planets."
        )

    else:

        # ---------------------------------------------
        # Search both possible orders
        # ---------------------------------------------

        result = war_result[
            (
                (
                    war_result["PLANNET_1"] == planet_1
                )
                &
                (
                    war_result["PLANNET_2"] == planet_2
                )
            )
            |
            (
                (
                    war_result["PLANNET_1"] == planet_2
                )
                &
                (
                    war_result["PLANNET_2"] == planet_1
                )
            )
        ].copy()


        # ---------------------------------------------
        # Result Found
        # ---------------------------------------------

        if not result.empty:

            row = result.iloc[0]

            stored_p1 = row["PLANNET_1"]
            stored_p2 = row["PLANNET_2"]

            winner = row["WINNER"]
            looser = row["LOOSER"]


            st.divider()

            st.subheader(
                f"⚔️ {planet_1} vs {planet_2}"
            )


            # =========================================
            # DRAW
            # =========================================

            if winner == "DRAW":

                st.success(
                    f"🤝 DRAW\n\n"
                    f"{planet_1} vs {planet_2}"
                )


            # =========================================
            # WINNER / LOOSER
            # =========================================

            else:

                c1, c2 = st.columns(2)


                with c1:

                    st.metric(
                        "🏆 WINNER",
                        str(winner)
                    )


                with c2:

                    st.metric(
                        "❌ LOOSER",
                        str(looser)
                    )


        # ---------------------------------------------
        # Result Not Found
        # ---------------------------------------------

        else:

            st.error(
                "❌ No Planet War rule found."
            )
