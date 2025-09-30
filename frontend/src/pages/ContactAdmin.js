import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/ContactAdmin.css";

function ContactAdmin() {
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    supplierName: "",
    location: "",
    subject: "New Account Request",
    description: "",
  });
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);
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

  const validateForm = () => {
    const newErrors = {};

    if (!formData.firstName.trim()) {
      newErrors.firstName = "First name is required";
    }

    if (!formData.lastName.trim()) {
      newErrors.lastName = "Last name is required";
    }

    if (!formData.email.trim()) {
      newErrors.email = "Email is required";
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = "Email is invalid";
    }

    if (!formData.supplierName.trim()) {
      newErrors.supplierName = "Supplier name is required";
    }

    if (!formData.location.trim()) {
      newErrors.location = "Location is required";
    }

    if (!formData.description.trim()) {
      newErrors.description = "Description is required";
    }

    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    const newErrors = validateForm();
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      setIsSubmitting(false);
      return;
    }

    try {
      // Send email request to backend
      const response = await fetch("http://localhost:5002/api/contact-admin", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        setSubmitSuccess(true);
        // Reset form
        setFormData({
          firstName: "",
          lastName: "",
          email: "",
          supplierName: "",
          location: "",
          subject: "New Account Request",
          description: "",
        });
      } else {
        const errorData = await response.text();
        console.error("Server response:", response.status, errorData);
        throw new Error(`Server error: ${response.status}`);
      }
    } catch (error) {
      console.error("Error submitting form:", error);
      setErrors({ submit: "Failed to send request. Please try again." });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleBackToLogin = () => {
    navigate("/login");
  };

  if (submitSuccess) {
    return (
      <div className="contact-admin-container">
        <div className="contact-admin-left-panel">
          <div className="logo-section">
            <img
              src="/saxcologo.jpeg"
              alt="SaxCo International"
              className="contact-admin-logo"
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

        <div className="contact-admin-right-panel">
          <div className="success-container">
            <div className="success-icon">✓</div>
            <h1 className="success-title">Request Sent Successfully!</h1>
            <p className="success-message">
              Your account request has been sent to the administrator. You will
              receive a response within 24-48 hours.
            </p>
            <button
              type="button"
              className="back-to-login-button"
              onClick={handleBackToLogin}
            >
              Back to Login
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="contact-admin-container">
      {/* Left side with logo */}
      <div className="contact-admin-left-panel">
        <div className="logo-section">
          <img
            src="/saxcologo.jpeg"
            alt="SaxCo International"
            className="contact-admin-logo"
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

      {/* Right side with contact form */}
      <div className="contact-admin-right-panel">
        <div className="contact-admin-form-container">
          <h1 className="contact-admin-title">Contact Administrator</h1>
          <p className="contact-admin-subtitle">
            Request access to the GHG Emission Calculator
          </p>

          <form onSubmit={handleSubmit} className="contact-admin-form">
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="firstName">First Name *</label>
                <input
                  type="text"
                  id="firstName"
                  name="firstName"
                  value={formData.firstName}
                  onChange={handleChange}
                  className={`form-input ${errors.firstName ? "error" : ""}`}
                  placeholder="Enter your first name"
                />
                {errors.firstName && (
                  <span className="error-message">{errors.firstName}</span>
                )}
              </div>

              <div className="form-group">
                <label htmlFor="lastName">Last Name *</label>
                <input
                  type="text"
                  id="lastName"
                  name="lastName"
                  value={formData.lastName}
                  onChange={handleChange}
                  className={`form-input ${errors.lastName ? "error" : ""}`}
                  placeholder="Enter your last name"
                />
                {errors.lastName && (
                  <span className="error-message">{errors.lastName}</span>
                )}
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="email">Email Address *</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className={`form-input ${errors.email ? "error" : ""}`}
                placeholder="Enter your email address"
              />
              {errors.email && (
                <span className="error-message">{errors.email}</span>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="supplierName">Supplier Name *</label>
              <input
                type="text"
                id="supplierName"
                name="supplierName"
                value={formData.supplierName}
                onChange={handleChange}
                className={`form-input ${errors.supplierName ? "error" : ""}`}
                placeholder="Enter your company/supplier name"
              />
              {errors.supplierName && (
                <span className="error-message">{errors.supplierName}</span>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="location">Location *</label>
              <input
                type="text"
                id="location"
                name="location"
                value={formData.location}
                onChange={handleChange}
                className={`form-input ${errors.location ? "error" : ""}`}
                placeholder="Enter your location (City, Country)"
              />
              {errors.location && (
                <span className="error-message">{errors.location}</span>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="subject">Subject</label>
              <input
                type="text"
                id="subject"
                name="subject"
                value={formData.subject}
                onChange={handleChange}
                className="form-input"
                placeholder="Subject"
              />
            </div>

            <div className="form-group">
              <label htmlFor="description">Description *</label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleChange}
                className={`form-textarea ${errors.description ? "error" : ""}`}
                placeholder="Please provide details about your account request..."
                rows="4"
              />
              {errors.description && (
                <span className="error-message">{errors.description}</span>
              )}
            </div>

            {errors.submit && (
              <div className="error-message">{errors.submit}</div>
            )}

            <div className="form-actions">
              <button
                type="button"
                className="back-button"
                onClick={handleBackToLogin}
              >
                Back to Login
              </button>
              <button
                type="submit"
                className="submit-button"
                disabled={isSubmitting}
              >
                {isSubmitting ? "Sending..." : "Send Request"}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default ContactAdmin;
