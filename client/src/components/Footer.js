import React from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {faInstagram, faXTwitter, faFacebook, faLinkedin} from '@fortawesome/free-brands-svg-icons'
import {faEnvelope, faLocationDot, faPhone} from '@fortawesome/free-solid-svg-icons'


function Footer() {
  return (
      <footer className="footer-container">
        {/* start of the top footer  */}
        <div className="footer-top">
            <div className="footer-top-column">
              <div className="footer-logo">
                <img src="./images/image.png" alt="logo" />
              </div>
            <div className="footer-subscribe">
                    <h5 className="footer-subscribe-title">Subscribe to our newsletter and get 15% off your first credit.</h5>
                    <div>
                        <form className="footer-subscribe-form">
                          <input type="email" className="footer-subscribe-input" placeholder="Your Email" />
                          <button className="footer-subscribe-button" type="submit">Subscribe</button>
                        </form>
                        <div className="footer-subscribe-disclaimer">
                          <input type='checkbox' className="footer-checkbox" defaultValue={true}/>
                          <p className="footer-subscribe-agreement">I agree to receive PesaFresh newsletters</p>
                        </div>
                    </div>
                </div>
                <div className="footer-social-row">
                  <ul className="footer-social-list">
                    <FontAwesomeIcon icon={faFacebook} /> 
                    <FontAwesomeIcon icon={faXTwitter} />
                    <FontAwesomeIcon icon={faInstagram} />
                    <FontAwesomeIcon icon={faLinkedin} />
                  </ul>
                </div>
            </div>
                <div className="footer-top-column">
                        <div className="footer-links-row">
                            <ul className="footer-links-list">
                                <li><a className="footer-link" href="/#">About Us</a></li>
                                <li><a className="footer-link" href="/#about-us-mission-vision">Team </a></li>
                                <li><a className="footer-link" href="/#">Blog</a></li>
                                <li><a className="footer-link" href="/#">Terms of Use</a></li>
                            </ul>
                        </div>
                        <div className="footer-address">
                         <div className="street">
                          <FontAwesomeIcon icon={faLocationDot} />
                          <p>123 Street, Nairobi, Kenya</p>
                         </div>
                         <div className="phone">
                          <FontAwesomeIcon icon={faPhone} />
                          <p>+254 000 000</p>
                         </div>
                         <div className="email">
                          <FontAwesomeIcon icon={faEnvelope} />
                          <p>info@pesafresh.com</p>
                         </div>
                        </div>
                </div>
                <div className="footer-top-column">
                    <h5 className="footer-links-title">Need Help?</h5>
                    <ul className="footer-links-list">
                        <li><a className="footer-link" href="/#">Contact Us</a></li>
                        <li><a className="footer-link" href="/#">FAQs</a></li>
                        <li><a className="footer-link" href="/#">Offers &amp; Kits</a></li>
                        <li><a className="footer-link" href="/#">Get the app</a></li>
                    </ul>
                </div>
        </div>
        {/* start of the bottom footer */}
      <div className="footer-bottom">
            <div className="footer-bottom-column">
                <div className="footer-bottom-left">
                    <p className="footer-bottom-text">© 2024 copyright by <a className="footer-bottom-link" href="/#">PesaFresh.com</a></p>
                </div>
            </div>
            <div className="footer-bottom-column">
                    <ul className="footer-bottom-right">
                        <li className="footer-bottom-item"><a href="/#" className="footer-bottom-link">Privacy &amp; Policy</a></li>
                        <li className="footer-bottom-item"><a href="/#" className="footer-bottom-link">FAQs</a></li>
                    </ul>
            </div>
      </div>
      </footer>
  )
}

export default Footer
