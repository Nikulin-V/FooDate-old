const domContainer = document.querySelector('#productsTimeLine');

class NoProducts extends React.Component {
    render() {
        return (
            <div className="row justify-content-center">
                <img src={`${staticUrl}images/icons/empty_fridge.png`}
                     style={{width: 200}}
                     alt="Нет продуктов"></img>
                <h4 className="text-apple text-center mt-5">В холодильнике пусто</h4>
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

class ProductRowRight extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            product: null,
            display: 'none'
        }
    }

    componentDidMount() {
        const productUrl = this.props.product['product_card'];
        productCards.getProductCard(productUrl)
            .then((r) => {
            this.setState({
                product: this.props.product,
                productCard: r,
                display: 'block'
            })
        })
    }

    render() {
        const product = this.state.product;
        const productCard = this.state.productCard;
        return (
            <div style={{'display': this.state.display}}>
                {this.state.product === null ?
                    <div></div>
                :
                    <div className='row'>
                        <div className='col'></div>
                        <div className='vertical-line-left col pb-5'>
                            <div className='row'>
                                <div className='col-1'>
                                    <img src={productCard['image']}
                                         id={`image-${this.state.id}`}
                                         className='product-image product-image-right'
                                         alt="Нет продуктов"></img>
                                </div>
                                <div className='col-11'>
                                    <a>
                                        <div className='row'>
                                            <span className='product-title'>
                                                {productCard['name']} {product['amount']} {product['amount_unit']}
                                            </span>
                                        </div>
                                        <div className='row'>
                                            <div className='col'>
                                                <span className='badge bg-success product-production-date'
                                                      data-bs-toggle='tooltip' data-bs-placement='top'
                                                      title='Дата изготовления'>
                                                    {parseDateTime(product['production_date'])}
                                                </span>
                                            </div>
                                            <div className='col'>
                                                <span className='badge bg-warning product-shelf-life'
                                                      data-bs-toggle='tooltip' data-bs-placement='top'
                                                      title='Срок годности'>
                                                    {parseDuration(productCard['shelf_life'])}
                                                </span>
                                            </div>
                                        </div>
                                        <br/>
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                }
            </div>
        )
    }
}


class ProductRowLeft extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            product: null,
            display: 'none'
        }
    }

    componentDidMount() {
        const productUrl = this.props.product['product_card'];
        productCards.getProductCard(productUrl)
            .then((r) => {
            this.setState({
                product: this.props.product,
                productCard: r,
                display: 'block'
            })
        })
    }

    render() {
        const product = this.state.product;
        const productCard = this.state.productCard;
        return (
            <div style={{'display': this.state.display}}>
                {this.state.product === null ?
                    <div></div>
                :
                    <div className='row'>
                        <div className='vertical-line-right col pb-5'>
                            <div className='row'>
                                <div className='col-11 text-end mr-3'>
                                    <div className='row'>
                                        <span className='product-title'>
                                            {productCard['name']} {product['amount']} {product['amount_unit']}
                                        </span>
                                    </div>
                                    <div className='row'>
                                        <div className='col'>
                                            <span className='badge bg-success product-production-date'
                                                  data-bs-toggle='tooltip' data-bs-placement='top'
                                                  title='Дата изготовления'>
                                                {parseDateTime(product['production_date'])}
                                            </span>
                                        </div>
                                        <div className='col'>
                                            <span className='badge bg-warning product-shelf-life'
                                                  data-bs-toggle='tooltip' data-bs-placement='top'
                                                  title='Срок годности'>
                                                {parseDuration(productCard['shelf_life'])}
                                            </span>
                                        </div>
                                    </div>
                                    <br/>
                                </div>
                                <div className='col-1'>
                                    <img src={productCard['image']}
                                         id={`image-${this.state.id}`}
                                         className='product-image product-image-left'
                                         alt="Нет продуктов"></img>
                                </div>
                            </div>
                        </div>
                        <div className='col'></div>
                    </div>
                }
            </div>
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
                    <ProductRowRight id={productId} product={product} />
                );
            else
                rows.push(
                    <ProductRowLeft id={productId} product={product} />
                );
        }
        return (
            <div id='products-timeline'>
                <div className='mt-5'></div>
                {rows}
                <div className='mb-3 d-flex justify-content-center'>
                    <img src='/static/images/fav/android-chrome-512x512.png'
                     style={{'height': '70px'}}
                     alt="Добавьте ещё продукты..."></img>
                </div>
                <h5 className='text-apple text-center'>Продолжение следует...</h5>
            </div>
        )
    }
}

products.getProducts().then(() => {
    if (products.getProductsJson['count'] === 0)
        ReactDOM.render(<NoProducts/>, domContainer);
    else
        ReactDOM.render(<ProductsTimeline/>, domContainer)
});



