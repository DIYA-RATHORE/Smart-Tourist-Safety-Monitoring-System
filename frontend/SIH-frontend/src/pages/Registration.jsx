import { useEffect } from 'react';
import Swal from 'sweetalert2';
import { SecuritySystem, blockchain } from '../lib/security';

export default function Registration() {
  useEffect(() => {
    const form = document.getElementById('idForm');
    const result = document.getElementById('idResult');
    if (!form || !result) return;

    function onSubmit(e) {
      e.preventDefault();
      const formData = {
        name: document.getElementById('name').value,
        aadhaar: document.getElementById('aadhaar').value,
        email: document.getElementById('email')?.value || '',
        phone: document.getElementById('phone')?.value || '',
        itinerary: document.getElementById('itinerary').value,
        emergency: document.getElementById('emergency').value,
        emergencyName: document.getElementById('emergencyName')?.value || ''
      };

      const digitalID = {
        id: 'TID-' + Date.now().toString(36) + Math.random().toString(36).slice(2),
        name: SecuritySystem.encrypt(formData.name),
        aadhaar: SecuritySystem.encrypt(formData.aadhaar),
        email: formData.email ? SecuritySystem.encrypt(formData.email) : '',
        phone: formData.phone ? SecuritySystem.encrypt(formData.phone) : '',
        itinerary: formData.itinerary,
        emergency: SecuritySystem.encrypt(formData.emergency),
        emergencyName: formData.emergencyName ? SecuritySystem.encrypt(formData.emergencyName) : '',
        validTill: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toLocaleDateString(),
        createdAt: Date.now()
      };

      blockchain.addTransaction(digitalID);

      Swal.fire({
        title: 'Digital ID Generated!',
        html: `
          <strong>Tourist ID:</strong> ${digitalID.id}<br>
          <strong>Name:</strong> ${formData.name}<br>
          <strong>Valid Till:</strong> ${digitalID.validTill}<br>
          <strong>Status:</strong> Active
        `,
        icon: 'success'
      });

      result.innerHTML = `
        <strong>Digital ID Generated Successfully</strong><br>
        ID: ${digitalID.id}<br>
        Name: ${formData.name}<br>
        Valid Till: ${digitalID.validTill}
      `;

      form.reset();
    }

    form.addEventListener('submit', onSubmit);
    return () => form.removeEventListener('submit', onSubmit);
  }, []);

  return (
    <>
      <section className="page-header">
        <h1 id="page-title">Digital Tourist ID Registration</h1>
        <p id="page-desc">Register for a secure digital ID to ensure your safety during your travels in India</p>
      </section>

      <section className="registration-section">
        <div className="registration-container">
          <div className="registration-info">
            <h2 id="info-title">Why Register?</h2>
            <ul id="info-list">
              <li id="info1">Secure digital identity with blockchain verification</li>
              <li id="info2">Real-time location tracking for emergency response</li>
              <li id="info3">Multi-language support for better communication</li>
              <li id="info4">Instant emergency alert system</li>
              <li id="info5">Access to safety analytics and insights</li>
            </ul>
          </div>

          <div className="registration-form-container">
            <form id="idForm" className="id-form">
              <h3 id="form-title">Registration Form</h3>

              <div className="form-group">
                <label id="name-label" htmlFor="name">Full Name *</label>
                <input type="text" id="name" required placeholder="Enter your full name" />
              </div>

              <div className="form-group">
                <label id="aadhaar-label" htmlFor="aadhaar">Aadhaar/Passport No. *</label>
                <input type="text" id="aadhaar" required placeholder="Enter Aadhaar or Passport number" />
              </div>

              <div className="form-group">
                <label id="email-label" htmlFor="email">Email Address *</label>
                <input type="email" id="email" required placeholder="Enter your email address" />
              </div>

              <div className="form-group">
                <label id="phone-label" htmlFor="phone">Phone Number *</label>
                <input type="tel" id="phone" required placeholder="Enter your phone number" />
              </div>

              <div className="form-group">
                <label id="itinerary-label" htmlFor="itinerary">Trip Itinerary *</label>
                <textarea id="itinerary" required placeholder="Describe your travel plans, destinations, and duration"></textarea>
              </div>

              <div className="form-group">
                <label id="emergency-label" htmlFor="emergency">Emergency Contact *</label>
                <input type="tel" id="emergency" required placeholder="Emergency contact number" />
              </div>

              <div className="form-group">
                <label id="emergency-name-label" htmlFor="emergencyName">Emergency Contact Name</label>
                <input type="text" id="emergencyName" placeholder="Name of emergency contact" />
              </div>

              <div className="form-group checkbox-group">
                <label className="checkbox-label">
                  <input type="checkbox" id="terms" required />
                  <span id="terms-text">I agree to the terms and conditions and privacy policy</span>
                </label>
              </div>

              <button type="submit" id="generate-btn" className="btn btn-primary btn-large">
                <i className="fas fa-id-card"></i> Generate Digital ID
              </button>
            </form>

            <div id="idResult" className="id-result"></div>
          </div>
        </div>
      </section>
    </>
  );
}


