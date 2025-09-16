import { useEffect } from 'react';
import Plotly from 'plotly.js-dist-min';

export default function Analytics() {
  useEffect(() => {
    const interval = setInterval(updateMetrics, 5000);
    updateMetrics();
    initializeCharts();
    startActivityFeed();
    return () => clearInterval(interval);
  }, []);

  return (
    <>
      <section className="page-header">
        <h1 id="page-title">Safety Analytics Dashboard</h1>
        <p id="page-desc">Real-time monitoring and analytics for tourist safety across India</p>
      </section>

      <section className="metrics-section">
        <div className="metrics-grid">
          {Metric('fas fa-users', 'metric1-title', 'Active Tourists', 'activeTourists', 'touristsChange', '+12%')}
          {Metric('fas fa-exclamation-triangle', 'metric2-title', 'Active Alerts', 'activeAlerts', 'alertsChange', '-5%')}
          {Metric('fas fa-map-marker-alt', 'metric3-title', 'High-Risk Zones', 'riskZones', 'zonesChange', '0%')}
          {Metric('fas fa-shield-alt', 'metric4-title', 'Safety Score', 'safetyScore', 'safetyChange', '+3%')}
        </div>
      </section>

      <section className="charts-section">
        <div className="charts-grid">
          <div className="chart-container">
            <h3 id="chart1-title">Tourist Activity Over Time</h3>
            <div id="touristChart" className="chart"></div>
          </div>
          <div className="chart-container">
            <h3 id="chart2-title">Safety Incidents by Region</h3>
            <div id="incidentChart" className="chart"></div>
          </div>
          <div className="chart-container">
            <h3 id="chart3-title">Emergency Response Times</h3>
            <div id="responseChart" className="chart"></div>
          </div>
          <div className="chart-container">
            <h3 id="chart4-title">Language Distribution</h3>
            <div id="languageChart" className="chart"></div>
          </div>
        </div>
      </section>

      <section className="updates-section">
        <h2 id="updates-title">Real-time Updates</h2>
        <div className="updates-container">
          <div className="update-feed">
            <h3 id="feed-title">Live Activity Feed</h3>
            <div id="activityFeed" className="feed-content"></div>
          </div>
          <div className="map-container">
            <h3 id="map-title">Tourist Locations</h3>
            <div className="map-placeholder">
              <i className="fas fa-map"></i>
              <p id="map-desc">Interactive map showing tourist locations</p>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}

function Metric(icon, titleId, title, valueId, changeId, changeText) {
  return (
    <div className="metric-card">
      <div className="metric-icon"><i className={icon}></i></div>
      <div className="metric-content">
        <h3 id={titleId}>{title}</h3>
        <p className="metric-value" id={valueId}>0</p>
        <span className="metric-change" id={changeId}>{changeText}</span>
      </div>
    </div>
  );
}

function updateMetrics() {
  const activeTourists = Math.floor(Math.random() * 2000) + 1000;
  const activeAlerts = Math.floor(Math.random() * 10);
  const riskZones = Math.floor(Math.random() * 5);
  const safetyScore = Math.floor(Math.random() * 20) + 80;
  const setText = (id, txt) => { const el = document.getElementById(id); if (el) el.textContent = txt; };
  setText('activeTourists', activeTourists.toLocaleString());
  setText('activeAlerts', activeAlerts);
  setText('riskZones', riskZones);
  setText('safetyScore', safetyScore + '%');
}

function initializeCharts() {
  Plotly.newPlot('touristChart', [{
    x: ['Jan','Feb','Mar','Apr','May','Jun'], y: [1200,1500,1800,1600,2000,2200], type: 'scatter', mode: 'lines+markers', name: 'Tourists', line: { color: '#00a8ff' }
  }], { title: 'Tourist Activity Over Time', xaxis: { title: 'Month' }, yaxis: { title: 'Number of Tourists' } });

  Plotly.newPlot('incidentChart', [{
    values: [45,25,20,10], labels: ['North','South','East','West'], type: 'pie', marker: { colors: ['#2ecc71','#f39c12','#e74c3c','#9b59b6'] }
  }], { title: 'Safety Incidents by Region' });

  Plotly.newPlot('responseChart', [{
    x: ['Police','Medical','Fire','Tourist Helpline'], y: [8,12,15,3], type: 'bar', marker: { color: '#e74c3c' }
  }], { title: 'Average Response Time (minutes)', xaxis: { title: 'Service' }, yaxis: { title: 'Time (minutes)' } });

  Plotly.newPlot('languageChart', [{
    values: [40,25,15,12,8], labels: ['English','Hindi','Bengali','Tamil','Telugu'], type: 'pie', marker: { colors: ['#3498db','#e74c3c','#f39c12','#2ecc71','#9b59b6'] }
  }], { title: 'Language Distribution' });
}

function startActivityFeed() {
  const activities = [
    'New tourist registered in Delhi',
    'Emergency alert resolved in Mumbai',
    'Safety check completed in Goa',
    'Tourist assistance provided in Kerala',
    'Location tracking activated for Rajasthan visitor',
    'Emergency contact updated for Chennai tourist'
  ];
  const feed = document.getElementById('activityFeed');
  if (!feed) return;
  setInterval(() => {
    const activity = activities[Math.floor(Math.random() * activities.length)];
    const time = new Date().toLocaleTimeString();
    const item = document.createElement('div');
    item.className = 'activity-item';
    item.innerHTML = `<div class="activity-time">${time}</div><div class="activity-text">${activity}</div>`;
    feed.insertBefore(item, feed.firstChild);
    while (feed.children.length > 10) feed.removeChild(feed.lastChild);
  }, 3000);
}


