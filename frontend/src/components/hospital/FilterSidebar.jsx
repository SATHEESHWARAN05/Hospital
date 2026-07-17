export default function FilterSidebar({ filters, onChange }) {
  const handleChange = (key, value) => {
    onChange({ ...filters, [key]: value });
  };

  return (
    <aside className="filter-sidebar">
      <h4>Filters</h4>

      <div className="filter-group">
        <label>City</label>
        <select
          value={filters.city || ''}
          onChange={(e) => handleChange('city', e.target.value)}
        >
          <option value="">All Cities</option>
          <option value="Mumbai">Mumbai</option>
          <option value="Delhi">Delhi</option>
          <option value="Bangalore">Bangalore</option>
          <option value="Chennai">Chennai</option>
          <option value="Gurgaon">Gurgaon</option>
        </select>
      </div>

      <div className="filter-group">
        <label>Specialization</label>
        <select
          value={filters.specialization || ''}
          onChange={(e) => handleChange('specialization', e.target.value)}
        >
          <option value="">All</option>
          <option value="Cardiology">Cardiology</option>
          <option value="Neurology">Neurology</option>
          <option value="Orthopedics">Orthopedics</option>
          <option value="Oncology">Oncology</option>
          <option value="Pediatrics">Pediatrics</option>
          <option value="ENT">ENT</option>
          <option value="Gastroenterology">Gastroenterology</option>
          <option value="Dermatology">Dermatology</option>
          <option value="Gynecology">Gynecology</option>
          <option value="Urology">Urology</option>
          <option value="Nephrology">Nephrology</option>
          <option value="Endocrinology">Endocrinology</option>
          <option value="Radiology">Radiology</option>
          <option value="Physiotherapy">Physiotherapy</option>
        </select>
      </div>

      <div className="filter-group">
        <label>Minimum Rating</label>
        <select
          value={filters.min_rating || ''}
          onChange={(e) => handleChange('min_rating', e.target.value)}
        >
          <option value="">Any</option>
          <option value="4.5">4.5+</option>
          <option value="4">4.0+</option>
          <option value="3.5">3.5+</option>
        </select>
      </div>
    </aside>
  );
}
