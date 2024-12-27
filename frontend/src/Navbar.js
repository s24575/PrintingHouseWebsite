import React, { useContext, useState } from "react";
import { Link } from "react-router-dom";
import { CartContext } from "./CartContext";
import { AuthContext } from "./AuthContext";
import "./Navbar.css";
import { CgProfile } from "react-icons/cg";
import { FaShoppingCart } from "react-icons/fa";
import { IconContext } from "react-icons";
import { useNavigate } from "react-router-dom";

function Navbar() {
  const { cart } = useContext(CartContext);
  const { isAuthenticated, logout } = useContext(AuthContext);
  const [isProfileMenuOpen, setIsProfileMenuOpen] = useState(false);
  const navigate = useNavigate();

  const toggleProfileMenu = () => {
    setIsProfileMenuOpen(!isProfileMenuOpen);
  };

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <p className="navbar-logo">D&K CENTRUM DRUKOWANIA</p>

        <ul className="navbar-menu">
          <li className="navbar-item">
            <Link to="/products">Produkty</Link>
          </li>
          <li className="navbar-item">
            <Link to="/orders">Zamówienia</Link>
          </li>
          <li className="navbar-item">
            <Link to="/cart" className="cart-link">
              <IconContext.Provider value={{ className: "cart-icon" }}>
                <FaShoppingCart size="25px" />
              </IconContext.Provider>
              <span className="cart-count">{cart.items.length}</span>
            </Link>
          </li>

          <li
            className="navbar-item profile-container"
            onClick={toggleProfileMenu}
          >
            <CgProfile size="30px" />
            {isProfileMenuOpen && (
              <ul className="profile-menu">
                {!isAuthenticated ? (
                  <>
                    <li className="profile-item">
                      <Link to="/register">Register</Link>
                    </li>
                    <li className="profile-item">
                      <Link to="/login">Login</Link>
                    </li>
                  </>
                ) : (
                  <li className="profile-item">
                    <button onClick={handleLogout} className="logout-button">
                      Logout
                    </button>
                  </li>
                )}
              </ul>
            )}
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;
