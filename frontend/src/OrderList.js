import React, { useEffect, useState } from "react";

function OrderList() {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch("http://localhost:5000/orders", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const data = await response.json();
        setOrders(data.orders);
      } catch (error) {
        console.error("Error:", error);
      }
    };

    fetchOrders();
  }, []);

  return (
    <div>
      <h1>Your Orders</h1>
      <ul>
        {orders.map((order) => (
          <li key={order.id}>
            <p>
              <strong>Name:</strong> {order.customer_name}
            </p>
            <p>
              <strong>Product:</strong> {order.product_name}
            </p>
            <p>
              <strong>Quantity:</strong> {order.quantity}
            </p>
            <p>
              <strong>Status:</strong> {order.status}
            </p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default OrderList;
