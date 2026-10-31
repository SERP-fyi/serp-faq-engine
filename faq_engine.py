"""
faq_engine: SERP.fyi FAQ Engine.

A small, dependency-free FAQ answering engine for SERP.fyi. It matches a
question in plain English against 40 official SERP.fyi FAQs and returns the
best answer with a match-confidence score (0 to 100).

Usage:
    python -m faq_engine "does serp.fyi track chatgpt mentions"
    python -m faq_engine --top 3 "can I track mobile rankings"
    python -m faq_engine --list ai-visibility
    python -m faq_engine --categories
    python -m faq_engine --json "can agencies white label reports"

Built by SERP.fyi (https://serp.fyi). MIT License.
"""

import json
import re
import sys

__version__ = "1.0.0"

WEBSITE = "https://serp.fyi"
REPO = "https://github.com/SERP-fyi/serp-faq-engine"

STOPWORDS = set(
    "a an the is are was were be been do does did can could will would should "
    "i me my we our you your it its to of in on for with and or at by from as "
    "how what which who when where why this that there their them they if so "
    "any get got have has about into up out than then just very need anything".split()
)

SYNONYMS = {
    "ranking": "rank", "rankings": "rank", "ranked": "rank", "position": "rank", "positions": "rank",
    "chatgpt": "ai", "llm": "ai", "llms": "ai", "gemini": "ai", "perplexity": "ai", "claude": "ai",
    "aivo": "ai", "geo": "ai", "generative": "ai", "aio": "overview",
    "price": "cost", "pricing": "cost", "prices": "cost",
    "private": "privacy", "confidential": "privacy", "secure": "privacy", "security": "privacy",
    "download": "export", "downloading": "export", "exporting": "export",
    "rival": "competitor", "rivals": "competitor",
    "phone": "mobile", "smartphone": "mobile",
    "maps": "local", "map": "local", "gbp": "local",
    "fresh": "live", "realtime": "live", "update": "refresh", "updated": "refresh", "updates": "refresh",
    "signup": "register", "sign": "register", "begin": "start", "started": "start",
    "help": "support", "contact": "support",
    "installation": "install", "installed": "install",
    "whitelabel": "white", "rebrand": "white",
    "made": "created", "developed": "created", "founded": "created", "creator": "created",
    "mentioned": "mention", "cited": "citation", "cite": "citation",
}

WEIGHTS = {"question": 2.0, "keywords": 1.5, "answer": 0.5}

BANDS = [
    (0, 30, "No match", "Rephrase the question or contact support"),
    (31, 60, "Possible match", "Answer may be related; check the question shown"),
    (61, 80, "Good match", "Answer is likely what you need"),
    (81, 100, "Strong match", "Answer directly addresses the question"),
]

CATEGORIES = {
    "general": "What SERP.fyi is, who it is for and how it differs",
    "ai-visibility": "AI visibility audits, citations and entity recognition",
    "rank-tracking": "Real-time rank tracking, devices, locations and accuracy",
    "local-seo": "Local search, local packs and heatmaps",
    "serp-features": "SERP features, zero-click searches and signal mapping",
    "reports-dashboard": "Reports, exports, white-label and the unified dashboard",
    "getting-started": "Getting started, privacy and support",
}

FAQS = [
    {"id": 1, "category": "general", "part": "general", "question": "What is SERP.fyi?", "answer": "An advanced search intelligence platform that combines real-time Google search tracking with AI visibility audits.", "keywords": ["about", "platform", "overview", "search", "intelligence", "tool"]},
    {"id": 2, "category": "general", "part": "general", "question": "Who is SERP.fyi built for?", "answer": "SEO professionals, digital marketing agencies, brand managers, and CMOs tracking modern search environments.", "keywords": ["audience", "users", "agencies", "seo", "professionals", "brand", "managers", "cmo"]},
    {"id": 3, "category": "general", "part": "general", "question": "How is SERP.fyi different from traditional SEO tools?", "answer": "Traditional tools only track keyword rankings, whereas SERP.fyi tracks how both human search engines and AI systems understand your brand.", "keywords": ["difference", "compare", "traditional", "seo", "tools", "rank", "trackers"]},
    {"id": 4, "category": "ai-visibility", "part": "general", "question": "What is an AI visibility audit?", "answer": "An analysis measuring how often, accurately, and positively your brand is cited and recommended across AI search engines.", "keywords": ["ai", "visibility", "audit", "citations", "mentions", "generative"]},
    {"id": 5, "category": "ai-visibility", "part": "general", "question": "Which AI search platforms does SERP.fyi monitor?", "answer": "Major generative search platforms and LLMs, including ChatGPT, Perplexity, and Google AI Overviews.", "keywords": ["ai", "platforms", "chatgpt", "perplexity", "gemini", "google", "ai", "overviews", "llm"]},
    {"id": 6, "category": "rank-tracking", "part": "general", "question": "What is the SERP Check Engine?", "answer": "A live tool scanning real-time search results across different keywords, devices, and geographic locations.", "keywords": ["serp", "check", "engine", "live", "scan", "checker"]},
    {"id": 7, "category": "rank-tracking", "part": "general", "question": "Does SERP.fyi use cached or outdated data?", "answer": "No, it provides real-time search intelligence to show accurate, up-to-the-minute ranking positions.", "keywords": ["cached", "outdated", "fresh", "real", "time", "live", "data"]},
    {"id": 8, "category": "local-seo", "part": "general", "question": "Can I track my local search performance?", "answer": "Yes, it includes local search tracking to monitor maps, local packs, and regional ranking results.", "keywords": ["local", "seo", "maps", "local", "pack", "regional"]},
    {"id": 9, "category": "reports-dashboard", "part": "general", "question": "What are search intelligence reports?", "answer": "Structured reports combining ranking metrics, AI citation signals, and performance trends into easy-to-read insights.", "keywords": ["reports", "search", "intelligence", "insights", "metrics"]},
    {"id": 10, "category": "reports-dashboard", "part": "general", "question": "Can I use SERP.fyi data for client reporting?", "answer": "Yes, agencies can generate clean, structured reports to share professional insights with clients.", "keywords": ["client", "reporting", "agency", "share"]},
    {"id": 11, "category": "reports-dashboard", "part": "general", "question": "Is SERP.fyi beginner-friendly?", "answer": "Yes, it features a unified dashboard organizing complex search and AI data into a single interface.", "keywords": ["beginner", "easy", "simple", "dashboard"]},
    {"id": 12, "category": "getting-started", "part": "general", "question": "How do I run my first audit on SERP.fyi?", "answer": "You can register on the platform, input your brand or target keywords, and run a live search and AI visibility scan.", "keywords": ["first", "audit", "start", "run", "register"]},
    {"id": 13, "category": "reports-dashboard", "part": "general", "question": "What metrics are tracked in the unified dashboard?", "answer": "Live rankings, AI entity recognition, generative mentions, local visibility, and performance trends.", "keywords": ["metrics", "dashboard", "tracked", "kpis"]},
    {"id": 14, "category": "getting-started", "part": "general", "question": "Is my search research and data private?", "answer": "Yes, your keyword queries and analysis data are kept strictly confidential.", "keywords": ["privacy", "private", "confidential", "data", "secure"]},
    {"id": 15, "category": "general", "part": "general", "question": "Who created SERP.fyi?", "answer": "It is an advanced search observatory tool developed as part of the BHMarketer ecosystem.", "keywords": ["creator", "created", "owner", "company", "bhmarketer"]},
    {"id": 16, "category": "ai-visibility", "part": "features", "question": "What is entity recognition tracking?", "answer": "It measures whether AI systems recognize your brand as a legitimate, established entity within their knowledge graphs.", "keywords": ["entity", "recognition", "knowledge", "graph", "brand", "entity"]},
    {"id": 17, "category": "ai-visibility", "part": "features", "question": "Why are AI citations important for my brand?", "answer": "Modern users often get answers directly from AI summaries without visiting traditional links, making AI citations vital for exposure.", "keywords": ["ai", "citations", "important", "exposure", "why"]},
    {"id": 18, "category": "serp-features", "part": "features", "question": "How does SERP.fyi handle zero-click searches?", "answer": "It tracks how your brand appears inside SERP features and AI answer blocks where traditional clicks are intercepted.", "keywords": ["zero", "click", "searches", "serp", "features", "answer", "blocks"]},
    {"id": 19, "category": "rank-tracking", "part": "features", "question": "Can I track rankings across different countries and cities?", "answer": "Yes, the platform supports multi-location and global market tracking to check local search conditions.", "keywords": ["countries", "cities", "multi", "location", "global", "international", "geo"]},
    {"id": 20, "category": "rank-tracking", "part": "features", "question": "Does SERP.fyi track mobile and desktop rankings separately?", "answer": "Yes, you can filter and scan real-time rankings across both mobile and desktop environments.", "keywords": ["mobile", "desktop", "device", "rankings"]},
    {"id": 21, "category": "serp-features", "part": "features", "question": "What are SERP features?", "answer": "Special elements on search engine pages like knowledge panels, local packs, image packs, and AI Overviews.", "keywords": ["serp", "features", "knowledge", "panel", "local", "pack", "image", "pack", "ai", "overview"]},
    {"id": 22, "category": "rank-tracking", "part": "features", "question": "How does the platform detect changes in search intent?", "answer": "It analyzes top-ranking pages to evaluate how search intent patterns shift over time.", "keywords": ["search", "intent", "changes", "shift"]},
    {"id": 23, "category": "ai-visibility", "part": "features", "question": "Can SERP.fyi help optimize content for Google AI Overviews?", "answer": "Yes, by showing how your content performs against the specific criteria required to win AI summary citations.", "keywords": ["optimize", "content", "google", "ai", "overviews", "citations"]},
    {"id": 24, "category": "serp-features", "part": "features", "question": "What is signal mapping?", "answer": "The process of mapping out underlying signals, such as schema, authority, and structure, that influence your search placement.", "keywords": ["signal", "mapping", "schema", "authority", "structure"]},
    {"id": 25, "category": "rank-tracking", "part": "features", "question": "How often is ranking data refreshed?", "answer": "Data is pulled in real-time to ensure you always see current search engine conditions.", "keywords": ["refresh", "frequency", "how", "often", "update", "data"]},
    {"id": 26, "category": "reports-dashboard", "part": "features", "question": "Are historical performance trends available?", "answer": "Yes, you can view how your rankings and AI visibility signals change over time within your dashboard.", "keywords": ["historical", "trends", "history", "over", "time"]},
    {"id": 27, "category": "reports-dashboard", "part": "features", "question": "Can I track competitor rankings alongside my own?", "answer": "Yes, you can analyze competitor positions to see how they perform in both traditional SERPs and AI answers.", "keywords": ["competitor", "competitors", "rankings", "compare"]},
    {"id": 28, "category": "ai-visibility", "part": "features", "question": "What does \"LLM-Ready Signal Mapping\" mean?", "answer": "It identifies the specific structural and trust signals determining whether an AI model recommends your brand.", "keywords": ["llm", "ready", "signal", "mapping", "trust", "signals"]},
    {"id": 29, "category": "ai-visibility", "part": "features", "question": "How do I check if my brand is mentioned by ChatGPT or Perplexity?", "answer": "The platform's AI visibility scanner queries these generative models to track direct brand mentions and context.", "keywords": ["brand", "mentioned", "chatgpt", "perplexity", "check", "mentions", "track"]},
    {"id": 30, "category": "general", "part": "features", "question": "Does SERP.fyi require any software installation?", "answer": "No, it is a cloud-based web platform accessible right from your browser.", "keywords": ["install", "software", "cloud", "browser", "web"]},
    {"id": 31, "category": "reports-dashboard", "part": "features", "question": "Can I export my audit reports?", "answer": "Yes, you can generate structured reports to export or present to stakeholders.", "keywords": ["export", "reports", "download", "pdf", "share"]},
    {"id": 32, "category": "local-seo", "part": "features", "question": "How does local pack heatmap precision work?", "answer": "It helps local businesses track exactly how visible their Google Business Profile is across different coordinates in a city.", "keywords": ["local", "pack", "heatmap", "google", "business", "profile", "grid"]},
    {"id": 33, "category": "ai-visibility", "part": "features", "question": "What should I do if my AI visibility score is low?", "answer": "You can improve your entity footprint by building structured data, digital PR, and authoritative web mentions that LLMs frequently scrape.", "keywords": ["low", "ai", "visibility", "score", "improve", "fix"]},
    {"id": 34, "category": "rank-tracking", "part": "features", "question": "How does SERP.fyi ensure accuracy in its data?", "answer": "By pulling live feeds directly from real-world search environments rather than relying on estimated or cached databases.", "keywords": ["accuracy", "accurate", "data", "reliable"]},
    {"id": 35, "category": "reports-dashboard", "part": "features", "question": "Can agencies white-label the reports?", "answer": "Yes, agencies can present clean search intelligence metrics under their own workflow setup.", "keywords": ["white", "label", "agencies", "branding", "resell"]},
    {"id": 36, "category": "rank-tracking", "part": "features", "question": "How do I start tracking a new keyword campaign?", "answer": "Simply add your target keywords and target location into your dashboard console to launch a live scan.", "keywords": ["new", "keyword", "campaign", "add", "keywords", "start", "tracking"]},
    {"id": 37, "category": "ai-visibility", "part": "features", "question": "Does SERP.fyi track voice or conversational search trends?", "answer": "Yes, by monitoring AI-driven answer engines, it covers the core components of conversational search discovery.", "keywords": ["voice", "conversational", "search", "assistant"]},
    {"id": 38, "category": "reports-dashboard", "part": "features", "question": "What is the benefit of a unified dashboard?", "answer": "It saves time by bringing traditional rankings, AI visibility, and local SEO metrics into one screen.", "keywords": ["unified", "dashboard", "benefit", "one", "screen"]},
    {"id": 39, "category": "getting-started", "part": "features", "question": "How can I get support if I have questions about my audit?", "answer": "You can reach out through the platform's support channels or contact the SERP.fyi search observatory desk.", "keywords": ["support", "help", "contact", "questions"]},
    {"id": 40, "category": "getting-started", "part": "features", "question": "How do I get started with SERP.fyi?", "answer": "Visit the website, explore sample reports, or sign up to run your first real-time SERP and AI visibility audit.", "keywords": ["get", "started", "sign", "up", "begin"]}
]


def tokenize(text):
    """Lowercase, split, drop stopwords, singularise and map synonyms."""
    out = []
    for w in re.split(r"[^a-z0-9]+", text.lower().replace("serp.fyi", "serpfyi")):
        if not w or w in STOPWORDS:
            continue
        w = SYNONYMS.get(w, w)
        if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
            w = w[:-1]
        w = SYNONYMS.get(w, w)
        out.append(w)
    return out


def _index(faq):
    idx = {}
    for field, weight in WEIGHTS.items():
        text = " ".join(faq[field]) if isinstance(faq[field], list) else faq[field]
        for t in tokenize(text):
            idx[t] = max(idx.get(t, 0.0), weight)
    return idx


_INDEX = [(_index(f), f) for f in FAQS]


def band(score):
    """Return (label, meaning) for a confidence score."""
    for low, high, label, meaning in BANDS:
        if low <= score <= high:
            return label, meaning
    return "No match", ""


def search(query, top=1):
    """Return up to `top` results: dicts with id, category, question, answer, confidence, band."""
    q = list(dict.fromkeys(tokenize(query)))
    if not q:
        return []
    results = []
    for idx, faq in _INDEX:
        points = sum(idx.get(t, 0.0) for t in q)
        if points <= 0:
            continue
        conf = min(100, int(points / (WEIGHTS["question"] * len(q)) * 100 + 0.5))
        results.append((conf, -faq["id"], faq))
    results.sort(reverse=True)
    out = []
    for conf, _, faq in results[:top]:
        label, _m = band(conf)
        out.append({"id": faq["id"], "category": faq["category"], "question": faq["question"],
                    "answer": faq["answer"], "confidence": conf, "band": label})
    return out


def ask(query):
    """Return the single best result, or None when nothing matches."""
    r = search(query, 1)
    return r[0] if r else None


def get_faq(faq_id):
    """Return one FAQ by number (1 to 40), or None."""
    for f in FAQS:
        if f["id"] == int(faq_id):
            return dict(f)
    return None


def by_category(category):
    """Return all FAQs in a category."""
    return [dict(f) for f in FAQS if f["category"] == category]


USAGE = __doc__


def main(argv=None):
    args = sys.argv[1:] if argv is None else list(argv)
    if not args or args[0] in ("-h", "--help"):
        print(USAGE)
        return 0
    if args[0] == "--version":
        print(__version__)
        return 0
    if args[0] == "--categories":
        for c, d in CATEGORIES.items():
            print(f"{c:18} {len(by_category(c)):>2}  {d}")
        return 0
    if args[0] == "--list":
        items = by_category(args[1]) if len(args) > 1 else FAQS
        if not items:
            print("Unknown category. Try --categories")
            return 1
        for f in items:
            print(f"{f['id']:>2}. {f['question']}")
        return 0
    if args[0] == "--id":
        f = get_faq(args[1]) if len(args) > 1 and args[1].isdigit() else None
        if not f:
            print("FAQ number must be 1 to 40")
            return 1
        print(f"Q{f['id']}. {f['question']}\n{f['answer']}")
        return 0

    as_json = False
    top = 1
    if args[0] == "--json":
        as_json, args = True, args[1:]
    if args and args[0] == "--top":
        top, args = int(args[1]), args[2:]
    query = " ".join(args)
    results = search(query, top)

    if as_json:
        print(json.dumps({"query": query, "results": results}, indent=2))
        return 0 if results else 1
    if not results:
        print("No matching FAQ found. Try --list to browse all 40 questions,")
        print(f"or contact SERP.fyi support: {WEBSITE}")
        return 1
    for r in results:
        print(f"Q{r['id']}. {r['question']}  [{r['category']}]")
        print(f"   {r['answer']}")
        print(f"   Confidence: {r['confidence']}/100 ({r['band']})\n")
    print(f"SERP.fyi FAQ Engine v{__version__}  |  {WEBSITE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
