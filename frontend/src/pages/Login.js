import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Login.css";

function Login() {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });
  const [errors, setErrors] = useState({});
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors((prev) => ({
        ...prev,
        [name]: "",
      }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Basic validation
    const newErrors = {};
    if (!formData.email) {
      newErrors.email = "Email is required";
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = "Email is invalid";
    }

    if (!formData.password) {
      newErrors.password = "Password is required";
    } else if (formData.password.length < 6) {
      newErrors.password = "Password must be at least 6 characters";
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    // For demo purposes, navigate to supplier data page
    // In a real app, you would authenticate with backend
    console.log("Login attempt:", formData);
    navigate("/supplier-data");
  };

  const handleForgotPassword = () => {
    alert("Forgot password functionality would be implemented here");
  };

  const handleSignUp = () => {
    alert("Sign up functionality would be implemented here");
  };

  return (
    <div className="login-container">
      {/* Left side with logo */}
      <div className="login-left-panel">
        <div className="logo-section">
          <img
            src="/saxcologo.jpeg"
            alt="SaxCo International"
            className="login-logo"
            onError={(e) => {
              console.error("Logo failed to load:", e);
              e.target.style.display = "none";
            }}
          />
          <div className="company-info">
            <h2>SaxCo International</h2>
            <p>GHG Emission Calculator</p>
          </div>
        </div>
      </div>

      {/* Right side with login form */}
      <div className="login-right-panel">
        <div className="login-form-container">
          <h1 className="login-title">Login</h1>

          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <input
                type="email"
                name="email"
                placeholder="Email"
                value={formData.email}
                onChange={handleChange}
                className={`form-input ${errors.email ? "error" : ""}`}
                autoComplete="email"
              />
              {errors.email && (
                <span className="error-message">{errors.email}</span>
              )}
            </div>

            <div className="form-group">
              <input
                type="password"
                name="password"
                placeholder="Password"
                value={formData.password}
                onChange={handleChange}
                className={`form-input ${errors.password ? "error" : ""}`}
                autoComplete="current-password"
              />
              {errors.password && (
                <span className="error-message">{errors.password}</span>
              )}
            </div>

            <button type="submit" className="login-button">
              Login
            </button>
          </form>

          <div className="login-footer">
            <button
              type="button"
              className="link-button"
              onClick={handleForgotPassword}
            >
              Forgot <span className="highlight">Password</span>?
            </button>

            <p className="signup-text">
              Don't have an account?
              <button
                type="button"
                className="link-button signup-link"
                onClick={handleSignUp}
              >
                Sign up
              </button>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
