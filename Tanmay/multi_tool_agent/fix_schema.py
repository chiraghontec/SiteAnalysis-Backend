"""
Fix database schema by adding missing columns
"""

from database_manager import DatabaseManager

def fix_database_schema():
    print("🔧 Fixing database schema...")
    
    try:
        db = DatabaseManager()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Add missing expires_at column to api_responses
        print("1. Adding expires_at column to api_responses...")
        cursor.execute("""
            ALTER TABLE api_responses 
            ADD COLUMN IF NOT EXISTS expires_at TIMESTAMP WITH TIME ZONE 
            DEFAULT (NOW() + INTERVAL '24 hours')
        """)
        
        # Add missing api_calls_made column to user_interactions
        print("2. Adding api_calls_made column to user_interactions...")
        cursor.execute("""
            ALTER TABLE user_interactions 
            ADD COLUMN IF NOT EXISTS api_calls_made INTEGER DEFAULT 0
        """)
        
        # Update existing rows to have expires_at values
        print("3. Updating existing api_responses with expires_at...")
        cursor.execute("""
            UPDATE api_responses 
            SET expires_at = created_at + INTERVAL '24 hours' 
            WHERE expires_at IS NULL
        """)
        
        # Update existing rows to have api_calls_made values
        print("4. Updating existing user_interactions with api_calls_made...")
        cursor.execute("""
            UPDATE user_interactions 
            SET api_calls_made = 1 
            WHERE api_calls_made IS NULL
        """)
        
        conn.commit()
        conn.close()
        
        print("✅ Database schema successfully updated!")
        print("   📅 expires_at column added to api_responses")
        print("   🔢 api_calls_made column added to user_interactions")
        print("   📝 Existing data updated with default values")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing database schema: {e}")
        return False

if __name__ == "__main__":
    fix_database_schema()
