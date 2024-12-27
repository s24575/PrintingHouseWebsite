import React, { useEffect, useState } from "react";
import "./OrderList.css";

function OrderList() {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch("http://localhost:5000/order", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (!response.ok) {
          throw new Error("Failed to fetch orders");
        }
        const data = await response.json();
        setOrders(data.orders);
      } catch (error) {
        console.error("Error:", error);
      }
    };

    fetchOrders();
  }, []);

  return (
    <div className="order-list">
      <h1>Moje zamówienia</h1>
      <table className="clean-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Status</th>
            <th>Koszt</th>
            <th>Dostawa</th>
            <th>Data zamówienia</th>
          </tr>
        </thead>
        <tbody>
          {orders.map((order) => (
            <tr key={order.order_id}>
              <td>{order.order_id}</td>
              <td>{order.status}</td>
              <td>${order.total_price.toFixed(2)}</td>
              <td>{order.shipping_method}</td>
              <td>{new Date(order.created_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default OrderList;
