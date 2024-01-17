import CartSummaryFrame from "../components/CartSummaryFrame"
import CartFrame from "../components/CartFrame"

const CartPage = ({cartItems, total}) => {


    return (
        <div>
            <CartFrame cartItems={cartItems}></CartFrame>
            <CartSummaryFrame total={total}></CartSummaryFrame>
        </div>
    )
}

export default CartPage