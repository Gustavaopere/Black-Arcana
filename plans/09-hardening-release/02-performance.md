# 09.02 — Performance

## Targets
No global tick scans; bounded per-cast work; bounded persistent queues; no leaked chunk tickets; controlled particles/network traffic.

## Profile
Black Flame frontier, projectile barrages, large AoE, active rituals, domains, many concurrent players and temporary-block restoration.

## Acceptance
Record representative timings/memory/queue sizes and establish regression thresholds. Any hotspot receives a reproducible benchmark/profile before optimization claims.
