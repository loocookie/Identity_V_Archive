import streamlit as st
from st_screen_stats import ScreenData
import pandas as pd
import numpy as np


st.set_page_config(page_title="Identity V Game Archive", layout="wide")
st.title("Identity V Game Archive")

screenD = ScreenData(setTimeout=0)
screen_d = screenD.st_screen_data_window_top()
# st.write(screen_d['innerWidth'])

if "data" not in st.session_state:
    sheet_id = "1t3gF2GR5PydYdEnwuBlwtx9MgpuYCaLk4T4O6PqmFA0"
    sheet_name = "Games"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    st.session_state["data"] = pd.read_csv(url, dtype=str)
    st.session_state["data_old"] = st.session_state["data"]

data = st.session_state["data"]

search_expander = st.expander("Search", expanded=False)

def set_show_all(key):
    st.session_state["show_all"] = key

def deal_nan(s):
    if s != s:
        return "-"
    return str(s)

if screen_d['innerWidth'] > 640:
    games, seasons, teams, maps = set(data['game']), set(data['season']), set(data['team_s']), set(data['map'])
    games.discard("")
    seasons.discard("")
    teams.discard("")
    maps.discard("")
    games = list(games)
    seasons = list(seasons)
    teams = list(teams)
    maps = list(maps)
    games.sort()
    seasons.sort()
    teams.sort()
    maps.sort()
    with search_expander:
        game, season, t_s, sc_s, t_h, m = st.columns([1, 1, 2, 2, 2, 2])
        st.session_state["game"] = game.selectbox("Game", [""] + games, placeholder="", key="game_input")
        st.session_state["season"] = season.selectbox("Season", [""] + seasons, placeholder="", key="season_input")
        st.session_state["team_s"] = t_s.selectbox("Survivor Team", [""] + teams, placeholder="", key="team_s_input")
        # t_s_s.markdown('<p style="text-align: center;font-size: 42px;">?</p>', unsafe_allow_html=True)
        # text_colon.markdown('<p style="text-align: center;font-size: 42px;">:</p>', unsafe_allow_html=True)
        # t_h_s.markdown('<p style="text-align: center;font-size: 42px;">?</p>', unsafe_allow_html=True)
        st.session_state["score_s"] = sc_s.selectbox("Score", ["", "5 : 0", "3 : 1", "2 : 2", "1 : 3", "0 : 5"], placeholder="", key="score_s_input")
        st.session_state["team_h"] = t_h.selectbox("Hunter Team", [""] + teams, placeholder="", key="team_h_input")
        # st.session_state["map"] = m.text_input("Map", value=("" if "map" not in st.session_state else st.session_state["map"]), key="map_input")
        st.session_state["map"] = m.selectbox("Map", [""] + maps, placeholder="")
        
        s1, s2, s3, s4, h = st.columns([3, 3, 3, 3, 3])
        st.session_state["player_s_1"] = s1.text_input("Survivor", key="s1_input")
        st.session_state["player_s_2"] = s2.text_input("Survivor", key="s2_input")
        st.session_state["player_s_3"] = s3.text_input("Survivor", key="s3_input")
        st.session_state["player_s_4"] = s4.text_input("Survivor", key="s4_input")
        st.session_state["player_h"] = h.text_input("Hunter", key="h_input")

        sc1, sc2, sc3, sc4, hc = st.columns([3, 3, 3, 3, 3])
        st.session_state["character_s_1"] = sc1.text_input("Character", key="sc1_input")
        st.session_state["character_s_2"] = sc2.text_input("Character", key="sc2_input")
        st.session_state["character_s_3"] = sc3.text_input("Character", key="sc3_input")
        st.session_state["character_s_4"] = sc4.text_input("Character", key="sc4_input")
        st.session_state["character_h"] = hc.text_input("Character", key="hc_input")

    for keyword in ["game", "season", "team_h", "team_s", "map", "player_h", "character_h"]:
        if keyword in st.session_state and st.session_state[keyword] != "":
            data = data[data[keyword] == st.session_state[keyword]]
    if "score_s" in st.session_state and st.session_state["score_s"] != "":
        print(st.session_state["score_s"][-1])
        data = data[data["n_kill"] == str(int(st.session_state["score_s"][-1]) - int(st.session_state["score_s"][-1]) // 4)]
    for i in range(1, 5):
        np = f"player_s_{i}" not in st.session_state or st.session_state[f"player_s_{i}"] == ""
        nc = f"character_s_{i}" not in st.session_state or st.session_state[f"character_s_{i}"] == ""
        data = data[(((data["player_s_1"] == st.session_state[f"player_s_{i}"]) | np) & ((data["character_s_1"] == st.session_state[f"character_s_{i}"]) | nc)) | 
                    (((data["player_s_2"] == st.session_state[f"player_s_{i}"]) | np) & ((data["character_s_2"] == st.session_state[f"character_s_{i}"]) | nc)) | 
                    (((data["player_s_3"] == st.session_state[f"player_s_{i}"]) | np) & ((data["character_s_3"] == st.session_state[f"character_s_{i}"]) | nc)) | 
                    (((data["player_s_4"] == st.session_state[f"player_s_{i}"]) | np) & ((data["character_s_4"] == st.session_state[f"character_s_{i}"]) | nc))]
        
    if not data.equals(st.session_state["data_old"]):
        set_show_all(None)
        st.session_state["data_old"] = data

    if screen_d['innerWidth'] < 1170:
        st.session_state["show_all"] = None
    if "show_all" in st.session_state and st.session_state["show_all"] is not None:
        data_to_show = data[data["url"] == st.session_state["show_all"]]
        for n_row, row in data_to_show.reset_index().iterrows():
            _, c1, c2, c3, _ = st.columns([0.4, 1.8, 3.6, 1.8, 0.4])
            rd = 'round'
            c1.caption(f"<p style='text-align: left;'>{row['game']} {row['season']} W{row['week']}D{row['day']}<br>MATCH{row['match']} {'EXTRA ROUND' if row['round'] != row['round'] else f'ROUND{row[rd]}'} {row['half']} HALF</p>", unsafe_allow_html=True)
            # c2.markdown("# Game Data")
            c2.markdown(f"<h1 style='text-align: center'>Game Data <a href='{row['url']}' style='text-decoration-line: none; color: black'>\u25B6</a></h1>", unsafe_allow_html=True)
            st.write(
                """
                <style>
                div.stButton>button {
                    float: right;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            c3.button("Show less", on_click=set_show_all, args=[None])

            # st.write(list(map(lambda s: s.strip(), row['ban_global'].split(","))))
            cols = st.columns([0.5, 1, 1, 1, 1, 1, 1, 1, 0.5])
            cols[1].markdown("<p style='text-align: right; font-weight: bold'>Global Ban</p>", unsafe_allow_html=True)
            try:
                bg = list(map(lambda s: s.strip(), row['ban_global'].strip().split(",")))
            except:
                bg = []
            try:
                bh = list(map(lambda s: s.strip(), row['ban_h'].strip().split(",")))
            except:
                bh = []
            bs = list(map(lambda s: s.strip(), row['ban_s'].strip().split(",")))
            ps = list(map(lambda s: s.strip(), row['pick_s'].strip().split(",")))
            for i in range(6):
                try:
                    c = bg[i]
                    cols[2 + i].markdown(f"<p style='text-align: center'>{c if c != '' else '-'}</p>", unsafe_allow_html=True)
                except:
                    cols[2 + i].markdown("<p style='text-align: center'>-</p>", unsafe_allow_html=True)
            cols = st.columns([0.5, 1, 2, 2, 2, 0.5])
            cols[1].markdown("<p style='text-align: right; font-weight: bold'>Hunter Ban</p>", unsafe_allow_html=True)
            for i in range(3):
                try:
                    c = bh[i]
                    cols[2 + i].markdown(f"<p style='text-align: center'>{c if c != '' else '-'}</p>", unsafe_allow_html=True)
                except:
                    cols[2 + i].markdown("<p style='text-align: center'>-</p>", unsafe_allow_html=True)
            cols = st.columns([0.5, 1, 1.5, 1.5, 1.5, 1.5, 0.5])
            cols[1].markdown("<p style='text-align: right; font-weight: bold'>Survivor Ban</p>", unsafe_allow_html=True)
            cols[1].markdown("<p style='text-align: right; font-weight: bold'>Survivor Pick</p>", unsafe_allow_html=True)
            for i in range(4):
                cols[2 + i].markdown(f"<p style='text-align: center'>{bs[i]}</p>", unsafe_allow_html=True)
                cols[2 + i].markdown(f"<p style='text-align: center'>{ps[i]}</p>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            _, _, m_b, _, _ = st.columns([1, 1, 3, 1, 1])
            m_b.markdown(f"<div style='text-align: center; font-size: 20px; color: {'#92C1C7;' if row['ban_map_team'] == row['team_s'] else '#C87F94'}; text-decoration: line-through'>{deal_nan(row['ban_map'])}</div>", unsafe_allow_html=True)

            ss, ts, m, th, sh = st.columns([1, 1, 3, 1, 1])
            ss.markdown(f"<p style='text-align: right; font-weight: bold; font-size: 40px; color: #92C1C7'>{4 - int(row['n_kill']) + (4 - int(row['n_kill'])) // 4}</p>", unsafe_allow_html=True)
            ts.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 40px; color: #92C1C7'>{row['team_s']}</p>", unsafe_allow_html=True)
            m.markdown(f"<p style='text-align: center; font-size: 40px; color: {'#92C1C7;' if row['pick_map_team'] == row['team_s'] else '#C87F94'}'>{row['map']}</p>", unsafe_allow_html=True)
            th.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 40px; color: #C87F94'>{row['team_h']}</p>", unsafe_allow_html=True)
            sh.markdown(f"<p style='text-align: left; font-weight: bold; font-size: 40px; color: #C87F94'>{int(row['n_kill']) + (int(row['n_kill'])) // 4}</p>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # 여기서부터
            _, player_h, char_h, _, cipher, destroy, hit, terror, down, _ = st.columns([0.4, 1.2, 1.2, 0.2, 0.8, 0.8, 0.8, 0.8, 0.8, 0.4])
            player_h.markdown("<p style='text-align: right; font-weight: bold'><br>Player</p>", unsafe_allow_html=True)
            char_h.markdown("<p style='text-align: left; font-weight: bold'><br>Character</p>", unsafe_allow_html=True)
            cipher.markdown("<p style='text-align: center; font-weight: bold'>Remaining<br>Ciphers</p>", unsafe_allow_html=True)
            destroy.markdown("<p style='text-align: center; font-weight: bold'>Pallets<br>Destroyed</p>", unsafe_allow_html=True)
            hit.markdown("<p style='text-align: center; font-weight: bold'>Survivor<br>Hits</p>", unsafe_allow_html=True)
            terror.markdown("<p style='text-align: center; font-weight: bold'>Terror<br>Shocks</p>", unsafe_allow_html=True)
            down.markdown("<p style='text-align: center; font-weight: bold'><br>Knockdowns</p>", unsafe_allow_html=True)
            player_h.markdown(f"<p style='text-align: right; font-weight: bold; color: #C87F94'>{row['team_h']}_{row['player_h']}</p>", unsafe_allow_html=True)
            char_h.markdown(f"<p style='text-align: left'>{row['character_h']}</p>", unsafe_allow_html=True)
            cipher.markdown(f"<p style='text-align: center'>{deal_nan(row['remaining_machines'])}</p>", unsafe_allow_html=True)
            destroy.markdown(f"<p style='text-align: center'>{deal_nan(row['pallet_destroyed'])}</p>", unsafe_allow_html=True)
            hit.markdown(f"<p style='text-align: center'>{deal_nan(row['survivor_hits'])}</p>", unsafe_allow_html=True)
            terror.markdown(f"<p style='text-align: center'>{deal_nan(row['terror_shocks'])}</p>", unsafe_allow_html=True)
            down.markdown(f"<p style='text-align: center'>{deal_nan(row['knockdowns'])}</p>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            _, player_s, char_s, escape, decode, strike, rescue, heal, contain, _ = st.columns([0.4, 1.2, 1.2, 0.2, 0.8, 0.8, 0.8, 0.8, 0.8, 0.4])
            player_s.markdown("<p style='text-align: right; font-weight: bold'><br>Player</p>", unsafe_allow_html=True)
            char_s.markdown("<p style='text-align: left; font-weight: bold'><br>Character</p>", unsafe_allow_html=True)
            escape.markdown("<p style='font-weight: bold'><br><br></p>", unsafe_allow_html=True)
            decode.markdown("<p style='text-align: center; font-weight: bold'>Decoding<br>Progress</p>", unsafe_allow_html=True)
            strike.markdown("<p style='text-align: center; font-weight: bold'>Pallet<br>Strikes</p>", unsafe_allow_html=True)
            rescue.markdown("<p style='text-align: center; font-weight: bold'><br>Rescues</p>", unsafe_allow_html=True)
            heal.markdown("<p style='text-align: center; font-weight: bold'><br>Heals</p>", unsafe_allow_html=True)
            contain.markdown("<p style='text-align: center; font-weight: bold'>Containment<br>Time</p>", unsafe_allow_html=True)
            for i in range(1, 5):
                player_s.markdown(f"<p style='text-align: right; font-weight: bold; color: #92C1C7'>{row['team_s']}_{row[f'player_s_{i}']}</p>", unsafe_allow_html=True)
                char_s.markdown(f"<p style='text-align: left'>{row[f'character_s_{i}']}</p>", unsafe_allow_html=True)
                escape.write(":runner:" if row[f'escaped_{i}'] == '1' else ":skull:")
                decode.markdown(f"<p style='text-align: center'>{deal_nan(row[f'decoding_progress_{i}'])}</p>", unsafe_allow_html=True)
                strike.markdown(f"<p style='text-align: center'>{deal_nan(row[f'pallet_strikes_{i}'])}</p>", unsafe_allow_html=True)
                rescue.markdown(f"<p style='text-align: center'>{deal_nan(row[f'rescue_{i}'])}</p>", unsafe_allow_html=True)
                heal.markdown(f"<p style='text-align: center'>{deal_nan(row[f'heal_{i}'])}</p>", unsafe_allow_html=True)
                contain.markdown(f"<p style='text-align: center'>{deal_nan(row[f'containment_time_{i}'])}</p>", unsafe_allow_html=True)
            
            st.write("---")

    else:
        n_cards_per_row = max(1, screen_d["innerWidth"] // 494)
        flag = True
        for n_row, row in data.reset_index().iterrows():
            i = n_row % n_cards_per_row
            if i == 0 and flag:
                st.write("---")
                cols = st.columns(n_cards_per_row, gap="small")
            # draw the card
            with cols[i]:
                # st.caption(f"{row['season'].strip()} W{row['week'].strip()}D{row['day'].strip()}<br>MATCH{row['match'].strip()} ROUND {row['round'].strip()} {row['half'].strip()} HALF", unsafe_allow_html=True)
                rd = 'round'
                st.markdown(f"<p style='text-align: center; font-size: 14px; color: rgba(49, 51, 63, 0.6)'>{row['game']} {row['season']} W{row['week']}D{row['day']}<br>MATCH{row['match']} {'EXTRA ROUND' if row['round'] != row['round'] else f'ROUND{row[rd]}'} {row['half']} HALF</p>", unsafe_allow_html=True)
                sp, sc, h = cols[i].columns([1, 1, 1])
                sc.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 20px'>vs</p>", unsafe_allow_html=True)
                sp.markdown(f"<p style='text-align: right; font-weight: bold; font-size: 20px; color: #92C1C7'>{row['team_s']} {4 - int(row['n_kill']) + (4 - int(row['n_kill'])) // 4}</p>", unsafe_allow_html=True)
                h.markdown(f"<p style='text-align: left; font-weight: bold; font-size: 20px; color: #C87F94'>{int(row['n_kill']) + int(row['n_kill']) // 4} {row['team_h']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 20px;'>{row['map']}</p>", unsafe_allow_html=True)
                sp, sc, h = cols[i].columns([1, 1, 1])
                h.markdown(f"<div style='text-align: left; font-weight: bold; color: #C87F94'>{row['team_h']}_{row['player_h']}</div>", unsafe_allow_html=True)
                h.markdown(f"<p style='text-align: left'>{row['character_h']}</p>", unsafe_allow_html=True)
                h.markdown(f"<div style='text-align: left'><a href='{row['url']}' style='text-decoration-line: none; font-size: 30px; color: black'>\u25B6</a></div>", unsafe_allow_html=True)
                h.button("Show more", key=n_row, on_click=set_show_all, args=[row['url']], disabled=screen_d['innerWidth'] < 1170)
                for j in range(1, 5):
                    sp.markdown(f"<p style='text-align: right; font-weight: bold; color: #92C1C7'>{row['team_s']}_{row[f'player_s_{j}']}</p>", unsafe_allow_html=True)
                    sc.markdown(f"<p style='text-align: left'>{row[f'character_s_{j}']}</p>", unsafe_allow_html=True)

    # st.table(data)

else:
    st.write("This page is optimized to PCs. If you are using a mobile device, please rotate it.")
