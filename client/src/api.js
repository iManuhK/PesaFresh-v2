import axios from 'axios';

const API_URL = 'http://127.0.0.1:5555'
const jwtToken = localStorage.getItem('jwtToken');

export const registerUser = async (userData) => {
    try {
      const response = await axios.post(`${API_URL}/users`, userData);
      return response;
    } catch (error) {
      console.error('Error registering user:', error);
      throw error;
    }
  };

export const login =async (credentials) => {

    try {
        const response = await axios.post(`${API_URL}/login`,credentials);
        return response.json();
    } catch (error) {
        console.error('Error login:', error);
        throw error;
    }
}

export const logout = async (userData) => {
    try {
        const response = await axios.post(`${API_URL}/logout`,userData,
            {
                headers: {
                    'Authorization': `Bearer ${jwtToken}`
                }
              }
            );
            return response;
          } catch (error) {
            console.error('Error creating project:', error);
            throw error;
          }
        };



