import React, { useState, useContext } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { AuthContext } from "./AuthContext";
import "./AuthPage.css";

const RegisterPage = () => {
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from?.pathname || "/";

  const [formData, setFormData] = useState({
    email: "",
    password: "",
    first_name: "",
    last_name: "",
    phone_number: "",
  });
  const [error, setError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const response = await fetch("http://localhost:5000/auth/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const data = await response.json();
        login(data.access_token);
        navigate(from, { replace: true });
      } else {
        const errorData = await response.json();
        setError(errorData.message || "Rejestracja nie powiodła się.");
      }
    } catch (err) {
      setError("Wystąpił błąd. Spróbuj ponownie później.");
    }
  };

  return (
    <div className="auth-form">
      <form onSubmit={handleSubmit}>
        <h2>Rejestracja</h2>
        <div className="auth-form-group">
          <label htmlFor="email">E-mail</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>
        <div className="auth-form-group">
          <label htmlFor="password">Hasło</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            minLength={8}
          />
        </div>
        <div className="auth-form-group">
          <label htmlFor="first_name">Imię</label>
          <input
            type="text"
            id="first_name"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
            required
          />
        </div>
        <div className="auth-form-group">
          <label htmlFor="last_name">Nazwisko</label>
          <input
            type="text"
            id="last_name"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
            required
          />
        </div>
        <div className="auth-form-group">
          <label htmlFor="phone_number">Numer telefonu</label>
          <input
            type="text"
            id="phone_number"
            name="phone_number"
            value={formData.phone_number}
            onChange={handleChange}
            required
          />
        </div>
        {error && <p className="auth-error">{error}</p>}
        <button type="submit" className="auth-submit">
          Zarejestruj się
        </button>
      </form>
    </div>
  );
};

export default RegisterPage;
