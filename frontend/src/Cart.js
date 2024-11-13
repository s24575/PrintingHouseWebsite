import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { CartContext } from "./CartContext";
import "./Cart.css";

function Cart() {
  const { cart, removeFromCart } = useContext(CartContext);

  if (cart.items.length === 0) {
    return <p>Your cart is empty.</p>;
  }

  console.log(cart.items);

  return (
    <div className="cart">
      <h1>Your Cart</h1>
      {cart.items.map((item) => (
        <div key={item.cart_item_id} className="cart-item">
          <h2>{item.name}</h2>
          <p>{item.price} PLN</p>
          <button
            className="remove-button"
            onClick={() => removeFromCart(item.cart_item_id)}
          >
            Remove
          </button>
        </div>
      ))}
      <h3>Total: {cart["total"]} PLN</h3>
      <Link to="/order" className="checkout-button">
        Proceed to Order
      </Link>
    </div>
  );
}

export default Cart;
