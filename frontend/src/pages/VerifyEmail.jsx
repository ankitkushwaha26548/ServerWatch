/* eslint-disable react-hooks/set-state-in-effect */
import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { verifyEmail } from "../api/serverApi";

export default function VerifyEmail() {
  const [params] = useSearchParams();
  const [state, setState] = useState({ loading: true, message: "", error: "" });
  useEffect(() => {
    const token = params.get("token");
    if (!token) {
      setState({ loading: false, message: "", error: "Verification token is missing." });
      return;
    }
    verifyEmail(token)
      .then(data => setState({ loading: false, message: data.message, error: "" }))
      .catch(error => setState({ loading: false, message: "", error: error.response?.data?.detail || "Verification failed." }));
  }, [params]);
  return <div className="login-page"><div className="login-form-wrap"><div className="login-form"><span className="brand-mark">S</span><span className="eyebrow">EMAIL VERIFICATION</span><h2>{state.loading ? "Verifying your email…" : state.message ? "Email verified" : "Verification failed"}</h2><p className={state.error ? "form-error" : "muted"}>{state.loading ? "Please wait while we confirm your email address." : state.message || state.error}</p>{!state.loading && <Link className="button primary full" to="/login">Continue to sign in <span>→</span></Link>}</div></div></div>;
}
