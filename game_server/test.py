from game_logic.Chessboard import ChessBoard

def test_main():
    board = ChessBoard()
    # board.local_terminal_game()
    # print(board.get_available_moves([0, 1]))
    board.print_board()
    board.move_piece((0, 1), (0, 3))
    board.print_board()

test_main()
