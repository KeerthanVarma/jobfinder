import requests
import os

# ---------------------- CONFIG ----------------------
API_KEY = os.getenv("GOOGLE_API_KEY")  # Your Google API Key
SEARCH_ENGINE_ID = os.getenv("GOOGLE_CSE_ID")  # Your Custom Search Engine ID

# ---------------------- FUNCTION ----------------------
def fetch_jobs_google(query: str, site: str = "", max_results: int = 10) -> list[dict]:
    """
    Fetch job postings using Google Custom Search API for a specific site.
    
    Args:
        query (str): Job role/company/location keywords.
        site (str): Restrict search to a specific site (e.g., 'linkedin.com/jobs').
        max_results (int): Number of results to fetch.
    
    Returns:
        list[dict]: List of job postings with standardized keys.
    """
    jobs = []
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": f"{query} site:{site}" if site else query,
        "num": min(max_results, 10)  # Google API max 10 per request
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        for item in data.get("items", []):
            jobs.append({
                "role": query,
                "company": "",  # Google API doesn't provide company directly
                "location": "",  # Can parse from snippet if needed
                "link": item.get("link", ""),
                "source": site or "Google Search",
                "description": item.get("snippet", ""),
                "stipend": ""
            })
    except Exception as e:
        print(f"Error fetching jobs from Google API for site {site}: {e}")

    return jobs

# ---------------------- SITE-SPECIFIC WRAPPERS ----------------------
def fetch_linkedin_jobs(role="", location="", max_jobs=10):
    query = f"{role} {location}".strip()
    return fetch_jobs_google(query=query, site="linkedin.com/jobs", max_results=max_jobs)

def fetch_naukri_jobs(role="", location="", max_jobs=10):
    query = f"{role} {location}".strip()
    return fetch_jobs_google(query=query, site="naukri.com", max_results=max_jobs)

def fetch_unstop_jobs(role="", location="", max_jobs=10):
    query = f"{role} {location}".strip()
    return fetch_jobs_google(query=query, site="unstop.com/jobs", max_results=max_jobs)

# ---------------------- DEBUG ----------------------
if __name__ == "__main__":
    sample = fetch_linkedin_jobs("Software Engineer", "Bangalore", max_jobs=5)
    for j in sample:
        print(j)
