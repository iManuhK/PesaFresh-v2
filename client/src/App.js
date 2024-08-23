import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import { AuthProvider } from './components/ContextProvider/AuthContext';
import Register from './components/RegisterUser';
import Login from './components/Login';
import NotFoundPage from './components/NotFoundPage';
import Homepage from './components/Homepage';
import AdminDashboard from './components/AdminDashboard';
import Dashboard from './components/Dashboard';
import About from './components/About';
import Contact from './components/Contact';
import Header from './components/Header';
import Footer from './components/Footer';
import UpdateProfile from './components/UpdateProfile';

const App = () => {
  return (
    <AuthProvider>
      <Router>
      <Header />
        <Routes>
          <Route path="/" element={<Homepage />} />
          <Route path="/admin" element={<AdminDashboard />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/update-profile/:id" element={<UpdateProfile />} />
          <Route path="*" element={<NotFoundPage />} />
          </Routes>
        <Footer />
      </Router>
    </AuthProvider>
  );
};

export default App;
