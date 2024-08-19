import { createContext, useContext, useState } from 'react';
import { login, logout } from '../../api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);

  const loginUser = async (userData) => {
    try {
      const loggedInUser = await login(userData);
      setCurrentUser(loggedInUser);
      localStorage.setItem('jwtToken', loggedInUser.token); // Save the JWT token after login
    } catch (error) {
      console.error('Failed to log in:', error);
    }
  };

  const logoutUser = async () => {
    try {
      await logout();
      setCurrentUser(null);
    } catch (error) {
      // Handle logout errors if necessary (e.g., display a message to the user)
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
