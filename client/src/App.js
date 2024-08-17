import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './components/ContextProvider/AuthContext';
import Login from './components/Login';
import Logout from './components/Logout';
import ProtectedRoute from './components/ProtectedRoute';
import Homepage from './components/Homepage';
import AdminDashboard from './components/AdminDashboard';
import Dashboard from './components/Dashboard';
import About from './components/About';
import Contact from './components/Contact';
import './App.css';

const App = () => {
  <div className="root">
    
  </div>
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Homepage />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/login" element={<Login />} />
          <Route path="/logout" element={<Logout />} />
          <Route
            path="/admin"
            element={<ProtectedRoute component={AdminDashboard} roles={['admin']} />}
          />
          <Route
            path="/dashboard"
            element={<ProtectedRoute component={Dashboard} roles={['user', 'admin']} />}
          />
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;
