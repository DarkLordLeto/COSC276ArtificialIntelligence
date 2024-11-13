import chess

class MinimaxAI():
    def __init__(self, depth):
        self.depth = depth 
        self.call = 0

    def choose_move(self, board):
        '''bestMove = None
        bestScore = bestScore = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            score = self.minimax(board, self.depth-1, False)
            board.pop()
            if score > bestScore:
                bestScore = score
                bestMove = move
        return bestMove'''
        value, move = self.minimax(board, self.depth, board.turn)
        #print(board.turn)
        print(f"Recommending move {move} with value {value}")
        print(f"Number of calls: {self.call}")
        return move
    
    def cutoffTest(self, board, depth):
        # Check if we reached the maximum depth or if the game is over
        return depth == 0 or board.is_game_over() or not board.legal_moves
    
    def minimax(self, board, depth, isMaximizing):
        self.call += 1
        if self.cutoffTest(board, depth):#if we reached the maximum depth or if the game is over, cut off test
            return self.evaluate(board), None
        bestMove = None
        if isMaximizing:#if it is the maximizing player's turn
            bestScore = float('-inf')

            for move in board.legal_moves:
                board.push(move)
                score = self.minimax(board, depth-1, False)[0]#recursively get max score
                board.pop()
                if score > bestScore:
                    bestScore = score
                    bestMove = move
            #return bestScore, bestMove
        else:
            bestScore = float('inf')#if it is the minimizing player's turn

            for move in board.legal_moves:
                board.push(move)
                score = self.minimax(board, depth-1, True)[0]
                board.pop()
                if score < bestScore:
                    bestScore = score
                    bestMove = move
        return bestScore, bestMove
    
    def evaluate(self, board):
        if board.is_checkmate():
            # If checkmate, return a large value (positive for white win, negative for black win)
            return float('inf') if board.turn else float('-inf')
            
        if board.is_stalemate() or board.is_insufficient_material():
            return 0.0
        score = 0.0
        pieceValues = {#assigning weights to each piece
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 1000}#THis did not appear in the psuedo code in book, I dont know whether it should be 1000 or 0, but 1000 seems have fewer steps to win
        for piece in pieceValues:
            score += len(board.pieces(piece, chess.WHITE)) * pieceValues[piece]#counting the number of pieces and multiplying by their values
            score -= len(board.pieces(piece, chess.BLACK)) * pieceValues[piece]
        return score
