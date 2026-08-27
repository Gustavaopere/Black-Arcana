# 09.03 — Dedicated Server & Multiplayer Abuse

## Scope
Client-classloading, packet spoof/spam, duplicate cast requests, concurrent ritual activation, disconnect mid-cast, permission/PvP rules and integration mismatch.

## Acceptance
Server boots and runs without client classes; malformed inputs fail safely; no item/resource duplication from disconnect/race conditions; server remains authoritative under intentionally stale/malicious client intent.
