# -*- coding: utf-8 -*-
"""
@author: Tanaya Joshi
"""

tan=[]

for line in open('input.txt'):
    tan.extend(line.split())


alpha=float("-inf")
beta=float("inf")
size=int(tan[0])
mode=str(tan[1])
player=tan[2]
max_depth=int(tan[3])

if(player=="X"):
    COMPUTER = "X"
    HUMAN = "O"

if(player=="O"):
    COMPUTER = "O"
    HUMAN = "X"
    

s1=int((size*size)-1)
cell = [tan[v:v+size] for v in range(4, 4+s1, size)]

list1=[]
for i in range(5+s1, 5+s1+size, 1):
    for ch in tan[i]:
        list1.extend(ch)        

board=[list1[v:v+size] for v in range(0, s1, size)]

backup_board = board

def evaluation(board1):
    score = 0
    j=0
    for i in range(size):
        for j in range(size):
            if(board[i][j]==COMPUTER):
                score+=int(cell[i][j])
            elif(board[i][j]==HUMAN):
                score-=int(cell[i][j])
    return score
    
    
def legalMoves(board):
    a = []
    for i in range(size):
        for j in range(size):
            if(board[i][j]=="."):
                a.append([i,j])
    return a


class Best:
    def __init__(self):
        self.move=[]
        self.score=0
        self.movetype=""

def adjacentTo(m):
    x=m[0]
    y=m[1]
    X=size
    Y=size
    neighbors = lambda x, y : [(x2, y2) for x2 in range(x-1, x+2)
                               for y2 in range(y-1, y+2)
                               if (-1 < x < X and
                                   -1 < y < Y and
                                   (x != x2 or y != y2) and
                                   (0 <= x2 < X) and
                                   (0 <= y2 < Y))]
    neighbors1 = lambda x, y : [(x2, y2) for x2 in (x-1, x+1)
                                   for y2 in (y-1, y+1)
                                   if (-1 < x < X and
                                       -1 < y < Y and
                                       (x != x2 or y != y2) and
                                       (0 <= x2 < X) and
                                       (0 <= y2 < Y))]

    adjacent=list(set(neighbors(x,y))-set(neighbors1(x,y)))
    return adjacent
    

def doRaid(m,player):
    adj = adjacentTo(m)
    raid_ho_sakta_kya = False
    raid_kiya = False
    raidedTiles = []
    for x in adj:
        if(board[x[0]][x[1]]==player):
            raid_ho_sakta_kya = True
    if(raid_ho_sakta_kya == True):
        for x in adj:
            if(board[x[0]][x[1]]==flip(player)):
                board[x[0]][x[1]] = player          
                raidedTiles.append([x[0],x[1]])
                raid_kiya = True
    return raid_kiya, raidedTiles 
    
def checkRaid(m,player):
    adj = adjacentTo(m)
    raid_ho_sakta_kya = False
    raid_kiya = False
    for x in adj:
        if(board[x[0]][x[1]]==player):
            raid_ho_sakta_kya = True
    if(raid_ho_sakta_kya == True):
        for x in adj:
            if(board[x[0]][x[1]]==flip(player)):
                raid_kiya = True
    return raid_kiya

    
def reverseRaid(m, player, raidedTiles):
    for tile in raidedTiles:
        if(board[tile[0]][tile[1]] == player):
            board[tile[0]][tile[1]] = flip(player)

    
def flip(player_mark):
    if(player_mark=="X"):
        return "O"
    if(player_mark=="O"):
        return "X"


def chooseMoveMin(side,depth,score):
    myBest = Best()
    reply = Best()
    full = True
    raidMoves=[]
    
    for i in range(size):
        for j in range(size):
            if(board[i][j] == '.'):
                full = False  

    if(full==True or depth==0):
        newBest = Best()
        newBest.score = score
        return newBest
    
    if(side == COMPUTER):
        myBest.score = -9999999
    if(side == HUMAN):
        myBest.score = 9999999

    allMoves = legalMoves(board)

    for m in allMoves:
        if(checkRaid(m,side)==True):
            raidMoves.append(m)

    for m in allMoves:
        board[m[0]][m[1]]=side
        score=evaluation(board)
        reply = chooseMoveMin(flip(side),depth-1, score)
        board[m[0]][m[1]]="."
            
        if(side==COMPUTER and reply.score > myBest.score):
            myBest.score = reply.score
            myBest.move = m
            myBest.movetype="Stake"
        
        if(side==HUMAN and reply.score < myBest.score):
            myBest.move = m
            myBest.score = reply.score
            myBest.movetype="Stake"
                
    for r in raidMoves:
        board[r[0]][r[1]]=side
        raided, raidedTiles = doRaid(r,side)
        score=evaluation(board)
        reply = chooseMoveMin(flip(side),depth-1, score)
        
        if(raided == True):
            reverseRaid(r, side, raidedTiles)

        board[r[0]][r[1]]="."
            
        if(side==COMPUTER and reply.score > myBest.score):
            myBest.score = reply.score
            myBest.move = r
            if(raided == True):
                myBest.movetype="Raid"
            
            else:
                myBest.movetype="Stake"
        
        if(side==HUMAN and reply.score < myBest.score):
            myBest.move = r
            myBest.score = reply.score
            if(raided == True):
                myBest.movetype="Raid"    
            
            else:
                myBest.movetype="Stake"
        
    return myBest


def chooseMoveAlpha(side,depth,score,alpha,beta):
    myBest = Best()
    reply = Best()
    full = True
    raidMoves = []
    
    for i in range(size):
        for j in range(size):
            if(board[i][j] == '.'):
                full = False  

    if(full==True or depth==0):
        newBest = Best()
        newBest.score = score
        return newBest
    
    if(side == COMPUTER):
        alpha=float("-inf")
        myBest.score= alpha

    if(side == HUMAN):
        beta=float("inf")
        myBest.score= beta
        
    allMoves = legalMoves(board)

    for m in allMoves:
        if(checkRaid(m,side)==True):
            raidMoves.append(m)
        
    for m in allMoves:
        board[m[0]][m[1]]=side
        score=evaluation(board)
        reply = chooseMoveAlpha(flip(side),depth-1, score,alpha,beta)
        reply.movetype="Stake"
        board[m[0]][m[1]]="."
            
        if(side==COMPUTER and reply.score > myBest.score):
            myBest.score = reply.score
            alpha = reply.score
            myBest.move = m
            myBest.movetype="Stake"
       
        if(side==HUMAN and reply.score < myBest.score):
            myBest.score = reply.score
            beta = reply.score
            myBest.move = m
            myBest.movetype="Stake"
                    
        if (beta<=alpha):
            return myBest
            
    for r in raidMoves:
        board[r[0]][r[1]]=side
        raided, raidedTiles = doRaid(r,side)
        score=evaluation(board)
        reply = chooseMoveAlpha(flip(side),depth-1, score,alpha,beta)

        if(raided == True):
            reverseRaid(r, side, raidedTiles)   
            
        board[r[0]][r[1]]="."
            
        if(side==COMPUTER and reply.score > myBest.score):
            myBest.score = reply.score
            alpha = reply.score
            myBest.move = r
            myBest.movetype="Raid"
       
        if(side==HUMAN and reply.score < myBest.score):
            myBest.score = reply.score
            beta = reply.score
            myBest.move = r
            myBest.movetype="Raid"
                    
        if (beta<=alpha):
            return myBest

    return myBest

open("output.txt", 'w').close()
mode=str(mode)
if(mode=="MINIMAX"):
    a=chooseMoveMin(COMPUTER,max_depth,-9999999)
    ascii_move = a.move[1]+65
    col = chr(ascii_move)
    row = a.move[0]+1
    print(col+str(row)+" "+a.movetype)
    op = open("output.txt","a+")
    op.write(col+str(row)+" "+a.movetype+"\n")
    backup_board[a.move[0]][a.move[1]]=player
    if(a.movetype=="Raid"):
        doRaid(a.move,player)
    for i in range(size):
        for j in range(size):
            print(backup_board[i][j],end="")
            op.write(backup_board[i][j])
        op.write("\n")
        print()
    op.close()
    


if(mode=="ALPHABETA"):
    a=chooseMoveAlpha(COMPUTER,max_depth,-9999999,alpha,beta)
    ascii_move = a.move[1]+65
    col = chr(ascii_move)
    row = a.move[0]+1
    print(col+str(row)+" "+a.movetype)
    op = open("output.txt","a+")
    op.write(col+str(row)+" "+a.movetype+"\n")
    backup_board[a.move[0]][a.move[1]]=player
    if(a.movetype=="Raid"):
        doRaid(a.move,player)
    for i in range(size):
        for j in range(size):
            print(backup_board[i][j],end="")
            op.write(backup_board[i][j])
        op.write("\n")
        print()
    op.close()