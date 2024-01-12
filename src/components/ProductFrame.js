import ProductCard from "./ProductCard"
import styles from "../styles/Product.module.css"

const ProductFrame = ({products, addToCart, changeCartQuantity, getCartQuantity, changeTotalNumItems, changeTotalAmt}) => {

    return (
        <div className={styles.frame}>
            {products.map(product => {
                return (
                    <div key={product.id}>
                    <ProductCard 
                        product={product} 
                        addToCart={addToCart} 
                        changeCartQuantity={changeCartQuantity} 
                        getCartQuantity={getCartQuantity} 
                        changeTotalNumItems = {changeTotalNumItems}
                        changeTotalAmt = {changeTotalAmt}
                    />
                    </div>
                )
            })}
        </div>
    )
}

export default ProductFrame