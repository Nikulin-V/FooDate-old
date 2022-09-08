// noinspection JSXNamespaceValidation

const domContainer = document.querySelector('#productsTimeLine');
const addMoreProductsDiv = document.querySelector('#add-more-products-div');

class NoProducts extends React.Component {
    render() {
        return (
            <div className="row justify-content-center">
                <img src={`${staticUrl}images/icons/empty_fridge.png`}
                     style={{width: 200}}
                     alt="Нет продуктов"></img>
                <h4 className="text-apple text-center mt-5 mb-3">В холодильнике пусто</h4>
                <AddMoreProductsButton/>
            </div>
        );
    }
}

function parseDateTime(datetime) {
    let date = datetime.split('T')[0].split('-');
    let year = date[0];
    let month = date[1];
    let day = date[2];
    let time = datetime.split('T')[1].split(':');
    let hours = time[0];
    let minutes = time[1];
    return `${year}.${month}.${day} ${hours}:${minutes}`
}

function parseDuration(duration) {
    duration = duration.split(' ');
    let days = duration[0];
    let hours = duration[1].split(':')[0];
    return `${days} дн. ${hours} ч.`

}

class ProductionDate extends React.Component {
    render() {
        return (
            this.props.date
                ?
                <div className='col-auto'>
                    <span className='badge bg-success product-production-date'
                          data-bs-toggle='tooltip' data-bs-placement='top'
                          title='Дата изготовления'>
                        {parseDateTime(this.props.date )}
                    </span>
                </div>
            :
                <div></div>
        )
    }
}

class ShelfLife extends React.Component {
    render() {
        return (
            this.props.shelfLife
                ?
                <div className='col-auto'>
                    <span className='badge bg-warning product-shelf-life'
                          data-bs-toggle='tooltip' data-bs-placement='top'
                          title='Срок годности'>
                        {parseDuration(this.props.shelfLife)}
                    </span>
                </div>
                :
                <div></div>
        )
    }

}

class ProductWeight extends React.Component {
    render() {
        return (
            (this.props.amount && this.props.unit) ?
                <span>{this.props.amount} {this.props.unit}</span>
                :
                <span></span>
        )
    }
}

class MenuItem extends React.Component {
    render() {
        return (
            <li onClick={this.props.onClick}
                className='list-group-item list-group-item-action'>
                <a href={this.props.href}>
                    {this.props.children}
                </a>
            </li>
        );
    }
}

class ContextMenu extends React.Component {
    render() {
        return (
            <ul id={this.props.id} className={this.props.className}>
                {this.props.children}
            </ul>
        );
    }
}

class ProductRow extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            product: null,
            display: 'none'
        }
    }

    componentDidMount() {
        const productCardUrl = this.props.product['product_card'];
        productCards.getProductCard(productCardUrl)
            .then((r) => {
                const product = this.props.product;
                this.setState({
                    product: this.props.product,
                    productCard: r,
                    contextMenuId: 'context-menu-' + product['slug'],
                    display: 'block',
                });
            })
    }

    render() {
        let contextMenuId = this.state.contextMenuId;

        function showContextMenu(event) {
            $('.context-show').toggleClass('context-show');
            let contextMenu = $('#' + contextMenuId);
            let x = event.clientX;
            let y = event.clientY;
            contextMenu.css('left', x.toString() + 'px');
            contextMenu.css('top', y.toString() + 'px');
            contextMenu.toggleClass('context-show');
        }

        if (this.state.product !== null) {
            const product = this.state.product;
            const productCard = this.state.productCard;
            function getInfo() {
                location.href = `${protocol}//book.${host}/products/${productCard['slug']}`
            }

            function deleteProduct() {
                // noinspection JSIgnoredPromiseFromCall
                products.deleteProduct(product['url']);
                $(`#row-div-${product['slug']}`).remove();
                CheckFridgeEmpty()
            }

            function CheckFridgeEmpty() {
                let productsTimeline = $('#products-timeline');
                if (productsTimeline.children().length <= 2) {
                    productsTimeline.html(`<div class="row justify-content-center"><img src="/static/images/icons/empty_fridge.png" alt="Нет продуктов" style="width: 200px;"><h4 class="text-apple text-center mt-5 mb-3">В холодильнике пусто</h4><button class="btn btn-outline-apple add-more-products-btn" data-bs-toggle="modal" data-bs-target="#newProductModal">Добавьте продукты</button></div>`);
                }
            }

            return (
                <div id={`row-div-${product['slug']}`} style={{'display': this.state.display}}>
                    {
                        this.props.side === 'right' ?
                            <div className='row'
                                 id={`row-${product['slug']}`}
                                 onContextMenu={showContextMenu}>
                                <ContextMenu id={'context-menu-' + product['slug']}
                                             className='context-menu'>
                                    <MenuItem onClick={getInfo}>📗 Информация о продукте</MenuItem>
                                    <MenuItem onClick={deleteProduct}>😋 Съедено</MenuItem>
                                    <MenuItem onClick={deleteProduct}>🗑 Испортилось</MenuItem>
                                </ContextMenu>
                                <div className='col'></div>
                                <div className='vertical-line-left col pb-5'>
                                    <div className='row'>
                                        <div className='col-1'>
                                            <a href={`${protocol}//book.${host}/products/${productCard['slug']}`}
                                               id={`image-div-${product['slug']}`}>
                                                <img
                                                    src={productCard['image'] ? productCard['image'] : '/static/images/icons/no_food_image_small.png'}
                                                    id={`image-${product['slug']}`}
                                                    className='product-image product-image-right'
                                                    alt="Нет продуктов"></img>
                                            </a>
                                        </div>
                                        <div className='col-11'>
                                            <a>
                                                <div className='row'>
                                                        <span className='product-title'>
                                                            {productCard['name']} <ProductWeight
                                                            amount={product['amount']}
                                                            unit={product['amount_unit']}/>
                                                        </span>
                                                </div>
                                                <div className='row justify-content-start'>
                                                    <ProductionDate
                                                        date={product['production_date']}/>
                                                    <ShelfLife
                                                        shelfLife={productCard['shelf_life']}/>
                                                </div>
                                                <br/>
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            :
                            <div className='row'
                                 id={`row-${product['slug']}`}
                                 onContextMenu={showContextMenu}>
                                <ContextMenu id={'context-menu-' + product['slug']}
                                             className='context-menu'>
                                    <MenuItem onClick={getInfo}>📗 Информация о продукте</MenuItem>
                                    <MenuItem onClick={deleteProduct}>😋 Съедено</MenuItem>
                                    <MenuItem onClick={deleteProduct}>🗑 Испортилось</MenuItem>
                                </ContextMenu>
                                <div className='vertical-line-right col pb-5'>
                                    <div className='row justify-content-end'>
                                        <div className='col-11 text-end mr-3'>
                                            <div className='row'>
                                                    <span className='product-title'>
                                                        {productCard['name']} <ProductWeight
                                                        amount={product['amount']}
                                                        unit={product['amount_unit']}/>
                                                    </span>
                                            </div>
                                            <div className='row justify-content-end'>
                                                <ProductionDate date={product['production_date']}/>
                                                <ShelfLife shelfLife={productCard['shelf_life']}/>
                                            </div>
                                            <br/>
                                        </div>
                                        <div className='col-1'>
                                            <a href={`${protocol}//book.${host}/products/${productCard['slug']}`}
                                               id={`image-div-${product['slug']}`}>
                                                <img
                                                    src={productCard['image'] ? productCard['image'] : '/static/images/icons/no_food_image_small.png'}
                                                    id={`image-${product['slug']}`}
                                                    className='product-image product-image-left'
                                                    alt="Нет продуктов"></img>
                                            </a>
                                        </div>
                                    </div>
                                </div>
                                <div className='col'></div>
                            </div>
                    }
                </div>
            );
        }
        return (
            <div></div>
        )
    }
}


class ProductsTimeline extends React.Component {
    render() {
        let rows = [];
        for (let productId = 0; productId < products.getProductsJson['results'].length; productId += 1) {
            const product = products.getProductsJson['results'][productId];
            if (productId % 2 === 0)
                rows.push(
                    <ProductRow id={productId} product={product} side='right'/>
                );
            else
                rows.push(
                    <ProductRow id={productId} product={product} side='left'/>
                );
        }
        return (
            <div id='products-timeline'>
                {rows}
                <div className='mb-3 d-flex justify-content-center'>
                    <img src='/static/images/fav/android-chrome-512x512.png'
                     style={{'height': '70px'}}
                     alt="Добавьте ещё продукты..."></img>
                </div>
                <div className='row justify-content-center text-center'>
                    <h5 className='text-apple mb-3'>Продолжение следует...</h5>
                    <AddMoreProductsButton/>
                </div>
            </div>
        )
    }
}

class AddMoreProductsButton extends React.Component {
    render() {
        return (
            <button className='btn btn-outline-apple add-more-products-btn'
                    data-bs-toggle="modal"
                    data-bs-target="#newProductModal">
                Добавьте продукты
            </button>
        )
    }
}

ReactDOM.render(<AddMoreProductsButton/>, addMoreProductsDiv);

products.getProducts().then(() => {
    if (products.getProductsJson['count'] === 0)
        ReactDOM.render(<NoProducts/>, domContainer);
    else
        ReactDOM.render(<ProductsTimeline/>, domContainer)
});

$(document).on('click', function () {
    $('.context-show').toggleClass('context-show')
});

$(domContainer).contextmenu(
    function (e) {
        e.preventDefault()
    }
);
