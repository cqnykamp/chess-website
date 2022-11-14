
const boardScreenHeightUsage = 0.65;

// The gameboard should never take up more than this percentage of the
// screen width
const boardMaxScreenWidthUsage = 0.8;

var moveCount = 0;


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


function loadPage() {

    let moves_elem = document.getElementById("moves-list");
    
    let moves_formatted = "<ol>";
    for(let move of moves_elem.innerHTML.split(" ")) {
        moves_formatted += `<li>${move}</li>`;
    }
    moves_formatted += "</ol>";

    moves_elem.innerHTML = moves_formatted;



    // console.log(capturedPieces);


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

function chessPieceImageHTML(pieceName) {
    return `<img src='${getStaticFolderURL()}/images/${pieceName}.png' />`;
}



function drawBoard() {

    // let board = initialBoardPosition();

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


    let board = boardPositions[moveCount].split("/");

    let squares = "";
    for(let row=0; row<board.length; row++) {
        let rowHtml = `<tr class="board_row">`;

        for(let col=0; col<board[0].length; col++) {
            
            let possibleImage = "";
            let pieceName = symbolToImageName(board[row][col]);

            if(pieceName != null) {
                possibleImage = chessPieceImageHTML(pieceName);
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


    document.getElementById("gameboard").innerHTML = squares;




    let currentCapturedPieces = "";
    for(let i=0; i< moveCount; i++) {
        currentCapturedPieces += capturedPieces[i];
    }

    let captured = ""

    if(currentCapturedPieces == "") {
        captured = "<em>None</em>";
    } else {
        for(let pieceSymbol of currentCapturedPieces) {
            captured += chessPieceImageHTML(symbolToImageName(pieceSymbol));
        }
    }

    document.getElementById("captured").innerHTML = captured;



    let moves = document.getElementById("moves-list").children[0].children;

    for(let i=0; i < moveCount; i++) {
        moves[i].classList.add(["played"])
    }

    for(let i=moveCount; i < moves.length; i++) {
        moves[i].classList.remove(["played"])
    }

}


function nextTurn() {
    if(moveCount + 1 < boardPositions.length) {
        moveCount += 1;
        document.getElementById("turn-counter").innerHTML = moveCount;
        drawBoard()
    }
}

function previousTurn() {
    if(moveCount > 0) {
        moveCount -= 1;
        document.getElementById("turn-counter").innerHTML = moveCount;
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