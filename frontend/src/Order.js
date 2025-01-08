import React, { useState, useContext } from "react";
import { CartContext } from "./CartContext";
import "./Order.css";
import { useNavigate } from "react-router-dom";

function Order() {
  const { cart } = useContext(CartContext);
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
      <h1>Szczegóły dostawy</h1>

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
        <label>Wybierz rodzaj dostawy:</label>
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
            <label htmlFor="local">Odbiór własny</label>
            <p>C.H. Metropolia, Jana Kilińskiego 4, Poziom 0, 80-452 Gdańsk</p>
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
            <p>Wybierz paczkomat w Twojej okolicy.</p>
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
            <p>Szybka dostawa przez kuriera DHL.</p>
          </div>
        </div>
      </div>

      {(deliveryOption === "inpost" || deliveryOption === "dhl") && (
        <>
          <div className="form-group">
            <label>Miasto:</label>
            <input
              type="text"
              value={city}
              onChange={(e) => setCity(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Ulica:</label>
            <input
              type="text"
              value={street}
              onChange={(e) => setStreet(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Numer mieszkania:</label>
            <input
              type="text"
              value={houseNumber}
              onChange={(e) => setHouseNumber(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Kod pocztowy:</label>
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
        <h2>Szczegóły zamówienia</h2>
        {cart.items.map((item, index) => (
          <div key={`${item.id}-${index}`} className="summary-item">
            <p>{item.name}</p>
            <p>{item.price} PLN</p>
          </div>
        ))}
        <hr />
        <p className="total-price">Cena: {cart.total} zł</p>
      </div>

      <button className="submit-order" onClick={handleSubmitOrder}>
        Złóż zamówienie
      </button>
    </div>
  );
}

export default Order;
