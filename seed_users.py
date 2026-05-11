"""
Seed demo users for testing.
Run once: python seed_users.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.database.db_manager import create_user, init_db

init_db()

users = [
    ("admin",   "admin@mizan.pk",   "admin123",  "admin"),
    ("lawyer1", "lawyer@mizan.pk",  "law12345",  "lawyer"),
    ("student1","student@mizan.pk", "stu12345",  "student"),
    ("citizen1","citizen@mizan.pk", "cit12345",  "citizen"),
]

print("Seeding demo users...")
for username, email, password, role in users:
    result = create_user(username, email, password, role)
    status = "✓" if result["success"] else "⚠ (already exists)"
    print(f"  {status} {username} ({role})")

print("\nDemo credentials:")
print("  admin   / admin123  — Admin panel access")
print("  lawyer1 / law12345  — Lawyer mode")
print("  student1/ stu12345  — Student mode")
print("  citizen1/ cit12345  — Citizen mode")
