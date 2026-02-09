from app.core.db import SessionLocal
from app.infrastructure.models.user import User

def seed_db():
    db = SessionLocal()
    try:
        # Check if admin exists
        admin = db.query(User).filter(User.email == "admin@example.com").first()
        if not admin:
            admin = User(
                email="admin@example.com",
                role="ADMIN"
            )
            db.add(admin)
            db.commit()
            print("Admin user seeded.")
        else:
            print("Admin user already exists.")
    except Exception as e:
        print(f"Failed to seed DB: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
