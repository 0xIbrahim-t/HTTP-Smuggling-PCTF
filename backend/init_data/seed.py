import asyncio
from sqlalchemy.orm import Session
from ..database.session import SessionLocal, init_db
from ..models.user import User, UserRole
from ..models.post import Post
from ..utils.security import hash_password

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

        # Create initial posts
        posts = [
            Post(
                title="Welcome to the Blog Platform",
                content="Hello everyone! Welcome to our new blog platform. We've recently upgraded to HTTP/2 for better performance!",
                author_id=admin.id
            ),
            Post(
                title="Security Updates",
                content="We've implemented several security measures to keep our platform safe.",
                author_id=admin.id
            ),
            Post(
                title="Platform Guidelines",
                content="Please read our community guidelines and help us maintain a secure environment.",
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
    # Create tables first
    asyncio.run(init_db())
    # Then seed data
    seed_data()