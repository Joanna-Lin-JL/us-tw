import CartCard from "./CartCard"
import styles from "../styles/Cart.module.css"

const CartFrame = ({cartItems}) => {
    return (
        <div>
            <div className={styles.rows}>
                {[...cartItems].map(product => {
                    return (
                        <CartCard product={product} key={product.id}/>
                    )
                })}
            </div>
            <button id="checkoutButton" className={styles.checkout}>Checkout</button>
        </div>
        
    )
}

export default CartFrame