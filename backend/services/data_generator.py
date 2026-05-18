"""
Synthetic data generator for training and testing
Generates realistic travel booking and refund data
"""

import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import List

import crud


# Data constants
AIRLINES = [
    "Air India", "Emirates", "Lufthansa", "British Airways", "Singapore Airlines",
    "Qatar Airways", "United Airlines", "Delta Airlines", "American Airlines", "KLM"
]

HOTELS = [
    "Marriott", "Hilton", "Hyatt", "Radisson", "ITC Hotels",
    "Taj Hotels", "Oberoi Hotels", "Holiday Inn", "Sheraton", "Westin"
]

INSURANCE_PROVIDERS = [
    "ICICI Lombard", "HDFC ERGO", "Bajaj Allianz", "Tata AIG", "Reliance General",
    "World Nomads", "Allianz Global", "AXA Travel Insurance"
]

VISA_SERVICES = [
    "VFS Global", "BLS International", "Cox & Kings", "Thomas Cook", "CIBT Visas"
]

CITIES = [
    ("Mumbai", "India"), ("Delhi", "India"), ("Bangalore", "India"),
    ("Dubai", "UAE"), ("London", "UK"), ("Paris", "France"),
    ("New York", "USA"), ("Singapore", "Singapore"), ("Tokyo", "Japan"),
    ("Sydney", "Australia"), ("Bangkok", "Thailand"), ("Istanbul", "Turkey"),
    ("Berlin", "Germany"), ("Toronto", "Canada"), ("Hong Kong", "China")
]

EVENT_TYPES = [
    "pandemic",           # COVID-19, health emergencies
    "war",               # Military conflicts
    "natural_disaster",  # Earthquakes, hurricanes, floods
    "flight_cancellation", # Airline operational issues
    "terrorism",         # Security threats, attacks
    "political_instability", # Government changes, protests
    "economic_crisis",   # Currency collapse, sanctions
    "civil_unrest"       # Riots, demonstrations
]
SEVERITIES = ["low", "medium", "high", "critical"]
COMPONENT_TYPES = ["flight", "hotel", "visa", "insurance"]


def random_date(start_days: int, end_days: int) -> datetime:
    """Generate random date within range"""
    days = random.randint(start_days, end_days)
    return datetime.now() + timedelta(days=days)


def generate_provider_policies(db: Session):
    """Generate provider refund policies"""
    print("  📋 Generating provider policies...")
    
    # Airlines
    for airline in AIRLINES:
        policy_data = {
            "provider_name": airline,
            "provider_type": "airline",
            "standard_refund_percentage": random.choice([0, 50, 75, 100]),
            "force_majeure_refund_percentage": random.choice([75, 85, 90, 100]),
            "cancellation_fee": random.choice([0, 50, 100, 150, 200]),
            "refund_processing_days": random.randint(15, 45),
            "policy_text": f"{airline} standard refund policy with cancellation fees applicable.",
            "force_majeure_clause": f"{airline} provides enhanced refunds during force majeure events as per international aviation regulations."
        }
        crud.create_provider_policy(db, policy_data)
    
    # Hotels
    for hotel in HOTELS:
        policy_data = {
            "provider_name": hotel,
            "provider_type": "hotel",
            "standard_refund_percentage": random.choice([0, 50, 80, 100]),
            "force_majeure_refund_percentage": random.choice([80, 90, 100]),
            "cancellation_fee": random.choice([0, 25, 50, 100]),
            "refund_processing_days": random.randint(10, 30),
            "policy_text": f"{hotel} cancellation policy varies by booking type.",
            "force_majeure_clause": f"{hotel} offers flexible cancellation during emergencies."
        }
        crud.create_provider_policy(db, policy_data)
    
    # Insurance
    for insurer in INSURANCE_PROVIDERS:
        policy_data = {
            "provider_name": insurer,
            "provider_type": "insurance",
            "standard_refund_percentage": 0,
            "force_majeure_refund_percentage": random.choice([50, 75, 90, 100]),
            "cancellation_fee": 0,
            "refund_processing_days": random.randint(20, 60),
            "policy_text": f"{insurer} travel insurance with comprehensive coverage.",
            "force_majeure_clause": f"{insurer} covers trip cancellations due to war, natural disasters, and pandemics (subject to terms)."
        }
        crud.create_provider_policy(db, policy_data)
    
    # Visa services
    for visa_service in VISA_SERVICES:
        policy_data = {
            "provider_name": visa_service,
            "provider_type": "visa",
            "standard_refund_percentage": 0,
            "force_majeure_refund_percentage": random.choice([0, 25, 50]),
            "cancellation_fee": random.choice([0, 50, 100]),
            "refund_processing_days": random.randint(30, 90),
            "policy_text": f"{visa_service} visa processing fees are generally non-refundable.",
            "force_majeure_clause": f"{visa_service} may offer partial refunds in exceptional circumstances."
        }
        crud.create_provider_policy(db, policy_data)
    
    print(f"  ✅ Created {len(AIRLINES) + len(HOTELS) + len(INSURANCE_PROVIDERS) + len(VISA_SERVICES)} provider policies")


def generate_risk_events(db: Session):
    """Generate current and historical risk events"""
    print("  ⚠️  Generating risk events...")
    
    events = [
        # Active Events
        {
            "event_type": "war",
            "severity": "critical",
            "affected_region": "Ukraine",
            "start_date": datetime(2022, 2, 24),
            "end_date": None,
            "description": "Ongoing military conflict in Ukraine",
            "is_active": True
        },
        {
            "event_type": "civil_unrest",
            "severity": "high",
            "affected_region": "Middle East",
            "start_date": datetime(2023, 10, 7),
            "end_date": None,
            "description": "Regional tensions and conflicts",
            "is_active": True
        },
        {
            "event_type": "political_instability",
            "severity": "medium",
            "affected_region": "Myanmar",
            "start_date": datetime(2024, 1, 1),
            "end_date": None,
            "description": "Ongoing political crisis and protests",
            "is_active": True
        },
        {
            "event_type": "economic_crisis",
            "severity": "high",
            "affected_region": "Argentina",
            "start_date": datetime(2024, 6, 1),
            "end_date": None,
            "description": "Currency devaluation and economic instability",
            "is_active": True
        },
        # Historical Events
        {
            "event_type": "pandemic",
            "severity": "critical",
            "affected_region": "Global",
            "start_date": datetime(2020, 3, 11),
            "end_date": datetime(2023, 5, 5),
            "description": "COVID-19 pandemic",
            "is_active": False
        },
        {
            "event_type": "natural_disaster",
            "severity": "critical",
            "affected_region": "Turkey",
            "start_date": datetime(2023, 2, 6),
            "end_date": datetime(2023, 3, 15),
            "description": "Major earthquake affecting multiple cities",
            "is_active": False
        },
        {
            "event_type": "natural_disaster",
            "severity": "high",
            "affected_region": "Morocco",
            "start_date": datetime(2023, 9, 8),
            "end_date": datetime(2023, 9, 20),
            "description": "Earthquake in Atlas Mountains",
            "is_active": False
        },
        {
            "event_type": "terrorism",
            "severity": "high",
            "affected_region": "France",
            "start_date": datetime(2024, 7, 15),
            "end_date": datetime(2024, 7, 20),
            "description": "Security threat during major event",
            "is_active": False
        },
        {
            "event_type": "flight_cancellation",
            "severity": "medium",
            "affected_region": "Europe",
            "start_date": datetime(2024, 8, 1),
            "end_date": datetime(2024, 8, 5),
            "description": "Major airline IT system failure causing widespread cancellations",
            "is_active": False
        },
        {
            "event_type": "natural_disaster",
            "severity": "high",
            "affected_region": "Japan",
            "start_date": datetime(2024, 1, 1),
            "end_date": datetime(2024, 1, 10),
            "description": "Earthquake and tsunami warning",
            "is_active": False
        },
        {
            "event_type": "civil_unrest",
            "severity": "medium",
            "affected_region": "France",
            "start_date": datetime(2023, 6, 27),
            "end_date": datetime(2023, 7, 5),
            "description": "Widespread protests and demonstrations",
            "is_active": False
        },
        {
            "event_type": "economic_crisis",
            "severity": "high",
            "affected_region": "Lebanon",
            "start_date": datetime(2023, 1, 1),
            "end_date": datetime(2023, 12, 31),
            "description": "Banking crisis and currency collapse",
            "is_active": False
        }
    ]
    
    for event_data in events:
        crud.create_risk_event(db, event_data)
    
    print(f"  ✅ Created {len(events)} risk events")


def generate_historical_refunds(db: Session, count: int = 500):
    """Generate historical refund data for ML training"""
    print(f"  📊 Generating {count} historical refund records...")
    
    for _ in range(count):
        component_type = random.choice(COMPONENT_TYPES)
        event_type = random.choice(EVENT_TYPES)
        event_severity = random.choice(SEVERITIES)
        was_force_majeure = random.random() > 0.3
        had_insurance = random.random() > 0.4
        
        # Select provider based on component type
        if component_type == "flight":
            provider = random.choice(AIRLINES)
        elif component_type == "hotel":
            provider = random.choice(HOTELS)
        elif component_type == "insurance":
            provider = random.choice(INSURANCE_PROVIDERS)
        else:  # visa
            provider = random.choice(VISA_SERVICES)
        
        # Generate realistic costs
        if component_type == "flight":
            original_cost = random.uniform(10000, 100000)
        elif component_type == "hotel":
            original_cost = random.uniform(5000, 50000)
        elif component_type == "insurance":
            original_cost = random.uniform(1000, 10000)
        else:  # visa
            original_cost = random.uniform(2000, 15000)
        
        # Calculate refund based on various factors
        base_refund_pct = 0
        
        if was_force_majeure:
            if event_severity == "critical":
                base_refund_pct = random.uniform(70, 100)
            elif event_severity == "high":
                base_refund_pct = random.uniform(50, 85)
            elif event_severity == "medium":
                base_refund_pct = random.uniform(30, 70)
            else:
                base_refund_pct = random.uniform(10, 50)
        else:
            if component_type == "flight":
                base_refund_pct = random.uniform(0, 75)
            elif component_type == "hotel":
                base_refund_pct = random.uniform(0, 80)
            elif component_type == "insurance":
                base_refund_pct = random.uniform(0, 50)
            else:  # visa
                base_refund_pct = random.uniform(0, 25)
        
        # Insurance boost
        if had_insurance and component_type != "insurance":
            base_refund_pct = min(100, base_refund_pct + random.uniform(10, 30))
        
        # Days before travel affects refund
        days_before_travel = random.randint(1, 180)
        if days_before_travel > 90:
            base_refund_pct = min(100, base_refund_pct + random.uniform(5, 15))
        elif days_before_travel < 7:
            base_refund_pct = max(0, base_refund_pct - random.uniform(10, 25))
        
        refund_percentage = max(0, min(100, base_refund_pct))
        refund_amount = original_cost * (refund_percentage / 100)
        
        city, region = random.choice(CITIES)
        
        refund_data = {
            "component_type": component_type,
            "provider_name": provider,
            "original_cost": round(original_cost, 2),
            "refund_amount": round(refund_amount, 2),
            "refund_percentage": round(refund_percentage, 2),
            "event_type": event_type,
            "event_severity": event_severity,
            "days_before_travel": days_before_travel,
            "was_force_majeure": was_force_majeure,
            "had_insurance": had_insurance,
            "refund_date": random_date(-365, -1),
            "region": region
        }
        
        crud.create_historical_refund(db, refund_data)
    
    print(f"  ✅ Created {count} historical refund records")


def generate_sample_bookings(db: Session, count: int = 50):
    """Generate sample travel bookings"""
    print(f"  🎫 Generating {count} sample bookings...")
    
    first_names = ["Rahul", "Priya", "Amit", "Sneha", "Vikram", "Anjali", "Rohan", "Kavya", "Arjun", "Meera"]
    last_names = ["Sharma", "Patel", "Kumar", "Singh", "Reddy", "Iyer", "Gupta", "Mehta", "Joshi", "Nair"]
    
    for i in range(count):
        origin_city, origin_region = random.choice(CITIES)
        dest_city, dest_region = random.choice([c for c in CITIES if c[0] != origin_city])
        
        customer_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        customer_email = f"{customer_name.lower().replace(' ', '.')}@example.com"
        
        travel_date = random_date(30, 180)
        
        # Generate components
        components = []
        
        # Flight
        flight_cost = random.uniform(15000, 80000)
        components.append({
            "component_type": "flight",
            "provider_name": random.choice(AIRLINES),
            "cost": round(flight_cost, 2),
            "refund_policy": "Standard airline refund policy applies",
            "is_refundable": random.choice([True, False]),
            "cancellation_fee": random.choice([0, 100, 200, 500])
        })
        
        # Hotel
        hotel_cost = random.uniform(8000, 40000)
        components.append({
            "component_type": "hotel",
            "provider_name": random.choice(HOTELS),
            "cost": round(hotel_cost, 2),
            "refund_policy": "Free cancellation up to 48 hours before check-in",
            "is_refundable": random.choice([True, False]),
            "cancellation_fee": random.choice([0, 50, 100])
        })
        
        # Visa (70% of bookings)
        if random.random() > 0.3:
            visa_cost = random.uniform(3000, 12000)
            components.append({
                "component_type": "visa",
                "provider_name": random.choice(VISA_SERVICES),
                "cost": round(visa_cost, 2),
                "refund_policy": "Visa fees are non-refundable",
                "is_refundable": False,
                "cancellation_fee": 0
            })
        
        # Insurance (60% of bookings)
        if random.random() > 0.4:
            insurance_cost = random.uniform(2000, 8000)
            components.append({
                "component_type": "insurance",
                "provider_name": random.choice(INSURANCE_PROVIDERS),
                "cost": round(insurance_cost, 2),
                "refund_policy": "Comprehensive travel insurance with force majeure coverage",
                "is_refundable": False,
                "cancellation_fee": 0
            })
        
        from schemas import BookingCreate, BookingComponentCreate
        
        booking_data = BookingCreate(
            customer_name=customer_name,
            customer_email=customer_email,
            travel_date=travel_date,
            destination=dest_city,
            origin=origin_city,
            components=[BookingComponentCreate(**comp) for comp in components]
        )
        
        crud.create_booking(db, booking_data)
    
    print(f"  ✅ Created {count} sample bookings")


def generate_synthetic_data(db: Session):
    """Generate all synthetic data"""
    print("\n🔄 Generating synthetic dataset...")
    
    generate_provider_policies(db)
    generate_risk_events(db)
    generate_historical_refunds(db, count=500)
    generate_sample_bookings(db, count=50)
    
    print("✅ Synthetic data generation complete!\n")

# Made with Bob
