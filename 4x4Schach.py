EMPTY = 0
WHITE = 1
BLACK = 2

print("The pieces '1' move first")

print("\nThese are the coordinates for moving a piece: \n")
print("    1  2  3  4  ... x")
print("1  [2, 2, 2, 2]")
print("2  [0, 0, 0, 0]")
print("3  [0, 0, 0, 0]")
print("4  [1, 1, 1, 1]")
print("\n...\ny")

print("\nPieces move like chess pawns. On the first move they can't move two spaces ahead.")

input("\nPress Enter to continue\n\n")

#Parameter setzen

BOARD_SIZE = int(input("Width of the board: "))

board4x4 = [[EMPTY]*BOARD_SIZE]*BOARD_SIZE


board4x4[0] = [BLACK]*BOARD_SIZE
board4x4[BOARD_SIZE-1] = [WHITE]*BOARD_SIZE

print("Board: ")
print("")
for i in board4x4:
    print(i)



game_turn = WHITE
computer_turn = int(input("\nComputer first ('1') You first ('2') "))
input("\nYou play with: " + "[" + str((computer_turn % 2) + 1) + "]")

def move(board, turn, p1, p2):
    #Überprüfen ob die zu ziehende Figur dem Spieler gehört der zieht
    if (not (board[p1[1]][p1[0]] == turn)):
        return False

    #Züge aus dem Spielfeld hinaus verhindern
    if (p2[0] < 0 or p2[0] > BOARD_SIZE - 1 or p2[1] < 0 or p2[1] > BOARD_SIZE - 1):
        return False

    #Vorwärtsbewegung
    if (p1[0] == p2[0]):
        if (turn == WHITE):
            if (not(p2[1] + 1 == p1[1])):
                return False
        else:
            if (not(p2[1] - 1 == p1[1])):
                return False

        if (not (board[p2[1]][p2[0]] == EMPTY)):
            return False
    
    #Diagonales Schlagen von gegnerischer Figur
    else:
        if (turn == WHITE):
            if (not((board[p2[1]][p2[0]] == BLACK) and (p1[0] - 1 == p2[0] or p1[0] + 1 == p2[0]) and (p1[1] - 1 == p2[1]))):
                return False
        else:
            if (not ((board[p2[1]][p2[0]] == WHITE) and (p1[0] - 1 == p2[0] or p1[0] + 1 == p2[0]) and (p1[1] + 1 == p2[1]))):
                return False
    
    #Zug ziehen
    board = [x[:] for x in board]

    board[p2[1]][p2[0]] = turn
    board[p1[1]][p1[0]] = EMPTY

    return board



def won(board, turn):
    #Hat ein Spieler die andere Seite erreicht
    for i in range(BOARD_SIZE):
        if (board[0][i] == WHITE):
            return WHITE
        if (board[BOARD_SIZE - 1][i] == BLACK):
            return BLACK

    #überprüfen ob weiss bei der gegebenen Position verliert
    if (turn == WHITE):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if (can_forward(board, turn, (j, i))):
                    return EMPTY
                if(can_capture_left(board, turn, (j, i)) or can_capture_right(board, turn, (j, i))):
                    return EMPTY
        return BLACK
    #überprüfen ob schwarz bei der gegebenen Position verliert
    else:
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if (can_forward(board, turn, (j, i))):
                    return EMPTY
                if(can_capture_left(board, turn, (j, i)) or can_capture_right(board, turn, (j, i))):
                    return EMPTY
        return WHITE


#Gibt alle möglichen Züge zurück
def possible_moves(board, turn):
    moves = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if (board[i][j] == turn):
                #für weiss
                if (turn == WHITE):
                    #Vorwärts
                    if (can_forward(board, turn, (j, i))):
                        moves.append([(j, i), (j, i - 1)])
                    #Diagonales Schlagen
                    if (can_capture_left(board, turn, (j, i))):
                        moves.append([(j, i), (j - 1, i - 1)])
                    if (can_capture_right(board, turn, (j, i))):
                        moves.append([(j, i), (j + 1, i - 1)])
                #für schwarz
                else:
                    #Vorwärts
                    if (can_forward(board, turn, (j, i))):
                        moves.append([(j, i), (j, i + 1)])
                    #Diagonales Schlagen
                    if (can_capture_left(board, turn, (j, i))):
                        moves.append([(j, i), (j - 1, i + 1)])
                    if (can_capture_right(board, turn, (j, i))):
                        moves.append([(j, i), (j + 1, i + 1)])
    return moves


def can_forward(board, turn, coordinates):
    if turn == WHITE:
        return not move([x[:] for x in board], turn, coordinates, (coordinates[0], coordinates[1] - 1)) == False
    return not move([x[:] for x in board], turn, coordinates, (coordinates[0], coordinates[1] + 1)) == False

def can_capture_right(board, turn, coordinates):
    if turn == WHITE:
        return not move([x[:] for x in board], turn, coordinates, (coordinates[0] + 1, coordinates[1] - 1)) == False
    return not move([x[:] for x in board], turn, coordinates, (coordinates[0] + 1, coordinates[1] + 1)) == False

    
def can_capture_left(board, turn, coordinates):
    if turn == WHITE:
        return not move([x[:] for x in board], turn, coordinates, (coordinates[0] - 1, coordinates[1] - 1)) == False
    return not move([x[:] for x in board], turn, coordinates, (coordinates[0] - 1, coordinates[1] + 1)) == False





#Sucht besten Zug für eine gewinnnende Position. Bei einer verlierenden Position wird der letzte gefundene Zug vorgeschlagen
def minimax(board, node, turn):
    #Überprüft ob die jetzt analysierte Position gewinnt
    if (won([x[:] for x in board], (node%2) + 1) == turn):
        return 1
    elif (not(won([x[:] for x in board], (node%2) + 1) == EMPTY)):
        return 0


    #Bei einer ungeraden Analysetiefe ist der Spieler am Zug -> alle nächstmöglichen Züge müssen für den Computer gewinnen
    if (node % 2 == 1):
        for i in possible_moves([x[:] for x in board], turn):
            #nächst tiefere Analysestufe
            if(minimax(move([x[:] for x in board], turn, (i[0][0], i[0][1]), (i[1][0], i[1][1])), node + 1, turn) == 1):
                if (node == 1):
                    return i
                else:
                    return 1
        if (node == 1):
            return(possible_moves([x[:] for x in board], turn)[1])
        else:
            return 0
    
    #Bei einer geraden Analysetiefe ist der Computer am Zug -> nur ein nächster Zug muss für den Computer gewinnen
    else:
        if (turn == WHITE):
            fturn = BLACK
        else:
            fturn = WHITE
        for i in possible_moves([x[:] for x in board], fturn):
            #nächst tiefere Analysestufe

            if(minimax(move([x[:] for x in board], fturn, (i[0][0], i[0][1]), (i[1][0], i[1][1])), node + 1, turn) == 0):
                if (node == 1):
                    return i
                else:
                    return 0
        return 1




#Spielverlauf
print("\n\nBoard: ")
while True:
    print("")
    for i in board4x4:
        print(i)
    print("")


    if (game_turn == WHITE):
        fturn = BLACK
    else:
        fturn = WHITE
    if game_turn == computer_turn:
        if(won(board4x4, fturn)):
            print("You won")
            input("Press Enter to exit")
            break
        print("Computer move: ")
        best_move = minimax([x[:] for x in board4x4], 1, game_turn)
        board4x4 = move(board4x4, game_turn, best_move[0], best_move[1])
        game_turn = fturn

    else:
        if(won(board4x4, fturn)):
            print("The computer won")
            input("Press Enter to exit")
            break
        print("Your turn: ")
        board4x4 = move(board4x4, game_turn, (int(input("x1 ")) - 1, int(input("y1 ")) - 1), (int(input("x2 ")) - 1, int(input("y2 ")) - 1))
        game_turn = fturn
