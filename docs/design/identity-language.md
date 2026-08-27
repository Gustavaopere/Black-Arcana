# Black Arcana identity and vocabulary

Status: PREPARATORY — player-facing naming proposal for Stage 01 review.

## Core fantasy

Black Arcana is forbidden magic acquired through knowledge, bargains and mastery. Its identity is not "stronger normal spells". It specializes in rules that ordinary magic avoids: life equivalence, soul custody, sympathetic links, projection of remembered armaments, thresholds between positions, contracts, gaze-bound control and temporary personal dominions.

The visual language should feel precise and ritualistic rather than noisy: thin geometric sigils, broken concentric rings, asymmetry used to indicate cost/debt, restrained contextual HUD elements, and clear telegraphs for dangerous area effects. No Mahou Tsukai glyphs, textures, circles, sounds, spell prose or fiction-specific symbols are reused.

## Player-facing domains

### Sanguine Arts
Blood, life, equivalence, curses and prices paid by the body. Sanguine magic should feel transactional: every benefit exposes a measurable debt, cap or vulnerability.

Candidates: Sanguine Harvest, Sympathetic Wound, Blood Price, Law of Recurrence, Equilibrium Rite.

### Sepulchral Arts
Souls, death records, spirit anchoring and necrotic perception. Prefer Malum spirit resources when available instead of creating a parallel soul currency.

Candidates: Mortal Ledger, Soul Anchor, Spirit Sight, Black Pyre integration hooks.

### Eidetic Arsenal
Magic of memory made briefly physical. An eidetic construct reproduces a **sanitized combat profile**, never arbitrary persistent item data.

Candidates: Echo Armament, Ephemeral Tempering, Rift Blades, Spectral Arsenal, Oathforged Ascension.

### Liminal Arts
Thresholds, position, velocity, reciprocal displacement and the boundary between body and projected self.

Candidates: Threshold Gate, Veilstep Reflex, Anchor Recall, Reciprocal Transposition, Vector Reversal, Astral Severance.

### Cinder Arcana
Forbidden soul-fire and destructive convergence. Cinder effects are visually threatening but obey Black Arcana world-effect budgets; permanent grief is never the default.

Candidates: Black Pyre; Ruinous Convergence is deferred.

### Dominion Rites
Wards, permissions, covenants, large geometric rituals and temporary personal domains. Dominion is the primary home of explicit world rules rather than raw damage.

Candidates: Vigil Ward, Exclusion Ward, Gravitic Ward, Hexward Aegis, Covenant, Malison Constellation, Inner Dominion. Usurped Mandate is deferred.

### Noetic Arts
Perception, gaze, divination, astral cognition and borrowed senses.

Candidates: Namescry, Gaze of Stillness, Nullifying Gaze, Occult Appraisal, Borrowed Sight. Noetic Foresight is deferred.

## Shared terminology

- **Covenant** — explicit persistent relationship/permission state between players/entities and Black Arcana constructs.
- **Ward** — bounded persistent area rule with owner, lifetime, budget and permission policy.
- **Grand Ritual** — prepared high-impact act whose result justifies material/world interaction and is never routine combat busywork.
- **Forbidden Cast** — direct or channeled high-tier magic with unusually strong cost/cooldown/risk gates; not synonymous with terrain destruction.
- **Soul Anchor** — one bounded death-prevention charge backed by a valid spirit cost and recovery lockout.
- **Echo** — ephemeral projected item/weapon representation that cannot be stored, traded, repaired into permanence or used to duplicate arbitrary NBT.
- **Dominion** — temporary isolated or bounded rulespace owned by a caster/ritual, with guaranteed cleanup/return semantics.

## Naming rules

1. Prefer short English names that communicate gameplay without external-fiction knowledge.
2. Do not use reference catalyst codes or spell names as registry IDs.
3. Registry IDs describe the Black Arcana concept: e.g. `black_arcana:black_pyre`, `black_arcana:anchor_recall`.
4. Lore may use evocative occult vocabulary, but tooltips must expose concrete cost, duration and restrictions.
5. Host integrations may present a spell inside the host's UI, but localization remains Black Arcana-owned.

## Rejected identity elements

- Permanent numeric `Mahou`-style resource HUD.
- Spend-to-grow resource cap.
- Universal self-harm circle setup for every spell.
- Mandatory three-catalyst recipe language.
- Reference-specific Fae/Leylines ecosystem.
- Mystic Code-style mandatory scroll container.
- Reality Marble, Rho Aias, Crimson Black Keys and other strongly derivative reference/fandom names.
