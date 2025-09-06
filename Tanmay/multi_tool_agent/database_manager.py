"""
Database Manager for Site Analysis Backend
Handles PostgreSQL integration with Neon serverless database
Provides caching, analytics, and spatial data operations
"""

import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseManager:
    """
    Manages database operations for the Site Analysis Backend
    Features:
    - Smart caching with spatial queries
    - User interaction analytics
    - Serverless database auto-resume handling
    - SSL secure connections to Neon PostgreSQL
    """
    
    def __init__(self):
        # Load environment variables explicitly
        load_dotenv()
        
        self.connection_params = {
            'host': os.getenv('DB_HOST'),
            'port': int(os.getenv('DB_PORT', 5432)),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'sslmode': 'require'
        }
        
        # Debug environment variables
        print(f"🔍 Environment check:")
        print(f"   DB_HOST: {'✅ Set' if self.connection_params['host'] else '❌ Missing'}")
        print(f"   DB_NAME: {'✅ Set' if self.connection_params['database'] else '❌ Missing'}")
        print(f"   DB_USER: {'✅ Set' if self.connection_params['user'] else '❌ Missing'}")
        print(f"   DB_PASSWORD: {'✅ Set' if self.connection_params['password'] else '❌ Missing'}")
        
        # Validate configuration
        missing_vars = []
        if not self.connection_params['host']:
            missing_vars.append('DB_HOST')
        if not self.connection_params['database']:
            missing_vars.append('DB_NAME')
        if not self.connection_params['user']:
            missing_vars.append('DB_USER')
        if not self.connection_params['password']:
            missing_vars.append('DB_PASSWORD')
            
        if missing_vars:
            raise ValueError(f"❌ Missing environment variables: {', '.join(missing_vars)}. Check your .env file.")
        
        print("🗄️ Database Manager initialized with Neon PostgreSQL")
        print(f"📡 Host: {self.connection_params['host']}")
    
    def get_connection(self):
        """
        Get a database connection with retry logic for serverless auto-resume
        Handles Neon's auto-pause/resume feature gracefully
        """
        for attempt in range(3):
            try:
                conn = psycopg2.connect(**self.connection_params)
                if attempt > 0:
                    print(f"✅ Database connection established (attempt {attempt + 1})")
                return conn
                
            except psycopg2.OperationalError as e:
                error_msg = str(e).lower()
                
                if attempt < 2 and any(phrase in error_msg for phrase in 
                                     ["server closed", "connection refused", "timeout"]):
                    # Database might be resuming from auto-pause
                    print(f"⏳ Database resuming from pause... (attempt {attempt + 1}/3)")
                    import time
                    time.sleep(1.0)  # Wait longer for serverless resume
                    continue
                else:
                    print(f"❌ Database connection failed: {e}")
                    raise e
            except Exception as e:
                print(f"❌ Unexpected database error: {e}")
                raise e
    
    def test_connection(self) -> bool:
        """Test database connection and return PostgreSQL version info"""
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';")
                table_count = cursor.fetchone()[0]
                
            conn.close()
            
            print(f"✅ Database connection successful!")
            print(f"📄 PostgreSQL version: {version[:50]}...")
            print(f"📊 Tables in database: {table_count}")
            return True
            
        except Exception as e:
            print(f"❌ Database connection test failed: {e}")
            return False
    
    def cache_api_response(self, api_name: str, lat: float, lng: float, response_data: dict) -> bool:
        """
        Cache API response with spatial indexing for future retrieval
        
        Args:
            api_name: Name of the API (e.g., 'bhuvan_pois', 'routing')
            lat: Latitude coordinate
            lng: Longitude coordinate  
            response_data: API response data to cache
        """
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO api_responses (api_name, latitude, longitude, response_data)
                    VALUES (%s, %s, %s, %s)
                """, (api_name, lat, lng, json.dumps(response_data)))
            
            conn.commit()
            conn.close()
            print(f"✅ Cached {api_name} response for ({lat:.4f}, {lng:.4f})")
            return True
            
        except Exception as e:
            print(f"❌ Error caching API response: {e}")
            return False
    
    def get_cached_response(self, api_name: str, lat: float, lng: float, radius_km: float = 0.1) -> Optional[dict]:
        """
        Retrieve cached API response using spatial proximity search
        
        Args:
            api_name: Name of the API to search for
            lat: Latitude coordinate
            lng: Longitude coordinate
            radius_km: Search radius in kilometers (default 0.1km = 100m)
        
        Returns:
            Cached response data if found and not expired, None otherwise
        """
        try:
            conn = self.get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Use PostGIS spatial query to find nearby cached responses
                cursor.execute("""
                    SELECT response_data, created_at, latitude, longitude,
                           ST_Distance(
                               ST_Point(longitude, latitude)::geography,
                               ST_Point(%s, %s)::geography
                           ) as distance_meters
                    FROM api_responses 
                    WHERE api_name = %s 
                    AND ST_DWithin(
                        ST_Point(longitude, latitude)::geography,
                        ST_Point(%s, %s)::geography,
                        %s * 1000
                    )
                    AND expires_at > NOW()
                    ORDER BY created_at DESC
                    LIMIT 1
                """, (lng, lat, api_name, lng, lat, radius_km))
                
                result = cursor.fetchone()
                conn.close()
                
                if result:
                    distance = round(result['distance_meters'], 1)
                    cache_age = datetime.now() - result['created_at'].replace(tzinfo=None)
                    age_minutes = int(cache_age.total_seconds() / 60)
                    
                    print(f"🎯 Found cached {api_name} response:")
                    print(f"   📍 Distance: {distance}m from query point")
                    print(f"   ⏰ Age: {age_minutes} minutes old")
                    
                    return result['response_data']
                
                return None
                
        except Exception as e:
            print(f"❌ Error retrieving cached response: {e}")
            return None
    
    def log_user_interaction(self, query: str, response: str, coordinates: dict = None, api_calls: int = 0) -> bool:
        """
        Log user interaction for analytics and behavior analysis
        
        Args:
            query: User's original query
            response: Agent's response summary
            coordinates: Dictionary with lat/lng if location-based
            api_calls: Number of API calls made for this interaction
        """
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO user_interactions (user_query, agent_response, coordinates, api_calls_made)
                    VALUES (%s, %s, %s, %s)
                """, (query, response[:1000], json.dumps(coordinates) if coordinates else None, api_calls))
            
            conn.commit()
            conn.close()
            print(f"📊 Logged interaction: {api_calls} API calls, {len(response)} chars response")
            return True
            
        except Exception as e:
            print(f"❌ Error logging user interaction: {e}")
            return False
    
    def log_analytics_event(self, event_type: str, event_data: dict, lat: float = None, lng: float = None) -> bool:
        """
        Log analytics event for system monitoring
        
        Args:
            event_type: Type of event (e.g., 'api_call', 'cache_hit', 'error')
            event_data: Event details as dictionary
            lat: Optional latitude for location-based events
            lng: Optional longitude for location-based events
        """
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO analytics (event_type, event_data, location_lat, location_lng)
                    VALUES (%s, %s, %s, %s)
                """, (event_type, json.dumps(event_data), lat, lng))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Error logging analytics: {e}")
            return False
    
    def get_analytics_summary(self, days: int = 7) -> dict:
        """
        Get comprehensive analytics summary for the last N days
        
        Args:
            days: Number of days to analyze (default 7)
        
        Returns:
            Dictionary with analytics metrics
        """
        try:
            conn = self.get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # User interaction analytics
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_interactions,
                        COUNT(DISTINCT DATE(created_at)) as active_days,
                        COALESCE(AVG(api_calls_made), 0) as avg_api_calls_per_interaction,
                        SUM(api_calls_made) as total_api_calls
                    FROM user_interactions 
                    WHERE created_at >= NOW() - INTERVAL '%s days'
                """, (days,))
                
                interaction_stats = cursor.fetchone()
                
                # API response cache analytics
                cursor.execute("""
                    SELECT 
                        COUNT(*) as cached_responses,
                        COUNT(DISTINCT api_name) as unique_apis_cached,
                        api_name,
                        COUNT(*) as count
                    FROM api_responses 
                    WHERE created_at >= NOW() - INTERVAL '%s days'
                    GROUP BY api_name
                    ORDER BY count DESC
                """, (days,))
                
                cache_stats = cursor.fetchall()
                
                # System events analytics
                cursor.execute("""
                    SELECT 
                        event_type,
                        COUNT(*) as event_count
                    FROM analytics 
                    WHERE created_at >= NOW() - INTERVAL '%s days'
                    GROUP BY event_type
                    ORDER BY event_count DESC
                """, (days,))
                
                event_stats = cursor.fetchall()
                
            conn.close()
            
            # Calculate cache hit rate estimate
            total_api_calls = interaction_stats.get('total_api_calls', 0) or 0
            cached_responses = sum(stat['count'] for stat in cache_stats) if cache_stats else 0
            
            cache_hit_rate = 0
            if total_api_calls > 0:
                cache_hit_rate = min((cached_responses / total_api_calls) * 100, 100)
            
            analytics_summary = {
                "period_days": days,
                "user_interactions": dict(interaction_stats) if interaction_stats else {},
                "cache_performance": {
                    "total_cached_responses": cached_responses,
                    "estimated_cache_hit_rate_percent": round(cache_hit_rate, 1),
                    "apis_by_usage": [dict(stat) for stat in cache_stats] if cache_stats else []
                },
                "system_events": [dict(stat) for stat in event_stats] if event_stats else [],
                "performance_insights": self._generate_insights(interaction_stats, cache_stats, cache_hit_rate)
            }
            
            return analytics_summary
            
        except Exception as e:
            print(f"❌ Error getting analytics summary: {e}")
            return {"error": str(e)}
    
    def _generate_insights(self, interaction_stats, cache_stats, cache_hit_rate) -> list:
        """Generate performance insights from analytics data"""
        insights = []
        
        if interaction_stats:
            avg_api_calls = interaction_stats.get('avg_api_calls_per_interaction', 0) or 0
            
            if avg_api_calls < 1:
                insights.append("✅ Excellent API efficiency - most queries use cached data")
            elif avg_api_calls < 2:
                insights.append("👍 Good API efficiency - balanced cache usage")
            else:
                insights.append("⚠️ High API usage - consider expanding cache coverage")
        
        if cache_hit_rate > 50:
            insights.append(f"🎯 Strong cache performance - {cache_hit_rate:.1f}% estimated hit rate")
        elif cache_hit_rate > 20:
            insights.append(f"📈 Moderate cache usage - {cache_hit_rate:.1f}% hit rate, room for improvement")
        else:
            insights.append("📊 Low cache utilization - consider longer cache TTL")
        
        if cache_stats and len(cache_stats) > 3:
            insights.append(f"🔄 Diverse API usage - {len(cache_stats)} different APIs being cached")
        
        return insights
    
    def cleanup_expired_cache(self) -> int:
        """Remove expired cache entries and return count of removed items"""
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM api_responses WHERE expires_at <= NOW()")
                deleted_count = cursor.rowcount
            
            conn.commit()
            conn.close()
            
            if deleted_count > 0:
                print(f"🧹 Cleaned up {deleted_count} expired cache entries")
            
            return deleted_count
            
        except Exception as e:
            print(f"❌ Error cleaning up cache: {e}")
            return 0
    
    def get_recent_activity(self, limit: int = 10) -> dict:
        """Get recent system activity for monitoring"""
        try:
            conn = self.get_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        user_query,
                        coordinates,
                        api_calls_made,
                        created_at
                    FROM user_interactions 
                    ORDER BY created_at DESC 
                    LIMIT %s
                """, (limit,))
                
                recent_interactions = cursor.fetchall()
                
                cursor.execute("""
                    SELECT 
                        api_name,
                        latitude,
                        longitude,
                        created_at
                    FROM api_responses 
                    ORDER BY created_at DESC 
                    LIMIT %s
                """, (limit,))
                
                recent_api_calls = cursor.fetchall()
                
            conn.close()
            
            return {
                "recent_interactions": [dict(row) for row in recent_interactions],
                "recent_api_calls": [dict(row) for row in recent_api_calls]
            }
            
        except Exception as e:
            print(f"❌ Error getting recent activity: {e}")
            return {"error": str(e)}

if __name__ == "__main__":
    # Quick test when run directly
    print("🧪 Testing Database Manager...")
    try:
        db = DatabaseManager()
        if db.test_connection():
            print("✅ Database Manager is working correctly!")
        else:
            print("❌ Database Manager test failed!")
    except Exception as e:
        print(f"❌ Database Manager initialization failed: {e}")
