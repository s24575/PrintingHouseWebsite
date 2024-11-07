import React, { useEffect, useState, useContext } from "react";
import { useParams } from "react-router-dom";
import { CartContext } from "./CartContext";
import "./ProductDetails.css";

function ProductDetails() {
  const { productId } = useParams();
  const [product, setProduct] = useState(null);
  const { addToCart } = useContext(CartContext);
  const [selectedOptions, setSelectedOptions] = useState({});

  useEffect(() => {
    const fetchProductDetails = async () => {
      try {
        const response = await fetch(
          `http://localhost:5000/products/${productId}`
        );
        const data = await response.json();
        setProduct(data);
      } catch (error) {
        console.error("Error fetching product details:", error);
      }
    };

    fetchProductDetails();
  }, [productId]);

  const handleOptionChange = (groupId, value) => {
    setSelectedOptions((prevOptions) => ({
      ...prevOptions,
      [groupId]: value,
    }));
  };

  if (!product) return null;

  return (
    <div className="product-details">
      <h1>{product.product.name}</h1>
      <img
        src={product.product.image_url}
        alt={product.product.name}
        className="product-detail-image"
      />
      <p>{product.product.description}</p>

      <div className="option-groups">
        {Object.values(product.all_options).map((group) => (
          <div
            key={group.option_group.option_group_id}
            className="option-group"
          >
            <h3>{group.option_group.title}</h3>

            {group.option_group.type === "select" && (
              <select
                value={
                  selectedOptions[group.option_group.option_group_id] || ""
                }
                onChange={(e) =>
                  handleOptionChange(
                    group.option_group.option_group_id,
                    e.target.value
                  )
                }
              >
                {group.options.map((option) => (
                  <option key={option.option_id} value={option.option_id}>
                    {option.name} (+{option.price_increment} PLN)
                  </option>
                ))}
              </select>
            )}

            {group.option_group.type === "number" && (
              <input
                type="number"
                value={selectedOptions[group.option_group.option_group_id] || 1}
                min="1"
                onChange={(e) =>
                  handleOptionChange(
                    group.option_group.option_group_id,
                    e.target.value
                  )
                }
              />
            )}
          </div>
        ))}
      </div>

      <button
        className="order-button"
        onClick={() => addToCart(product, Object.values(selectedOptions))}
      >
        Dodaj do koszyka
      </button>
    </div>
  );
}

export default ProductDetails;
