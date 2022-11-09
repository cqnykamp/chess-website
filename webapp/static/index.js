

function getAPIBaseURL() {
    var baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port
                    + '/api';
    return baseURL;
}

function onSearch() {

    console.log('Search button clicked');

    var url = getAPIBaseURL() + '/gameslist';

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(games) {

        var listBody = '';
        for (let game of games) {

            listBody += `<li>${ game['white_username'] } vs ${ game['black_username'] }</li>\n`;

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
