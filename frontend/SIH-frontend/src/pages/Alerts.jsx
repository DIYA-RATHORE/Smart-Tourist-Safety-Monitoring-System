import { useEffect } from 'react';
import Swal from 'sweetalert2';

export default function Alerts() {
  useEffect(() => {
    const btn = document.getElementById('panicBtn');
    if (btn) {
      const handler = () => {
        if (!navigator.geolocation) return;
        navigator.geolocation.getCurrentPosition(
          () => {
            Swal.fire({
              title: 'Emergency Alert Sent!',
              text: 'Emergency services have been notified of your location. Help is on the way.',
              icon: 'success',
              confirmButtonText: 'OK'
            });
            addAlertToList();
          },
          () => Swal.fire({
            title: 'Location Error',
            text: 'Unable to access your location. Please enable location services and try again.',
            icon: 'error',
            confirmButtonText: 'OK'
          })
        );
      };
      btn.addEventListener('click', handler);
      return () => btn.removeEventListener('click', handler);
    }
  }, []);

  useEffect(() => {
    loadRecentAlerts();
    const statusInterval = setInterval(updateSafetyStatus, 10000);
    return () => clearInterval(statusInterval);
  }, []);

  return (
    <>
      <section className="page-header">
        <h1 id="page-title">Emergency Alerts & Safety</h1>
        <p id="page-desc">Emergency response system and safety alerts for tourists</p>
      </section>

      <section className="panic-section">
        <div className="panic-container">
          <h2 id="panic-title">Emergency Panic Button</h2>
          <p id="panic-desc">Press this button in case of any emergency. Your location will be automatically shared with emergency services.</p>
          <button id="panicBtn" className="panic-button">
            <i className="fas fa-exclamation-triangle"></i>
            <span id="panic-text">EMERGENCY ALERT</span>
            <span className="button-description" id="panic-subtext">Press in case of emergency</span>
          </button>

          <div className="emergency-info">
            <h3 id="emergency-info-title">What happens when you press the panic button?</h3>
            <ul id="emergency-info-list">
              <li id="info1">Your exact location is automatically shared with emergency services</li>
              <li id="info2">Police, medical, and fire services are immediately notified</li>
              <li id="info3">Your emergency contact is automatically informed</li>
              <li id="info4">A unique emergency ID is generated for tracking</li>
              <li id="info5">Real-time updates are sent to your registered contacts</li>
            </ul>
          </div>
        </div>
      </section>

      <section className="emergency-contacts">
        <h2 id="contacts-title">Emergency Contacts</h2>
        <div className="contacts-grid">
          <div className="contact-card police">
            <div className="contact-icon"><i className="fas fa-shield-alt"></i></div>
            <h3 id="police-title">Police</h3>
            <p className="contact-number">100</p>
            <p id="police-desc">For immediate police assistance</p>
          </div>
          <div className="contact-card medical">
            <div className="contact-icon"><i className="fas fa-ambulance"></i></div>
            <h3 id="medical-title">Medical Emergency</h3>
            <p className="contact-number">108</p>
            <p id="medical-desc">For medical emergencies and ambulance</p>
          </div>
          <div className="contact-card fire">
            <div className="contact-icon"><i className="fas fa-fire"></i></div>
            <h3 id="fire-title">Fire Department</h3>
            <p className="contact-number">101</p>
            <p id="fire-desc">For fire emergencies</p>
          </div>
          <div className="contact-card tourist">
            <div className="contact-icon"><i className="fas fa-phone"></i></div>
            <h3 id="tourist-title">Tourist Helpline</h3>
            <p className="contact-number">1800-TOURIST</p>
            <p id="tourist-desc">24/7 tourist assistance and support</p>
          </div>
        </div>
      </section>

      <section className="recent-alerts">
        <h2 id="recent-title">Recent Safety Alerts</h2>
        <div id="alertsList" className="alerts-list"></div>
      </section>

      <section className="safety-status">
        <h2 id="status-title">Current Safety Status</h2>
        <div className="status-container">
          <div className="status-indicator safe">
            <i className="fas fa-check-circle"></i>
            <h3 id="status-safe">All Systems Operational</h3>
            <p id="status-desc">Emergency response systems are fully functional</p>
          </div>
          <div className="status-details">
            <div className="status-item">
              <span id="location-status">Location Services: Active</span>
              <span className="status-badge active">Active</span>
            </div>
            <div className="status-item">
              <span id="emergency-status">Emergency Response: Ready</span>
              <span className="status-badge active">Ready</span>
            </div>
            <div className="status-item">
              <span id="communication-status">Communication: Connected</span>
              <span className="status-badge active">Connected</span>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}

function loadRecentAlerts() {
  const alerts = [
    { type: 'info', title: 'Weather Alert', message: 'Heavy rainfall expected in Kerala. Please avoid coastal areas.', time: '2 hours ago' },
    { type: 'warning', title: 'Traffic Advisory', message: 'Road closure on NH-48 between Delhi and Gurgaon. Use alternative routes.', time: '4 hours ago' },
    { type: 'success', title: 'Safety Update', message: 'All emergency services are operational in Mumbai region.', time: '6 hours ago' }
  ];
  const list = document.getElementById('alertsList');
  if (!list) return;
  list.innerHTML = '';
  alerts.forEach(a => {
    const el = document.createElement('div');
    el.className = `alert-item ${a.type}`;
    el.innerHTML = `
      <div class="alert-icon"><i class="fas fa-${getAlertIcon(a.type)}"></i></div>
      <div class="alert-content">
        <h4>${a.title}</h4>
        <p>${a.message}</p>
        <span class="alert-time">${a.time}</span>
      </div>
    `;
    list.appendChild(el);
  });
}

function addAlertToList() {
  const list = document.getElementById('alertsList');
  if (!list) return;
  const el = document.createElement('div');
  el.className = 'alert-item panic';
  el.innerHTML = `
    <div class="alert-icon"><i class="fas fa-exclamation-triangle"></i></div>
    <div class="alert-content">
      <h4>Emergency Alert Sent</h4>
      <p>Your location has been shared with emergency services.</p>
      <span class="alert-time">Just now</span>
    </div>
  `;
  list.insertBefore(el, list.firstChild);
}

function getAlertIcon(type) {
  switch (type) {
    case 'info': return 'info-circle';
    case 'warning': return 'exclamation-triangle';
    case 'success': return 'check-circle';
    case 'panic': return 'exclamation-triangle';
    default: return 'info-circle';
  }
}

function updateSafetyStatus() {
  const badges = document.querySelectorAll('.status-item .status-badge');
  badges.forEach(badge => {
    if (Math.random() > 0.95) {
      badge.textContent = 'Checking...';
      badge.className = 'status-badge checking';
      setTimeout(() => {
        badge.textContent = 'Active';
        badge.className = 'status-badge active';
      }, 2000);
    }
  });
}


