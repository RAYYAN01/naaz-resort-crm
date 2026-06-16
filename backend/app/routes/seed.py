from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db, init_db
from app.models.room import Room
from app.models.booking import User, UserRole
from app.services.auth_service import get_password_hash

router = APIRouter(prefix="/seed", tags=["seed"])


@router.post("/init")
def seed_database(db: Session = Depends(get_db)):
    init_db()

    existing_rooms = db.query(Room).count()
    if existing_rooms == 0:
        rooms = [
            Room(
                name="Standard Room",
                room_type="Standard Room",
                description="Comfortable room with modern amenities. Perfect for budget-conscious travelers.",
                price_per_night=120,
                max_adults=2,
                max_children=1,
                total_rooms=10,
                available_rooms=10,
                amenities="Wi-Fi,TV,Air Conditioning, Mini Bar, Room Service",
            ),
            Room(
                name="Deluxe Room",
                room_type="Deluxe Room",
                description="Spacious room with premium furnishings and garden view.",
                price_per_night=200,
                max_adults=2,
                max_children=2,
                total_rooms=8,
                available_rooms=8,
                amenities="Wi-Fi,TV,Air Conditioning, Mini Bar, Room Service, Balcony, Garden View",
            ),
            Room(
                name="Suite",
                room_type="Suite",
                description="Luxurious suite with separate living area and panoramic views.",
                price_per_night=350,
                max_adults=3,
                max_children=2,
                total_rooms=5,
                available_rooms=5,
                amenities="Wi-Fi,TV,Air Conditioning, Mini Bar, Room Service, Living Area, Balcony, Ocean View, Jacuzzi",
            ),
            Room(
                name="Villa",
                room_type="Villa",
                description="Private villa with personal pool, garden, and butler service.",
                price_per_night=550,
                max_adults=4,
                max_children=3,
                total_rooms=3,
                available_rooms=3,
                amenities="Wi-Fi,TV,Air Conditioning, Full Bar, Private Pool, Garden, Butler Service, Kitchen, Ocean View",
            ),
            Room(
                name="Presidential Suite",
                room_type="Presidential Suite",
                description="Our finest accommodation with panoramic ocean views, private terrace, and personalized concierge.",
                price_per_night=1200,
                max_adults=4,
                max_children=2,
                total_rooms=2,
                available_rooms=2,
                amenities="Wi-Fi,TV,Air Conditioning,Full Bar,Private Pool,Butler Service,Personal Concierge,Terrace,Ocean View,Jacuzzi,Private Chef",
            ),
        ]

        for room in rooms:
            db.add(room)
        db.commit()

    # Check for existing admin user
    existing_admin = db.query(User).filter(User.role == UserRole.ADMIN).first()
    if not existing_admin:
        admin_user = User(
            username="admin",
            email="admin@naazresort.com",
            hashed_password=get_password_hash("admin123"),
            full_name="Administrator",
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        return {"message": f"Seeded database successfully! Created admin user: admin / admin123"}

    return {"message": "Database already seeded."}
