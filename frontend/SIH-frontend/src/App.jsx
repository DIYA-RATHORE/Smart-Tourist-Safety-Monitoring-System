import { Outlet, NavLink } from 'react-router-dom';
import Header from './components/Header.jsx';
import Footer from './components/Footer.jsx';

export default function App() {
  return (
    <>
      <Header />
      <main>
        <Outlet />
      </main>
      <Footer />
    </>
  );
}