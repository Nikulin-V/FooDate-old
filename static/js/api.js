protocol = location.protocol;
if (location.host.split('.').length === 2) {
    subdomain = null;
    host = location.host
} else {
    subdomain = location.host.split('.', 1)[0];
    host = location.host.split('.', 1)[1]
}
origin = `${protocol}//${host}`;
api_origin = `${origin}/api`;

const csrftoken = Cookies.get('csrftoken');

products = Object();
products.url = `${api_origin}/products`;

products.getProducts = async function getProducts() {
    let response = await fetch(products.url, {
        method: 'GET',
        headers: {'X-CSRFToken': csrftoken},
    });
    if (response.ok) {
        let json = await response.json();
        products.getProductsJson = json;
        return json
    } else
        console.warn(`Ошибка API: ${response.status} ${products.url}`)
};

products.getProduct = async function getProducts(productUrl) {
    productUrl = productUrl.replace('http://', 'https://');
    let response = await fetch(productUrl, {
        method: 'GET',
        headers: {'X-CSRFToken': csrftoken},
    });
    if (response.ok) {
        let json = await response.json();
        products.getProductJson = json;
        return json
    } else
        console.warn(`Ошибка API: ${response.status} ${productUrl}`)
};

products.deleteProduct = async function deleteProduct(productUrl) {
    productUrl = productUrl.replace('http://', 'https://');
    let response = await fetch(productUrl, {
        method: 'DELETE',
        headers: {'X-CSRFToken': csrftoken},
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
    productCardUrl = productCardUrl.replace('http://', 'https://');
    let response = await fetch(productCardUrl);
    if (response.ok) {
        let json = await response.json();
        productCards.getProductCardJson = json;
        return json
    } else
        console.warn(`Ошибка API: ${response.status} ${productCardUrl}`)
};