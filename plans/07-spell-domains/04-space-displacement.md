# 07.04 — Space & Displacement

## Candidate mechanics
Blink, ordered teleport, target swap, projectile displacement/recall, astral projection and spatial disorientation.

## Safety
Destinations must be server-validated for loaded chunk, collision, world border, dimension rules and protection. Never teleport into guaranteed lethal/invalid geometry unless the spell explicitly documents risk and server allows it.

## Integration
Ars may host utility/resource interactions; Iron's may host combat casts; core owns authoritative destination validation.

## Acceptance
GameTests cover world border, unloaded chunks, vehicles, bosses, players, fluids, suffocation and dimension mismatch.
