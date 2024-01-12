import CheckoutFrame from "../components/CheckoutFrame"
import CartFrame from "../components/CartFrame"

const CartPage = ({cartItems}) => {

    var total = 0;

    return (
        <div>
            <CartFrame cartItems={cartItems}></CartFrame>
            <CheckoutFrame total={total}></CheckoutFrame>
        </div>
    )
}

export default CartPage