import streamlit as st
import numpy as np


def check_winner(board: np.ndarray):
    row_sum = np.sum(board, axis=1)
    col_sum = np.sum(board, axis=0)

    if 3 in row_sum or 3 in col_sum:
        return "X"
    if -3 in row_sum or -3 in col_sum:
        return "O"

    if np.trace(board) == 3 or np.trace(np.fliplr(board)) == 3:
        return "X"
    if np.trace(board) == -3 or np.trace(np.fliplr(board)) == -3:
        return "O"

    if 0 not in board:
        return "DRAW"

    return None


def symbol(value: int) -> str:
    if value == 1:
        return "X"
    if value == -1:
        return "O"
    return " "


st.set_page_config(page_title="Tic Tac Toe", page_icon="🎮", layout="centered")
st.title("🎮 Tic-Tac-Toe")

if "board" not in st.session_state:
    st.session_state.board = np.zeros((3, 3), dtype=int)

if "current" not in st.session_state:
    st.session_state.current = 1

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "winner" not in st.session_state:
    st.session_state.winner = None


def reset_game():
    st.session_state.board = np.zeros((3, 3), dtype=int)
    st.session_state.current = 1
    st.session_state.game_over = False
    st.session_state.winner = None


if st.button("🔄 Reset Game"):
    reset_game()
    st.rerun()


if not st.session_state.game_over:
    player = "X" if st.session_state.current == 1 else "O"
    st.info(f"👉 Turn: **{player}**")


outer_left, outer_mid, outer_right = st.columns([2, 1, 2])

with outer_mid:
    for r in range(3):
        cols = st.columns(3, gap="small")
        for c in range(3):
            value = st.session_state.board[r, c]
            label = symbol(value)
            disabled = (value != 0) or st.session_state.game_over

            if cols[c].button(
                label,
                key=f"{r}-{c}",
                disabled=disabled,
                use_container_width=True,
            ):
                st.session_state.board[r, c] = st.session_state.current

                result = check_winner(st.session_state.board)
                if result is not None:
                    st.session_state.game_over = True
                    st.session_state.winner = result
                else:
                    st.session_state.current *= -1

                st.rerun()


if st.session_state.game_over:
    if st.session_state.winner == "DRAW":
        st.warning("🤝 It's a Draw!")
    else:
        st.success(f"🏆 **{st.session_state.winner} wins!**")