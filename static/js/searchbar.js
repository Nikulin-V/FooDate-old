let searchbar = document.getElementById('searchbar');
let searchQuery = getUrlParameter('search');

if (searchQuery)
    searchbar.value = searchQuery;

$("#searchbar").keyup(
    function(event) {
        if (event.keyCode === 13)
            search()
    }
);

function search() {
    if (searchbar.value)
        if (location.search) {
            let args = location.search.slice(1).split('&');
            for (let argId = 0; argId < args.length; argId += 1) {
                if (args[argId].startsWith('search=')) {
                    args.splice(argId);
                    break
                }
            }
            args.push('search=' + searchbar.value);
            args.push(cardsPerPageQuery);
            location.search = '?' + args.join('&')
        }
        else
            location.search = '?search=' + searchbar.value + '&' +cardsPerPageQuery
}
