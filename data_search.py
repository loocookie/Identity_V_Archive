import streamlit as st
import pandas as pd
import numpy as np


st.set_page_config(page_title="IVL Archive", layout="wide")
st.title("IVL Archive")

st.markdown(
    """
    <style>
        div[data-testid="column"]
        {
            text-align: center;
        } 
    </style>
    """,unsafe_allow_html=True
)

if "data" not in st.session_state:
    sheet_id = "1t3gF2GR5PydYdEnwuBlwtx9MgpuYCaLk4T4O6PqmFA0"
    sheet_name = "IVL"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    st.session_state["data"] = pd.read_csv(url, dtype=str)

data = st.session_state["data"]

search_expander = st.expander("Search", expanded=True)
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

n_cards_per_row = 3
for n_row, row in data.reset_index().iterrows():
    i = n_row % n_cards_per_row
    if i == 0:
        st.write("---")
        cols = st.columns(n_cards_per_row, gap="small")
    # draw the card
    with cols[i]:
        st.caption(f"{row['season'].strip()} W{row['week'].strip()}D{row['day'].strip()}<br>MATCH{row['match'].strip()} ROUND {row['round'].strip()} {row['half'].strip()} HALF", unsafe_allow_html=True)
        
        sp, sc, h = cols[i].columns([1, 1, 1])
        sc.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 20px'>vs</p>", unsafe_allow_html=True)
        sp.markdown(f"<p style='text-align: right; font-weight: bold; font-size: 20px; color: #92C1C7'>{row['team_s'].strip()} {4 - int(row['n_kill'].strip()) + (4 - int(row['n_kill'].strip())) // 4}</p>", unsafe_allow_html=True)
        h.markdown(f"<p style='text-align: left; font-weight: bold; font-size: 20px; color: #C87F94'>{int(row['n_kill'].strip()) + int(row['n_kill'].strip()) // 4} {row['team_h'].strip()}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 20px;'>{row['map'].strip()}</p>", unsafe_allow_html=True)
        sp, sc, h = cols[i].columns([1, 1, 1])
        h.markdown(f"<div style='text-align: left; font-weight: bold; color: #C87F94'>{row['team_h'].strip()}_{row['player_h']}</div>", unsafe_allow_html=True)
        h.markdown(f"<div style='text-align: left'>{row['character_h']}</div>", unsafe_allow_html=True)
        for j in range(1, 5):
            sp.markdown(f"<p style='text-align: right; font-weight: bold; color: #92C1C7'>{row['team_s'].strip()}_{row[f'player_s_{j}']}</p>", unsafe_allow_html=True)
            sc.markdown(f"<p style='text-align: left'>{row[f'character_s_{j}']}</p>", unsafe_allow_html=True)


# st.table(data)
