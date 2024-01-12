import './App.css';

import { BrowserRouter, Routes, Route } from "react-router-dom";

import products from './products.json';
import ProductFrame from "./components/ProductFrame"
import CartPage from "./pages/CartPage"
import React, { useState } from 'react';


function App() {
  const [cartQuantities, setCartQuantities] = useState({});
  const [cartItems, setCartItems] = useState(new Set([]));
  const [totalNumItems, setTotalNumItems] = useState(0);
  const [totalAmt, setTotalAmt] = useState(0);

  function changeCartQuantity(product, add) {
    setCartQuantities(dict => {
      dict[product.id] = dict[product.id]===undefined? 1: add? dict[product.id]+1: dict[product.id]-1
      return dict
    })
  }

  function getCartQuantity(product) {
    return cartQuantities[product.id]
  }

  function addToCart(product){
    setCartItems(cartSet => {
      cartSet.add(product);
      return cartSet;
    })
  }

  function changeTotalNumItems(add){
    return add? totalNumItems+1:totalNumItems-1;
  }

  function changeTotalAmt (add, price){
    return add? totalAmt+price: totalAmt-price; 
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
      <CartPage cartItems={cartItems}/>
    </>
  );
}

export default App;
