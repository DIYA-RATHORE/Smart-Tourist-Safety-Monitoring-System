import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import './index.css';
import App from './App.jsx';
import Home from './pages/Home.jsx';
import Registration from './pages/Registration.jsx';
import Analytics from './pages/Analytics.jsx';
import Alerts from './pages/Alerts.jsx';

const router = createBrowserRouter([
  { path: '/', element: <App />, children: [
    { index: true, element: <Home /> },
    { path: 'registration', element: <Registration /> },
    { path: 'analytics', element: <Analytics /> },
    { path: 'alerts', element: <Alerts /> },
  ]},
]);

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);