export default function SearchBar({ initialQuery, initialCity, initialSpecialization, onSearch }) {
  const handleSubmit = (e) => {
    e.preventDefault();
    const form = e.target;
    onSearch({
      q: form.q.value,
      city: form.city.value,
      specialization: form.specialization.value,
    });
  };

  return (
    <form className="search-bar" onSubmit={handleSubmit}>
      <input
        name="q"
        type="text"
        placeholder="Search hospitals by name or description..."
        defaultValue={initialQuery || ''}
      />
      <select name="city" defaultValue={initialCity || ''}>
        <option value="">All Cities</option>
        <option value="Mumbai">Mumbai</option>
        <option value="Delhi">Delhi</option>
        <option value="Bangalore">Bangalore</option>
        <option value="Chennai">Chennai</option>
        <option value="Gurgaon">Gurgaon</option>
      </select>
      <select name="specialization" defaultValue={initialSpecialization || ''}>
        <option value="">All Specializations</option>
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
      <button type="submit">Search</button>
    </form>
  );
}
