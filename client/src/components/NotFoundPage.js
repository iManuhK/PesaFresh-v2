import React from 'react'

function NotFoundPage() {
  return (
    <div className="not-found-error">
      <div className="error-message">
        <img src="./images/image.png" alt="logo" />
        <h1>404</h1>
        <h2>Oops! Page Not Found</h2>
        <p>Sorry, the page you're looking for doesn't exist or has been moved.</p>
        <a href="/" className="home-button">Back to Home</a>
      </div>
    </div>
  )
}

export default NotFoundPage