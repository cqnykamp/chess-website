

var gamesData = []

function getBaseURL() {
    return window.location.protocol
        + '//' + window.location.hostname
        + ':' + window.location.port;
    
}

function getAPIBaseURL() {
    return getBaseURL() + '/api';
}


function urlExtend(search_parameters){
    var extension = "";

    for(let key in search_parameters) {
        value = search_parameters[key];

        if(value !== "") {
            if(extension === "") {
                extension += "?" + key + "=" + value;
            } else {
                extension += "&" + key + "=" + value;
            }
        }
    }

    return extension;
}


function onSearchButtonClicked() {

    let opening_moves_unparsed = document.getElementById("opening_moves_search").value;
    let opening_moves = opening_moves_unparsed.replace("+", "%2B").replace(" ", "+");

    let moves_unparsed = document.getElementById("moves_search").value;
    let moves = moves_unparsed.replace("+", "%2B").replace(" ", "+");

    // console.log('Search button clicked');
    var parameters = {
        // These keys should match the API parameter names
        user: document.getElementById('user_search').value, 
        opening_moves: opening_moves,
        moves: moves,
        opening_name:  document.getElementById("opening_name_search").value, 
        turns: document.getElementById("movenumb_search").value, 
        rating_max:  document.getElementById("above_rate_search").value,
        rating_min: document.getElementById("below_rate_search").value,

        // page_size: 10,
        page_id: 0,
    };

    search(parameters);
}


function search(parameters) {

    console.log("search");

    // console.log(parameters);

    var url = getAPIBaseURL() + '/games' + urlExtend(parameters);

    // console.log("url is");
    // console.log(url);

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(games) {

        console.log("Response received");
        gamesData = games;

        // console.log(games)
        var listBody = '';
        for (let game of games) {
            var game_id = game.game_id

            let outcome = 'draw'
            if(game.winner != 'draw') {
                outcome = game.winner + " won by " + game.victory_status;
            }

            listBody += `<tr>
                <td><a href='${ getBaseURL() }/game/${ game_id }'>View</td>
                <td>
                <h3>${game.white_username} (${game.white_rating}) vs ${game.black_username} (${game.black_rating})</h3>
                    ${game.turns} ${game.turns == 1? 'turn' : 'turns' },
                    ${outcome},
                    ${game.rated_status == 'true' ? 'rated' : 'not rated'},
                    ${game.increment_code}
                </td>
                <td>
                    ${game.opening_names.join("<br>")}
                </td>
                <td>
                    
                    <div>
                        <div>Checks: ${game.checks}</div>
                        <div>Captures: ${game.captures}</div>
                        <div>Promotions: ${game.promotions}</div>
                        <div>En passants: ${game.en_passants}</div>
                    </div>

                </td>

            </a></tr>\n`;            

        }

        var searchResultsElement = document.getElementById('searchResults');
        if (searchResultsElement) {

            searchResultsElement.innerHTML = `
            <h1 class='panel without-space-below'>Results</h1>
            <table>
                <tr>
                    <th></th>
                    <th>Game</th>
                    <th>Openings</th>
                    <th>Stats</th>
                </tr>
                ${listBody}
            </table>`;



        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

function initialize() {
    var button = document.getElementById('searchbutton');
    button.onclick = onSearchButtonClicked;

    document.getElementById("user_search").addEventListener("keyup", handleSearchKeyDown);
    document.getElementById("below_rate_search").addEventListener("keyup", handleSearchKeyDown);
    document.getElementById("above_rate_search").addEventListener("keyup", handleSearchKeyDown);

    document.getElementById("opening_name_search").addEventListener("keyup", handleSearchKeyDown);
    document.getElementById("opening_moves_search").addEventListener("keyup", handleSearchKeyDown);

    document.getElementById("moves_search").addEventListener("keyup", handleSearchKeyDown);
    document.getElementById("movenumb_search").addEventListener("keyup", handleSearchKeyDown);

    document.getElementById("checks_search").addEventListener("keyup", handleSearchKeyDown);
    document.getElementById("captures_search").addEventListener("keyup", handleSearchKeyDown);
    document.getElementById("castles_search").addEventListener("keyup", handleSearchKeyDown);
    document.getElementById("en_passants_search").addEventListener("keyup", handleSearchKeyDown);

}


function handleSearchKeyDown(e) {
    if(e.keyCode == 13) {
        //Enter
        onSearchButtonClicked();
    }
}


// This causes initialization to wait until after the HTML page and its
// resources are all ready to go, which is often what you want. This
// "window.onload" approach is a bit old-fashioned. See
// https://www.dyn-web.com/tutorials/init.php for an interesting and
// brief discussion of problems with this old-fashioned approach that
// can become relevant with more complex web pages than the ones
// we are writing.
window.onload = () => {
    initialize();
    search({page_id: 0});
};
