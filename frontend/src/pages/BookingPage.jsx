import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation } from '@tanstack/react-query';
import { hospitalAPI, doctorAPI, roomAPI, bookingAPI } from '../api/client';
import DoctorCard from '../components/doctor/DoctorCard';
import RoomCard from '../components/room/RoomCard';

const REGISTRATION_STORAGE_KEY = 'hospital_front_desk_registrations';

const readRegistrations = () => {
  if (typeof window === 'undefined') return [];

  try {
    const raw = window.localStorage.getItem(REGISTRATION_STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
};

const writeRegistrations = (registrations) => {
  if (typeof window === 'undefined') return;
  window.localStorage.setItem(REGISTRATION_STORAGE_KEY, JSON.stringify(registrations));
};

export default function BookingPage() {
  const { hospitalId } = useParams();
  const navigate = useNavigate();

  const [step, setStep] = useState(1);
  const [selectedDoctor, setSelectedDoctor] = useState(null);
  const [selectedRoom, setSelectedRoom] = useState(null);
  const [bookingType, setBookingType] = useState('consultation');
  const [checkInDate, setCheckInDate] = useState('');
  const [checkOutDate, setCheckOutDate] = useState('');
  const [patientName, setPatientName] = useState('');
  const [patientPhone, setPatientPhone] = useState('');
  const [patientEmail, setPatientEmail] = useState('');
  const [notes, setNotes] = useState('');
  const [treatmentTime, setTreatmentTime] = useState('');
  const [confirmation, setConfirmation] = useState(null);
  const [bookingError, setBookingError] = useState('');
  const [totalPatients, setTotalPatients] = useState(() => readRegistrations().length);

  // Fetch hospital detail (to show name, doctors, rooms)
  const { data: hospitalData } = useQuery({
    queryKey: ['hospital', hospitalId],
    queryFn: () => hospitalAPI.detail(hospitalId),
    enabled: !!hospitalId,
  });

  // Fetch doctors
  const { data: doctorsData } = useQuery({
    queryKey: ['doctors', hospitalId],
    queryFn: () => doctorAPI.list({ hospital_id: hospitalId }),
    enabled: !!hospitalId,
  });

  // Fetch rooms
  const { data: roomsData } = useQuery({
    queryKey: ['rooms', hospitalId],
    queryFn: () => roomAPI.list({ hospital_id: hospitalId, is_available: true }),
    enabled: !!hospitalId,
  });

  const createBooking = useMutation({
    mutationFn: bookingAPI.create,
    onSuccess: (res) => {
      const bookingRecord = {
        id: res.id,
        patient_name: patientName,
        doctor_name: selectedDoctor?.name || 'Doctor not selected',
        room_type: selectedRoom?.room_type || 'Room not selected',
        treatment_time: treatmentTime,
        created_at: new Date().toISOString(),
      };

      const registrations = readRegistrations();
      const updatedRegistrations = [bookingRecord, ...registrations];
      writeRegistrations(updatedRegistrations);
      setTotalPatients(updatedRegistrations.length);

      setConfirmation({
        ...res,
        treatment_time: treatmentTime,
        patient_name: patientName,
        doctor_name: selectedDoctor?.name || 'Doctor not selected',
      });
      setStep(5);
    },
    onError: (err) => {
      setBookingError(err.response?.data?.detail || 'Booking failed. Please try again.');
    },
  });

  const hospital = hospitalData?.hospital;
  const doctors = doctorsData?.doctors || [];
  const rooms = roomsData?.rooms || [];

  // Calculate price preview
  const calculatePreviewPrice = () => {
    let total = 0;
    const breakdown = [];

    if ((bookingType === 'consultation' || bookingType === 'both') && selectedDoctor) {
      const fee = Number(selectedDoctor.consultation_fee);
      breakdown.push({ label: 'Consultation Fee', amount: fee });
      total += fee;
    }

    if ((bookingType === 'admission' || bookingType === 'both') && selectedRoom && checkInDate && checkOutDate) {
      const days = Math.max(1, Math.ceil((new Date(checkOutDate) - new Date(checkInDate)) / (1000 * 60 * 60 * 24)));
      const roomCost = Number(selectedRoom.price_per_day) * days;
      breakdown.push({ label: `Room (${days} day${days > 1 ? 's' : ''})`, amount: roomCost });
      total += roomCost;
    }

    return { total, breakdown };
  };

  const pricePreview = calculatePreviewPrice();

  const handleSubmitBooking = () => {
    setBookingError('');

    if (!patientName || !patientPhone) {
      setBookingError('Please fill in patient name and phone number.');
      return;
    }

    if ((bookingType === 'admission' || bookingType === 'both') && (!checkInDate || !checkOutDate)) {
      setBookingError('Please select check-in and check-out dates.');
      return;
    }

    const uniqueTreatmentTime = new Date().toISOString();
    setTreatmentTime(uniqueTreatmentTime);

    createBooking.mutate({
      patient_name: patientName,
      patient_phone: patientPhone,
      patient_email: patientEmail || null,
      hospital_id: hospitalId,
      doctor_id: selectedDoctor?.id || null,
      room_id: selectedRoom?.id || null,
      booking_type: bookingType,
      check_in_date: checkInDate,
      check_out_date: checkOutDate || null,
      notes: notes || null,
    });
  };

  // ════════════════════════════════════════════════
  // Confirmation screen
  // ════════════════════════════════════════════════
  if (confirmation) {
    return (
      <section className="container">
        <div className="confirmation-card">
          <div className="check-icon">✅</div>
          <h2>Registration Successful</h2>
          <p className="booking-id">Booking ID: {confirmation.id}</p>

          <div className="confirmation-details">
            <div className="row"><span>Hospital</span><strong>{hospital?.name}</strong></div>
            <div className="row"><span>Patient</span><strong>{confirmation.patient_name}</strong></div>
            <div className="row"><span>Doctor</span><strong>{confirmation.doctor_name || selectedDoctor?.name || 'Doctor not selected'}</strong></div>
            {confirmation.room_id && <div className="row"><span>Room</span><strong>{selectedRoom?.room_type} - {selectedRoom?.room_number}</strong></div>}
            <div className="row"><span>Check-in</span><strong>{confirmation.check_in_date}</strong></div>
            {confirmation.check_out_date && <div className="row"><span>Check-out</span><strong>{confirmation.check_out_date}</strong></div>}
            <div className="row"><span>Treatment Time</span><strong>{confirmation.treatment_time || treatmentTime}</strong></div>
            <div className="row"><span>Total Price</span><strong>₹{Number(confirmation.total_price).toLocaleString('en-IN')}</strong></div>
            <div className="row"><span>Total Patients Registered</span><strong>{totalPatients}</strong></div>
          </div>

          <div style={{ display: 'flex', gap: 12, justifyContent: 'center' }}>
            <button className="btn btn-outline" onClick={() => { setConfirmation(null); setStep(1); }}>
              Book Another
            </button>
            <button className="btn btn-primary" onClick={() => navigate('/')}>
              Go Home
            </button>
          </div>
        </div>
      </section>
    );
  }

  // ════════════════════════════════════════════════
  // Wizard
  // ════════════════════════════════════════════════
  return (
    <section className="container">
      <div className="booking-wizard">
        {/* Wizard Steps Indicator */}
        <div className="wizard-steps">
          {[1, 2, 3].map((s) => (
            <span key={s} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span className={`wizard-step ${step > s ? 'done' : ''} ${step === s ? 'active' : ''}`}>
                {step > s ? '✓' : s}
              </span>
              {s < 3 && <span className={`wizard-step-line ${step > s ? 'done' : ''}`} />}
            </span>
          ))}
        </div>

        {/* Step 1: Select Services */}
        {step === 1 && (
          <div className="booking-step">
            <h2>Step 1: Select Services</h2>

            <div className="form-group">
              <label>Booking Type</label>
              <select value={bookingType} onChange={(e) => setBookingType(e.target.value)}>
                <option value="consultation">Consultation Only</option>
                <option value="admission">Admission Only</option>
                <option value="both">Consultation + Admission</option>
              </select>
            </div>

            {/* Select Doctor */}
            {(bookingType === 'consultation' || bookingType === 'both') && (
              <div className="mb-24">
                <h4 style={{ marginBottom: 12, color: 'var(--gray-700)' }}>Choose a Doctor (Optional)</h4>
                {doctors.length === 0 ? (
                  <p style={{ color: 'var(--gray-500)', fontSize: '0.9rem' }}>No doctors available.</p>
                ) : (
                  <div className="doctor-grid">
                    {doctors.map((d) => (
                      <DoctorCard
                        key={d.id}
                        doctor={d}
                        selected={selectedDoctor?.id === d.id}
                        onSelect={() => setSelectedDoctor(selectedDoctor?.id === d.id ? null : d)}
                      />
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Select Room */}
            {(bookingType === 'admission' || bookingType === 'both') && (
              <div className="mb-24">
                <h4 style={{ marginBottom: 12, color: 'var(--gray-700)' }}>Choose a Room (Optional)</h4>
                {rooms.length === 0 ? (
                  <p style={{ color: 'var(--gray-500)', fontSize: '0.9rem' }}>No rooms available.</p>
                ) : (
                  <div className="room-grid">
                    {rooms.map((r) => (
                      <RoomCard
                        key={r.id}
                        room={r}
                        selected={selectedRoom?.id === r.id}
                        onSelect={() => setSelectedRoom(selectedRoom?.id === r.id ? null : r)}
                      />
                    ))}
                  </div>
                )}
              </div>
            )}

            <div className="wizard-actions">
              <div />
              <button className="btn btn-primary" onClick={() => setStep(2)}>Next: Choose Dates</button>
            </div>
          </div>
        )}

        {/* Step 2: Select Dates */}
        {step === 2 && (
          <div className="booking-step">
            <h2>Step 2: Choose Dates</h2>

            <div className="form-group">
              <label>Check-in Date *</label>
              <input
                type="date"
                value={checkInDate}
                onChange={(e) => setCheckInDate(e.target.value)}
                min={new Date().toISOString().split('T')[0]}
              />
            </div>

            {(bookingType === 'admission' || bookingType === 'both') && (
              <div className="form-group">
                <label>Check-out Date *</label>
                <input
                  type="date"
                  value={checkOutDate}
                  onChange={(e) => setCheckOutDate(e.target.value)}
                  min={checkInDate || new Date().toISOString().split('T')[0]}
                />
              </div>
            )}

            {/* Price Preview */}
            {pricePreview.breakdown.length > 0 && (
              <div className="price-summary">
                <h4>Price Breakdown</h4>
                {pricePreview.breakdown.map((item, i) => (
                  <div key={i} className="row">
                    <span>{item.label}</span>
                    <span>₹{item.amount.toLocaleString('en-IN')}</span>
                  </div>
                ))}
                <div className="total">
                  <span>Total</span>
                  <span>₹{pricePreview.total.toLocaleString('en-IN')}</span>
                </div>
              </div>
            )}

            <div className="wizard-actions mt-24">
              <button className="btn btn-outline" onClick={() => setStep(1)}>Back</button>
              <button className="btn btn-primary" onClick={() => setStep(3)}>Next: Patient Details</button>
            </div>
          </div>
        )}

        {/* Step 3: Patient Details */}
        {step === 3 && (
          <div className="booking-step">
            <h2>Step 3: Patient Details</h2>

            <div className="form-group">
              <label>Full Name *</label>
              <input
                type="text"
                placeholder="Enter patient name"
                value={patientName}
                onChange={(e) => setPatientName(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label>Phone Number *</label>
              <input
                type="tel"
                placeholder="Enter phone number"
                value={patientPhone}
                onChange={(e) => setPatientPhone(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                placeholder="Enter email (optional)"
                value={patientEmail}
                onChange={(e) => setPatientEmail(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label>Notes</label>
              <textarea
                rows={3}
                placeholder="Any special requests or notes..."
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
              />
            </div>

            {/* Summary */}
            <div className="price-summary">
              <h4>Booking Summary</h4>
              <div className="row"><span>Hospital</span><span>{hospital?.name}</span></div>
              {selectedDoctor && <div className="row"><span>Doctor</span><span>{selectedDoctor.name}</span></div>}
              {selectedRoom && <div className="row"><span>Room</span><span>{selectedRoom.room_type}</span></div>}
              <div className="row"><span>Booking Type</span><span style={{ textTransform: 'capitalize' }}>{bookingType}</span></div>
              <div className="row"><span>Check-in</span><span>{checkInDate}</span></div>
              {checkOutDate && <div className="row"><span>Check-out</span><span>{checkOutDate}</span></div>}
              {pricePreview.breakdown.length > 0 && pricePreview.breakdown.map((item, i) => (
                <div key={i} className="row"><span>{item.label}</span><span>₹{item.amount.toLocaleString('en-IN')}</span></div>
              ))}
              {pricePreview.total > 0 && (
                <div className="total">
                  <span>Total</span>
                  <span>₹{pricePreview.total.toLocaleString('en-IN')}</span>
                </div>
              )}
            </div>

            {bookingError && (
              <div style={{ background: 'var(--danger-light)', color: 'var(--danger)', padding: '12px 16px', borderRadius: 'var(--radius)', marginTop: 16, fontSize: '0.9rem' }}>
                {bookingError}
              </div>
            )}

            <div className="wizard-actions mt-24">
              <button className="btn btn-outline" onClick={() => setStep(2)}>Back</button>
              <button
                className="btn btn-success"
                onClick={handleSubmitBooking}
                disabled={createBooking.isPending}
              >
                {createBooking.isPending ? 'Booking...' : 'Confirm Booking'}
              </button>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
