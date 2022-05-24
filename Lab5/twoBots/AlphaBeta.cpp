#include "Othello.h"
#include "OthelloBoard.h"
#include "OthelloPlayer.h"
#include <cstdlib>
#include <climits>
#include <chrono>

using namespace std;
using namespace Desdemona;

auto start = chrono::steady_clock::now();
int time_taken() {
    return ( chrono::duration_cast<chrono::milliseconds>(chrono::steady_clock::now() - start).count() );
}


class MyBot: public OthelloPlayer
{
    public:
        MyBot( Turn turn );
        virtual Move play(const OthelloBoard& board );
        virtual int AlphaBeta(OthelloBoard& board, Turn turn, int depth, Move move, int alpha, int beta);
        virtual int heuristicValue( OthelloBoard &board);
    private:
};

MyBot::MyBot( Turn turn ) : OthelloPlayer( turn ){}

Move MyBot::play(const OthelloBoard& board)
{
    start = chrono::steady_clock::now();
    list<Move> moves = board.getValidMoves( turn );
    Move BestMove = *(moves.begin());
    int BestScore = INT_MIN; 
    int MaxDepth = 0;
    while(++MaxDepth) {
        for (Move move: moves) {
            OthelloBoard newBoard = OthelloBoard(board);
            int hValue = AlphaBeta(newBoard, this->turn, MaxDepth, move, INT_MIN, INT_MAX);
            if(hValue == INT_MIN) { 
                return BestMove;
            }
            if(hValue > BestScore) { 
                BestMove = move; 
                BestScore = hValue;
            }
        } 
    }
    return BestMove;
}

int MyBot::AlphaBeta(OthelloBoard& board, Turn turn, int depth, Move move, int alpha, int beta) {
    if(time_taken() > 1600) {
        return INT_MIN;
    }
    OthelloBoard newBoard = OthelloBoard(board);
    newBoard.makeMove(turn, move);
    list<Move> moves = newBoard.getValidMoves(other(turn));
    if(depth == 0) {
        return heuristicValue(newBoard);
    }
    if(this->turn == turn) {  
        int best = INT_MAX;
        for (Move eachMove: moves) {
            int hValue = alpha_beta(newBoard, other(turn), depth-1, eachMove, alpha, beta);
            best = min(hValue, best); 
            beta = min(best, beta); 
            if (beta <= alpha) break;
        }  
        return best;
    } else {
        int best = INT_MIN;
        for (Move eachMove: moves) {
            int hValue = alpha_beta(newBoard, other(turn), depth-1, eachMove, alpha, beta);
            if(hValue == INT_MIN){
                return INT_MIN;
            }
            best = max(hValue, best); 
            alpha = max(best, alpha);  
            if (beta <= alpha) 
                break; 
        }  
        return best;
    }
}

int MyBot::heuristicValue(OthelloBoard &board) {

    int xCoord[] = {0, 0, 7, 7};
    int yCoord[] = {0, 7, 0, 7};
    int noOfMyCorners = 0, noOfOpponentCorners = 0;
    int noOfMyMoves = board.getValidMoves(this->turn).size();
    int noOfOpponentMoves = board.getValidMoves(other(this->turn)).size();
    int heuristic = 0;
    if(this->turn == BLACK) heuristic = heuristic + board.getBlackCount() - board.getRedCount();
    else heuristic = heuristic + board.getRedCount() - board.getBlackCount();
    for (int i = 0; i < 4; ++i) {
        if (board.get(xCoord[i], yCoord[i]) == this->turn)
            noOfMyCorners++;
        else if (board.get(xCoord[i], yCoord[i]) == other(this->turn))
            noOfOpponentCorners++;
    }
    heuristic = heuristic + noOfMyCorners - noOfOpponentCorners;
    heuristic = heuristic + ( noOfMyMoves  - noOfOpponentMoves );
    return heuristic;
}

extern "C" {
    OthelloPlayer* createBot( Turn turn ) {
        return new MyBot( turn );
    }
    void destroyBot( OthelloPlayer* bot ) {
        delete bot;
    }
}

