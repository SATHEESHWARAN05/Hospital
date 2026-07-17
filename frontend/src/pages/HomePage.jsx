import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { hospitalAPI } from '../api/client';
import SearchBar from '../components/hospital/SearchBar';
import HospitalCard from '../components/hospital/HospitalCard';

export default function HomePage() {
  const navigate = useNavigate();

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['hospitals', 'featured'],
    queryFn: () => hospitalAPI.list({ page: 1, page_size: 6, sort_by: 'rating' }),
  });

  const hospitals = data?.hospitals || [];

  const handleSearch = (params) => {
    const qs = new URLSearchParams();
    if (params.q) qs.set('q', params.q);
    if (params.city) qs.set('city', params.city);
    if (params.specialization) qs.set('specialization', params.specialization);
    navigate(`/hospitals?${qs.toString()}`);
  };

  return (
    <>
      {/* Hero */}
      <section className="hero">
        <h1>Find the Right Hospital, Right Now</h1>
        <p>Search across {data?.total || '200+'}+ hospitals, compare prices, check availability, and book instantly.</p>
        <SearchBar onSearch={handleSearch} />
      </section>

      {/* Featured Hospitals */}
      <section className="container">
        <h2 className="section-title">Top Rated Hospitals</h2>

        {isLoading && <div className="loading">Loading hospitals...</div>}
        {isError && <div className="error">Error loading hospitals: {error?.message}</div>}

        {!isLoading && !isError && hospitals.length > 0 && (
          <div className="hospital-grid">
            {hospitals.map((h) => (
              <HospitalCard key={h.id} hospital={h} />
            ))}
          </div>
        )}

        {!isLoading && !isError && hospitals.length === 0 && (
          <div className="empty">No featured hospitals available right now.</div>
        )}

        <div className="text-center mt-24">
          <button
            className="btn btn-primary"
            style={{ padding: '12px 32px', fontSize: '1rem' }}
            onClick={() => navigate('/hospitals')}
          >
            View All Hospitals
          </button>
        </div>
      </section>
    </>
  );
}
