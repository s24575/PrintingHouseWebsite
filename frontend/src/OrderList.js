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

  const statusLabels = {
    created: "Utworzone",
    in_progress: "W trakcie realizacji",
    completed: "Zakończone",
    canceled: "Anulowane",
  };

  const deliveryLabels = {
    self_pickup: "Odbiór osobisty",
    inpost: "InPost",
    dhl: "DHL",
  };

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
              <td>{statusLabels[order.status] || "Nieznany status"}</td>
              <td>{order.total_price.toFixed(2)} zł</td>
              <td>
                {deliveryLabels[order.shipping_method] || "Nieznana metoda"}
              </td>
              <td>
                {new Date(order.created_at).toLocaleString("pl-PL", {
                  day: "2-digit",
                  month: "2-digit",
                  year: "numeric",
                  hour: "2-digit",
                  minute: "2-digit",
                  second: "2-digit",
                })}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default OrderList;
