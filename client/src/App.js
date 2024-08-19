import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import { AuthProvider } from './components/ContextProvider/AuthContext';
import Register from './components/RegisterUser';
import Login from './components/Login';
import ProtectedRoute from './components/ProtectedRoute';
import Homepage from './components/Homepage';
import AdminDashboard from './components/AdminDashboard';
import Dashboard from './components/Dashboard';
import About from './components/About';
import Contact from './components/Contact';
import Header from './components/Header';
import Footer from './components/Footer';

const App = () => {
  return (
    <AuthProvider>
      <Router>
      <Header />
        <Routes>
          <Route path="/" element={<Homepage />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route
            path="/admin"
            element={<ProtectedRoute component={AdminDashboard} roles={['admin']} />}
          />
          <Route
            path="/dashboard"
            element={<ProtectedRoute component={Dashboard} roles={['user', 'admin']} />}
          />
        </Routes>
        <Footer />
      </Router>
    </AuthProvider>
  );
};

export default App;
