import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useSearchParams } from 'react-router-dom';
import { hospitalAPI } from '../api/client';
import SearchBar from '../components/hospital/SearchBar';
import HospitalCard from '../components/hospital/HospitalCard';
import FilterSidebar from '../components/hospital/FilterSidebar';

export default function HospitalListingPage() {
  const [searchParams, setSearchParams] = useSearchParams();

  const [filters, setFilters] = useState({
    city: searchParams.get('city') || '',
    specialization: searchParams.get('specialization') || '',
    min_rating: searchParams.get('min_rating') || '',
  });

  const query = searchParams.get('q') || '';
  const page = parseInt(searchParams.get('page') || '1', 10);
  const pageSize = 12;

  const buildQueryParams = () => {
    const params = { page, page_size: pageSize, sort_by: 'rating' };
    if (query) params.q = query;
    if (filters.city) params.city = filters.city;
    if (filters.specialization) params.specialization = filters.specialization;
    if (filters.min_rating) params.min_rating = parseFloat(filters.min_rating);
    return params;
  };

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['hospitals', 'search', query, filters, page],
    queryFn: () => hospitalAPI.search(buildQueryParams()),
  });

  const handleSearch = (params) => {
    const qs = new URLSearchParams();
    if (params.q) qs.set('q', params.q);
    if (params.city) qs.set('city', params.city);
    if (params.specialization) qs.set('specialization', params.specialization);
    setSearchParams(qs);
  };

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
    const qs = new URLSearchParams(searchParams);
    if (newFilters.city) qs.set('city', newFilters.city); else qs.delete('city');
    if (newFilters.specialization) qs.set('specialization', newFilters.specialization); else qs.delete('specialization');
    if (newFilters.min_rating) qs.set('min_rating', newFilters.min_rating); else qs.delete('min_rating');
    qs.set('page', '1');
    setSearchParams(qs);
  };

  const goToPage = (p) => {
    const qs = new URLSearchParams(searchParams);
    qs.set('page', String(p));
    setSearchParams(qs);
  };

  const totalPages = data ? Math.ceil(data.total / pageSize) : 0;

  return (
    <section className="container">
      <div className="mb-24">
        <SearchBar
          initialQuery={query}
          initialCity={filters.city}
          initialSpecialization={filters.specialization}
          onSearch={handleSearch}
        />
      </div>

      <div className="listing-layout">
        <FilterSidebar filters={filters} onChange={handleFilterChange} />

        <div className="listing-main">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
            <p style={{ color: 'var(--gray-500)', fontSize: '0.9rem' }}>
              {data ? `${data.total} hospital${data.total !== 1 ? 's' : ''} found` : ''}
            </p>
          </div>

          {isLoading && <div className="loading">Searching hospitals...</div>}
          {isError && <div className="error">Error loading hospitals: {error?.message}</div>}

          {data && data.hospitals.length === 0 && (
            <div className="empty">No hospitals found. Try different filters.</div>
          )}

          {data && data.hospitals.length > 0 && (
            <>
              <div className="hospital-grid">
                {data.hospitals.map((h) => (
                  <HospitalCard key={h.id} hospital={h} />
                ))}
              </div>

              {/* Pagination */}
              {totalPages > 1 && (
                <div className="pagination">
                  <button disabled={page <= 1} onClick={() => goToPage(page - 1)}>
                    Previous
                  </button>
                  {Array.from({ length: totalPages }, (_, i) => i + 1)
                    .filter((p) => p === 1 || p === totalPages || Math.abs(p - page) <= 2)
                    .map((p, idx, arr) => (
                      <span key={p}>
                        {idx > 0 && arr[idx - 1] !== p - 1 && <span style={{ padding: '0 4px' }}>...</span>}
                        <button
                          className={p === page ? 'active' : ''}
                          onClick={() => goToPage(p)}
                        >
                          {p}
                        </button>
                      </span>
                    ))}
                  <button disabled={page >= totalPages} onClick={() => goToPage(page + 1)}>
                    Next
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </section>
  );
}
