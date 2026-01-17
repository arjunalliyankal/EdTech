
import asyncio
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.dirname(__file__))

from app.core.database import db, connect_to_mongo

async def check_courses():
    await connect_to_mongo()
    
    print("\n--- Checking Users ---")
    # For mock DB or actual Motor client, we need to inspect the object type carefully
    # But usually db.client is the client.
    
    try:
        # Check if we are using the Mock or Real DB
        client = db.client
        print(f"DB Client Type: {type(client)}")
        
        users_cursor = client.edtech_platform.users.find()
        users = []
        async for u in users_cursor:
            users.append(u)
            
        for u in users:
            print(f"User: {u.get('email')} | ID: {u.get('_id')} ({type(u.get('_id'))})")
            
            # Check courses for this user
            uid_str = str(u.get('_id'))
            print(f"  Checking courses for instructor_id: {uid_str}")
            
            courses_cursor = client.edtech_platform.courses.find({"instructor_id": uid_str})
            courses = []
            async for c in courses_cursor:
                courses.append(c)
                
            print(f"  Found {len(courses)} courses.")
            for c in courses:
                print(f"    - {c.get('title')} (Source: {c.get('source_file')})")
                
        print("\n--- Testing ObjectId Consistency ---")
        # Check if any courses exist at all
        all_courses_cursor = client.edtech_platform.courses.find()
        all_courses = []
        async for c in all_courses_cursor:
            all_courses.append(c)
            
        print(f"Total courses in DB: {len(all_courses)}")
        if len(all_courses) > 0:
            sample = all_courses[0]
            print(f"Sample Course Instructor ID: {sample.get('instructor_id')} (Type: {type(sample.get('instructor_id'))})")

    except Exception as e:
        print(f"Error inspecting DB: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(check_courses())
