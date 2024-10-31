from sqlalchemy.orm import Session
from ..database.session import SessionLocal, init_db
from ..models.user import User, UserRole
from ..models.post import Post
from ..utils.security import hash_password
import asyncio

# ... previous imports ...

def seed_data():
    db = SessionLocal()
    try:
        # First check if data already exists
        if db.query(User).first() is not None:
            print("Database already seeded!")
            return

        print("Seeding database...")

        # Create admin user
        admin = User(
            username="admin",
            password_hash=hash_password("s3cur3_4dm1n_p4ss!"),
            role=UserRole.ADMIN
        )
        db.add(admin)

        # Create regular users
        alice = User(
            username="alice",
            password_hash=hash_password("user1_pass"),
            role=UserRole.USER
        )
        bob = User(
            username="bob",
            password_hash=hash_password("user2_pass"),
            role=UserRole.USER
        )
        db.add(alice)
        db.add(bob)
        
        # Commit users first to get their IDs
        db.commit()

        # Create initial posts (all from admin now)
        posts = [
            Post(
                title="Welcome to the Official Blog",
                content="Welcome to our company blog! This platform is designed for official company announcements and updates. Only administrators can create posts, but all users can read and report posts if they find any issues.",
                author_id=admin.id
            ),
            Post(
                title="Security Updates and Features",
                content="We've recently upgraded our platform to use HTTP/2 for better performance and security. Please report any suspicious content or technical issues you encounter.",
                author_id=admin.id
            ),
            Post(
                title="Community Guidelines",
                content="While this is a read-only blog for our users, we encourage active participation through the reporting feature. Help us maintain a safe and secure platform!",
                author_id=admin.id
            )
        ]
        
        for post in posts:
            db.add(post)
        
        db.commit()
        print("Database seeded successfully!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(init_db())
    seed_data()