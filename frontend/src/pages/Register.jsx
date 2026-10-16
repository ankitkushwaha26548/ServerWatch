import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { registerUser } from "../api/serverApi";
import { AuthLayout } from "./Login";

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [error, setError] = useState("");
  const submit = async (event) => {
    event.preventDefault();
    setError("");
    try {
      await registerUser(form);
      navigate("/login");
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to create your account.");
    }
  };
  return <AuthLayout title="Build with" accent="confidence." subtitle="Start monitoring your infrastructure in minutes."><span className="eyebrow">GET STARTED</span><h2>Create your workspace account</h2><p className="muted">Your account gives you access to the monitoring console.</p><form onSubmit={submit}><label>Username<input value={form.username} onChange={e => setForm({ ...form, username: e.target.value })} placeholder="your-name" required /></label><label>Email address<input type="email" value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} placeholder="you@company.com" required /></label><label>Password<input type="password" minLength="8" value={form.password} onChange={e => setForm({ ...form, password: e.target.value })} placeholder="At least 8 characters" required /></label>{error && <div className="form-error">{error}</div>}<button className="button primary full" type="submit">Create account <span>→</span></button></form><p className="login-hint">Already have an account? <Link className="auth-link" to="/login">Sign in</Link></p></AuthLayout>;
}
