from sqlalchemy.orm import Session
from ..database.session import SessionLocal, init_db
from ..models.user import User, UserRole
from ..models.post import Post
from ..utils.security import hash_password
import asyncio

def seed_data():
    db = SessionLocal()
    try:
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
        db.commit()

        # Create initial posts
        posts = [
            Post(
                title="Welcome to CTF Blog",
                content="This is the official blog platform. Happy hacking!",
                author_id=admin.id
            ),
            Post(
                title="My First Post",
                content="Hello everyone! This is my first post here.",
                author_id=alice.id
            ),
            Post(
                title="Testing the Platform",
                content="Just testing out this new blog platform!",
                author_id=bob.id
            )
        ]
        
        for post in posts:
            db.add(post)
        
        db.commit()

    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(init_db())
    seed_data()