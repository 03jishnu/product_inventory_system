

import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./css/CreateProduct.css";

const CreateProduct = () => {
  const [productData, setProductData] = useState({
    product_id: "",
    product_code: "",
    product_name: "",
    variants: [
      {
        name: "",
        options: [{ option_name: "", stock: "" }],
        subvariants: [{ name: "", option_name: { option_name: "", stock: "" } }],
      },
    ],
  });

  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      setError("You must be logged in to create a product.");
      navigate("/"); 
    }
  }, [navigate]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProductData({ ...productData, [name]: value });
  };

  const handleVariantChange = (e, variantIndex) => {
    const { name, value } = e.target;
    const updatedVariants = [...productData.variants];
    updatedVariants[variantIndex][name] = value;
    setProductData({ ...productData, variants: updatedVariants });
  };

  const handleOptionChange = (e, variantIndex, optionIndex) => {
    const { name, value } = e.target;
    const updatedVariants = [...productData.variants];
    updatedVariants[variantIndex].options[optionIndex][name] = value;
    setProductData({ ...productData, variants: updatedVariants });
  };

  const handleSubvariantChange = (e, variantIndex, subvariantIndex) => {
    const { name, value } = e.target;
    const updatedVariants = [...productData.variants];
    const subvariant = updatedVariants[variantIndex].subvariants[subvariantIndex];

    if (name === "option_name" || name === "stock") {
      subvariant.option_name = {
        ...subvariant.option_name,
        [name]: value,
      };
    } else {
      subvariant[name] = value;
    }

    setProductData({ ...productData, variants: updatedVariants });
  };

  const addOption = (variantIndex) => {
    const updatedVariants = [...productData.variants];
    updatedVariants[variantIndex].options.push({ option_name: "", stock: "" });
    setProductData({ ...productData, variants: updatedVariants });
  };

  const addSubvariant = (variantIndex) => {
    const updatedVariants = [...productData.variants];
    updatedVariants[variantIndex].subvariants.push({
      name: "",
      option_name: { option_name: "", stock: "" },
    });
    setProductData({ ...productData, variants: updatedVariants });
  };

  const calculateTotalStock = () => {
    let totalStock = 0;
    productData.variants.forEach((variant) => {
      variant.options.forEach((option) => {
        totalStock += parseInt(option.stock) || 0;
      });
      variant.subvariants.forEach((subvariant) => {
        totalStock += parseInt(subvariant.option_name.stock) || 0;
      });
    });
    return totalStock;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const totalStock = calculateTotalStock();
    const updatedVariants = productData.variants.map((variant) => {
      let variantStock = 0;
      variant.options.forEach((option) => {
        variantStock += parseInt(option.stock) || 0;
      });

      let subvariantStock = 0;
      variant.subvariants.forEach((subvariant) => {
        subvariantStock += parseInt(subvariant.option_name.stock) || 0;
      });

      variant.total_stock = variantStock + subvariantStock;

      variant.subvariants.forEach((subvariant) => {
        subvariant.total_stock = parseInt(subvariant.option_name.stock) || 0;
      });

      return variant;
    });

    const productDataWithTotalStock = { ...productData, total_stock: totalStock, variants: updatedVariants };
    const accessToken = localStorage.getItem("access_token");

    try {
      const response = await axios.post(
        "http://localhost:8000/create_product/",
        productDataWithTotalStock,
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );
      console.log("Product created successfully:", response.data);
      navigate("/products");
      setProductData({
        product_id: "",
        product_code: "",
        product_name: "",
        variants: [
          {
            name: "",
            options: [{ option_name: "", stock: "" }],
            subvariants: [{ name: "", option_name: { option_name: "", stock: "" } }],
          },
        ],
      });
    } catch (error) {
      console.error("Error creating product:", error.response?.data || error.message);
    }
  };

  return (
    <div className="create-product-container">
      <h1>Create Product</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Product ID:</label>
          <input type="text" name="product_id" value={productData.product_id} onChange={handleChange} required />
        </div>
        <div>
          <label>Product Code:</label>
          <input type="text" name="product_code" value={productData.product_code} onChange={handleChange} required />
        </div>
        <div>
          <label>Product Name:</label>
          <input type="text" name="product_name" value={productData.product_name} onChange={handleChange} required />
        </div>

        <h3>Variants:</h3>
        {productData.variants.map((variant, variantIndex) => (
          <div className="variant-section" key={variantIndex}>
            <div>
              <label>Variant Name:</label>
              <input
                type="text"
                name="name"
                value={variant.name}
                onChange={(e) => handleVariantChange(e, variantIndex)}
                required
              />
            </div>

            <h4>Options:</h4>
            {variant.options.map((option, optionIndex) => (
              <div className="option-item" key={optionIndex}>
                <label>Option Name:</label>
                <input
                  type="text"
                  name="option_name"
                  value={option.option_name}
                  onChange={(e) => handleOptionChange(e, variantIndex, optionIndex)}
                  required
                />
                <label>Stock:</label>
                <input
                  type="number"
                  name="stock"
                  value={option.stock}
                  onChange={(e) => handleOptionChange(e, variantIndex, optionIndex)}
                  required
                />
              </div>
            ))}
            <button type="button" onClick={() => addOption(variantIndex)}>
              Add Option
            </button>

            <h4>Subvariants:</h4>
            {variant.subvariants.map((subvariant, subvariantIndex) => (
              <div className="subvariant-item" key={subvariantIndex}>
                <label>Subvariant Name:</label>
                <input
                  type="text"
                  name="name"
                  value={subvariant.name}
                  onChange={(e) => handleSubvariantChange(e, variantIndex, subvariantIndex)}
                  required
                />
                <label>Option Name:</label>
                <input
                  type="text"
                  name="option_name"
                  value={subvariant.option_name.option_name}
                  onChange={(e) => handleSubvariantChange(e, variantIndex, subvariantIndex)}
                  required
                />
                <label>Stock:</label>
                <input
                  type="number"
                  name="stock"
                  value={subvariant.option_name.stock}
                  onChange={(e) => handleSubvariantChange(e, variantIndex, subvariantIndex)}
                  required
                />
              </div>
            ))}
            <button type="button" onClick={() => addSubvariant(variantIndex)}>
              Add Subvariant
            </button>
          </div>
        ))}

        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default CreateProduct;
