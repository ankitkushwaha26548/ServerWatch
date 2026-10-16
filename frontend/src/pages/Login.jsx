import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { loginUser } from "../api/serverApi";

export default function Login() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const submit = async (event) => {
    event.preventDefault();
    setError("");
    try {
      const data = await loginUser(form);
      localStorage.setItem("access_token", data.access_token);
      navigate("/");
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed. Check your credentials.");
    }
  };
  return <AuthLayout title="Clarity for" accent="every server." subtitle="One calm, focused view of your entire infrastructure."><span className="eyebrow">WELCOME BACK</span><h2>Sign in to your workspace</h2><p className="muted">Enter your credentials to continue monitoring.</p><form onSubmit={submit}><label>Email address<input type="email" value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} placeholder="you@company.com" required /></label><label>Password<input type="password" value={form.password} onChange={e => setForm({ ...form, password: e.target.value })} placeholder="••••••••" required /></label>{error && <div className="form-error">{error}</div>}<button className="button primary full" type="submit">Sign in <span>→</span></button></form><p className="login-hint">New to ServerWatch? <Link className="auth-link" to="/register">Create an account</Link></p></AuthLayout>;
}

function AuthLayout({ children, title, accent, subtitle }) { return <div className="login-page"><div className="login-art"><div className="art-grid" /><div className="login-quote"><span className="brand-mark">S</span><h1>{title}<br /><span>{accent}</span></h1><p>{subtitle}</p></div><span className="login-version">SERVERWATCH · v1.0</span></div><div className="login-form-wrap"><div className="login-form"><div className="mobile-brand"><span className="brand-mark">S</span> Server<span className="brand-accent">Watch</span></div>{children}</div></div></div>; }

export { AuthLayout };
