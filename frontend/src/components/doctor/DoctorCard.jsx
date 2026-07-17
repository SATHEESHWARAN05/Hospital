export default function DoctorCard({ doctor, onSelect, selected }) {
  return (
    <div className="doctor-card" style={selected ? { border: '2px solid var(--primary)', background: 'var(--primary-light)' } : {}}>
      <div className="doctor-avatar">
        {doctor.name.split(' ').map(w => w[0]).join('').slice(0, 2)}
      </div>
      <div className="doctor-info">
        <h4>{doctor.name}</h4>
        <p className="specialization">{doctor.specialization}</p>
        <p className="fee">₹{Number(doctor.consultation_fee).toLocaleString('en-IN')}</p>
        {doctor.experience_years && (
          <p className="exp">{doctor.experience_years} yrs exp • {doctor.qualification}</p>
        )}
        {onSelect && (
          <button
            className="btn btn-primary"
            style={{ marginTop: 8 }}
            onClick={() => onSelect(doctor)}
          >
            {selected ? 'Selected ✓' : 'Select'}
          </button>
        )}
      </div>
    </div>
  );
}
