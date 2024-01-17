import styles from "../styles/Cart.module.css"


const CartCard = ({product}) => {

    return (
        <div className={styles.card}>
            <img
                src = {product.image}
                alt = {product.title}
            />
            <span>
                <h3>{product.title}</h3>
                <p>${product.price}</p>
            </span>
        </div>
    )
}

export default CartCard