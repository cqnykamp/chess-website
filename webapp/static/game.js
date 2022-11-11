
const boardScreenHeightUsage = 0.65;

// The gameboard should never take up more than this percentage of the
// screen width
const boardMaxScreenWidthUsage = 0.8;


function initialBoardPosition() {
    let board = Array.from({ length: 8 }, () => 
    Array.from({ length: 8 }, () => "")
    );

    let special_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook'];
    for(let [id, piece] of special_pieces.entries()) {
        board[0][id] = piece + '-white';
    }
    for(let [id, piece] of special_pieces.entries()) {
        board[7][id] = piece + '-black';
    }

    board[1] = Array.from({length: 8}, () => 'pawn-white')
    board[6] = Array.from({length: 8}, () => 'pawn-black')

    return board;
}


/**
 * Given a move such as Nxf3+, find which piece we're referring to by finding its position before the move
 * Returns (y-pos, x-pos) as indices
 * @param move the move string
 */
function findMovingPiecePosition(move) {

    unparsedMove 

    let pieceType;
    if(move[0] == 'K') {
        pieceType = 'king';

    } else if(move[0] == 'Q') {
        pieceType = 'queen';
    } else if(move[0] == 'R') {
        pieceType = 'rook';
    } else if(move[0] == 'B') {
        pieceType = 'bishop';
    } else if(move[0] == 'N') {
        pieceType = 'knight';
    } else {
        // no letter
        pieceType = 'pawn';
    }



}


var pieceLetterToName = {
    'K': 'king',
    'Q': 'queen',
    'R': 'rook',
    'B': 'bishop',
    'N': 'knight',

    // otherwise pawn
}

var colLetterToIndex = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7,
};


function chessNotationToIndex(move) {
    let colLetter = move[0];
    let rowNum = move[1];
    let extra = move.substring(2);

    console.log(`Column: ${colLetter} row: ${rowNum} extra: ${extra}`);

    return (colLetterToIndex[colLetter], Number(rowNum), extra);
}


function boardPositionFrom(moves) {
    let board = initialBoardPosition();

}



function draw() {


    chessNotationToIndex('c4');

    let board = initialBoardPosition();


    let gameboard = document.getElementById("gameboard");
    // console.log(gameboard);

    // let screenHeight = document.body.clientHeight;
    // let screenWidth = document.body.clientWidth;
    let screenHeight = window.innerHeight;
    let screenWidth = window.innerWidth;

    console.log(`Screen size is ${screenWidth} wide and ${screenHeight} tall`);

    let heightConstraint = screenHeight * boardScreenHeightUsage;
    let widthConstraint = screenWidth * boardMaxScreenWidthUsage;

    let boardSize = Math.min(widthConstraint, heightConstraint);

    let squareSize = boardSize / 8;
    console.log(`Square size is ${squareSize}`);


    let squares = "";
    for(let row=0; row<board.length; row++) {
        let rowHtml = `<tr class="board_row">`;

        for(let col=0; col<board[0].length; col++) {
            
            let possibleImage = "";
            if(board[row][col] != "") {
                possibleImage = `<img src='../static/images/${board[row][col]}.png' />`;

            }

            let squareColor = ((row + col) % 2 == 1) ? 'white-square' : 'black-square';

            rowHtml += `<td id='square_${row}_${col}'
                class="${squareColor}"
                style="width: ${squareSize}px; height: ${squareSize}px;">
                    ${possibleImage}
            </td>`;

            // rowHtml += `<td id='square_${row}_${col}'
            //     class="${squareColor}"
            //         ${possibleImage}
            // </td>`;

        }
        rowHtml += `</tr>`;
        squares = rowHtml + squares;
    }

    gameboard.innerHTML = squares;
}

window.onload = draw;
window.onresize = () => draw();
