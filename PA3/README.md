How to run: change the player 1 and player2 in test_chess.py or gui_chess.py, and run it directly

player1 = MinimaxAI(4)    
player2 = AlphaBetaAI(4)

*note: IterativeDeepeningAI is based on AlphaBetaAI and in the file with this name.
*note2: the game will exit with AttributeError when there's no legal move possible for a player, then the oppsite win is considered in this case