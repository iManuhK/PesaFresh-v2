// import { createContext, useContext, useState } from 'react';
// import { login, logout } from '../../api';

// const AuthContext = createContext();

// export const AuthProvider = ({ children }) => {
//   const [currentUser, setCurrentUser] = useState(null);

//   const loginUser = async (userData) => {
//     try {
//       const loggedInUser = await login(userData);
//       setCurrentUser(loggedInUser);
//       localStorage.setItem('jwtToken', loggedInUser.token);
//     } catch (error) {
//       console.error('Failed to log in:', error);
//     }
//   };

//   const logoutUser = async () => {
//     try {
//       await logout();
//       setCurrentUser(null);
//     } catch (error) {
//       console.error('Failed to log out:', error);
//     }
//   };
  

//   return (
//     <AuthContext.Provider value={{ currentUser, loginUser, logoutUser }}>
//       {children}
//     </AuthContext.Provider>
//   );
// };

// export const useAuth = () => useContext(AuthContext);

import { createContext, useContext, useState } from 'react';
import { login, logout } from '../../api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);

  const loginUser = async (userData) => {
    try {
      const loggedInUser = await login(userData);
      setCurrentUser(loggedInUser);
      localStorage.setItem('jwtToken', loggedInUser.token); // Save token to localStorage
    } catch (error) {
      console.error('Failed to log in:', error);
    }
  };

  const logoutUser = async () => {
    try {
      await logout(); // This should be a function that logs out the user
      setCurrentUser(null);
      localStorage.removeItem('jwtToken'); // Remove token from localStorage
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
