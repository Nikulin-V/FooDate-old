// noinspection HttpUrlsUsage

protocol = location.protocol;
if (location.host.endsWith('dev.foodate.ru')) {
    host = 'dev.foodate.ru'
    if (location.host.split('.').length === 3) {
        subdomain = null;
    } else {
        let location_data = location.host.split('.');
        subdomain = location_data[0];
    }
} else {
    if (location.host.split('.').length === 2) {
        subdomain = null;
        host = location.host
    } else {
        let location_data = location.host.split('.');
        subdomain = location_data[0];
        host = location_data[1] + '.' + location_data[2];
    }
}


origin_ = `${protocol}//${host}`;
api_origin = `${origin_}/api`;

let csrftoken = Cookies.get('csrftoken');

function checkHTTPS(url) {
    return url.replace('http://', 'https://')
}

products = Object();
products.url = `${api_origin}/products`;

products.getProducts = async function getProducts() {
    let response = await fetch(products.url, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrftoken,
            'Authorization': `Token ${token}`
        },
    });
    if (response.ok) {
        let json = await response.json();
        products.getProductsJson = json;
        return json
    } else
        console.warn(`Ошибка API: ${response.status} ${products.url}`)
};

products.getProduct = async function getProducts(productUrl) {
    productUrl = checkHTTPS(productUrl);
    let response = await fetch(productUrl, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrftoken,
            'Authorization': `Token ${token}`
        },
    });
    if (response.ok) {
        let json = await response.json();
        products.getProductJson = json;
        return json
    } else
        console.warn(`Ошибка API: ${response.status} ${productUrl}`)
};

products.deleteProduct = async function deleteProduct(productUrl) {
    productUrl = checkHTTPS(productUrl);
    let response = await fetch(productUrl, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrftoken,
            'Authorization': `Token ${token}`
        },
    });
    if (response.ok) {
        return 'Success'
    } else {
        console.warn(`Ошибка API (DELETE): ${response.status} ${productUrl}`);
        return 'Error'
    }
};



productCards = Object();
productCards.url = `${api_origin}/product-cards`;

productCards.getProductCards = async function getProductCards() {
    let response = await fetch(productCards.url);
    if (response.ok) {
        let json = await response.json();
        productCards.getProductCardsJson = json;
        return json
    } else
        console.warn(`Ошибка API: ${response.status} ${productCards.url}`)
};

productCards.getProductCard = async function getProductCard(productCardUrl) {
    productCardUrl = checkHTTPS(productCardUrl);
    let response = await fetch(productCardUrl);
    if (response.ok) {
        let json = await response.json();
        productCards.getProductCardJson = json;
        return json
    } else
        console.warn(`Ошибка API: ${response.status} ${productCardUrl}`)
};