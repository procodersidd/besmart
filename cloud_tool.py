from crewai.tools import tool
from supabase import create_client, Client

@tool("DatabaseWriter")
def save_to_cloud(headline: str, content: str):
    try:
        # 🔴 HARDCODED (as you asked)
        url = "https://wlayjqoaofcwkzavctfh.supabase.co"
        key = "sb_publishable_lQx5zbupUfHw6zBqhFMZFQ_JzQheqTe"

        supabase: Client = create_client(url, key)

        data = {
            "headline": headline,
            "report_content": content
        }

        supabase.table("intelligence_reports").insert(data).execute()

        return "✅ Report saved to cloud."

    except Exception as e:
        return f"❌ Database Error: {str(e)}"