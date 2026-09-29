# Invention Disclosure Form (abbreviated version)

> Note: Fields marked with * are required. Please fill in as completely as possible; incomplete information may affect the evaluation progress.

## Basic Information

- **Disclosure No.**: INV-2025-017
- **Invention title**: Learning-model-based cache eviction algorithm
- **Inventor**: Xiaolin (backend platform team)
- **Date completed**: 2025-07-28
- **Contact**: xiaolin@company.com (extension 2103)

## Summary of the Technical Solution

A novel cache eviction algorithm was designed: a lightweight learning model (an online-trained gradient boosting tree or logistic regression variant) predicts the short-term access probability of each cache entry, replacing the fixed-priority strategy of traditional LRU/LFU. Cache entries are sorted by the model-predicted access probability, and the entry with the lowest probability is evicted.

Key features:
1. The prediction features use only low-cost statistics of the entry itself (access frequency, interval since the most recent access, entry size, historical patterns), without relying on business semantics;
2. The model is updated incrementally online; after each round of eviction, "whether the entry was accessed again" is used as the label fed back into training;
3. Prototype validation: on a self-built workload (a zipfian distribution simulating hot-spot shifting), the hit rate improved 12%-18% compared with LRU and 8%-11% compared with LFU; the memory overhead increment is about 3%.

## Prototype and Validation

- Prototype status: complete (Python implementation, about 900 lines), already running in the company's test environment.
- Validation data: self-built simulated workload + log replay of two internal services (about 2 weeks of traffic).
- Performance data: hit-rate improvement as above; extra CPU overhead about 2%, extra memory about 3%.

## Public Disclosure Status

- An article introducing the solution was published on the company's technical blog in May 2025 (including the overall approach, pseudo-code-level descriptions, and some experimental results).
- Not disclosed through any other public channels (conferences, journals, open-source repositories).

## Existing Patents / Prior Art

- (Not filled in)
- (Not filled in)

## Commercial Value and Implementation Plans

- (Not filled in)

## Figures / Appendices

- (Not filled in)
