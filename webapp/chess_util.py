
'''
Returns a character symbol representing the piece type of
of the capturer on this move, or None if there is no capturer.
Uppercase signifies white piece, lowercase signifies black.
'''
def capturing_piece_type(board, move):
    
    capturing_piece_type = None
    if board.is_capture(move):
        source_square = move.from_square
        capturing_piece_type = board.piece_at(source_square).symbol()

    return capturing_piece_type



'''
Returns a character symbol representing the piece type of
of the captured piece this move, or None if no piece was captured.
Uppercase signifies white piece, lowercase signifies black.
'''
def captured_piece_type(board, move):

    captured_piece_type = None
    if board.is_capture(move):

        target_square = move.to_square
        if board.is_en_passant(move):
            # Ensure that target square points to the position of the captured piece
            if target_square < 32:
                target_square += 8
            else:
                target_square -= 8

        captured_piece_type = board.piece_at(target_square).symbol()

    return captured_piece_type