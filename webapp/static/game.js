
const boardScreenHeightUsage = 0.65;

// The gameboard should never take up more than this percentage of the
// screen width
const boardMaxScreenWidthUsage = 0.8;

var currentTurn = 1;


function getStaticFolderURL() {
    let staticFolderURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port
                    + '/static';
    return staticFolderURL;
}


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

    // console.log(`Column: ${colLetter} row: ${rowNum} extra: ${extra}`);

    return (colLetterToIndex[colLetter], Number(rowNum), extra);
}


function boardPositionFrom(moves) {
    let board = initialBoardPosition();
}


function loadPage() {

    let moves_elem = document.getElementById("moves-list");
    
    let moves_formatted = "<ol>";
    for(let move of moves_elem.innerHTML.split(" ")) {
        moves_formatted += `<li>${move}</li>`;
    }
    moves_formatted += "</ol>";

    moves_elem.innerHTML = moves_formatted;



    // console.log(boardPositions)


    drawBoard();
}


function symbolToImageName(symbol) {
    switch(symbol) {
        case 'P': return 'pawn-white';
        case 'R': return 'rook-white';
        case 'N': return 'knight-white';
        case 'B': return 'bishop-white';
        case 'Q': return 'queen-white';
        case 'K': return 'king-white';
        case 'p': return 'pawn-black';
        case 'r': return 'rook-black';
        case 'n': return 'knight-black';
        case 'b': return 'bishop-black';
        case 'q': return 'queen-black';
        case 'k': return 'king-black';

        default: return null;
    }
}



function drawBoard() {

    // let board = initialBoardPosition();


    let gameboard = document.getElementById("gameboard");

    // let screenHeight = document.body.clientHeight;
    // let screenWidth = document.body.clientWidth;
    let screenHeight = window.innerHeight;
    let screenWidth = window.innerWidth;
    // console.log(`Screen size is ${screenWidth} wide and ${screenHeight} tall`);

    let heightConstraint = screenHeight * boardScreenHeightUsage;
    let widthConstraint = screenWidth * boardMaxScreenWidthUsage;

    let boardSize = Math.min(widthConstraint, heightConstraint);

    let squareSize = boardSize / 8;
    // console.log(`Square size is ${squareSize}`);


    let board = boardPositions[currentTurn-1].split("/");

    let squares = "";
    for(let row=0; row<board.length; row++) {
        let rowHtml = `<tr class="board_row">`;

        for(let col=0; col<board[0].length; col++) {
            
            let possibleImage = "";
            let pieceName = symbolToImageName(board[row][col]);

            if(pieceName != null) {
                possibleImage = `<img src='${getStaticFolderURL()}/images/${pieceName}.png' />`;
            }
            
            let squareColor = ((row + col) % 2 == 1) ? 'white-square' : 'black-square';

            rowHtml += `<td id='square_${row}_${col}'
                class="${squareColor}"
                style="width: ${squareSize}px; height: ${squareSize}px;">
                    ${possibleImage}
            </td>`;

        }
        rowHtml += `</tr>`;
        squares += rowHtml;
    }

    gameboard.innerHTML = squares;
}

//remember currentTurn is 1-indexed 

function nextTurn() {
    if(currentTurn < boardPositions.length - 1) {
        currentTurn += 1;
        document.getElementById("turn-counter").innerHTML = currentTurn;
        drawBoard()
    }
}

function previousTurn() {
    if(currentTurn > 1) {
        currentTurn -= 1;
        document.getElementById("turn-counter").innerHTML = currentTurn;
        drawBoard()
    }
}


window.onload = loadPage;
window.onresize = drawBoard;

document.onkeydown = function(event) {
    if(event.key == "ArrowLeft") {
        previousTurn()
    } else if(event.key == "ArrowRight") {
        nextTurn()
    }
}