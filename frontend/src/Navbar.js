import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { CartContext } from "./CartContext";
import "./Navbar.css";

function Navbar() {
  const { cart } = useContext(CartContext);

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-logo">
          <Link to="/">D&K CENTRUM DRUKOWANIA</Link>
        </div>
        <ul className="navbar-menu">
          <li className="navbar-item">
            <Link to="/register">Register</Link>
          </li>
          <li className="navbar-item">
            <Link to="/login">Login</Link>
          </li>
          <li className="navbar-item">
            <Link to="/orders">View Orders</Link>
          </li>
          <li className="navbar-item">
            <Link to="/products">Products</Link>
          </li>
          <li className="navbar-item">
            <Link to="/cart">Cart ({cart.length})</Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;
