export default function RoomCard({ room, onSelect, selected }) {
  return (
    <div
      className={`room-card ${selected ? 'selected' : ''}`}
      onClick={() => onSelect && onSelect(room)}
      style={onSelect ? { cursor: 'pointer' } : {}}
    >
      <h4>{room.room_type}</h4>
      <p className="room-number">Room: {room.room_number}</p>
      <p className="price">₹{Number(room.price_per_day).toLocaleString('en-IN')}<span style={{ fontSize: '0.75rem', fontWeight: 400, color: 'var(--gray-500)' }}>/day</span></p>
      <div className="amenities">
        {room.amenities?.map((a, i) => (
          <span key={i} className="amenity-tag">{a}</span>
        ))}
      </div>
      {room.description && (
        <p style={{ fontSize: '0.8rem', color: 'var(--gray-500)', marginBottom: 8 }}>{room.description}</p>
      )}
      {onSelect && (
        <button className={`btn ${selected ? 'btn-success' : 'btn-outline'}`}>
          {selected ? 'Selected ✓' : 'Select Room'}
        </button>
      )}
    </div>
  );
}
