import chess
import sys
from random import choice
import multiprocessing



piece_values = {
    chess.KING: 2000,
    chess.QUEEN: 950,
    chess.ROOK: 540,
    chess.BISHOP: 330,
    chess.KNIGHT: 320,
    chess.PAWN: 100
}
def get_positional_value_for_piece(piece: str, square: chess.Square, player_color: chess.COLOR_NAMES,
                                   board: chess.Board = None):
    pawn = [0, 0, 0, 0, 0, 0, 0, 0,
            50, 50, 50, 50, 50, 50, 50, 50,
            10, 10, 20, 30, 30, 20, 10, 10,
            5, 5, 10, 25, 25, 10, 5, 5,
            0, 0, 0, 20, 20, 0, 0, 0,
            5, -5, -10, 0, 0, -10, -5, 5,
            5, 10, 10, -20, -20, 10, 10, 5,
            0, 0, 0, 0, 0, 0, 0, 0]

    knight = [-50, -40, -30, -30, -30, -30, -40, -50,
              -40, -20, 0, 0, 0, 0, -20, -40,
              -30, 0, 10, 15, 15, 10, 0, -30,
              -30, 5, 15, 20, 20, 15, 5, -30,
              -30, 0, 15, 20, 20, 15, 0, -30,
              -30, 5, 10, 15, 15, 10, 5, -30,
              -40, -20, 0, 5, 5, 0, -20, -40,
              -50, -40, -30, -30, -30, -30, -40, -50]

    bishop = [-20, -10, -10, -10, -10, -10, -10, -20,
              -10, 0, 0, 0, 0, 0, 0, -10,
              -10, 0, 5, 10, 10, 5, 0, -10,
              -10, 5, 5, 10, 10, 5, 5, -10,
              -10, 0, 10, 10, 10, 10, 0, -10,
              -10, 10, 10, 10, 10, 10, 10, -10,
              -10, 5, 0, 0, 0, 0, 5, -10,
              -20, -10, -10, -10, -10, -10, -10, -20]

    rook = [0, 0, 0, 0, 0, 0, 0, 0,
            5, 10, 10, 10, 10, 10, 10, 5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            0, 0, 0, 5, 5, 0, 0, 0]

    queen = [-20, -10, -10, -5, -5, -10, -10, -20,
             -10, 0, 0, 0, 0, 0, 0, -10,
             -10, 0, 5, 5, 5, 5, 0, -10,
             -5, 0, 5, 5, 5, 5, 0, -5,
             0, 0, 5, 5, 5, 5, 0, -5,
             -10, 5, 5, 5, 5, 5, 0, -10,
             -10, 0, 5, 0, 0, 0, 0, -10,
             -20, -10, -10, -5, -5, -10, -10, -20]

    king_mg = [-30, -40, -40, -50, -50, -40, -40, -30,
               -30, -40, -40, -50, -50, -40, -40, -30,
               -30, -40, -40, -50, -50, -40, -40, -30,
               -30, -40, -40, -50, -50, -40, -40, -30,
               -20, -30, -30, -40, -40, -30, -30, -20,
               -10, -20, -20, -20, -20, -20, -20, -10,
               20, 20, 0, 0, 0, 0, 20, 20,
               20, 30, 10, 0, 0, 10, 30, 20]

    king_eg = [-50, -40, -30, -20, -20, -30, -40, -50,
               -30, -20, -10, 0, 0, -10, -20, -30,
               -30, -10, 20, 30, 30, 20, -10, -30,
               -30, -10, 30, 40, 40, 30, -10, -30,
               -30, -10, 30, 40, 40, 30, -10, -30,
               -30, -10, 20, 30, 30, 20, -10, -30,
               -30, -30, 0, 0, 0, 0, -30, -30,
               -50, -30, -30, -30, -30, -30, -30, -50]

    if piece == 'pawn':
        if player_color == chess.WHITE:
            return pawn[63 - square]
        else:
            return pawn[square]

    if piece == 'knight':
        if player_color == chess.WHITE:
            return knight[63 - square]
        else:
            return knight[square]

    if piece == 'bishop':
        if player_color == chess.WHITE:
            return bishop[63 - square]
        else:
            return bishop[square]

    if piece == 'rook':
        if player_color == chess.WHITE:
            return rook[63 - square]
        else:
            return rook[square]

    if piece == 'queen':
        if player_color == chess.WHITE:
            return queen[63 - square]
        else:
            return queen[square]

    if piece == 'king':
        if player_color == chess.WHITE:
            if is_endgame(board):
                return king_eg[63 - square]
            else:
                return king_mg[square]

        if is_endgame(board):
            return king_eg[63 - square]
        else:
            return king_mg[square]


def evaluate_board(board: chess.Board, depth: int, alpha: int, beta: int):
    if depth == 0:
        evaluation = evaluate_position(board)
        return evaluation

    if board.is_repetition(3):
        return 0

    moves = board.legal_moves

    if moves.count() == 0:
        if board.is_check():
            return -999999

        return 0

    for move in moves:

        board.push(move)
        move_evaluation = -evaluate_board(board, depth - 1, -beta, -alpha)
        board.pop()
        if move_evaluation >= beta:
            return beta

        if move_evaluation > alpha:
            alpha = move_evaluation

    return alpha


def is_endgame(board):

    white_knights = board.pieces(chess.KNIGHT, chess.WHITE)
    white_bishops = board.pieces(chess.BISHOP, chess.WHITE)
    white_rooks = board.pieces(chess.ROOK, chess.WHITE)
    white_queen = board.pieces(chess.QUEEN, chess.WHITE)

    black_knights = board.pieces(chess.KNIGHT, chess.BLACK)
    black_bishops = board.pieces(chess.BISHOP, chess.BLACK)
    black_rooks = board.pieces(chess.ROOK, chess.BLACK)
    black_queen = board.pieces(chess.QUEEN, chess.BLACK)

    has_white_queen = len(white_queen) != 0
    has_black_queen = len(black_queen) != 0

    has_no_queens = has_white_queen is False and has_black_queen is False

    if has_no_queens:
        return True

    else:
        if has_white_queen:
            if len(white_knights) + len(white_bishops) + len(white_rooks) > 1:
                return False
        if has_black_queen:
            if len(black_knights) + len(black_bishops) + len(black_rooks) > 1:
                return False

        return True


def evaluate_position(board: chess.Board):
    white_material = 0
    black_material = 0

    white_pawns = board.pieces(chess.PAWN, chess.WHITE)
    white_knights = board.pieces(chess.KNIGHT, chess.WHITE)
    white_bishops = board.pieces(chess.BISHOP, chess.WHITE)
    white_rooks = board.pieces(chess.ROOK, chess.WHITE)
    white_queen = board.pieces(chess.QUEEN, chess.WHITE)

    for square in white_pawns:
        square_value = get_positional_value_for_piece('pawn', square, chess.WHITE)
        white_material += piece_values[chess.PAWN] + square_value
    for square in white_knights:
        square_value = get_positional_value_for_piece('knight', square, chess.WHITE)
        white_material += piece_values[chess.KNIGHT] + square_value
    for square in white_bishops:
        square_value = get_positional_value_for_piece('bishop', square, chess.WHITE)
        white_material += piece_values[chess.BISHOP] + square_value
    for square in white_rooks:
        square_value = get_positional_value_for_piece('rook', square, chess.WHITE)
        white_material += piece_values[chess.ROOK] + square_value
    for square in white_queen:
        square_value = get_positional_value_for_piece('queen', square, chess.WHITE)
        white_material += piece_values[chess.QUEEN] + square_value

    black_pawns = board.pieces(chess.PAWN, chess.BLACK)
    black_knights = board.pieces(chess.KNIGHT, chess.BLACK)
    black_bishops = board.pieces(chess.BISHOP, chess.BLACK)
    black_rooks = board.pieces(chess.ROOK, chess.BLACK)
    black_queen = board.pieces(chess.QUEEN, chess.BLACK)

    for square in black_pawns:
        square_value = get_positional_value_for_piece('pawn', square, chess.BLACK)
        black_material += piece_values[chess.PAWN] + square_value
    for square in black_knights:
        square_value = get_positional_value_for_piece('knight', square, chess.BLACK)
        black_material += piece_values[chess.KNIGHT] + square_value
    for square in black_bishops:
        square_value = get_positional_value_for_piece('bishop', square, chess.BLACK)
        black_material += piece_values[chess.BISHOP] + square_value
    for square in black_rooks:
        square_value = get_positional_value_for_piece('rook', square, chess.BLACK)
        black_material += piece_values[chess.ROOK] + square_value
    for square in black_queen:
        square_value = get_positional_value_for_piece('queen', square, chess.BLACK)
        black_material += piece_values[chess.QUEEN] + square_value

    white_material += piece_values[chess.KING] + get_positional_value_for_piece('king', board.king(chess.WHITE),
                                                                                chess.WHITE, board)
    black_material += piece_values[chess.KING] + get_positional_value_for_piece('king', board.king(chess.BLACK),
                                                                                chess.BLACK, board)

    evaluation = white_material - black_material

    if board.turn == chess.BLACK:
        evaluation = evaluation * -1

    return evaluation

board = chess.Board()

def get_move_score(e):
    return e["score"]
def find_move(max_depth):
    local_board = board.copy()
    moves = local_board.legal_moves

    current_best_score = 999999
    current_best_move = None
    scored_moves = {}
    for current_move in moves:
        local_board.push(current_move)

        score = evaluate_board(local_board, max_depth, -999999, 999999)
        if score < current_best_score:
            current_best_score = score
        local_board.pop()
        scored_moves.update({current_move: score})
    best_moves = []
    
    for move in scored_moves:
        if scored_moves[move] == current_best_score:
            best_moves.append(move)

    return choice(best_moves)
while 1:
    for line in sys.stdin:
        line = line.rstrip()
        if line == 'ucinewgame':
            board.reset()
        if line == 'isready':
            sys.stdout.write('readyok\n')
            sys.stdout.flush()

        if line.startswith('position'):
            options = line.split(' ')
            if options[1] == 'startpos':
                fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
            else:
                fen = options[1]

            board.set_fen(fen)

            if 'moves' in options:
                move_start_index = options.index('moves')
                for i in range(move_start_index + 1, len(options)):
                    move = options[i]
                    board.push(chess.Move.from_uci(move))

        if line.startswith('go'):

            white_time = -1
            black_time = -1
            time_check = 99999999
            if ' ' in line:
                split_line = line.split(' ')

                if 'wtime' in split_line:
                    wtime_index = split_line.index('wtime')
                    white_time = split_line[wtime_index + 1]
                if 'btime' in split_line:
                    btime_index = split_line.index('btime')
                    black_time = split_line[btime_index + 1]
            d = 3

            white_time = int(white_time)
            black_time = int(black_time)

            if white_time != -1:
                if board.turn == chess.WHITE:
                    time_check = white_time / 1000
            if black_time != -1:
                if board.turn == chess.BLACK:
                    time_check = black_time / 1000

            if time_check != 99999999:
                if time_check > 300:   
                    d = 4
                if time_check <= 240:  
                    d = 3
                if time_check <= 60:   
                    d = 2
                if time_check <= 20:   
                    d = 1

            moves_depth_one = len(list(board.legal_moves))
            move_reduction = 0

            if moves_depth_one > 10:
                move_reduction = 1
            elif moves_depth_one > 20:
                move_reduction = 2
            elif moves_depth_one > 30:
                move_reduction = 3

            d = max(1, d - move_reduction)

            move = find_move(d)

            sys.stdout.write(f'bestmove {move}\n')
            sys.stdout.flush()

        if line == 'quit':
            exit(0)