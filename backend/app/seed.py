"""
Seed script — populates the database with demo hospitals, doctors, and rooms.

Run with:
    cd backend
    python -m app.seed
"""

from app.database import SessionLocal, engine, Base
from app.models import Hospital, Doctor, Room

# Drop & recreate all tables (development only!)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# ── Seed Data ──────────────────────────────────────────────────────────────

hospitals_data = [
    {
        "name": "City General Hospital",
        "address": "123 Marine Drive, Colaba",
        "city": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400001",
        "phone": "022-22345678",
        "email": "info@citygenhospital.com",
        "website": "https://citygenhospital.com",
        "rating": 4.5,
        "description": "Multi-specialty hospital with state-of-the-art cardiac and orthopedic care.",
        "image_url": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=600",
    },
    {
        "name": "Apollo Health City",
        "address": "Jubilee Hills, Road No. 72",
        "city": "Delhi",
        "state": "Delhi",
        "pincode": "110001",
        "phone": "011-23456789",
        "email": "contact@apollohealth.com",
        "website": "https://apollohealth.com",
        "rating": 4.7,
        "description": "World-class healthcare facility offering comprehensive medical services across all major specialties.",
        "image_url": "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=600",
    },
    {
        "name": "Fortis Memorial",
        "address": "Sector 44, Opposite HUDA City Centre",
        "city": "Bangalore",
        "state": "Karnataka",
        "pincode": "560001",
        "phone": "080-34567890",
        "email": "info@fortismemorial.com",
        "website": "https://fortismemorial.com",
        "rating": 4.6,
        "description": "Leading neuroscience and oncology center with advanced diagnostic and treatment facilities.",
        "image_url": "https://images.unsplash.com/photo-1538108149393-fbbd81895907?w=600",
    },
    {
        "name": "AIIMS Delhi",
        "address": "Sri Aurobindo Marg, Ansari Nagar",
        "city": "Delhi",
        "state": "Delhi",
        "pincode": "110029",
        "phone": "011-26588500",
        "email": "info@aiims.edu",
        "website": "https://aiims.edu",
        "rating": 4.8,
        "description": "India's premier teaching hospital offering comprehensive medical services across all specialties.",
        "image_url": "https://images.unsplash.com/photo-1551076805-e1869033e561?w=600",
    },
    {
        "name": "Manipal Hospital",
        "address": "98, HAL Airport Road",
        "city": "Chennai",
        "state": "Tamil Nadu",
        "pincode": "600001",
        "phone": "044-23456789",
        "email": "contact@manipalhospital.com",
        "website": "https://manipalhospitals.com",
        "rating": 4.4,
        "description": "Trusted healthcare provider with excellence in cardiology and pediatric care.",
        "image_url": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=600",
    },
    {
        "name": "Max Super Specialty",
        "address": "FC-50, C & D Block, Shalimar Bagh",
        "city": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400002",
        "phone": "022-34567890",
        "email": "info@maxhospital.com",
        "website": "https://maxhealthcare.in",
        "rating": 4.3,
        "description": "Specialized in orthopedics and ENT with advanced surgical facilities.",
        "image_url": "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=600",
    },
    {
        "name": "Kokilaben Dhirubhai Ambani Hospital",
        "address": "Rao Saheb Achutrao Patwardhan Marg, Four Bungalows",
        "city": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400053",
        "phone": "022-30999999",
        "email": "info@kdhospital.com",
        "website": "https://kokilabenhospital.com",
        "rating": 4.6,
        "description": "Advanced multi-specialty hospital with cutting-edge technology and world-class patient care.",
        "image_url": "https://images.unsplash.com/photo-1538108149393-fbbd81895907?w=600",
    },
    {
        "name": "Medanta Medicity",
        "address": "Sector 38, CH Baktawar Singh Road",
        "city": "Gurgaon",
        "state": "Haryana",
        "pincode": "122001",
        "phone": "0124-4141414",
        "email": "info@medanta.org",
        "website": "https://medanta.org",
        "rating": 4.5,
        "description": "Premier multi-super specialty institute with focus on cardiology and gastroenterology.",
        "image_url": "https://images.unsplash.com/photo-1551076805-e1869033e561?w=600",
    },
]

doctors_by_hospital = [
    # City General Hospital (Mumbai) — Cardiology, Orthopedics
    [
        {"name": "Dr. Rajesh Sharma", "specialization": "Cardiology", "experience_years": 18, "qualification": "MD, DM Cardiology", "consultation_fee": 1500, "availability": {"days": ["Mon", "Wed", "Fri"], "slots": ["09:00-13:00", "17:00-19:00"]}},
        {"name": "Dr. Priya Mehta", "specialization": "Cardiology", "experience_years": 12, "qualification": "MD, DNB Cardiology", "consultation_fee": 1200, "availability": {"days": ["Tue", "Thu", "Sat"], "slots": ["10:00-14:00"]}},
        {"name": "Dr. Vikram Singh", "specialization": "Orthopedics", "experience_years": 20, "qualification": "MS Orthopedics", "consultation_fee": 1800, "availability": {"days": ["Mon", "Tue", "Thu", "Sat"], "slots": ["09:00-13:00"]}},
        {"name": "Dr. Anjali Patel", "specialization": "Orthopedics", "experience_years": 10, "qualification": "MS Ortho, DNB", "consultation_fee": 1000, "availability": {"days": ["Wed", "Fri"], "slots": ["14:00-18:00"]}},
    ],
    # Apollo Health City (Delhi) — Multi-specialty
    [
        {"name": "Dr. Suresh Gupta", "specialization": "Neurology", "experience_years": 22, "qualification": "MD, DM Neurology", "consultation_fee": 2000, "availability": {"days": ["Mon", "Wed", "Fri"], "slots": ["09:00-13:00"]}},
        {"name": "Dr. Kavita Reddy", "specialization": "Oncology", "experience_years": 15, "qualification": "MD Radiotherapy", "consultation_fee": 2500, "availability": {"days": ["Tue", "Thu", "Sat"], "slots": ["10:00-15:00"]}},
        {"name": "Dr. Amit Verma", "specialization": "Cardiology", "experience_years": 16, "qualification": "MD, DM Cardiology", "consultation_fee": 1800, "availability": {"days": ["Mon", "Tue", "Thu"], "slots": ["08:00-12:00"]}},
        {"name": "Dr. Neha Kapoor", "specialization": "Pediatrics", "experience_years": 11, "qualification": "MD Pediatrics", "consultation_fee": 1000, "availability": {"days": ["Mon", "Wed", "Fri", "Sat"], "slots": ["09:00-13:00"]}},
        {"name": "Dr. Rohan Desai", "specialization": "Dermatology", "experience_years": 9, "qualification": "MD Dermatology", "consultation_fee": 1200, "availability": {"days": ["Tue", "Thu", "Sat"], "slots": ["14:00-18:00"]}},
    ],
    # Fortis Memorial (Bangalore) — Neurology, Oncology
    [
        {"name": "Dr. Meera Iyer", "specialization": "Neurology", "experience_years": 19, "qualification": "MD, DM Neurology", "consultation_fee": 2200, "availability": {"days": ["Mon", "Tue", "Thu"], "slots": ["09:00-14:00"]}},
        {"name": "Dr. Sanjay Rao", "specialization": "Oncology", "experience_years": 21, "qualification": "MD, DM Oncology", "consultation_fee": 2800, "availability": {"days": ["Wed", "Fri", "Sat"], "slots": ["10:00-15:00"]}},
        {"name": "Dr. Pooja Nair", "specialization": "Radiology", "experience_years": 13, "qualification": "MD Radiology", "consultation_fee": 1500, "availability": {"days": ["Mon", "Wed", "Fri"], "slots": ["09:00-13:00"]}},
    ],
    # AIIMS Delhi — All specializations
    [
        {"name": "Dr. Anil Kumar", "specialization": "Cardiology", "experience_years": 25, "qualification": "MD, DM Cardiology, FACC", "consultation_fee": 800, "availability": {"days": ["Mon", "Wed", "Fri"], "slots": ["09:00-14:00"]}},
        {"name": "Dr. Sunita Devi", "specialization": "Neurology", "experience_years": 23, "qualification": "MD, DM Neurology", "consultation_fee": 800, "availability": {"days": ["Tue", "Thu"], "slots": ["09:00-14:00"]}},
        {"name": "Dr. Rakesh Tiwari", "specialization": "Orthopedics", "experience_years": 20, "qualification": "MS Orthopedics", "consultation_fee": 500, "availability": {"days": ["Mon", "Tue", "Fri"], "slots": ["09:00-13:00"]}},
        {"name": "Dr. Lakshmi Nair", "specialization": "Gastroenterology", "experience_years": 17, "qualification": "MD, DM Gastroenterology", "consultation_fee": 800, "availability": {"days": ["Wed", "Thu", "Sat"], "slots": ["09:00-13:00"]}},
    ],
    # Manipal Hospital (Chennai) — Cardiology, Pediatrics
    [
        {"name": "Dr. Arvind Subramanian", "specialization": "Cardiology", "experience_years": 20, "qualification": "MD, DM Cardiology", "consultation_fee": 1400, "availability": {"days": ["Mon", "Thu", "Sat"], "slots": ["09:00-14:00"]}},
        {"name": "Dr. Shalini Menon", "specialization": "Pediatrics", "experience_years": 14, "qualification": "MD Pediatrics", "consultation_fee": 900, "availability": {"days": ["Mon", "Wed", "Fri"], "slots": ["09:00-13:00"]}},
        {"name": "Dr. Karthik Rajan", "specialization": "ENT", "experience_years": 16, "qualification": "MS ENT", "consultation_fee": 1100, "availability": {"days": ["Tue", "Thu", "Sat"], "slots": ["10:00-14:00"]}},
    ],
    # Max Super Specialty (Mumbai) — Orthopedics, ENT
    [
        {"name": "Dr. Rahul Joshi", "specialization": "Orthopedics", "experience_years": 18, "qualification": "MS Orthopedics", "consultation_fee": 1600, "availability": {"days": ["Mon", "Wed", "Fri"], "slots": ["09:00-13:00"]}},
        {"name": "Dr. Deepa Shah", "specialization": "ENT", "experience_years": 14, "qualification": "MS ENT, DLO", "consultation_fee": 1300, "availability": {"days": ["Tue", "Thu", "Sat"], "slots": ["10:00-14:00"]}},
        {"name": "Dr. Manoj Thakur", "specialization": "Physiotherapy", "experience_years": 10, "qualification": "MPT", "consultation_fee": 700, "availability": {"days": ["Mon", "Tue", "Wed", "Thu", "Fri"], "slots": ["08:00-16:00"]}},
    ],
    # Kokilaben Ambani (Mumbai) — Multi-specialty
    [
        {"name": "Dr. Ritu Agarwal", "specialization": "Cardiology", "experience_years": 19, "qualification": "MD, DM Cardiology", "consultation_fee": 2000, "availability": {"days": ["Mon", "Wed", "Fri"], "slots": ["09:00-13:00"]}},
        {"name": "Dr. Vivek Khanna", "specialization": "Oncology", "experience_years": 21, "qualification": "MD, DM Oncology", "consultation_fee": 2500, "availability": {"days": ["Tue", "Thu", "Sat"], "slots": ["09:00-14:00"]}},
        {"name": "Dr. Seema Deshmukh", "specialization": "Gynecology", "experience_years": 16, "qualification": "MD, DGO", "consultation_fee": 1500, "availability": {"days": ["Mon", "Tue", "Thu", "Fri"], "slots": ["10:00-15:00"]}},
        {"name": "Dr. Nitin Bansal", "specialization": "Urology", "experience_years": 15, "qualification": "MS, MCh Urology", "consultation_fee": 1800, "availability": {"days": ["Mon", "Wed", "Fri"], "slots": ["09:00-13:00"]}},
    ],
    # Medanta Medicity (Gurgaon) — Cardiology, Gastroenterology
    [
        {"name": "Dr. Alok Srivastava", "specialization": "Cardiology", "experience_years": 23, "qualification": "MD, DM Cardiology, FACC", "consultation_fee": 2200, "availability": {"days": ["Mon", "Tue", "Thu"], "slots": ["09:00-14:00"]}},
        {"name": "Dr. Poonam Yadav", "specialization": "Gastroenterology", "experience_years": 17, "qualification": "MD, DM Gastroenterology", "consultation_fee": 1800, "availability": {"days": ["Wed", "Fri", "Sat"], "slots": ["09:00-13:00"]}},
        {"name": "Dr. Sameer Khan", "specialization": "Nephrology", "experience_years": 14, "qualification": "MD, DM Nephrology", "consultation_fee": 1600, "availability": {"days": ["Mon", "Wed", "Fri"], "slots": ["10:00-15:00"]}},
        {"name": "Dr. Ananya Mishra", "specialization": "Endocrinology", "experience_years": 12, "qualification": "MD, DM Endocrinology", "consultation_fee": 1500, "availability": {"days": ["Tue", "Thu"], "slots": ["09:00-14:00"]}},
    ],
]

rooms_by_hospital = [
    # City General Hospital
    [
        {"room_type": "General Ward", "room_number": "GW-101", "price_per_day": 500, "is_available": True, "amenities": ["Shared Bathroom", "Fan", "Basic Bed"], "description": "Economical general ward with 6 beds"},
        {"room_type": "Semi-Private", "room_number": "SP-201", "price_per_day": 1500, "is_available": True, "amenities": ["AC", "TV", "Attached Bathroom"], "description": "Twin sharing room with TV and AC"},
        {"room_type": "Private", "room_number": "PR-301", "price_per_day": 3000, "is_available": True, "amenities": ["AC", "TV", "WiFi", "Attached Bathroom", "Sofa"], "description": "Single occupancy private room"},
        {"room_type": "ICU", "room_number": "ICU-001", "price_per_day": 8000, "is_available": True, "amenities": ["Ventilator", "Monitor", "24x7 Nursing"], "description": "Intensive Care Unit bed"},
        {"room_type": "Deluxe", "room_number": "DLX-501", "price_per_day": 5500, "is_available": True, "amenities": ["AC", "TV", "WiFi", "Attached Bathroom", "Sofa", "Mini-Fridge"], "description": "Premium deluxe room with extra amenities"},
    ],
    # Apollo Health City
    [
        {"room_type": "General Ward", "room_number": "GW-110", "price_per_day": 600, "is_available": True, "amenities": ["Shared Bathroom", "Fan", "Basic Bed"], "description": "General ward bed"},
        {"room_type": "Semi-Private", "room_number": "SP-210", "price_per_day": 2000, "is_available": True, "amenities": ["AC", "TV", "Attached Bathroom"], "description": "Twin sharing semi-private room"},
        {"room_type": "Private", "room_number": "PR-310", "price_per_day": 4000, "is_available": True, "amenities": ["AC", "TV", "WiFi", "Attached Bathroom", "Sofa", "Refrigerator"], "description": "Premium private room"},
        {"room_type": "ICU", "room_number": "ICU-010", "price_per_day": 10000, "is_available": True, "amenities": ["Ventilator", "Monitor", "24x7 Nursing", "Isolation"], "description": "Advanced ICU bed"},
        {"room_type": "Deluxe", "room_number": "DLX-510", "price_per_day": 7000, "is_available": True, "amenities": ["AC", "TV", "WiFi", "Attached Bathroom", "Sofa", "Mini-Fridge", "In-room Dining"], "description": "Luxury deluxe suite"},
    ],
    # Fortis Memorial
    [
        {"room_type": "General Ward", "room_number": "GW-201", "price_per_day": 550, "is_available": True, "amenities": ["Shared Bathroom", "Fan"], "description": "General ward"},
        {"room_type": "Private", "room_number": "PR-401", "price_per_day": 3500, "is_available": True, "amenities": ["AC", "TV", "WiFi", "Attached Bathroom"], "description": "Private single room"},
        {"room_type": "ICU", "room_number": "ICU-020", "price_per_day": 9000, "is_available": True, "amenities": ["Ventilator", "Monitor", "24x7 Nursing"], "description": "ICU critical care"},
        {"room_type": "Deluxe", "room_number": "DLX-601", "price_per_day": 6000, "is_available": True, "amenities": ["AC", "TV", "WiFi", "Attached Bathroom", "Sofa", "Mini-Fridge"], "description": "Deluxe room"},
    ],
    # AIIMS Delhi
    [
        {"room_type": "General Ward", "room_number": "GW-301", "price_per_day": 200, "is_available": True, "amenities": ["Shared Bathroom", "Fan"], "description": "Subsidized general ward"},
        {"room_type": "Semi-Private", "room_number": "SP-301", "price_per_day": 800, "is_available": True, "amenities": ["AC", "TV", "Attached Bathroom"], "description": "Semi-private room"},
        {"room_type": "Private", "room_number": "PR-501", "price_per_day": 1500, "is_available": True, "amenities": ["AC", "TV", "WiFi", "Attached Bathroom"], "description": "Private room"},
        {"room_type": "ICU", "room_number": "ICU-030", "price_per_day": 4000, "is_available": True, "amenities": ["Ventilator", "Monitor", "24x7 Nursing"], "description": "Teaching hospital ICU"},
    ],
    # Manipal Hospital
    [
        {"room_type": "General Ward", "room_number": "GW-401", "price_per_day": 450, "is_available": True, "amenities": ["Shared Bathroom", "Fan"], "description": "General ward"},
        {"room_type": "Semi-Private", "room_number": "SP-401", "price_per_day": 1200, "is_available": True, "amenities": ["AC", "TV", "Attached Bathroom"], "description": "Semi-private twin sharing"},
        {"room_type": "Private", "room_number": "PR-601", "price_per_day": 2500, "is_available": True, "amenities": ["AC", "TV", "WiFi", "Attached Bathroom"], "description": "Private room"},
        {"room_type": "Deluxe", "room_number": "DLX-701", "price_per_day": 5000, "is_available": True, "amenities": ["AC", "TV", "WiFi", "Attached Bathroom", "Sofa", "Mini-Fridge"], "description": "Deluxe room"},
    ],
    # Max Super Specialty
    [
        {"room_type": "General Ward", "room_number": "GW-501", "price_per_day": 500, "is_available": True, "amenities": ["Shared Bathroom", "Fan"], "description": "General ward"},
        {"room_type": "Private", "room_number": "PR-701", "price_per_day": 3000, "is_available": True, "amenities": ["AC", "TV", "WiFi", "Attached Bathroom"], "description": "Private room"},
        {"room_type": "ICU", "room_number": "ICU-040", "price_per_day": 8500, "is_available": True, "amenities": ["Ventilator", "Monitor", "24x7 Nursing"], "description": "ICU bed"},
        {"room_type": "Deluxe", "room_number": "DLX-801", "price_per_day": 5500, "is_available": True, "amenities": ["AC", "TV", "WiFi", "Attached Bathroom", "Sofa", "Mini-Fridge"], "description": "Deluxe suite"},
    ],
    # Kokilaben Ambani
    [
        {"room_type": "Semi-Private", "room_number": "SP-501", "price_per_day": 2500, "is_available": True, "amenities": ["AC", "TV", "WiFi", "Attached Bathroom"], "description": "Premium semi-private"},
        {"room_type": "Private", "room_number": "PR-801", "price_per_day": 5000, "is_available": True, "amenities": ["AC", "TV", "WiFi", "Attached Bathroom", "Sofa", "Refrigerator"], "description": "Private deluxe room"},
        {"room_type": "ICU", "room_number": "ICU-050", "price_per_day": 12000, "is_available": True, "amenities": ["Ventilator", "Monitor", "24x7 Nursing", "Isolation"], "description": "Advanced ICU"},
        {"room_type": "Deluxe", "room_number": "DLX-901", "price_per_day": 8000, "is_available": True, "amenities": ["AC", "TV", "WiFi", "Attached Bathroom", "Sofa", "Mini-Fridge", "In-room Dining", "Guest Bed"], "description": "Super deluxe suite"},
    ],
    # Medanta Medicity
    [
        {"room_type": "General Ward", "room_number": "GW-601", "price_per_day": 700, "is_available": True, "amenities": ["Shared Bathroom", "Fan", "Basic Bed"], "description": "General ward"},
        {"room_type": "Semi-Private", "room_number": "SP-601", "price_per_day": 2200, "is_available": True, "amenities": ["AC", "TV", "Attached Bathroom"], "description": "Semi-private"},
        {"room_type": "Private", "room_number": "PR-901", "price_per_day": 4500, "is_available": True, "amenities": ["AC", "TV", "WiFi", "Attached Bathroom", "Sofa"], "description": "Private room"},
        {"room_type": "ICU", "room_number": "ICU-060", "price_per_day": 11000, "is_available": True, "amenities": ["Ventilator", "Monitor", "24x7 Nursing"], "description": "ICU bed"},
        {"room_type": "Deluxe", "room_number": "DLX-1001", "price_per_day": 7500, "is_available": True, "amenities": ["AC", "TV", "WiFi", "Attached Bathroom", "Sofa", "Mini-Fridge", "In-room Dining"], "description": "Deluxe suite"},
    ],
]

# ── Insert data ────────────────────────────────────────────────────────────

for i, h_data in enumerate(hospitals_data):
    hospital = Hospital(**h_data)
    db.add(hospital)
    db.flush()  # get hospital.id

    for d_data in doctors_by_hospital[i]:
        d_data["hospital_id"] = hospital.id
        doctor = Doctor(**d_data)
        db.add(doctor)

    for r_data in rooms_by_hospital[i]:
        r_data["hospital_id"] = hospital.id
        room = Room(**r_data)
        db.add(room)

db.commit()
db.close()

print("Seed data inserted successfully!")
print(f"   - {len(hospitals_data)} hospitals")
print(f"   - {sum(len(d) for d in doctors_by_hospital)} doctors")
print(f"   - {sum(len(r) for r in rooms_by_hospital)} rooms")
