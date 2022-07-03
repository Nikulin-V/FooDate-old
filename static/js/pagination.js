let cardsRadio20 = $('#cardsPerPage-20')
let cardsRadio40 = $('#cardsPerPage-40')
let cardsRadio60 = $('#cardsPerPage-60')

cardsRadio20.on('change', changeCardsPerPage)
cardsRadio40.on('change', changeCardsPerPage)
cardsRadio60.on('change', changeCardsPerPage)

let cards = getUrlParameter('cardsPerPage')
switch (cards) {
    case '20': cardsRadio20.prop('checked', true); break;
    case '40': cardsRadio40.prop('checked', true); break;
    case '60': cardsRadio60.prop('checked', true); break;
}


function openPage(pageNumber) {
    if (location.search) {
        let args = location.search.slice(1).split('&')
        for (let argId = 0; argId < args.length; argId += 1) {
            if (args[argId].startsWith('page=')) {
                args.splice(argId)
                break
            }
        }
        args.push('page=' + pageNumber.toString())
        location.search = '?' + args.join('&')
    }
    else
        location.search = '?page=' + pageNumber.toString()
}

function getCardsPerPage() {
    if (cardsRadio20.is(':checked'))
        return '20'
    if (cardsRadio40.is(':checked'))
        return '40'
    if (cardsRadio60.is(':checked'))
        return '60'
    return false
}

function changeCardsPerPage() {
    let cardsPerPage = getCardsPerPage().toString()

    if (location.search) {
        let args = location.search.slice(1).split('&')
        for (let argId = 0; argId < args.length; argId += 1) {
            if (args[argId].startsWith('cardsPerPage=')) {
                args.splice(argId)
                break
            }
        }
        args.push('cardsPerPage=' + cardsPerPage)
        location.search = '?' + args.join('&')
    }
    else
        location.search = '?cardsPerPage=' + cardsPerPage
}
