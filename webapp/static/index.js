

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

    // console.log('Search button clicked');
    var parameters = {
        // These keys should match the API parameter names
        user: document.getElementById('user_search').value, 
        opening_moves: document.getElementById("startmove_search").value, 
        turns: document.getElementById("movenumb_search").value, 
        rating_max:  document.getElementById("above_rate_search").value,
        rating_min: document.getElementById("below_rate_search").value,

        // page_size: 10,
        page_id: 0,
    };

    search(parameters);
}


function search(parameters) {

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

            // listBody += `<tr>
            //     <td>${game['white_username'] }</td>
            //     <td>${game['white_rating']}</td>
            //     <td>${game['black_username'] }</td>
            //     <td>${game['black_rating']}</td>
            //     <td>${game['turns']}</td>
            //     <td>${game['victory_status']}</td>
            //     <td>${game['winner']}</td>
            //     <td>${game['rated_status']}</td>
            //     <td>${game['opening_name']}</td>
            //     <td>${game['increment_code']}</td>

            //     <td class='details'><a href='${ getBaseURL() }/game/${ game_id }'>View</td>

            // </a></tr>\n`;

            let outcome = 'draw'
            if(game.winner != 'draw') {
                outcome = game.winner + " won by " + game.victory_status;
            }

            listBody += `<tr>
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
                    Checks: ${game.checks}<br/>
                    Captures: ${game.captures}<br/>
                    Promotions: ${game.promotions}<br/>
                    En passants: ${game.en_passants}
                </td>

                <td class='details'><a href='${ getBaseURL() }/game/${ game_id }'>View</td>

            </a></tr>\n`;            

        }

        var searchResultsElement = document.getElementById('searchResults');
        if (searchResultsElement) {

            searchResultsElement.innerHTML = `<table>
                <tr>
                    <th>Game</th>
                    <th>Opening</th>
                    <th>Stats</th>

                    <th class='details'>Details</th>
                </tr>
                ${listBody}
            </table>`;




            // searchResultsElement.innerHTML = `<table>
            //     <tr>
            //         <th>White username</th>
            //         <th>White rating</th>
            //         <th>Black username</th>
            //         <th>Black rating</th>
            //         <th>Turns</th>
            //         <th>Victory status</th>
            //         <th>Winner</th>
            //         <th>Rated</th>
            //         <th>Opening</th>
            //         <th>Increment</th>

            //         <th class='details'>Details</th>
            //     </tr>
            //     ${listBody}
            // </table>`;


        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

function initialize() {
    var button = document.getElementById('searchbutton');
    button.onclick = onSearchButtonClicked;
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
