import React, { useState, useContext } from "react";
import { CartContext } from "./CartContext";
import "./Order.css";
import { useNavigate } from "react-router-dom";

function Order() {
  const { cart, calculateTotal } = useContext(CartContext);
  const [deliveryOption, setDeliveryOption] = useState("local");
  const [email, setEmail] = useState("");
  const navigate = useNavigate();

  const [city, setCity] = useState("");
  const [street, setStreet] = useState("");
  const [houseNumber, setHouseNumber] = useState("");
  const [postalCode, setPostalCode] = useState("");

  const handleSubmitOrder = () => {
    navigate("/payment");
  };

  return (
    <div className="order">
      <h1>Delivery Information</h1>

      <div className="form-group">
        <label>Email:</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>

      <div className="form-group">
        <label>Choose a delivery option:</label>
        <div className="delivery-options">
          <div
            className={`delivery-card ${
              deliveryOption === "local" ? "selected" : ""
            }`}
            onClick={() => setDeliveryOption("local")}
          >
            <input
              type="radio"
              id="local"
              name="delivery"
              value="local"
              checked={deliveryOption === "local"}
              onChange={() => setDeliveryOption("local")}
              className="hidden-radio"
            />
            <label htmlFor="local">Local Pickup</label>
            <p>You will pick up the order yourself.</p>
          </div>

          <div
            className={`delivery-card ${
              deliveryOption === "inpost" ? "selected" : ""
            }`}
            onClick={() => setDeliveryOption("inpost")}
          >
            <input
              type="radio"
              id="inpost"
              name="delivery"
              value="inpost"
              checked={deliveryOption === "inpost"}
              onChange={() => setDeliveryOption("inpost")}
              className="hidden-radio"
            />
            <label htmlFor="inpost">InPost</label>
            <p>Pickup from your chosen InPost locker.</p>
          </div>

          <div
            className={`delivery-card ${
              deliveryOption === "dhl" ? "selected" : ""
            }`}
            onClick={() => setDeliveryOption("dhl")}
          >
            <input
              type="radio"
              id="dhl"
              name="delivery"
              value="dhl"
              checked={deliveryOption === "dhl"}
              onChange={() => setDeliveryOption("dhl")}
              className="hidden-radio"
            />
            <label htmlFor="dhl">DHL</label>
            <p>Fast delivery to your address via DHL courier.</p>
          </div>
        </div>
      </div>

      {(deliveryOption === "inpost" || deliveryOption === "dhl") && (
        <>
          <div className="form-group">
            <label>City:</label>
            <input
              type="text"
              value={city}
              onChange={(e) => setCity(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Street:</label>
            <input
              type="text"
              value={street}
              onChange={(e) => setStreet(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>House Number:</label>
            <input
              type="text"
              value={houseNumber}
              onChange={(e) => setHouseNumber(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Postal Code:</label>
            <input
              type="text"
              value={postalCode}
              onChange={(e) => setPostalCode(e.target.value)}
              required
            />
          </div>
        </>
      )}

      <div className="price-summary">
        <h2>Order Summary</h2>
        {cart.items.map((item, index) => (
          <div key={`${item.id}-${index}`} className="summary-item">
            <p>{item.name}</p>
            <p>{item.price} PLN</p>
          </div>
        ))}
        <hr />
        <p className="total-price">Total: {cart.total} PLN</p>
      </div>

      <button className="submit-order" onClick={handleSubmitOrder}>
        Place Order
      </button>
    </div>
  );
}

export default Order;
