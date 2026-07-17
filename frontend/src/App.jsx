import { Routes, Route } from 'react-router-dom';
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';
import HomePage from './pages/HomePage';
import HospitalListingPage from './pages/HospitalListingPage';
import HospitalDetailPage from './pages/HospitalDetailPage';
import BookingPage from './pages/BookingPage';
import RegisterPage from './pages/RegisterPage';

export default function App() {
  return (
    <div className="app">
      <Navbar />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/hospitals" element={<HospitalListingPage />} />
          <Route path="/hospitals/:id" element={<HospitalDetailPage />} />
          <Route path="/book/:hospitalId" element={<BookingPage />} />
          <Route path="/register" element={<RegisterPage />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}
