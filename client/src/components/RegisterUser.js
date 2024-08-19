import React, { useState } from 'react';
import { Link as Weblink } from 'react-router-dom';
import { useAuth } from './ContextProvider/AuthContext';

function Register() {
  const { register } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [repeatPassword, setRepeatPassword] = useState("");
  const [first_name, setName] = useState("");
  const [username, setUserName] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (password !== repeatPassword) {
      alert("Passwords do not match");
      return;
    }
    register(first_name, username, email, password);
  }

  return (
    <section className="registration-page">
        <div className="registration-image-background">
            <div className="registration-image-overlay">
                <img src="./images/Wakulima.jpeg" alt="background-image-registration-login" />
                <h1 className="registration-image-title">Join our<span> PesaFresh </span>community today</h1>
            </div>
        </div>
        <div className="register-section">
            <div className="register-container">
                <div className="register-form-container">
                    <div className="register-card">
                        <div className="register-card-body">
                            <h2 className="login-title">Welcome to <span>PesaFresh!</span></h2>
                            <p className="login-description">Register today and open up a world of unlimited opportunities.</p>
                            <form onSubmit={handleSubmit}>
                            <div className="form-group">
                            <div className="form-floating">
                                <input
                                type="text"
                                value={first_name}
                                onChange={(e) => setName(e.target.value)}
                                className="form-control"
                                placeholder="Name"
                                required
                                />
                                <label>Name</label>
                            </div>
                            </div>
                            <div className="form-group">
                            <div className="form-floating">
                                <input
                                type="text"
                                value={username}
                                onChange={(e) => setUserName(e.target.value)}
                                className="form-control"
                                placeholder="Preferred Username"
                                required
                                />
                                <label>Username</label>
                            </div>
                            </div>
                            <div className="form-group">
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
                            <div className="form-floating">
                                <input
                                type="password"
                                value={repeatPassword}
                                onChange={(e) => setRepeatPassword(e.target.value)}
                                className="form-control"
                                placeholder="Confirm Password"
                                required
                                />
                                <label>Confirm Password</label>
                            </div>
                            </div>
                            <div className="form-group">
                            <button className="register-submit-btn" type="submit">Signup</button>
                            </div>
                            <div className="form-group">
                            <p className="register-login-text">Already have an account? <Weblink to="/login" className="login-register-link">Login</Weblink></p>
                            </div>
                        </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
  );
}

export default Register;
