import React from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./Navbar";
import Register from "./Register";
import Login from "./Login";
import OrderList from "./OrderList";
import Products from "./Products";
import ProductDetails from "./ProductDetails";
import { CartProvider } from "./CartContext";
import Cart from "./Cart";
import Order from "./Order";

function App() {
  return (
    <div>
      <CartProvider>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/orders" element={<OrderList />} />
          <Route path="/products" element={<Products />} />
          <Route path="/products/:productId" element={<ProductDetails />} />
          <Route path="/cart" element={<Cart />} />
          <Route path="/order" element={<Order />} />
        </Routes>
      </CartProvider>
    </div>
  );
}

function Home() {
  return <h1>Welcome to the Printing House</h1>;
}

export default App;
