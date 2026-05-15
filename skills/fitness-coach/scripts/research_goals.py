#!/usr/bin/env python3
"""Search PubMed for evidence-based protocol for user's fitness goals."""
import json
import sys
import urllib.request
import urllib.parse
from pathlib import Path

PUBMED_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

GOAL_QUERIES = {
    "recomposition": "body recomposition resistance training protein",
    "fat_loss": "fat loss resistance training caloric deficit preserve muscle",
    "muscle_gain": "hypertrophy resistance training volume frequency",
    "performance": "athletic performance strength training periodization",
    "general_health": "resistance training health outcomes older adults",
}


def search_pubmed(query, max_results=5):
    params = urllib.parse.urlencode(
        {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "sort": "relevance",
            "retmode": "json",
        }
    )
    url = f"{PUBMED_BASE}/esearch.fcgi?{params}"
    with urllib.request.urlopen(url, timeout=10) as r:
        data = json.loads(r.read())
    return data.get("esearchresult", {}).get("idlist", [])


def fetch_abstract(pmid):
    params = urllib.parse.urlencode(
        {"db": "pubmed", "id": pmid, "rettype": "abstract", "retmode": "text"}
    )
    url = f"{PUBMED_BASE}/efetch.fcgi?{params}"
    with urllib.request.urlopen(url, timeout=10) as r:
        return r.read().decode("utf-8", errors="replace")[:800]


def research(goal):
    query = GOAL_QUERIES.get(goal, f"exercise training {goal}")
    print(f"Searching PubMed for: {query}")

    pmids = search_pubmed(query)
    results = []
    for pmid in pmids[:3]:
        try:
            abstract = fetch_abstract(pmid)
            results.append({"pmid": pmid, "abstract": abstract[:400]})
            print(f"  PMID {pmid}: fetched")
        except Exception as e:
            print(f"  PMID {pmid}: error ({e})")

    out = Path.home() / "Projects/fitness-coach/research" / f"{goal}-research.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps({"goal": goal, "query": query, "studies": results}, indent=2)
    )
    print(f"Saved to {out}")
    return results


if __name__ == "__main__":
    goal = sys.argv[1] if len(sys.argv) > 1 else "recomposition"
    research(goal)
