import products from '../products.json';
import ProductFrame from "../components/ProductFrame"
import CartPage from "./CartPage"
import React, { useState } from 'react';

const HomePage = ({cartItems, total}) => {
    const [cartQuantities, setCartQuantities] = useState({});
    const [cartItems, setCartItems] = useState(new Set([]));
    const [totalNumItems, setTotalNumItems] = useState(0);
    const [totalAmt, setTotalAmt] = useState(0);
  
    /**
     * Items already in cart, just changing quantity
     * @param {*} product is the product to change quantity of
     * @param {*} add is whether to add 1 or subtract 1 (true is add)
     */
    function changeCartQuantity(product, add) {
      setCartQuantities(dict => {
        dict[product.id] = dict[product.id]===undefined? 1: add? dict[product.id]+1: dict[product.id]-1
        return dict
      })
    }
  
    /**
     * 
     * @param {*} product 
     * @returns the number of quantity of the given product in cart
     */
    function getCartQuantity(product) {
      return cartQuantities[product.id]===undefined? 0: cartQuantities[product.id]
    }
  
    /**
     * add product to cart with quantity = 1
     * @param {*} product 
     */
    function addToCart(product){
      setCartItems(cartSet => {
        cartSet.add(product);
        return cartSet;
      })
    }
  
    /**
     * change number of items in cart
     * @param {*} add whether add an item or subtract one (true is add)
     */
    function changeTotalNumItems(add){
      setTotalNumItems( prevAmt => {
        return add? prevAmt+1:prevAmt-1;
      })
    }
  
    /**
     * change the total dollar in cart
     * @param {*} add whether add or subtract (true is add)
     * @param {*} price price of the item added/subtracted
     */
    function changeTotalAmt (add, price){
      setTotalAmt( prevAmt => {
        return add? prevAmt+price: prevAmt-price; 
      })
    }
  
    return (
      <>
        <h1>Product frame</h1>
        <ProductFrame 
          products={products} 
          addToCart={addToCart} 
          changeCartQuantity={changeCartQuantity} 
          getCartQuantity={getCartQuantity} 
          changeTotalNumItems = {changeTotalNumItems}
          changeTotalAmt = {changeTotalAmt}
        />
        <h1>Cart frame</h1>
        <Link href="/page/CartPage">Cart Page</Link>
        <CartPage cartItems={cartItems} total={totalAmt}/>
        <CartPage cartItems={products} total={100}/>
      </>
    );
}

export default HomePage