import os
from crewai.tools import tool
from supabase import create_client, Client

# These will be loaded from your main file or .env
url = os.environ.get("https://wlayjqoaofcwkzavctfh.supabase.co")
key = os.environ.get("sb_publishable_lQx5zbupUfHw6zBqhFMZFQ_JzQheqTe")

@tool("DatabaseWriter")
def save_to_cloud(headline: str, content: str):
    """
    Saves a completed geopolitical intelligence report to the cloud database.
    Inputs:
        headline: The topic of the inquiry.
        content: The full synthesized report/manifest.
    """
    try:
        supabase: Client = create_client(url, key)
        data = {
            "headline": headline,
            "report_content": content,
            "created_at": "now()" # Supabase handles the timestamp
        }
        # Ensure your table name is 'intelligence_reports'
        supabase.table("intelligence_reports").insert(data).execute()
        return "✅ Success: The Intelligence Manifest has been archived in the cloud."
    except Exception as e:
        return f"❌ Database Error: {str(e)}"