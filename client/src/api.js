import axios from 'axios';

const API_URL = 'http://127.0.0.1:5555';
const jwtToken = localStorage.getItem('jwtToken');

export const registerUser = async (userData) => {
  try {
    const response = await axios.post(`${API_URL}/users`, userData);
    return response.data;
  } catch (error) {
    console.error('Error registering user:', error);
    throw error;
  }
};

export const login = async (credentials) => {
  try {
    const response = await axios.post(`${API_URL}/login`, credentials);
    return response.data;
  } catch (error) {
    console.error('Error login:', error);
    throw error;
  }
};

export const logout = async () => {
  try {
    // Ensure the token is available
    if (!jwtToken) {
      throw new Error('No JWT token found, user might not be logged in.');
    }

    const response = await axios.post(
      `${API_URL}/logout`,
      {},
      {
        headers: {
          Authorization: `Bearer ${jwtToken}`,
        },
      }
    );

    // Clear the token after a successful logout
    localStorage.removeItem('jwtToken');
    
    return response.data;
  } catch (error) {
    console.error('Error logging out:', error.message || error);
    throw error;
  }
};

