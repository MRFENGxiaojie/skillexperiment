# Marketing context ? acme-enterprise.cn

## Current state

- Company: Acme Enterprise (B2B corporate IT services), public site acme-enterprise.cn, WordPress.
- Sitemap (exported 2026-08-05) contains 223 URLs: /services/ (8), /solutions/ (5), /products/ (4), /blog/ (120 current posts + 5 legacy 2023 posts), /resources/ (30 whitepapers), /landing/ (15 ai-consulting pages), /legacy/ (12 services-2019 pages), 4 category pages, plus home, about, case-studies, contact.
- Content team publishes roughly 3?4 blog articles weekly; organic search is the primary acquisition channel (quote requests via contact and case-studies).
- No section hub or landing page exists for /resources/ or /landing/; those pages are only reachable from campaigns and ads.

## Crawl notes

- crawl-export.csv is a partial crawl of all 223 sitemap URLs run on 2026-08-06 with a home-hosted crawler; JS-rendered links were not followed, so internal inlink counts may undercount.
- Columns: url, http_status, redirect_to, title, inlinks.
- Confirmed dead links (HTTP 404): /BLOG/tech-tips/, /services/Cloud-Migration/, /legacy/services-2019-* (12), /blog/posts/2023/*/old-post-* (5).
- /?p=345 and /?p=892 return HTTP 301 and should be cleaned up or canonicalized.
- Pages with 0 inlinks in this crawl: /landing/ai-consulting-* (15), /resources/whitepaper-* (30), /legacy/*, /blog/posts/2023/* ? treat these as orphan candidates.

## Business priorities

- Fix the structural issues that keep new content from ranking: duplicate/case-variant URLs, dead links, orphan pages, and 4+ level nesting.
- Pair every URL change with a 301 redirect; prefer low-effort, high-ROI fixes first.
