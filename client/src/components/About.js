import React from 'react'

function About() {
  return (<>
        <section className="about-introduction">
          <div className="text-center">
            <h1>PesaFresh</h1>
            <p>PesaFresh is a platform that connects businesses and farmers to credit in a seamless, efficient, and transparent way.</p>
            <a href="#">Get Started</a>
          </div>
        </section>
        <section className="about-container" >
        <div className="about-us">
          <h2>Why our users love our platform</h2>
        <div className='about-us-content'>
          <i className="fa fa-mobile"></i>
          <h4>Accessible and Convenient</h4>
          <p>With an easy-to-use platform, PesaFresh makes it simple for farmers to apply for and manage their loans, reducing the bureaucratic hurdles often associated with traditional banking.</p>
        </div>
        <div className='about-us-content'>
          <i className="fa fa-money"></i>
          <h4>Tailored Financial Solutions</h4>
          <p>PesaFresh understands the unique financial needs and challenges of farmers, providing customized credit solutions that are aligned with the agricultural cycles.</p>
        </div>
        <div className='about-us-content'>
          <i className="fa fa-percent"></i>
          <h4>Competitive Rates</h4>
          <p>PesaFresh offers competitive interest rates and flexible repayment terms that are designed to be manageable for farmers, ensuring they can repay loans without compromising their livelihood.</p>
        </div>
        <div className='about-us-content'>
          <i className="fa fa-users"></i>
          <h4>Community Focus</h4>
          <p>By focusing on the farming community, PesaFresh fosters a sense of trust and reliability, which is essential for long-term partnerships and sustainable agricultural growth.</p>
        </div>
        </div>
    </section>
    <section className='about-us-mission-vision'>
      <div className='mission-vision'>
        <h3>Our Mission</h3>
        <p>To empower farmers, create a more equitable and sustainable agricultural landscape, and promote the development of agricultural economies by providing a secure and transparent financial solution.</p>
      </div>
      <div className='mission-vision'>
        <h3>Our Vision</h3>
        <p>To become the leading platform for businesses and farmers to access credit in a seamless, efficient, and transparent manner, while fostering a sense of community and trust in the agricultural sector.</p>
      </div>
      <div className='mission-vision'>
        <h3>Our Values</h3>
        <ul>
          <li>Transparency</li>
          <li>Efficiency</li>
          <li>Equity</li>
          <li>Community</li>
          <li>Innovation</li>
          <li>Sustainability</li>
          <li>Excellence</li>
          <li>Responsibility</li>
          <li>Accountability</li>
          <li>Diversity</li>
          <li>Inclusivity</li>
        </ul>
        </div>
        <div className='mission-vision-team'>
          <h3>Our Team</h3>
          <p>We are a diverse team of experts and professionals, committed to creating a unique and innovative solution that aligns with the needs of farmers and businesses.</p>
          <div className="team-members">
            <div className="team-member">
              <img src="team-member-1.jpg" alt="Team Member 1" />
              <h4>Team Member 1</h4>
              <p>Position</p>
            </div>
            <div className="team-member">
              <img src="team-member-2.jpg" alt="Team Member 2" />
              <h4>Team Member 2</h4>
              <p>Position</p>
            </div>
            <div className="team-member">
              <img src="team-member-3.jpg" alt="Team Member 3" />
              <h4>Team Member 3</h4>
              <p>Position</p>
            </div>
          </div>
        </div>
    </section>
    </>
  )
}

export default About