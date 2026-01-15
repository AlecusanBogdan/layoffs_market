#!/usr/bin/env python3
"""
Script to import team members as candidates with odds based on their evaluations.
Connects to Vercel's Neon Postgres database.

Usage:
  DATABASE_URL="your-neon-connection-string" python import_candidates.py

Or set DATABASE_URL in a .env file
"""

import re
import os

# Team members data (extracted from team_members.sql - only active members)
TEAM_MEMBERS = {
    # id: (name, teamId)
    '1d7b77af-7892-4f14-b158-dc77c0d5846a': ('Bogdan Mazilu', '8d51d4a9-e868-4027-be00-206228b0c06b'),
    '725d3a90-96dc-4b5a-a0f4-d54cc8ec1140': ('Dan Virgiliu Neacsu', '8d51d4a9-e868-4027-be00-206228b0c06b'),
    '0248422f-574a-4284-8458-f31234ee9029': ('Ionut Frunza', '8d51d4a9-e868-4027-be00-206228b0c06b'),
    '158d7c07-52cb-422e-9f78-3587fb1a00b8': ('Mihai Lupea', '8d51d4a9-e868-4027-be00-206228b0c06b'),
    'bb4820a8-5a6b-4a95-8173-d13ade2747c9': ('Robert Buica', '8d51d4a9-e868-4027-be00-206228b0c06b'),
    'f8ea898a-1738-4242-a37c-5d3b5a4a5f15': ('Daniel Grosu', '8d51d4a9-e868-4027-be00-206228b0c06b'),
    'b3a017ee-b22d-4cfc-bc78-33008737fe90': ('Marius Borza', '8d51d4a9-e868-4027-be00-206228b0c06b'),
    '13f319fc-6e22-4dbe-b437-22b4bddf2d61': ('Alexandru-Mihai Savu', '8d51d4a9-e868-4027-be00-206228b0c06b'),
    '3e641c6d-b195-42e6-bf68-a55321278efd': ('Maksym Kobzar', '8d51d4a9-e868-4027-be00-206228b0c06b'),
    '57022cb8-5ea9-4b4f-9826-8f1b052b51f3': ('Daniel Matac', '8d51d4a9-e868-4027-be00-206228b0c06b'),
    'c61c3786-d924-4778-8eff-722f3981b3b2': ('Bogdan Domide', '8d51d4a9-e868-4027-be00-206228b0c06b'),
    '8294e448-c19e-4707-9af1-44b0b4f3c390': ('Eduard-Gabriel Cristea', '8d51d4a9-e868-4027-be00-206228b0c06b'),
    'd9a1980f-42e4-46e5-b1c5-5a727f7dbfdc': ('Alexandru Neculai', 'f7f23663-2e05-4ce6-919e-f96e09c0aa7b'),
    '119c88aa-19c4-4cfd-8da2-482fc7a6eb4c': ('Stefan Ionescu', 'f7f23663-2e05-4ce6-919e-f96e09c0aa7b'),
    '8293cbde-628e-4f07-9991-7dd1d2e43678': ('Razvan Balasa', 'f7f23663-2e05-4ce6-919e-f96e09c0aa7b'),
    '2e9d94ea-8e69-4c8b-93ea-ec6afbca9c7a': ('Adrian Lazar', 'f7f23663-2e05-4ce6-919e-f96e09c0aa7b'),
    'ceeb62a7-7efc-43f1-b307-bcc32f6877e6': ('Sergiu Grigoras', 'e8945f0d-ac4c-4006-b454-09d01bf63ec9'),
    'fbb7ac7f-a981-4964-b7f3-2dc7c6e1122a': ('Bogdan Ionas', 'e8945f0d-ac4c-4006-b454-09d01bf63ec9'),
    '13483218-b358-4426-b89e-3f50277f0303': ('Alexandra Gheorghe', 'e8945f0d-ac4c-4006-b454-09d01bf63ec9'),
    '2f80decf-847a-4426-adeb-a3e8b47d8759': ('Catalin Pruteanu', 'e8945f0d-ac4c-4006-b454-09d01bf63ec9'),
    'c17cc6c9-e2a2-4381-bf59-7b663817a82f': ('Octavian Cristea', 'e8945f0d-ac4c-4006-b454-09d01bf63ec9'),
    'd377617f-c77a-4d3f-84d5-00f83ce529b7': ('Dan Ion', 'e8945f0d-ac4c-4006-b454-09d01bf63ec9'),
    'ffd0af7f-a430-4b94-bdbb-178ea250b676': ('Cristian Paraschivescu', 'e8945f0d-ac4c-4006-b454-09d01bf63ec9'),
    '5e99381e-111b-40e1-b68a-083cfd81ef15': ('Vladimir Zapciu', 'e8945f0d-ac4c-4006-b454-09d01bf63ec9'),
    'd6a971bf-d591-4bbe-8c4d-fb54e4620334': ('Andrei Matacă', 'e50e0079-83f2-4bf3-8279-3d16da6f353f'),
    'a5dd05d8-e4c5-4fb7-a0b4-484e9d8028f7': ('Catalin Dancescu', 'e50e0079-83f2-4bf3-8279-3d16da6f353f'),
    '6f9983a1-d9c3-4141-bf2a-07872520867e': ('Adrian Brotea', 'e50e0079-83f2-4bf3-8279-3d16da6f353f'),
    '3e5d188a-6f35-44b5-9108-bcc39ea32ead': ('Adrian Burcea', 'e50e0079-83f2-4bf3-8279-3d16da6f353f'),
    '7277e5d1-66d4-4783-8269-4c092bdabed0': ('Daniel Costea', 'e50e0079-83f2-4bf3-8279-3d16da6f353f'),
    'b3b0edd3-8bd7-4fe8-ba3d-019261eb3336': ('Cosmin Tanjeala', 'f7f23663-2e05-4ce6-919e-f96e09c0aa7b'),
    '7c5635bf-72a2-4050-bccd-a9a5d55672d7': ('Stanislav B', 'f7f23663-2e05-4ce6-919e-f96e09c0aa7b'),
}

# Evaluation scores (extracted from people_evaluations.sql)
# memberId -> list of scores (we'll average them)
EVALUATIONS = {
    'b3a017ee-b22d-4cfc-bc78-33008737fe90': [10, 10],  # Marius Borza - excellent
    '158d7c07-52cb-422e-9f78-3587fb1a00b8': [4],       # Mihai Lupea - needs improvement
    'bb4820a8-5a6b-4a95-8173-d13ade2747c9': [10, 10, 10],  # Robert Buica - excellent
    'c17cc6c9-e2a2-4381-bf59-7b663817a82f': [0, 0],    # Octavian Cristea - low score
    'c61c3786-d924-4778-8eff-722f3981b3b2': [7.5],     # Bogdan Domide - good
    '8294e448-c19e-4707-9af1-44b0b4f3c390': [0],       # Eduard-Gabriel Cristea - low
    'd9a1980f-42e4-46e5-b1c5-5a727f7dbfdc': [0],       # Alexandru Neculai - low
    '8293cbde-628e-4f07-9991-7dd1d2e43678': [5],       # Razvan Balasa - average
    '1d7b77af-7892-4f14-b158-dc77c0d5846a': [5],       # Bogdan Mazilu - average
}

def calculate_odds(score):
    """
    Calculate betting odds based on evaluation score.
    
    In betting: LOW odds = likely to happen (small payout)
                HIGH odds = unlikely to happen (big payout)
    
    Score 0 (bad) = odds 1.5 (likely to be fired - safe bet, small win)
    Score 10 (good) = odds 5.0 (unlikely to be fired - risky bet, big win)
    No evaluation = odds 3.0 (unknown - medium)
    """
    if score is None:
        return 3.0
    # Linear interpolation: score 0->1.5, score 10->5.0
    odds = 1.5 + (score / 10.0) * 3.5
    return round(odds, 2)

def get_average_score(member_id):
    """Get average evaluation score for a member"""
    if member_id not in EVALUATIONS:
        return None
    scores = EVALUATIONS[member_id]
    return sum(scores) / len(scores)

def main():
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("ERROR: DATABASE_URL environment variable not set!")
        print("\nTo get your DATABASE_URL:")
        print("1. Go to Vercel Dashboard -> layoffs-market -> Storage")
        print("2. Click on your Neon database")
        print("3. Copy the connection string")
        print("\nThen run:")
        print('DATABASE_URL="postgresql://..." python import_candidates.py')
        return
    
    # Fix postgres:// -> postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    print("Connecting to database...")
    
    try:
        import psycopg2
    except ImportError:
        print("Installing psycopg2-binary...")
        os.system('pip install psycopg2-binary')
        import psycopg2
    
    conn = psycopg2.connect(database_url)
    cur = conn.cursor()
    
    # Get the first C# Developer position (or any developer position)
    cur.execute("SELECT id, title FROM position WHERE title LIKE '%Developer%' LIMIT 1")
    position = cur.fetchone()
    
    if not position:
        # Get any position
        cur.execute("SELECT id, title FROM position LIMIT 1")
        position = cur.fetchone()
    
    if not position:
        print("ERROR: No positions found in database. Please seed the database first.")
        conn.close()
        return
    
    position_id, position_title = position
    print(f"Using position: {position_title} (ID: {position_id})")
    
    # Import candidates
    added = 0
    updated = 0
    
    for member_id, (name, team_id) in TEAM_MEMBERS.items():
        avg_score = get_average_score(member_id)
        odds = calculate_odds(avg_score)
        
        score_info = f"score={avg_score:.1f}" if avg_score is not None else "no evaluation"
        bio = f"Team member. Evaluation: {score_info}"
        
        # Check if candidate already exists
        cur.execute("SELECT id, odds FROM candidate WHERE name = %s", (name,))
        existing = cur.fetchone()
        
        if existing:
            # Update odds
            cur.execute(
                "UPDATE candidate SET odds = %s, bio = %s WHERE id = %s",
                (odds, bio, existing[0])
            )
            print(f"  Updated: {name} - odds {existing[1]} -> {odds}")
            updated += 1
        else:
            # Insert new candidate
            cur.execute(
                "INSERT INTO candidate (name, photo, odds, bio, is_laid_off, position_id) VALUES (%s, %s, %s, %s, %s, %s)",
                (name, 'default.png', odds, bio, False, position_id)
            )
            print(f"  Added: {name} - odds {odds} ({score_info})")
            added += 1
    
    conn.commit()
    cur.close()
    conn.close()
    
    print(f"\n✅ Done! Added {added} candidates, updated {updated} candidates.")
    print(f"🎰 Odds range: 1.5 (safe) to 5.0 (high risk)")

if __name__ == '__main__':
    main()

