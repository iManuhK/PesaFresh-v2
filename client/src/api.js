import axios from 'axios';

const API_URL = 'http://127.0.0.1:5555';
const getJwtToken = () => localStorage.getItem('jwt_Token');

const registerUser = async (userData) => {
    try {
        const response = await axios.post(`${API_URL}/register`, userData);
        return response.data;
    } catch (error) {
        console.error('Error registering user:', error);
        throw error;
    }
};
export default registerUser;

export const login = async (credentials) => {
    try {
        const response = await axios.post(`${API_URL}/login`, credentials);
        const token = response.data.access_token;
        if (token) {
            localStorage.setItem('jwt_Token', token);
        }
        return token;
    } catch (error) {
        console.error('Error logging in:', error.response?.data || error.message || error);
        throw error;
    }
};

export const logout = async () => {
    try {
        const token = getJwtToken();
        if (!token) {
            throw new Error('No token found');
        }
        const response = await axios.post(`${API_URL}/logout`, null, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });
        localStorage.removeItem('jwt_Token');
        return response.status
    } catch (error) {
        console.error('Error logging out:', error.response?.data || error.message || error);
        throw error;
    }
};

