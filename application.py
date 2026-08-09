import streamlit as st
import csv

# =========================
# LOAD CSV
# =========================

def load_csv(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return list(csv.DictReader(file))
    except Exception as e:
        st.error(f"Error: {e}")
        return []


# =========================
# SAFE INTEGER CONVERSION
# =========================

def safe_int(value):
    try:
        return int(float(str(value).strip()))
    except:
        return 0


# =========================
# POINTS TABLE
# =========================

def show_points(matches):

    points = {}

    for match in matches:

        team1 = match.get("team1")
        team2 = match.get("team2")
        result = match.get("result", "").lower()

        if team1:
            points.setdefault(team1, 0)

        if team2:
            points.setdefault(team2, 0)

        if team1 and team1.lower() in result:
            points[team1] += 2

        elif team2 and team2.lower() in result:
            points[team2] += 2

    st.subheader("🏆 Points Table")

    for team, pts in sorted(
        points.items(),
        key=lambda x: x[1],
        reverse=True
    ):
        st.write(f"**{team}** : {pts}")


# =========================
# TOP RUN SCORER
# =========================

def top_runs(players):

    if not players:
        st.error("No player data found")
        return

    player = max(
        players,
        key=lambda x: safe_int(x.get("Runs"))
    )

    st.subheader("🏏 Top Run Scorer")

    st.write("Player :", player["Player"])
    st.write("Team :", player["Team"])
    st.write("Runs :", player["Runs"])


# =========================
# TOP WICKET TAKER
# =========================

def top_wickets(players):

    if not players:
        st.error("No player data found")
        return

    player = max(
        players,
        key=lambda x: safe_int(x.get("Wickets"))
    )

    st.subheader("🎯 Top Wicket Taker")

    st.write("Player :", player["Player"])
    st.write("Team :", player["Team"])
    st.write("Wickets :", player["Wickets"])


# =========================
# SEARCH PLAYER
# =========================

def search_player(players):

    name = st.text_input("Enter Player Name")

    if name:

        found = False

        for player in players:

            if name.strip().lower() == player["Player"].strip().lower():

                st.subheader("✅ Player Found")

                st.write("Name :", player["Player"])
                st.write("Team :", player["Team"])
                st.write("Role :", player["Role"])
                st.write("Matches :", player["Matches"])
                st.write("Runs :", player["Runs"])
                st.write("Wickets :", player["Wickets"])

                found = True
                break

        if not found:
            st.error("Player not found")


# =========================
# TOURNAMENT WINNER
# =========================

def show_winner(matches):

    for match in matches:

        if match.get("match_type", "").lower() == "final":

            st.subheader("🏆 Tournament Winner")

            st.success(match.get("result"))

            return

    st.error("Final match data not found")


# =========================
# MAIN APP
# =========================

def main():

    st.title("🏏 IPL Analytics Dashboard")

    matches_file = st.text_input(
        "Matches CSV File",
        "matches.csv"
    )

    players_file = st.text_input(
        "Players CSV File",
        "players.csv"
    )

    matches = load_csv(matches_file)
    players = load_csv(players_file)

    if not matches:
        st.warning("Match file not loaded")
        return

    if not players:
        st.warning("Player file not loaded")
        return

    option = st.sidebar.selectbox(
        "Select Option",
        [
            "Points Table",
            "Top Run Scorer",
            "Top Wicket Taker",
            "Search Player",
            "Tournament Winner"
        ]
    )

    if option == "Points Table":
        show_points(matches)

    elif option == "Top Run Scorer":
        top_runs(players)

    elif option == "Top Wicket Taker":
        top_wickets(players)

    elif option == "Search Player":
        search_player(players)

    elif option == "Tournament Winner":
        show_winner(matches)


# =========================
# START APP
# =========================

if __name__ == "__main__":
    main()