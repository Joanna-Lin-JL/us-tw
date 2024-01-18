import './App.css';

// import Link from 'next/link';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import React, { useState, useEffect } from "react";

import HomePage from "./pages/HomePage"
import CartPage from "./pages/CartPage"
import Product from "./objects/product"


function App() {

  // console.log(products)

  return(
    <HomePage/>
  )

  // return (<BrowserRouter>
  //   <Routes>
  //     <Route exact path="/" component={HomePage}/>
  //     {/* <Route path="/cart" component={CartPage}/> */}
  //   </Routes>
  // </BrowserRouter>)
}

export default App;
