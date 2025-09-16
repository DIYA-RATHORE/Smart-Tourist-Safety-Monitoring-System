export default function Footer() {
    return (
      <footer>
        <div className="footer-content">
          <div className="footer-section">
            <h3>Contact</h3>
            <p>Email: support@touristsafety.gov.in</p>
            <p>Emergency: 1800-TOURIST</p>
          </div>
          <div className="footer-section">
            <h3>Quick Links</h3>
            <a href="/registration">Registration</a>
            <a href="/analytics">Analytics</a>
            <a href="/alerts">Emergency</a>
          </div>
          <div className="footer-section">
            <h3>Languages</h3>
            <p>English | हिंदी | বাংলা | தமிழ் | తెలుగు</p>
          </div>
        </div>
        <p>&copy; 2023 Smart Tourist Safety Monitoring & Incident Response System. All rights reserved.</p>
      </footer>
    );
  }