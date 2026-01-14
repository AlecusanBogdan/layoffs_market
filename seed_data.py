"""
Seed script to populate the database with departments and positions
Run this after starting the app at least once (to create the database)
"""

import os
import sys

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Department, Position

# Data parsed from the provided table
# "total" = total employees in that position
# We'll set positions_to_cut to 0 initially - admin can set it manually
SEED_DATA = {
    "Boost": [
        {"title": "Machine Learning Engineer", "cor_code": "251204", "total": 1},
    ],
    "CC (Caesars Slots)": [
        {"title": "2D Animator", "cor_code": "251101", "total": 1},
        {"title": "2D Artist", "cor_code": "251101, 251201", "total": 7},
        {"title": "Animator", "cor_code": "251101", "total": 3},
        {"title": "Art Group Manager", "cor_code": "122314", "total": 1},
        {"title": "Art Team Leader", "cor_code": "122314, 251206", "total": 2},
        {"title": "C# Developer", "cor_code": "251202, 251204, 351201", "total": 17},
        {"title": "C# Technical Lead", "cor_code": "251202, 251204", "total": 5},
        {"title": "Copywriter", "cor_code": "351202", "total": 1},
        {"title": "Flash Integrator", "cor_code": "251101, 351202", "total": 7},
        {"title": "Java Developer", "cor_code": "251202, 251204", "total": 11},
        {"title": "Java Technical Lead", "cor_code": "121904, 251202, 251204", "total": 5},
        {"title": "JavaScript Developer", "cor_code": "251202, 251204", "total": 2},
        {"title": "JavaScript Technical Lead", "cor_code": "251202", "total": 1},
        {"title": "Lead Animator", "cor_code": "251201", "total": 1},
        {"title": "Manual QA Engineer", "cor_code": "251201, 351202", "total": 17},
        {"title": "Monetization Operations Specialist", "cor_code": "251201", "total": 2},
        {"title": "Product Owner (Tech)", "cor_code": "121904", "total": 1},
        {"title": "Product Senior Expert", "cor_code": "121904", "total": 1},
        {"title": "Program Lead", "cor_code": "251206", "total": 1},
        {"title": "QA Automation Engineer", "cor_code": "251201, 251202, 351202", "total": 4},
        {"title": "QA Automation Team Leader", "cor_code": "251206", "total": 1},
        {"title": "QA Technical Lead", "cor_code": "251201, 351202", "total": 2},
        {"title": "R&D Group Manager", "cor_code": "251206", "total": 3},
        {"title": "R&D Team Leader", "cor_code": "122314, 251206", "total": 9},
        {"title": "Senior Director of Research & Development", "cor_code": "251206", "total": 1},
        {"title": "Technical Product Owner", "cor_code": "122314, 251206", "total": 2},
    ],
    "Cross Communication": [
        {"title": "Communication and Brand Manager", "cor_code": "243104", "total": 1},
    ],
    "Cross Finance": [
        {"title": "Bookkeeper", "cor_code": "263102", "total": 1},
    ],
    "Cross HR": [
        {"title": "HR Director", "cor_code": "121207", "total": 1},
        {"title": "HR Operations Specialist", "cor_code": "242314", "total": 2},
        {"title": "Talent Acquisition Specialist", "cor_code": "242309", "total": 2},
        {"title": "Talent Acquisition Team Lead", "cor_code": "121207", "total": 1},
    ],
    "Cross Legal & Finance": [
        {"title": "Chief Accountant", "cor_code": "112020", "total": 1},
        {"title": "Expert Corporate Counsel", "cor_code": "261103", "total": 1},
    ],
    "Cross Operations": [
        {"title": "HSE Responsible", "cor_code": "242304", "total": 1},
    ],
    "Cross Slots Central": [
        {"title": "2D Animator", "cor_code": "251101", "total": 2},
        {"title": "2D Artist", "cor_code": "251101, 251201, 351202", "total": 5},
        {"title": "Animator", "cor_code": "251101, 251201", "total": 3},
        {"title": "Art Director", "cor_code": "251206", "total": 1},
        {"title": "Art Team Leader", "cor_code": "251206", "total": 2},
        {"title": "Expert Animator", "cor_code": "351202", "total": 1},
        {"title": "Expert Artist", "cor_code": "251101, 351202", "total": 2},
        {"title": "Lead Animator", "cor_code": "251101", "total": 1},
        {"title": "Product Owner", "cor_code": "251206", "total": 2},
        {"title": "Product Team Leader", "cor_code": "251206", "total": 1},
        {"title": "Technical Art Lead", "cor_code": "121904, 251101", "total": 2},
        {"title": "Technical Artist", "cor_code": "251101", "total": 1},
    ],
    "Cross Technologies": [
        {"title": "Incident Engineer", "cor_code": "251201, 351202", "total": 2},
        {"title": "Incident Engineer Expert", "cor_code": "351202", "total": 1},
        {"title": "IT Service Specialist", "cor_code": "251101, 251203", "total": 2},
        {"title": "IT System Engineer", "cor_code": "251101", "total": 1},
        {"title": "Service Operations Analyst", "cor_code": "351202", "total": 1},
        {"title": "Site Reliability Engineer", "cor_code": "251204", "total": 1},
        {"title": "SRE Expert", "cor_code": "251204", "total": 1},
        {"title": "SVP Technologies Program", "cor_code": "251206", "total": 1},
        {"title": "System Operations Engineer", "cor_code": "351202", "total": 1},
        {"title": "Tech Project Management Expert", "cor_code": "121904", "total": 1},
        {"title": "Technical Account Manager", "cor_code": "351202", "total": 1},
        {"title": "MIS Group Manager", "cor_code": "251206", "total": 1},
    ],
    "HOF (House of Fun)": [
        {"title": "Manual QA Engineer", "cor_code": "251201", "total": 2},
        {"title": "Monetization Operation Team Leader", "cor_code": "251206", "total": 1},
        {"title": "Monetization Operations Lead", "cor_code": "351202", "total": 1},
        {"title": "Monetization Operations Specialist", "cor_code": "251201", "total": 1},
        {"title": "QA Technical Lead", "cor_code": "351202", "total": 1},
        {"title": "Technical Art Lead", "cor_code": "351202", "total": 1},
        {"title": "Technical Artist", "cor_code": "251101", "total": 1},
    ],
    "SHARED TECH": [
        {"title": "Director of Architecture", "cor_code": "251101", "total": 1},
    ],
    "WSOP": [
        {"title": "C# Developer", "cor_code": "251202", "total": 1},
        {"title": "Full Stack Developer", "cor_code": "251202", "total": 1},
        {"title": "Java Developer", "cor_code": "251202", "total": 14},
        {"title": "Java Technical Lead", "cor_code": "251202", "total": 3},
        {"title": "JavaScript Developer", "cor_code": "251202, 251204", "total": 3},
        {"title": "JavaScript Technical Lead", "cor_code": "251202", "total": 2},
        {"title": "Manual QA Engineer", "cor_code": "251201, 351202", "total": 16},
        {"title": "Monetization Operation Team Leader", "cor_code": "251206", "total": 1},
        {"title": "QA Automation Engineer", "cor_code": "251202, 351202", "total": 5},
        {"title": "QA Automation Team Leader", "cor_code": "251206", "total": 1},
        {"title": "QA Manager", "cor_code": "251206", "total": 1},
        {"title": "QA Technical Lead", "cor_code": "251201, 351202", "total": 3},
        {"title": "R&D Director", "cor_code": "251206", "total": 1},
        {"title": "R&D Group Manager", "cor_code": "251206", "total": 3},
        {"title": "R&D Team Leader", "cor_code": "251206", "total": 8},
        {"title": "Release Engineer", "cor_code": "251206", "total": 1},
        {"title": "Software Architect", "cor_code": "251101", "total": 2},
        {"title": "Technical Artist", "cor_code": "251101, 351202", "total": 5},
        {"title": "Technical Product Owner", "cor_code": "251202", "total": 1},
        {"title": "Unity Developer", "cor_code": "251202, 251204, 351201, 351202", "total": 18},
        {"title": "Unity Technical Lead", "cor_code": "251202, 251204", "total": 4},
        {"title": "VP of Research & Development", "cor_code": "112019", "total": 1},
    ],
    "Youda": [
        {"title": "Product Manager", "cor_code": "251206", "total": 1},
    ],
}


def seed_database():
    with app.app_context():
        # Recreate tables to add new column
        db.create_all()
        
        # Check if data already exists
        existing_depts = Department.query.count()
        if existing_depts > 0:
            print(f"⚠️  Database already has {existing_depts} departments.")
            response = input("Do you want to clear and re-seed? (y/N): ")
            if response.lower() != 'y':
                print("Aborted.")
                return
            
            # Clear existing data
            print("🗑️  Clearing existing data...")
            Position.query.delete()
            Department.query.delete()
            db.session.commit()
        
        total_positions = 0
        total_employees = 0
        
        print("\n💀 SEEDING THE LAYOFF DATABASE 💀\n")
        print("=" * 60)
        
        for dept_name, positions in SEED_DATA.items():
            # Create department
            dept = Department(name=dept_name, code=dept_name[:3].upper())
            db.session.add(dept)
            db.session.flush()  # Get the ID
            
            dept_employees = 0
            for pos_data in positions:
                position = Position(
                    title=pos_data["title"],
                    cor_code=pos_data["cor_code"],
                    total_employees=pos_data["total"],
                    positions_to_cut=0,  # Admin will set this
                    department_id=dept.id
                )
                db.session.add(position)
                total_positions += 1
                dept_employees += pos_data["total"]
            
            total_employees += dept_employees
            print(f"🏢 {dept_name}: {len(positions)} positions, {dept_employees} employees")
        
        db.session.commit()
        
        print("=" * 60)
        print(f"\n✅ Database seeded successfully!")
        print(f"   📊 Total departments: {len(SEED_DATA)}")
        print(f"   💼 Total position types: {total_positions}")
        print(f"   👥 Total employees: {total_employees}")
        print(f"\n💀 Now go to admin panel to:")
        print(f"   1. Set 'positions to cut' for each position")
        print(f"   2. Add candidates (employees) with photos and odds")
        print(f"\n   http://127.0.0.1:5001/admin")


if __name__ == "__main__":
    seed_database()
