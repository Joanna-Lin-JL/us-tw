import ProductFrame from "../components/ProductFrame"
import React, { useState, useEffect } from "react";
import CartPage from "./CartPage"
import Product from "../objects/product"
// import Link from 'next/link';


const HomePage = () => {
    const [cartItems, setCartItems] = useState([]);
    const [totalNumItems, setTotalNumItems] = useState(0);
    const [totalAmt, setTotalAmt] = useState(0);
    const [products, setProducts] = useState([])

    async function getData(url = "", token= "") {
      const response = await fetch(url, {
          method: "GET",
          mode: "cors",
          headers: {Authorization: 'Bearer '+token}
      });
      return response
    }
  
    async function postData(url = "", token="", data = {}) {
        const response = await fetch(url, {
            method: "POST",
            mode: "cors",
            headers: {Authorization: 'Bearer '+token},
            body: JSON.stringity(data)
        })
        return response.json()
    }
  
    useEffect(() => {
      // const app = express()
      // fetch(`https://api.allorigins.win/get?url=${encodeURIComponent('http://localhost:5000/api/')}`)
      //                 .then(response => {
      //                   if (response.ok) return response.json()
      //                   throw new Error('Network response was not ok.')
      //                 })
      //                 .then(data => console.log(data.contents));
      // const encoded = ("http://localhost:5000/api/")
      getData("api/").then((data) => {
        data.text().then((d) => console.log(d) )
      });
      getData("api/products/").then((res) => {
        res.json().then((d) => {
          let new_arr = d.data.products.map(function (data) {
            return new Product(data.prodID, data.name, data.price, data.description, data.ingredients, data.weight_oz, data.category, data.picture);
          })
          setProducts(new_arr);
          console.log(products);
        })
      });

      }, []);
  
    /**
     * Items already in cart, just changing quantity
     * @param {*} product is the product to change quantity of
     * @param {*} add is whether to add 1 or subtract 1 (true is add)
     */
    // function changeCartQuantity(product, add) {
    //   setCartQuantities(dict => {
    //     dict[product.id] = dict[product.id]===undefined? 1: add? dict[product.id]+1: dict[product.id]-1
    //     return dict
    //   })
    // }
  
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
  
    return (<></>
      // <>
      //   <h1>Product frame</h1>
      //   <ProductFrame 
      //     products={products} 
      //     addToCart={addToCart} 
      //     changeCartQuantity={changeCartQuantity} 
      //     getCartQuantity={getCartQuantity} 
      //     changeTotalNumItems = {changeTotalNumItems}
      //     changeTotalAmt = {changeTotalAmt}
      //   />
      //   <h1>Cart frame</h1>
      //   {/* <Link href="/page/CartPage">Cart Page</Link> */}
      //   <CartPage cartItems={cartItems} total={totalAmt}/>
      //   <CartPage cartItems={products} total={100}/>
      // </>
    );
}

export default HomePage