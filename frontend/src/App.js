import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./Navbar";
import Register from "./Register";
import Login from "./Login";
import OrderList from "./OrderList";
import Products from "./Products";
import ProductDetails from "./ProductDetails";
import { CartProvider } from "./CartContext";
import { AuthProvider } from "./AuthContext";
import Cart from "./Cart";
import Order from "./Order";
import Payment from "./Payment";
import ProtectedRoute from "./ProtectedRoute";

function App() {
  return (
    <div>
      <AuthProvider>
        <CartProvider>
          <Navbar />
          <Routes>
            <Route path="/" element={<Navigate to="/products" replace />} />
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
            <Route path="/orders" element={<OrderList />} />
            <Route path="/products" element={<Products />} />
            <Route path="/products/:productId" element={<ProductDetails />} />
            <Route
              path="/cart"
              element={
                <ProtectedRoute>
                  <Cart />
                </ProtectedRoute>
              }
            />
            <Route path="/order" element={<Order />} />
            <Route path="/payment" element={<Payment />} />
          </Routes>
        </CartProvider>
      </AuthProvider>
    </div>
  );
}

export default App;
