import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { hospitalAPI } from '../api/client';
import DoctorCard from '../components/doctor/DoctorCard';
import RoomCard from '../components/room/RoomCard';

export default function HospitalDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('overview');

  const { data, isLoading, isError } = useQuery({
    queryKey: ['hospital', id],
    queryFn: () => hospitalAPI.detail(id),
    enabled: !!id,
  });

  if (isLoading) return <div className="loading">Loading hospital details...</div>;
  if (isError || !data) return <div className="error">Hospital not found.</div>;

  const { hospital, doctors, rooms } = data;

  return (
    <section className="container">
      {/* Header */}
      <div className="detail-header">
        <img
          className="detail-header-img"
          src={hospital.image_url || 'https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=800'}
          alt={hospital.name}
        />
        <div className="detail-header-body">
          <h1>{hospital.name}</h1>
          <p className="location">📍 {hospital.address}, {hospital.city}, {hospital.state} - {hospital.pincode}</p>
          <p className="description">{hospital.description}</p>
          <div className="detail-meta">
            <span>⭐ {hospital.rating.toFixed(1)}</span>
            <span>📞 {hospital.phone}</span>
            {hospital.email && <span>✉️ {hospital.email}</span>}
          </div>
          <div className="mt-16">
            <button
              className="btn btn-primary"
              style={{ padding: '12px 32px', fontSize: '1rem' }}
              onClick={() => navigate(`/book/${hospital.id}`)}
            >
              Book Now
            </button>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="tabs">
        <button
          className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button
          className={`tab ${activeTab === 'doctors' ? 'active' : ''}`}
          onClick={() => setActiveTab('doctors')}
        >
          Doctors ({doctors.length})
        </button>
        <button
          className={`tab ${activeTab === 'rooms' ? 'active' : ''}`}
          onClick={() => setActiveTab('rooms')}
        >
          Rooms ({rooms.length})
        </button>
      </div>

      {/* Tab Content */}
      {activeTab === 'overview' && (
        <div style={{ background: 'var(--white)', borderRadius: 'var(--radius-lg)', padding: 24, boxShadow: 'var(--shadow)' }}>
          <h3 className="section-title">About {hospital.name}</h3>
          <p style={{ color: 'var(--gray-600)', lineHeight: 1.8, marginBottom: 16 }}>
            {hospital.description || 'No additional information available.'}
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginTop: 24 }}>
            <div>
              <h4 style={{ marginBottom: 8, color: 'var(--gray-700)' }}>Contact Information</h4>
              <p style={{ fontSize: '0.9rem', color: 'var(--gray-500)' }}>📞 {hospital.phone}</p>
              {hospital.email && <p style={{ fontSize: '0.9rem', color: 'var(--gray-500)' }}>✉️ {hospital.email}</p>}
              {hospital.website && <p style={{ fontSize: '0.9rem', color: 'var(--gray-500)' }}>🌐 {hospital.website}</p>}
            </div>
            <div>
              <h4 style={{ marginBottom: 8, color: 'var(--gray-700)' }}>Quick Stats</h4>
              <p style={{ fontSize: '0.9rem', color: 'var(--gray-500)' }}>👨‍⚕️ {doctors.length} Doctors</p>
              <p style={{ fontSize: '0.9rem', color: 'var(--gray-500)' }}>🛏️ {rooms.length} Room Types</p>
              <p style={{ fontSize: '0.9rem', color: 'var(--gray-500)' }}>⭐ {hospital.rating.toFixed(1)} Rating</p>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'doctors' && (
        <div>
          {doctors.length === 0 ? (
            <div className="empty">No doctors listed for this hospital.</div>
          ) : (
            <div className="doctor-grid">
              {doctors.map((d) => (
                <DoctorCard key={d.id} doctor={d} />
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'rooms' && (
        <div>
          {rooms.length === 0 ? (
            <div className="empty">No rooms listed for this hospital.</div>
          ) : (
            <div className="room-grid">
              {rooms.map((r) => (
                <RoomCard key={r.id} room={r} />
              ))}
            </div>
          )}
        </div>
      )}
    </section>
  );
}
