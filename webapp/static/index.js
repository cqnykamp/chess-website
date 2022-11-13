

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


function onSearch() {

    // console.log('Search button clicked');
    var parameters = {
        // These keys should match the API parameter names
        user: document.getElementById('user_search').value, 
        opening_moves: document.getElementById("startmove_search").value, 
        turns: document.getElementById("movenumb_search").value, 
        rating_max:  document.getElementById("above_rate_search").value,
        rating_min: document.getElementById("below_rate_search").value,

        page_size: 10,
        page_id: 0,
    };

    // console.log(parameters);

    var url = getAPIBaseURL() + '/gameslist' + urlExtend(parameters);

    // console.log("url is");
    // console.log(url);

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(games) {
        // console.log(games)
        var listBody = '';
        for (let game of games) {
            var game_id = game.game_id

            listBody += `<li><a href=` + getBaseURL() +'/game/'+game_id+ `>${ game['white_username'] } vs ${ game['black_username'] }</li>\n`;

        }

        var searchResultsElement = document.getElementById('searchResults');
        if (searchResultsElement) {
            searchResultsElement.innerHTML = listBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

function initialize() {
    var button = document.getElementById('searchbutton');
    button.onclick = onSearch;
}

// This causes initialization to wait until after the HTML page and its
// resources are all ready to go, which is often what you want. This
// "window.onload" approach is a bit old-fashioned. See
// https://www.dyn-web.com/tutorials/init.php for an interesting and
// brief discussion of problems with this old-fashioned approach that
// can become relevant with more complex web pages than the ones
// we are writing.
window.onload = initialize;
