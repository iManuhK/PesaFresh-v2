import { createContext, useContext, useState, useEffect } from 'react';
import { login, logout, getCurrentUser } from '../../api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);

  useEffect(() => {
    const validateToken = async () => {
      const token = localStorage.getItem('jwtToken');
      if (token) {
        try {
          const user = await getCurrentUser();
          setCurrentUser(user);
        } catch (error) {
          console.error('Failed to fetch current user:', error);
          localStorage.removeItem('jwtToken'); // Clear invalid token
        }
      }
    };

    validateToken();
  }, []);

  const loginUser = async (userData) => {
    try {
      const loggedInUser = await login(userData);
      setCurrentUser(loggedInUser);
      localStorage.setItem('jwtToken', loggedInUser.token);
    } catch (error) {
      console.error('Failed to log in:', error);
    }
  };

  const logoutUser = async () => {
    try {
      await logout();
      setCurrentUser(null);
      localStorage.removeItem('jwtToken');
    } catch (error) {
      console.error('Failed to log out:', error);
    }
  };

  return (
    <AuthContext.Provider value={{ currentUser, loginUser, logoutUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
