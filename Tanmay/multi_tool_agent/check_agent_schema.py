"""""""""

Script to check the Agent table schema in the database

"""Script to check the Agent table schema in the databaseScript to check the Agent table schema in the database



import psycopg2""""""

import os

from dotenv import load_dotenv

from psycopg2.extras import RealDictCursor

import psycopg2import psycopg2

# Load environment variables

load_dotenv()import osimport os



def check_table_schema():from dotenv import load_dotenvfrom dotenv import load_dotenv

    """Check the schema of the agent table"""

    print("🔍 Checking agent table schema...")from psycopg2.extras import RealDictCursorfrom psycopg2.extras import RealDictCursor

    

    connection_params = {

        'host': os.getenv('DB_HOST'),

        'port': int(os.getenv('DB_PORT', 5432)),# Load environment variables# Load environment variables

        'database': os.getenv('DB_NAME'),

        'user': os.getenv('DB_USER'),load_dotenv()load_dotenv()

        'password': os.getenv('DB_PASSWORD'),

        'sslmode': 'require'

    }

    def check_table_schema():def check_table_schema():

    try:

        conn = psycopg2.connect(**connection_params)    """Check the schema of the agent table"""    """Check the schema of the agent table"""

        with conn.cursor(cursor_factory=RealDictCursor) as cursor:

            # Check if the table exists    print("🔍 Checking agent table schema...")    print("🔍 Checking agent table schema...")

            cursor.execute("""

                SELECT EXISTS (        

                    SELECT FROM information_schema.tables 

                    WHERE table_schema = 'public'     connection_params = {    connection_params = {

                    AND table_name = 'agent'

                );        'host': os.getenv('DB_HOST'),        'host': os.getenv('DB_HOST'),

            """)

                    'port': int(os.getenv('DB_PORT', 5432)),        'port': int(os.getenv('DB_PORT', 5432)),

            table_exists = cursor.fetchone()['exists']

                    'database': os.getenv('DB_NAME'),        'database': os.getenv('DB_NAME'),

            if not table_exists:

                print("❌ Agent table does not exist")        'user': os.getenv('DB_USER'),        'user': os.getenv('DB_USER'),

                return False

                    'password': os.getenv('DB_PASSWORD'),        'password': os.getenv('DB_PASSWORD'),

            # Get column information

            cursor.execute("""        'sslmode': 'require'        'sslmode': 'require'

                SELECT column_name, data_type, is_nullable

                FROM information_schema.columns    }    }

                WHERE table_schema = 'public' 

                AND table_name = 'agent'        

                ORDER BY ordinal_position;

            """)    try:    try:

            

            columns = cursor.fetchall()        conn = psycopg2.connect(**connection_params)        conn = psycopg2.connect(**connection_params)

            

            print("\n📋 Agent Table Schema:")        with conn.cursor(cursor_factory=RealDictCursor) as cursor:        with conn.cursor(cursor_factory=RealDictCursor) as cursor:

            print("-" * 50)

            print(f"{'COLUMN':<20} {'TYPE':<20} {'NULLABLE':<10}")            # Check if the table exists            # Check if the table exists

            print("-" * 50)

                        cursor.execute("""            cursor.execute("""

            for col in columns:

                print(f"{col['column_name']:<20} {col['data_type']:<20} {col['is_nullable']:<10}")                SELECT EXISTS (                SELECT EXISTS (

                

            # Check for data                    SELECT FROM information_schema.tables                     SELECT FROM information_schema.tables 

            cursor.execute("SELECT COUNT(*) as record_count FROM agent")

            count = cursor.fetchone()['record_count']                    WHERE table_schema = 'public'                     WHERE table_schema = 'public' 

            print(f"\n📊 Records in agent table: {count}")

                                AND table_name = 'agent'                    AND table_name = 'agent'

        conn.close()

        return True                );                );

        

    except Exception as e:            """)            """)

        print(f"❌ Error checking schema: {e}")

        return False                        



if __name__ == "__main__":            table_exists = cursor.fetchone()['exists']            table_exists = cursor.fetchone()['exists']

    check_table_schema()
                        

            if not table_exists:            if not table_exists:

                print("❌ Agent table does not exist")                print("❌ Agent table does not exist")

                print("\n📋 Creating Agent table...")                return

                            

                # Create the agent table            # Get column information

                cursor.execute("""            cursor.execute("""

                    CREATE TABLE IF NOT EXISTS agent (                SELECT column_name, data_type, is_nullable

                        id SERIAL PRIMARY KEY,                FROM information_schema.columns

                        session_id VARCHAR(100) NOT NULL,                WHERE table_schema = 'public' 

                        user_id VARCHAR(100),                AND table_name = 'agent'

                        user_queries JSONB,                ORDER BY ordinal_position;

                        coordinates JSONB,            """)

                        api_calls JSONB,            

                        api_count INTEGER DEFAULT 0,            columns = cursor.fetchall()

                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,            

                        response_length INTEGER DEFAULT 0            print("\n📋 Agent Table Schema:")

                    );            print("-" * 50)

                                print(f"{'COLUMN':<20} {'TYPE':<20} {'NULLABLE':<10}")

                    -- Create indexes            print("-" * 50)

                    CREATE INDEX IF NOT EXISTS idx_agent_session_id ON agent(session_id);            

                    CREATE INDEX IF NOT EXISTS idx_agent_user_id ON agent(user_id);            for col in columns:

                    CREATE INDEX IF NOT EXISTS idx_agent_created_at ON agent(created_at);                print(f"{col['column_name']:<20} {col['data_type']:<20} {col['is_nullable']:<10}")

                """)            

                        conn.close()

                conn.commit()        

                print("✅ Agent table created successfully")    except Exception as e:

                return        print(f"❌ Error checking schema: {e}")

            

            # Get column informationif __name__ == "__main__":

            cursor.execute("""    check_table_schema()
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_schema = 'public' 
                AND table_name = 'agent'
                ORDER BY ordinal_position;
            """)
            
            columns = cursor.fetchall()
            
            print("\n📋 Agent Table Schema:")
            print("-" * 50)
            print(f"{'COLUMN':<20} {'TYPE':<20} {'NULLABLE':<10}")
            print("-" * 50)
            
            for col in columns:
                print(f"{col['column_name']:<20} {col['data_type']:<20} {col['is_nullable']:<10}")
                
            # Check for data
            cursor.execute("SELECT COUNT(*) as record_count FROM agent")
            count = cursor.fetchone()['record_count']
            print(f"\n📊 Records in agent table: {count}")
            
        conn.close()
        
    except Exception as e:
        print(f"❌ Error checking schema: {e}")

if __name__ == "__main__":
    check_table_schema()