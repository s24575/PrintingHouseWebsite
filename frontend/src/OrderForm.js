import React, { useState } from "react";

function OrderForm() {
  const [order, setOrder] = useState({
    customer_name: "",
    product_name: "",
    quantity: "",
  });
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setOrder((prevOrder) => ({ ...prevOrder, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:5000/orders", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(order),
      });
      const data = await response.json();
      setMessage(data.message);
    } catch (error) {
      console.error("Error:", error);
      setMessage("Order submission failed!");
    }
  };

  return (
    <div>
      <h1>Place Your Order</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Name:
          <input
            type="text"
            name="customer_name"
            value={order.customer_name}
            onChange={handleChange}
            required
          />
        </label>
        <br />
        <label>
          Product Name:
          <input
            type="text"
            name="product_name"
            value={order.product_name}
            onChange={handleChange}
            required
          />
        </label>
        <br />
        <label>
          Quantity:
          <input
            type="number"
            name="quantity"
            value={order.quantity}
            onChange={handleChange}
            required
          />
        </label>
        <br />
        <button type="submit">Submit Order</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

export default OrderForm;
