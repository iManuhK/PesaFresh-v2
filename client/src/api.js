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


export const updateProfile = async (userData) => {
    const { id, ...data } = userData;
    try {
        const response = await axios.patch(`${API_URL}/users/${id}`, data, {
            headers: {
                Authorization: `Bearer ${getJwtToken()}`
            }
        });
        return response.data;
    } catch (error) {
        console.error('Error updating profile:', error.response?.data || error.message || error);
        throw error;
    }
};

export const getCurrentUser = async () => {
    try {
        const response = await axios.get(`${API_URL}/current_user`, {
            headers: {
                Authorization: `Bearer ${getJwtToken()}`
            }
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching current user:', error.response?.data || error.message || error);
        throw error;
    }
};

export const getMyCredits = async () => {
    try {
        const response = await axios.get(`${API_URL}/dashboard/my-credits`, {
            headers: {
                Authorization: `Bearer ${getJwtToken()}`
            }
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching my credits:', error.response?.data || error.message || error);
        throw error;
    }
};