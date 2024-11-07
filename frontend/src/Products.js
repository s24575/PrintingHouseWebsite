import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./Products.css";

function Products() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await fetch("http://localhost:5000/products");
        const data = await response.json();
        setProducts(data.products);
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    };

    fetchProducts();
  }, []);

  return (
    <div className="products-container">
      <h1>Products</h1>
      <div className="products-grid">
        {products.map((product) => (
          <Link
            key={product.product_id}
            to={`/products/${product.product_id}`}
            className="product-tile"
          >
            <img
              src={product.image_url}
              alt={product.name}
              className="product-image"
            />
            <p className="product-name">{product.name}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}

export default Products;
