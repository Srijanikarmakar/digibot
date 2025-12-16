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
      alert("Please enter email and password");
      return;
    }

    try {
      const res = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) {
        throw new Error("Login failed");
      }

      // ✅ login success → go to chat
      navigate("/chat");

    } catch (err) {
      alert("Backend API /login not found or server not running");
    }
  }

  return (
    <div className="login-body">
      <div className="navbar">
        <span className="logo">DigiBot</span>
      </div>

      <div className="wrapper">
        <form onSubmit={handleSubmit}>
          <h1>Login</h1>

          <div className="input-box">
            <input
              type="email"
              placeholder="Email"
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="input-box">
            <input
              type="password"
              placeholder="Password"
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button className="btn">Login</button>
        </form>
      </div>
    </div>
  );
}
