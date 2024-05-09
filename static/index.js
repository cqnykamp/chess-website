
// Stores the most recent result from calling the API
var gamesData = []
var visibleRows = 0

const PAGE_SIZE = 50;


function getBaseURL() {
    return window.location.protocol
        + '//' + window.location.hostname
        + ':' + window.location.port;
    
}

function getAPIBaseURL() {
    return getBaseURL() + '/api';
}


/**
 * Set up event listeners for input boxes and search button
 */
function initialize() {
    var button = document.getElementById('searchbutton');
    button.onclick = onSearch;

    document.getElementById("user_search").addEventListener("keyup", handleSearchKeyUp);
    document.getElementById("below_rate_search").addEventListener("keyup", handleSearchKeyUp);
    document.getElementById("above_rate_search").addEventListener("keyup", handleSearchKeyUp);

    document.getElementById("opening_name_search").addEventListener("keyup", handleSearchKeyUp);
    document.getElementById("opening_moves_search").addEventListener("keyup", handleSearchKeyUp);

    document.getElementById("moves_search").addEventListener("keyup", handleSearchKeyUp);
    document.getElementById("movenumb_search").addEventListener("keyup", handleSearchKeyUp);

    document.getElementById("checks_search").addEventListener("keyup", handleSearchKeyUp);
    document.getElementById("captures_search").addEventListener("keyup", handleSearchKeyUp);
    document.getElementById("promotions_search").addEventListener("keyup", handleSearchKeyUp);
    document.getElementById("castles_search").addEventListener("keyup", handleSearchKeyUp);
    document.getElementById("en_passants_search").addEventListener("keyup", handleSearchKeyUp);

    let winnerOptions = document.getElementsByName("winner-search");
    for(let option of winnerOptions) {
        option.addEventListener("keyup", handleSearchKeyUp);
    }
}

/**
 * Event listener for search input elements.
 * Enter key pressed while focusing on input element starts the search.
 * @param {} e 
 */
function handleSearchKeyUp(e) {
    if(e.keyCode == 13) {
        //Enter
        onSearch();
    }
}




/**
 * Generate the url parameters from a dictionary of key-values
 * Only includes key if value is non-empty
 * @param {*} search_parameters
 * @returns url parameters string
 */
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


/**
 * Gather the input data from the DOM elements and enact API call with them
 */
function onSearch() {

    let opening_moves_unparsed = document.getElementById("opening_moves_search").value;
    let opening_moves = opening_moves_unparsed.replace("+", "%2B").replace(" ", "+");

    let moves_unparsed = document.getElementById("moves_search").value;
    let moves = moves_unparsed.replace("+", "%2B").replace(" ", "+");

    let winnerelems = document.getElementsByName("winner-search");
    let winner = "";
    for(let elem of winnerelems) {
        if(elem.checked) {
            winner = elem.value;
        }
    }

    var parameters = {
        // These keys should match the API parameter names
        user: document.getElementById('user_search').value, 
        rating_min: document.getElementById("below_rate_search").value,
        rating_max:  document.getElementById("above_rate_search").value,
    
        opening_moves: opening_moves,
        opening_name: document.getElementById("opening_name_search").value, 

        moves: moves,
        turns: document.getElementById("movenumb_search").value, 

        checks: document.getElementById("checks_search").value,
        captures: document.getElementById("captures_search").value,
        promotions: document.getElementById("promotions_search").value,
        castles: document.getElementById("castles_search").value,
        en_passants: document.getElementById("en_passants_search").value,

        winner: winner,

        // page_size: 10,
        // page_id: 0,
    };

    callApiAndUpdateResults(parameters);
}

/**
 * Given a parameters object, construct the API url with those key-values,
 * send the request, and display contents in DOM when server responds
 * @param {*} parameters 
 */
function callApiAndUpdateResults(parameters) {

    var url = getAPIBaseURL() + '/games' + urlExtend(parameters);
    console.log("search with url " + url);

    document.getElementById('searchResults').innerHTML = `<h1 class='panel without-space-below'>Loading...</h1>`;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(games) {

        // Make returned data globally accessible by this script
        gamesData = games;

        // Reset counter for the number of rows the results table is displaying
        visibleRows = 0;

        var searchResultsElement = document.getElementById('searchResults');

        if(games.length > 0) {
            // Display results table with corresponding headers
            searchResultsElement.innerHTML = `
            <h1 class='panel without-space-below'>Results (${games.length})</h1>
            <table>
                <tr>
                    <th></th>
                    <th>Game</th>
                    <th>Openings</th>
                    <th>Stats</th>
                </tr>
            </table>`;

            loadMoreResults();

        } else {
            // No results
            searchResultsElement.innerHTML = `<h1 class='panel without-space-below'>No results found</h1>`;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}


function generateTableRows(games) {

    var resultsData = '';
    for (let game of games) {

        let outcome_description = (game.winner=='draw' ? 'draw' : game.winner+" won by "+game.victory_status);

        // One table row in the results table
        resultsData += `<tr>
            <td><a href='${ getBaseURL() }/game/${ game.game_id }'>View</td>
            <td>
            <h3>${game.white_username} (${game.white_rating}) vs ${game.black_username} (${game.black_rating})</h3>
                ${game.turns} ${game.turns == 1? 'turn' : 'turns' },
                ${outcome_description},
                ${game.increment_code}
                ${game.rated_status == 'true' ? 'rated' : 'not rated'}
            </td>
            <td>
                ${game.opening_names.join("<br>")}
            </td>
            <td>
                <div>Checks: ${game.checks}</div>
                <div>Captures: ${game.captures}</div>
                <div>Promotions: ${game.promotions}</div>
                <div>Castles: ${game.castles}</div>
                <div>En passants: ${game.en_passants}</div>
            </td>

        </a></tr>\n`;

    }

    return resultsData;
}


function loadMoreResults() {
    let table = document.getElementById('searchResults').getElementsByTagName('table')[0];
    let newRows = generateTableRows(gamesData.slice(visibleRows, visibleRows + PAGE_SIZE));
    table.innerHTML += newRows;

    visibleRows = Math.min(gamesData.length, visibleRows + PAGE_SIZE);

    let moreResults = document.getElementById("more-results");
    moreResults.innerHTML = (gamesData.length > visibleRows) ? `<button onclick='loadMoreResults();'>More results</button>` : '';
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
};
