"""
Update positions_to_cut based on before/after data
positions_to_cut = total_employees (before) - after_total
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Department, Position

# After-cut data (what remains after layoffs)
AFTER_CUT_DATA = {
    "Boost": {
        "Machine Learning Engineer": 1,
    },
    "CC (Caesars Slots)": {
        "2D Animator": 1,
        "2D Artist": 6,
        "Animator": 2,
        "Art Group Manager": 1,
        "Art Team Leader": 2,
        "C# Developer": 7,
        "C# Technical Lead": 5,
        "Copywriter": 1,
        "Flash Integrator": 4,
        "Java Developer": 11,
        "Java Technical Lead": 5,
        "JavaScript Developer": 2,
        "JavaScript Technical Lead": 1,
        "Lead Animator": 1,
        "Manual QA Engineer": 11,
        "Monetization Operations Specialist": 2,
        "Product Owner (Tech)": 0,  # Completely cut
        "Product Senior Expert": 1,
        "Program Lead": 1,
        "QA Automation Engineer": 3,
        "QA Automation Team Leader": 0,  # Completely cut
        "QA Technical Lead": 2,
        "R&D Group Manager": 3,
        "R&D Team Leader": 7,
        "Senior Director of Research & Development": 1,
        "Technical Product Owner": 2,
    },
    "Cross Communication": {
        "Communication and Brand Manager": 0,  # Not in after list = cut
    },
    "Cross Finance": {
        "Bookkeeper": 1,
    },
    "Cross HR": {
        "HR Director": 1,
        "HR Operations Specialist": 2,
        "Talent Acquisition Specialist": 1,
        "Talent Acquisition Team Lead": 1,
    },
    "Cross Legal & Finance": {
        "Chief Accountant": 1,
        "Expert Corporate Counsel": 1,
    },
    "Cross Operations": {
        "HSE Responsible": 0,  # Not in after list = cut
    },
    "Cross Slots Central": {
        "2D Animator": 0,  # Not in after list
        "2D Artist": 1,
        "Animator": 0,  # Not in after list
        "Art Director": 1,
        "Art Team Leader": 0,  # Not in after list
        "Expert Animator": 0,  # Not in after list
        "Expert Artist": 1,
        "Lead Animator": 1,
        "Product Owner": 1,
        "Product Team Leader": 1,
        "Technical Art Lead": 0,  # Not in after list
        "Technical Artist": 0,  # Not in after list
    },
    "Cross Technologies": {
        "Incident Engineer": 1,
        "Incident Engineer Expert": 0,  # Not in after list
        "IT Service Specialist": 1,
        "IT System Engineer": 1,
        "Service Operations Analyst": 0,  # Not in after list
        "Site Reliability Engineer": 1,
        "SRE Expert": 1,
        "SVP Technologies Program": 1,
        "System Operations Engineer": 1,
        "Tech Project Management Expert": 1,
        "Technical Account Manager": 1,
        "MIS Group Manager": 1,
    },
    "HOF (House of Fun)": {
        "Manual QA Engineer": 2,
        "Monetization Operation Team Leader": 1,
        "Monetization Operations Lead": 1,
        "Monetization Operations Specialist": 1,
        "QA Technical Lead": 1,
        "Technical Art Lead": 1,
        "Technical Artist": 0,  # Not in after list
    },
    "SHARED TECH": {
        "Director of Architecture": 0,  # Not in after list = cut
    },
    "WSOP": {
        "C# Developer": 1,
        "Full Stack Developer": 1,
        "Java Developer": 14,
        "Java Technical Lead": 3,
        "JavaScript Developer": 3,
        "JavaScript Technical Lead": 2,
        "Manual QA Engineer": 13,
        "Monetization Operation Team Leader": 1,
        "QA Automation Engineer": 3,
        "QA Automation Team Leader": 1,
        "QA Manager": 0,  # Not in after list
        "QA Technical Lead": 3,
        "R&D Director": 1,
        "R&D Group Manager": 3,
        "R&D Team Leader": 8,
        "Release Engineer": 1,
        "Software Architect": 2,
        "Technical Artist": 3,
        "Technical Product Owner": 1,
        "Unity Developer": 15,
        "Unity Technical Lead": 4,
        "VP of Research & Development": 1,
    },
    "Youda": {
        "Product Manager": 1,
    },
}


def update_positions_to_cut():
    with app.app_context():
        total_before = 0
        total_after = 0
        total_cuts = 0
        
        print("\n🪓 UPDATING POSITIONS TO CUT 🪓\n")
        print("=" * 70)
        print(f"{'Department':<25} {'Position':<30} {'Before':>6} {'After':>6} {'Cut':>5}")
        print("=" * 70)
        
        departments = Department.query.all()
        
        for dept in departments:
            dept_name = dept.name
            after_data = AFTER_CUT_DATA.get(dept_name, {})
            
            for position in dept.positions:
                before = position.total_employees
                after = after_data.get(position.title, 0)  # Default to 0 if not in after list
                cuts = before - after
                
                if cuts < 0:
                    print(f"⚠️  WARNING: {dept_name} - {position.title}: after ({after}) > before ({before})")
                    cuts = 0
                
                position.positions_to_cut = cuts
                total_before += before
                total_after += after
                total_cuts += cuts
                
                if cuts > 0:
                    print(f"{dept_name:<25} {position.title:<30} {before:>6} {after:>6} {cuts:>5} 🔥")
                else:
                    print(f"{dept_name:<25} {position.title:<30} {before:>6} {after:>6} {cuts:>5}")
        
        db.session.commit()
        
        print("=" * 70)
        print(f"\n✅ Updated successfully!")
        print(f"   👥 Total before: {total_before}")
        print(f"   👥 Total after:  {total_after}")
        print(f"   🪓 Total cuts:   {total_cuts}")
        print(f"\n   Expected after from your data: 199")
        print(f"   Calculated cuts: {total_before} - {total_after} = {total_cuts}")


if __name__ == "__main__":
    update_positions_to_cut()

