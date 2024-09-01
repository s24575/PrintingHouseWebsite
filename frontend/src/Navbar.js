import React from "react";
import { Link } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-logo">
          <Link to="/">D&K CENTRUM</Link>
        </div>
        <ul className="navbar-menu">
          <li className="navbar-item">
            <Link to="/">Home</Link>
          </li>
          <li className="navbar-item">
            <Link to="/register">Register</Link>
          </li>
          <li className="navbar-item">
            <Link to="/login">Login</Link>
          </li>
          <li className="navbar-item">
            <Link to="/order">Place Order</Link>
          </li>
          <li className="navbar-item">
            <Link to="/orders">View Orders</Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;
