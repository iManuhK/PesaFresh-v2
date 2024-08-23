import React, { useState } from 'react';
import { Link as Weblink, useNavigate } from 'react-router-dom';
import { useAuth } from './ContextProvider/AuthContext';


export default function Login() {
  const { loginUser } = useAuth();
  // const [email, setEmail] = useState("");
  const [national_id, setNatID] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();


  async function handleSubmit(e) {
    e.preventDefault();
    try {
      await loginUser({ national_id, password });
      navigate('/');
      alert("Login successful.!")
    } catch (error) {
      console.error('Login failed:', error);
      alert("Login failed:", error);
    }
  }

  return (
    <section className="login-section">
      <div className="registration-image-background">
        <div className="registration-image-overlay">
          <img src="./images/MIT-Mobile-Money-2-Press.jpg" alt="background-image-registration-login" />
        </div>
      </div>
      <div className="login-container">
        <div className="login-form-container">
          <div className="login-card">
            <div className="login-card-body">
              <h2 className="login-title">Welcome Back to <span>PesaFresh!</span></h2>
              <p className="login-description">Login to access your account and manage your transactions.</p>
              <form onSubmit={handleSubmit}>
                {/* <div className="form-group">
                  <div className="form-floating">
                    <input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className="form-control"
                      placeholder="name@example.com"
                      required
                    />
                    <label>Email</label>
                  </div>
                </div> */}
                <div className="form-group">
                  <div className="form-floating">
                    <input
                      type="number"
                      value={national_id}
                      onChange={(e) => setNatID(e.target.value)}
                      className="form-control"
                      placeholder="ID Number"
                      required
                    />
                    <label>National ID</label>
                  </div>
                </div>
                <div className="form-group">
                  <div className="form-floating">
                    <input
                      type="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className="form-control"
                      placeholder="Password"
                      required
                    />
                    <label>Password</label>
                  </div>
                </div>
                <div className="form-group">
                  <button className="login-submit-btn" type="submit">Login</button>
                </div>
                <div className="form-group">
                  <p className="register-login-text">Don't have an account? <Weblink to="/register" className="login-register-link">Sign Up Here</Weblink></p>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
