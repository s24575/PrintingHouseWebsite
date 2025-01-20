import React, { useEffect, useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { useParams } from "react-router-dom";
import { CartContext } from "./CartContext";
import "./ProductDetails.css";

function ProductDetails() {
  const { productId } = useParams();
  const [product, setProduct] = useState(null);
  const { addToCart } = useContext(CartContext);
  const [selectedOptions, setSelectedOptions] = useState({});
  const [price, setPrice] = useState(null);
  const [files, setFiles] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProductDetails = async () => {
      try {
        const response = await fetch(
          `http://localhost:5000/products/${productId}`
        );
        const data = await response.json();

        const defaultOptions = {};
        const filteredGroups = {};

        Object.values(data.all_options).forEach((optionGroup) => {
          if (optionGroup.option_group.type === "select") {
            if (optionGroup.options && optionGroup.options.length > 0) {
              defaultOptions[optionGroup.option_group.option_group_id] =
                optionGroup.options[0].option_id;

              filteredGroups[optionGroup.option_group.option_group_id] =
                optionGroup;
            }
          } else if (optionGroup.option_group.type === "number") {
            const defaultValue = optionGroup.default || 1;
            defaultOptions[optionGroup.option_group.option_group_id] =
              defaultValue;

            filteredGroups[optionGroup.option_group.option_group_id] =
              optionGroup;
          }
        });

        setProduct({ ...data, all_options: filteredGroups });
        setSelectedOptions(defaultOptions);
        updatePrice(defaultOptions);
      } catch (error) {
        console.error("Error fetching product details:", error);
      }
    };

    fetchProductDetails();
  }, [productId]);

  const updatePrice = async (options) => {
    try {
      const response = await fetch(
        `http://localhost:5000/products/${productId}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            selected_options: options,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to fetch price");
      }

      const data = await response.json();
      setPrice(data.price);
    } catch (error) {
      console.error("Error updating price:", error);
    }
  };

  const handleOptionChange = (groupId, value) => {
    setSelectedOptions((prevOptions) => {
      const updatedOptions = {
        ...prevOptions,
        [groupId]: isNaN(value) ? value : parseInt(value),
      };

      updatePrice(updatedOptions);

      return updatedOptions;
    });
  };

  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files);
    // setFiles((prevFiles) => [...prevFiles, ...selectedFiles]);
    setFiles(selectedFiles);
  };

  const handleRemoveFile = (index) => {
    setFiles((prevFiles) => prevFiles.filter((_, i) => i !== index));
  };

  const handleSubmit = async () => {
    try {
      await addToCart(product, selectedOptions, files);
      navigate("/cart");
    } catch (error) {
      console.error("Error submitting cart:", error);
    }
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
                value={selectedOptions[group.option_group.option_group_id]}
                onChange={(e) =>
                  handleOptionChange(
                    group.option_group.option_group_id,
                    e.target.value
                  )
                }
              >
                {group.options.map((option) => (
                  <option key={option.option_id} value={option.option_id}>
                    {option.name}
                  </option>
                ))}
              </select>
            )}

            {group.option_group.type === "number" && (
              <input
                type="number"
                value={selectedOptions[group.option_group.option_group_id]}
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

      <div className="file-upload">
        <h3>Załącz plik:</h3>
        <label htmlFor="file-input" className="file-upload-area">
          Przeciągnij i upuść plik tutaj lub kliknij, aby wybrać
          <input
            id="file-input"
            type="file"
            onChange={handleFileChange}
            accept=".pdf"
            // multiple
          />
        </label>
        <div className="file-list">
          {files.map((file, index) => (
            <div key={index} className="file-item">
              <span>{file.name}</span>
              <button
                type="button"
                className="remove-file-button"
                onClick={() => handleRemoveFile(index)}
              >
                ✕
              </button>
            </div>
          ))}
        </div>
      </div>

      <div className="price-summary">
        <h3>Cena: {price !== null ? `${price} zł` : "Obliczanie..."}</h3>
      </div>

      <button className="order-button" onClick={handleSubmit}>
        Dodaj do koszyka
      </button>
    </div>
  );
}

export default ProductDetails;
