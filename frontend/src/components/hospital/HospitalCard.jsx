import { useNavigate } from 'react-router-dom';

export default function HospitalCard({ hospital }) {
  const navigate = useNavigate();

  return (
    <div
      className="hospital-card"
      onClick={() => navigate(`/hospitals/${hospital.id}`)}
    >
      <img
        className="hospital-card-img"
        src={hospital.image_url || 'https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=400'}
        alt={hospital.name}
      />
      <div className="hospital-card-body">
        <h3>{hospital.name}</h3>
        <p className="location">📍 {hospital.city}, {hospital.state}</p>
        <p className="description">{hospital.description}</p>
        <div className="hospital-card-footer">
          <span className="rating">
            <span className="star">⭐</span> {hospital.rating.toFixed(1)}
          </span>
          <span className="btn btn-outline">View Details</span>
        </div>
      </div>
    </div>
  );
}
