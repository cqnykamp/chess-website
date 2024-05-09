
const boardScreenHeightUsage = 0.65;

// The gameboard should never take up more than this percentage of the screen width
const boardMaxScreenWidthUsage = 0.8;

var moveCount = 0;


function getStaticFolderURL() {
    let staticFolderURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port
                    + '/static';
    return staticFolderURL;
}


function loadPage() {
    drawBoard();
}


/**
 * Convert from the symbols the API returns to chess pieces names
 */
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

/**
 * Convert from chess pieces names to image relative paths
 */
function chessPieceImageHTML(pieceName) {
    return `<img src='${getStaticFolderURL()}/images/${pieceName}.png' />`;
}



function drawBoard() {
    
    let screenHeight = window.innerHeight;
    let screenWidth = window.innerWidth;

    let heightConstraint = screenHeight * boardScreenHeightUsage;
    let widthConstraint = screenWidth * boardMaxScreenWidthUsage;

    let boardSize = Math.min(widthConstraint, heightConstraint);

    let squareSize = boardSize / 8;

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


function setMove(move) {
if(move < boardPositions.length && move >= 0) {
    moveCount = move;
    document.getElementById("turn-counter").innerHTML = moveCount;
    drawBoard();
}

}

function nextTurn() {
    if(moveCount + 1 < boardPositions.length) {
        moveCount += 1;
        document.getElementById("turn-counter").innerHTML = moveCount;
        drawBoard();
    }
}

function previousTurn() {
    if(moveCount > 0) {
        moveCount -= 1;
        document.getElementById("turn-counter").innerHTML = moveCount;
        drawBoard();
    }
}

var intervalForward;
var intervalBack;


function startMovingForward() {
    stopMoving();
    nextTurn();
    intervalForward = setInterval(nextTurn, 200);
}

function startMovingBackward() {
    stopMoving();
    previousTurn();
    intervalForward = setInterval(previousTurn, 200);
}


function stopMoving() {
    clearInterval(intervalForward);
    clearInterval(intervalBack);
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