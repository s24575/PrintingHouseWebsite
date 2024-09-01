import React from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./Navbar";
import Register from "./Register";
import Login from "./Login";
import OrderForm from "./OrderForm";
import OrderList from "./OrderList";

function App() {
  return (
    <div>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/order" element={<OrderForm />} />
        <Route path="/orders" element={<OrderList />} />
      </Routes>
    </div>
  );
}

function Home() {
  return <h1>Welcome to the Printing House</h1>;
}

export default App;
