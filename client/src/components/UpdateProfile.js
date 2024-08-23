import React, { useState, useEffect } from 'react';
import updateProfile from '../api.js';
import { useParams } from'react-router-dom';


function UpdateProfile({ initialData }) {
    const { id } = useParams();

    const [formData, setFormData] = useState({
        first_name: "",
        last_name: "",
        national_id: "",
        phone: "",
        username: "",
        email: ""
    });
    const [error, setError] = useState(null)

    useEffect(() => {
        if (initialData) {
            setFormData(initialData);
        }
    }, [initialData]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    const handleUpdateProfile = async (e) => {
        e.preventDefault();
        try {
            const updatedData = await updateProfile({ id, ...formData });
            console.log('Profile updated successfully:', updatedData);
            alert('Profile updated successfully');
        } catch (error) {
            setError('Failed to update profile. Please try again.', error);
        }
    };

    return (
        <div className="update-profile">
            <h1>Update your profile</h1>
            <form onSubmit={handleUpdateProfile}>
                <div>
                    <label htmlFor="first_name">First Name:</label>
                    <input
                        type="text"
                        id="first_name"
                        name="first_name"
                        value={formData.first_name}
                        onChange={handleInputChange}
                    />
                </div>
                <div>
                    <label htmlFor="last_name">Last Name:</label>
                    <input
                        type="text"
                        id="last_name"
                        name="last_name"
                        value={formData.last_name}
                        onChange={handleInputChange}
                    />
                </div>
                <div>
                    <label htmlFor="national_id">National ID:</label>
                    <input
                        type="number"
                        id="national_id"
                        name="national_id"
                        value={formData.national_id}
                        onChange={handleInputChange}
                    />
                </div>
                <div>
                    <label htmlFor="username">Username:</label>
                    <input
                        type="text"
                        id="username"
                        name="username"
                        value={formData.username}
                        onChange={handleInputChange}
                    />
                </div>
                <div>
                    <label htmlFor="email">Email:</label>
                    <input
                        type="email"
                        id="email"
                        name="email"
                        value={formData.email}
                        onChange={handleInputChange}
                    />
                </div>
                <div>
                    <label htmlFor="phone">Phone:</label>
                    <input
                        type="text"
                        id="phone"
                        name="phone"
                        value={formData.phone}
                        onChange={handleInputChange}
                    />
                </div>
                <button type="submit">Save Changes</button>
            </form>
        </div>
    );
}

export default UpdateProfile;
