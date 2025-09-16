export default function Home() {
    return (
      <>
        <section className="hero">
          <div className="hero-content">
            <h1 id="hero-title">Smart Tourist Safety Monitoring & Incident Response System</h1>
            <p id="hero-subtitle">Ensuring safe and secure travel experiences for tourists across India with cutting-edge technology</p>
            <div className="hero-buttons">
              <a href="/registration" className="btn btn-primary">Get Started</a>
              <a href="/analytics" className="btn btn-secondary">View Analytics</a>
            </div>
          </div>
          <div className="hero-image">
            <i className="fas fa-shield-alt"></i>
          </div>
        </section>
  
        <section className="features">
          <h2 id="features-title">Key Features</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">
                <i className="fas fa-id-card"></i>
              </div>
              <h3 id="feature1-title">Digital ID Generation</h3>
              <p id="feature1-desc">Secure, encrypted digital IDs for tourists with tamper-proof blockchain technology</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <i className="fas fa-map-marker-alt"></i>
              </div>
              <h3 id="feature2-title">Real-time Tracking</h3>
              <p id="feature2-desc">GPS-based location monitoring and emergency response system</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <i className="fas fa-chart-line"></i>
              </div>
              <h3 id="feature3-title">Analytics Dashboard</h3>
              <p id="feature3-desc">Comprehensive data visualization and safety metrics monitoring</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <i className="fas fa-exclamation-triangle"></i>
              </div>
              <h3 id="feature4-title">Emergency Alerts</h3>
              <p id="feature4-desc">Instant panic button with automatic location sharing to emergency services</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <i className="fas fa-language"></i>
              </div>
              <h3 id="feature5-title">Multi-language Support</h3>
              <p id="feature5-desc">Available in English, Hindi, Bengali, Tamil, and Telugu</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <i className="fas fa-lock"></i>
              </div>
              <h3 id="feature6-title">Secure & Encrypted</h3>
              <p id="feature6-desc">AES encryption and blockchain technology ensure data security</p>
            </div>
          </div>
        </section>
  
        <section className="about">
          <div className="about-content">
            <h2 id="about-title">About This Initiative</h2>
            <p id="about-desc">The Smart Tourist Safety Monitoring & Incident Response System is a comprehensive digital platform designed to enhance tourist safety across India. Our system combines cutting-edge technologies including blockchain, encryption, real-time tracking, and multi-language support to provide a secure and user-friendly experience for both tourists and authorities.</p>
            <div className="stats">
              <div className="stat">
                <h3 id="stat1-number">50,000+</h3>
                <p id="stat1-label">Tourists Protected</p>
              </div>
              <div className="stat">
                <h3 id="stat2-number">99.9%</h3>
                <p id="stat2-label">Uptime</p>
              </div>
              <div className="stat">
                <h3 id="stat3-number">24/7</h3>
                <p id="stat3-label">Support</p>
              </div>
            </div>
          </div>
        </section>
  
        <section className="cta">
          <h2 id="cta-title">Ready to Experience Safe Travel?</h2>
          <p id="cta-desc">Join thousands of tourists who trust our system for their safety</p>
          <a href="/registration" className="btn btn-primary btn-large">Register Now</a>
        </section>
      </>
    );
  }