# Stage 05.15 casting audiovisual asset provenance

Status: Phase D project-owned resource tranche.

The four generic cast sounds introduced by this tranche are **project-owned** and were **procedurally generated** specifically for Black Arcana. No source audio, sample, stem, melody, signature effect, or extracted resource from another mod, game, film, television work, or other copyrighted audiovisual source was used.

Generation method: simple numerical waveform synthesis produced mono 44.1 kHz PCM source material, followed by OGG/Vorbis encoding with FFmpeg/libvorbis. The sounds are intentionally short generic interface/presentation cues rather than attempts to reproduce any provider's recognizable audio language.

| Resource | Presentation role | Size | SHA-256 |
|---|---|---:|---|
| `sounds/cast/intent.ogg` | restrained local anticipation; never authoritative success | 4039 bytes | `6f390e205e006eab5419f9e2d852569e69c33c78678edab2b0b965584e0c977d` |
| `sounds/cast/success.ogg` | generic authoritative cast settlement success | 4295 bytes | `9d448f8df64f74984d3224b9c4d785663e84e463a5c46fa914301e10931491c0` |
| `sounds/cast/denied.ogg` | generic authoritative denial reinforcement | 4159 bytes | `2c1f1d9f0764f1069aa72dac1cd0123ab8b8f64ae480d449ad7321dc537f8844` |
| `sounds/cast/failed.ogg` | generic authoritative effect-failure reinforcement | 4486 bytes | `cbe4b348a3e0698239097c0afdc5c19283b6137388a389550312acb04aee8644` |

Clean-room boundary: these assets are not derived from, modeled after, traced from, or intended to recreate signature sounds from **Mahou Tsukai**, **Iron's Spells 'n Spellbooks**, Epic Fight, EFIS, Ars Nouveau, or any other provider/mod. Conceptual inspiration for Black Arcana does not authorize copying provider audiovisual identity.

Runtime authority boundary: sound availability is presentation-only. Missing, malformed, muted, or reloaded audio must degrade to no audio/fallback presentation and cannot deny a valid cast, approve an invalid cast, alter cost/cooldown/target/world mutation, or replace server-authored result semantics. Critical denial/failure information remains available through the existing non-audio Stage 05 feedback surfaces.

Future third-party audiovisual material may enter the project only after compatible license/permission and durable provenance are recorded before merge. Provider-native presentation should be preferred on provider-hosted surfaces where a verified seam already owns the presentation, to avoid duplicate animation/audio/VFX.
