# SERP.fyi: FAQ Engine 🔎🤖

[![npm](https://img.shields.io/npm/v/@serp-fyi/serp-faq-engine?style=flat-square)](https://www.npmjs.com/package/@serp-fyi/serp-faq-engine)
[![PyPI](https://img.shields.io/pypi/v/serp-faq-engine?style=flat-square)](https://pypi.org/project/serp-faq-engine/)
[![DOI](https://img.shields.io/badge/DOI-pending-8A8A8A?style=flat-square)](#links)
[![Docs](https://img.shields.io/badge/docs-readthedocs-0A7E8C?style=flat-square)](https://serp-faq-engine.readthedocs.io)
[![License](https://img.shields.io/badge/license-MIT-8A8A8A?style=flat-square)](LICENSE)

SERP.fyi FAQ Engine answers questions about SERP.fyi in plain English. Ask about real-time rank tracking, AI visibility audits, ChatGPT and Perplexity mentions, entity recognition, local SEO, SERP features, reports or getting started, and the engine returns the best official answer from 40 SERP.fyi FAQs with a confidence score from 0 to 100. Built by [SERP.fyi](https://serp.fyi).

## Overview

SERP.fyi is a search intelligence platform that combines real-time Google search tracking with AI visibility audits. This repository publishes its 40 official FAQs as structured, machine-readable data and ships a lightweight question-matching engine for Node.js (NPM) and Python (PyPI), so the same answers can power help centers, chat widgets, support tools and AI assistants.

The engine has no external dependencies and makes no network calls. It tokenizes the question, maps SEO synonyms (for example *rankings* to *rank* or *ChatGPT* to *AI*), scores every FAQ by weighted keyword overlap, and returns the strongest matches.

## Key Capabilities

- **Plain-English Matching**: Ask in your own words and get the closest official SERP.fyi answer
- **Confidence Scoring**: Every answer carries a 0 to 100 match-confidence score and band
- **40 Official FAQs**: 15 platform FAQs and 25 feature and technical FAQs across 7 categories
- **SEO-Aware Synonyms**: Rankings, positions, LLM names, AI Overviews, local packs and more
- **Top-N Results**: Return the best 1, 3 or more answers for a question
- **Two Runtimes**: Identical results from the Node.js (TypeScript) and Python implementations
- **JSON Output**: Machine-readable results for widgets and integrations
- **FAQPage Schema**: All 40 FAQs as JSON-LD structured data in [`schema.json`](schema.json)

## FAQ Categories

| Category | Covers | FAQs |
|---|---|---|
| `general` | What SERP.fyi is, who it is for and how it differs | 5 |
| `ai-visibility` | AI visibility audits, citations and entity recognition | 9 |
| `rank-tracking` | Real-time rank tracking, devices, locations and accuracy | 8 |
| `local-seo` | Local search, local packs and heatmaps | 2 |
| `serp-features` | SERP features, zero-click searches and signal mapping | 3 |
| `reports-dashboard` | Reports, exports, white-label and the unified dashboard | 9 |
| `getting-started` | Getting started, privacy and support | 4 |

## Quick Start

### Node.js
```bash
npm install @serp-fyi/serp-faq-engine
npx serp-faq "does serp.fyi track chatgpt mentions"
npx serp-faq --top 3 "can I track mobile rankings"
npx serp-faq --list ai-visibility
```

### Python
```bash
pip install serp-faq-engine
serp-faq "can agencies white label reports"
python -m faq_engine --json "how often is data updated"
```

### In code
```python
import faq_engine

print(faq_engine.ask("is my data private"))
print(faq_engine.search("local pack heatmap", top=3))
```

```javascript
const { ask, search } = require("@serp-fyi/serp-faq-engine");

console.log(ask("what are serp features"));
```

### CLI Options

| Option | Output |
|---|---|
| `"question"` | Best matching answer |
| `--top N "question"` | Top N answers |
| `--json "question"` | Results as JSON |
| `--list [category]` | All questions, or one category |
| `--id N` | One FAQ by number (1 to 40) |
| `--categories` | Categories and FAQ counts |

## Example Matches

| Question asked | Matched FAQ | Confidence |
|---|---|---|
| "does it track chatgpt mentions" | Q29 | 92 |
| "can I track mobile rankings" | Q20 | 100 |
| "can agencies white label reports" | Q35 | 100 |
| "how often is data updated" | Q25 | 92 |
| "who made serp.fyi" | Q15 | 100 |

## Score Interpretation

| Score | Band | Meaning |
|---|---|---|
| 0 to 30 | No match | Rephrase the question or contact support |
| 31 to 60 | Possible match | Answer may be related; check the question shown |
| 61 to 80 | Good match | Answer is likely what you need |
| 81 to 100 | Strong match | Answer directly addresses the question |

## Dataset

[`dataset/serp_faqs.csv`](dataset/serp_faqs.csv) holds all 40 FAQs with `id`, `category`, `part`, `question`, `answer` and `keywords` columns. A walkthrough notebook is in [`kaggle/notebook.ipynb`](kaggle/notebook.ipynb).

## Related SERP.fyi Repositories

| Repository | Description |
|---|---|
| [serp-fyi-serp-tracker](https://github.com/SERP-fyi/serp-fyi-serp-tracker) | Track keyword rankings, SERP features and AI Overview visibility across Google, Bing, ChatGPT and Perplexity |
| [SERP-Checker-Tool](https://github.com/SERP-fyi/SERP-Checker-Tool) | Analyze search results in real time with a TypeScript and Python SERP checker |

## Keywords

SERP.fyi · SERP FAQ · Search Intelligence · Real-Time Rank Tracking · AI Visibility Audit · AI Overviews · ChatGPT Brand Mentions · Entity Recognition · Local SEO · SERP Features · LLM Signal Mapping

## Links

| Platform | URL |
|---|---|
| Website | https://serp.fyi |
| SERP Checker | https://serp.fyi/serp-checker/ |
| Local SEO & AIVO Audit | https://serp.fyi/local-seo-and-avio-audit/ |
| GitHub | https://github.com/SERP-fyi/serp-faq-engine |
| GitHub Pages | https://serp-fyi.github.io/serp-faq-engine/ |
| NPM | https://www.npmjs.com/package/@serp-fyi/serp-faq-engine |
| PyPI | https://pypi.org/project/serp-faq-engine/ |
| Hugging Face | https://huggingface.co/datasets/serp-fyi/serp-faq-dataset |
| Kaggle | https://www.kaggle.com/datasets/serpfyi/serp-faq-dataset |
| Zenodo | Pending |
| Docs | https://serp-faq-engine.readthedocs.io |

### Company Profiles

| Platform | URL |
|---|---|
| GoodFirms | https://www.goodfirms.co/company/serpfyi |
| SuperbCompanies | https://superbcompanies.com/organizations/serp-fyi/ |
| ProvenExpert | https://www.provenexpert.com/serp-fyi/ |
| Glassdoor | https://www.glassdoor.co.in/Overview/Working-at-SERP-fyi-EI_IE11124673.11,19.htm |

## About SERP.fyi

SERP.fyi is a search intelligence platform built for SEO professionals, digital marketing agencies, brand managers and CMOs. It combines real-time Google search tracking with AI visibility audits that show how search engines and AI systems such as ChatGPT, Perplexity and Google AI Overviews understand a brand. SERP.fyi is developed as part of the BHMarketer ecosystem.

## License

MIT, SERP.fyi
