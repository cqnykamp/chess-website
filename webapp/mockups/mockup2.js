
// var board = initialBoardPosition();

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

const boardScreenHeightUsage = 0.65;

// The gameboard should never take up more than this percentage of the
// screen width
const boardMaxScreenWidthUsage = 0.8;


function drawBoard() {

    let gameHeading = document.getElementById("game-heading");

    let board = initialBoardPosition();

    let gameboard = document.getElementById("gameboard");
    console.log(gameboard);

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


    gameHeading.style.width = `${boardSize}px`;
    gameHeading.style.fontSize = `${boardSize / 15}px`;


    let squares = "";
    for(let row=0; row<board.length; row++) {
        let rowHtml = `<div class="board_row">`;

        for(let col=0; col<board[0].length; col++) {
            
            let possibleImage = "";
            if(board[row][col] != "") {
                possibleImage = `<img src='chess-piece-images/${board[row][col]}.png' />`;

            }

            let backgroundColor = ((row + col) % 2 == 1) ? 'white' : 'grey';

            rowHtml += `<div id='square_${row}_${col}'
                class="game-square"
                style="width: ${squareSize}px; height: ${squareSize}px; background-color: ${backgroundColor};">
                    ${possibleImage}
            </div>`;
        }
        rowHtml += `</div>`;
        squares = rowHtml + squares;
    }

    gameboard.innerHTML = squares;
}

window.onload = drawBoard;
window.onresize = () => drawBoard();
