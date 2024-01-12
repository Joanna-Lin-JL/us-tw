import styles from "../styles/Product.module.css"

const ProductCard = ({product, addToCart, changeCartQuantity, getCartQuantity, changeTotalNumItems, changeTotalAmt}) => {

    const addToCartID = "addToCartButton" + product.id;
    const minusID = "minusButton" + product.id;
    const plusID = "plusButton" + product.id;
    const quantityID = "quantity" + product.id;

    var prodQuantity = getCartQuantity(product)===undefined? 0: getCartQuantity(product);

    function clickAddToCart() {
        document.getElementById(addToCartID).setAttribute("hidden", "hidden");
        addToCart(product);
        changeCartQuantity(product, true);
        changeTotalNumItems(true);
        changeTotalAmt(true, product.price);
        prodQuantity = getCartQuantity(product);
        document.getElementById(minusID).removeAttribute("hidden");
        document.getElementById(quantityID).removeAttribute("hidden");
        document.getElementById(plusID).removeAttribute("hidden");
        document.getElementById(quantityID).textContent= prodQuantity;
    }

    function changeQuantity (add) {
        changeCartQuantity(product, add);
        changeTotalNumItems(add);
        changeTotalAmt(add, product.price);
        prodQuantity = getCartQuantity(product);
        document.getElementById(quantityID).textContent= prodQuantity;
        if (prodQuantity === 0) {
            document.getElementById(addToCartID).removeAttribute("hidden");
            document.getElementById(minusID).setAttribute("hidden", "hidden"); 
            document.getElementById(quantityID).setAttribute("hidden", "hidden");
            document.getElementById(plusID).setAttribute("hidden", "hidden");
        }
    }

    return (
        <div className={styles.card}>
            <img
                src = {product.image}
                alt = {product.title}
            />
            <h3>{product.title}</h3>
            <p>${product.price}</p>
            <button id = {addToCartID} onClick={() => clickAddToCart()}>Add to Cart</button>
            <button id = {minusID} onClick = {() => changeQuantity(false)} hidden>-</button>
            <p id = {quantityID} hidden>{prodQuantity}</p>
            <button id = {plusID} onClick = {() => changeQuantity(true)} hidden>+</button>
        </div>
    )
}

export default ProductCard