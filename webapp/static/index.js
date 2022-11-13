

function getAPIBaseURL() {
    var baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port
                    + '/api';
    return baseURL;
}
function urlExtend(search_parameters){
    var extension = "?";
    if (search_parameters.user){
        extension += "user="+search_parameters.user;
    }
    if(search_parameters.move){
        extension+="startmove="+search_parameters.move
    }
    if(search_parameters.turns){
        extension+="turn="+search_parameters.turns
    }
    if(search_parameters.rate_below){
        extension+="rating_min="+search_parameters.rate_below
    }
    if(search_parameters.rate_above){
        extension+="rating_max="+search_parameters.rate_above
    }
    if(extension !== "?"){
        return extension;
    }
    return "";
}


function onSearch() {

    console.log('Search button clicked');
    var parameters = {user:document.getElementById('user_search').value, 
    move:document.getElementById("startmove_search").value, 
    turns:document.getElementById("movenumb_search").value, 
    rate_above: document.getElementById("above_rate_search").value,
    rate_below:document.getElementById("below_rate_search").value};

    var url = getAPIBaseURL() + '/gameslist'+urlExtend(parameters);


    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(games) {
        console.log(games)
        var listBody = '';
        for (let game of games) {
            var game_id = game.game_id

            listBody += `<li><a href=` + baseURL+'/game/'+game_id+ `>${ game['white_username'] } vs ${ game['black_username'] }</li>\n`;

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
