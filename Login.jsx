import "boxicons/css/boxicons.min.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/auth.css";

export default function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();

    if (!email || !password) {
      alert("Please enter both email and password");
      return;
    }

    try {
      const res = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();

      if (res.ok) {
        alert("Login successful!");
        navigate("/chat"); // ✅ Direct to chatbot
      } else {
        alert(data.detail || "Invalid credentials");
      }
    } catch (error) {
      alert("Backend not reachable");
    }
  }

  return (
    <div className="login-body">
      {/* Logo Navbar */}
      <div className="navbar">
        <span className="logo">DigiBot</span>
      </div>

      {/* Login Box */}
      <div className="wrapper">
        <form onSubmit={handleSubmit}>
          <h1>Login</h1>

          <div className="input-box">
            <input
              type="email"
              placeholder="Email"
              required
              onChange={(e) => setEmail(e.target.value)}
            />
            <i className="bx bxs-envelope"></i>
          </div>

          <div className="input-box">
            <input
              type="password"
              placeholder="Password"
              required
              onChange={(e) => setPassword(e.target.value)}
            />
            <i className="bx bxs-lock-alt"></i>
          </div>

          <button type="submit" className="btn">
            Login
          </button>
        </form>
      </div>
    </div>
  );
}
