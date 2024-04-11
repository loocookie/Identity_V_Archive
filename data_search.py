import streamlit as st
import pandas as pd
import numpy as np


st.set_page_config(page_title="IVL Archive", layout="wide")
st.title("IVL Archive")


try:
    from st_screen_stats import ScreenData
    screenD = ScreenData(setTimeout=0)
    screen_d = screenD.st_screen_data_window_top()
    st.session_state["innerwidth"] = screen_d['innerWidth']
except:
    from streamlit_js_eval import streamlit_js_eval
    streamlit_js_eval(js_expressions='window.innerWidth', key='innerwidth')


if "data" not in st.session_state:
    sheet_id = "1t3gF2GR5PydYdEnwuBlwtx9MgpuYCaLk4T4O6PqmFA0"
    sheet_name = "IVL"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    st.session_state["data"] = pd.read_csv(url, dtype=str)
    st.session_state["data_old"] = st.session_state["data"]

data = st.session_state["data"]

search_expander = st.expander("Search", expanded=True)

def set_show_all(key):
        st.session_state["show_all"] = key

if st.session_state["innerwidth"] > 640:
    with search_expander:
        season, t_s, t_s_s, text_colon, t_h_s, t_h, m = st.columns([3, 3, 1, 1, 1, 3, 3])
        st.session_state["season"] = season.text_input("Season", key="season_input")
        st.session_state["team_s"] = t_s.text_input("Survivor Team", key="team_s_input")
        t_s_s.markdown('<p style="font-size: 42px;">?</p>', unsafe_allow_html=True)
        text_colon.markdown('<p style="font-size: 42px;">:</p>', unsafe_allow_html=True)
        t_h_s.markdown('<p style="font-size: 42px;">?</p>', unsafe_allow_html=True)
        st.session_state["team_h"] = t_h.text_input("Hunter Team", key="team_h_input")
        # st.session_state["map"] = m.text_input("Map", value=("" if "map" not in st.session_state else st.session_state["map"]), key="map_input")
        st.session_state["map"] = m.selectbox("Map", ["", "Arms Factory", "The Red Church", "Sacred Heart Hospital", "Lakeside Village", "Moonlit River Park", "Leo's Memory", "Eversleeping Town", "China Town"])
        
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

    for keyword in ["season", "team_h", "team_s", "map", "player_h", "character_h"]:
        if keyword in st.session_state and st.session_state[keyword] != "":
            data  = data[data[keyword] == st.session_state[keyword]]
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

    if "show_all" in st.session_state and st.session_state["show_all"] is not None:
        data_to_show = data[data["url"] == st.session_state["show_all"]]
        for n_row, row in data_to_show.reset_index().iterrows():
            c1, c2, c3 = st.columns([1, 3, 1])
            c1.caption(f"<p style='text-align: left;'>{row['season'].strip()} W{row['week'].strip()}D{row['day'].strip()}<br>MATCH{row['match'].strip()} ROUND {row['round'].strip()} {row['half'].strip()} HALF</p>", unsafe_allow_html=True)
            # c2.markdown("# Game Data")
            c2.markdown(f"<h1 style='text-align: center'>Game Data</h1>", unsafe_allow_html=True)
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

            ss, ts, m, th, sh = st.columns([1, 1, 3, 1, 1])
            ss.markdown(f"<p style='text-align: right; font-weight: bold; font-size: 40px; color: #92C1C7'>{4 - int(row['n_kill'].strip()) + (4 - int(row['n_kill'].strip())) // 4}</p>", unsafe_allow_html=True)
            ts.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 40px; color: #92C1C7'>{row['team_s'].strip()}</p>", unsafe_allow_html=True)
            m.markdown(f"<p style='text-align: center; font-size: 40px;'>{row['map'].strip()}</p>", unsafe_allow_html=True)
            th.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 40px; color: #C87F94'>{row['team_h'].strip()}</p>", unsafe_allow_html=True)
            sh.markdown(f"<p style='text-align: left; font-weight: bold; font-size: 40px; color: #C87F94'>{int(row['n_kill'].strip()) + (int(row['n_kill'].strip())) // 4}</p>", unsafe_allow_html=True)

            # 여기서부터
            # player_s, char_s, escape, decode, hit, rescue, heal, contain, player_h, character_h = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    else:
        n_cards_per_row = max(1, st.session_state["innerwidth"] // 494)
        st.write(st.session_state["innerwidth"])
        flag = True
        for n_row, row in data.reset_index().iterrows():
            i = n_row % n_cards_per_row
            if i == 0 and flag:
                st.write("---")
                cols = st.columns(n_cards_per_row, gap="small")
            # draw the card
            with cols[i]:
                # st.caption(f"{row['season'].strip()} W{row['week'].strip()}D{row['day'].strip()}<br>MATCH{row['match'].strip()} ROUND {row['round'].strip()} {row['half'].strip()} HALF", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; font-size: 14px; color: rgba(49, 51, 63, 0.6)'>{row['season'].strip()} W{row['week'].strip()}D{row['day'].strip()}<br>MATCH{row['match'].strip()} ROUND {row['round'].strip()} {row['half'].strip()} HALF</p>", unsafe_allow_html=True)
                sp, sc, h = cols[i].columns([1, 1, 1])
                sc.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 20px'>vs</p>", unsafe_allow_html=True)
                sp.markdown(f"<p style='text-align: right; font-weight: bold; font-size: 20px; color: #92C1C7'>{row['team_s'].strip()} {4 - int(row['n_kill'].strip()) + (4 - int(row['n_kill'].strip())) // 4}</p>", unsafe_allow_html=True)
                h.markdown(f"<p style='text-align: left; font-weight: bold; font-size: 20px; color: #C87F94'>{int(row['n_kill'].strip()) + int(row['n_kill'].strip()) // 4} {row['team_h'].strip()}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 20px;'>{row['map'].strip()}</p>", unsafe_allow_html=True)
                sp, sc, h = cols[i].columns([1, 1, 1])
                h.markdown(f"<div style='text-align: left; font-weight: bold; color: #C87F94'>{row['team_h'].strip()}_{row['player_h']}</div>", unsafe_allow_html=True)
                h.markdown(f"<p style='text-align: left'>{row['character_h']}</p>", unsafe_allow_html=True)
                h.markdown(f"<div style='text-align: left'><a href='{row['url'].strip()}' style='text-decoration-line: none; font-size: 30px; color: black'>\u25B6</a></div>", unsafe_allow_html=True)
                h.button("Show more", key=n_row, on_click=set_show_all, args=[row['url'].strip()])
                for j in range(1, 5):
                    sp.markdown(f"<p style='text-align: right; font-weight: bold; color: #92C1C7'>{row['team_s'].strip()}_{row[f'player_s_{j}']}</p>", unsafe_allow_html=True)
                    sc.markdown(f"<p style='text-align: left'>{row[f'character_s_{j}']}</p>", unsafe_allow_html=True)

    # st.table(data)
