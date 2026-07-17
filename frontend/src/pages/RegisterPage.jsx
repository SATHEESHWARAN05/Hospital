import { useState } from 'react';

export default function RegisterPage() {
  const [form, setForm] = useState({
    name: '',
    phone: '',
    email: '',
    interestedService: 'consultation',
    hospitalName: '',
    notes: '',
  });
  const [submitted, setSubmitted] = useState(false);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    setSubmitted(true);
  };

  if (submitted) {
    return (
      <section className="container">
        <div className="register-card success-card">
          <div className="check-icon">✅</div>
          <h2>Registration Successful</h2>
          <p>Your registration request has been received successfully.</p>
          <div className="summary-box">
            <div className="row">
              <span>Patient</span>
              <strong>{form.name}</strong>
            </div>
            <div className="row">
              <span>Phone</span>
              <strong>{form.phone}</strong>
            </div>
            <div className="row">
              <span>Service</span>
              <strong>{form.interestedService}</strong>
            </div>
            <div className="row">
              <span>Hospital</span>
              <strong>{form.hospitalName || 'Not specified'}</strong>
            </div>
          </div>
          <button className="btn btn-primary" onClick={() => setSubmitted(false)}>
            Register Another
          </button>
        </div>
      </section>
    );
  }

  return (
    <section className="container">
      <div className="register-card">
        <h2>Patient Registration</h2>
        <p className="register-subtitle">Register quickly for consultation or admission support.</p>

        <form className="register-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Full Name</label>
            <input name="name" value={form.name} onChange={handleChange} required />
          </div>

          <div className="form-group">
            <label>Phone Number</label>
            <input name="phone" value={form.phone} onChange={handleChange} required />
          </div>

          <div className="form-group">
            <label>Email</label>
            <input type="email" name="email" value={form.email} onChange={handleChange} />
          </div>

          <div className="form-group">
            <label>Interested Service</label>
            <select name="interestedService" value={form.interestedService} onChange={handleChange}>
              <option value="consultation">Consultation</option>
              <option value="admission">Admission</option>
              <option value="both">Consultation + Admission</option>
            </select>
          </div>

          <div className="form-group">
            <label>Preferred Hospital</label>
            <input name="hospitalName" value={form.hospitalName} onChange={handleChange} placeholder="Hospital name" />
          </div>

          <div className="form-group">
            <label>Notes</label>
            <textarea name="notes" rows={4} value={form.notes} onChange={handleChange} placeholder="Any additional details" />
          </div>

          <div className="wizard-actions">
            <button type="submit" className="btn btn-primary">Register Now</button>
          </div>
        </form>
      </div>
    </section>
  );
}
