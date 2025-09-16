import { useState } from 'react';
import { NavLink } from 'react-router-dom';

export default function Header() {
  const [open, setOpen] = useState(false);

  return (
    <header>
      <nav className="main-nav">
        <div className="logo">Smart Tourist Safety Monitoring & Incident Response System</div>
        <button id="hamburger-menu" className={`hamburger ${open ? 'active' : ''}`} onClick={() => setOpen(!open)}>☰</button>
        <div className={`nav-links ${open ? 'active' : ''}`}>
          <select id="languageSelect" aria-label="Select Language" title="Language Selection">
            <option value="en">English</option>
            <option value="hi">हिंदी</option>
            <option value="bn">বাংলা</option>
            <option value="ta">தமிழ்</option>
            <option value="te">తెలుగు</option>
          </select>
          <NavLink to="/" end className={({ isActive }) => isActive ? 'active' : undefined}>
            <i className="fas fa-home"></i> Home
          </NavLink>
          <NavLink to="/registration" className={({ isActive }) => isActive ? 'active' : undefined}>
            <i className="fas fa-id-card"></i> Registration
          </NavLink>
          <NavLink to="/analytics" className={({ isActive }) => isActive ? 'active' : undefined}>
            <i className="fas fa-chart-line"></i> Analytics
          </NavLink>
          <NavLink to="/alerts" className={({ isActive }) => isActive ? 'active' : undefined}>
            <i className="fas fa-exclamation-triangle"></i> Emergency
          </NavLink>
        </div>
      </nav>
    </header>
  );
}