# Alex's Caves 1.0.10 — auditoria dos tipos de dano

**Status:** ⚠️ fechamento apenas de recursos `11/11`; consumidores Java, DamageSource em runtime, hooks e QA física continuam pendentes. O conteúdo aqui **não** é um certificado técnico `COMPLETE_PERK_READY`.

- Artefato oficial: SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, tamanho 75.279.314 bytes.
- Auditor: [`docs/qa/alexscaves_1010_damage_type_probe.py`](../../../../../docs/qa/alexscaves_1010_damage_type_probe.py); [CI da sonda](https://github.com/Gustavaopere/Black-Arcana/actions/runs/40985275338).
- Manifesto: [JSON fixado](EXACT-RESOURCE-MANIFEST-1.0.10.json); inclui hashes por membro do ZIP, valores JSON, seis tag JSONs e memberships textuais diretas.
- Proveniência: os valores são lidos do JAR 1.0.10 verificado, **não** da fonte 1.1.1.
- Contagem de magia: 0 spells/ações novas; estes 11 registros são classificadores de dano, não 11 feitiços.

## Campos literais comparados

| Registry ID | `message_id` | `scaling` | `exhaustion` | Tags diretas | Ficha |
|---|---|---|---:|---:|---|
| `alexscaves:acid` | `acid` | `never` | 0.1 | 0 | [`acid`](acid.md) |
| `alexscaves:dark_arrow` | `desolate_dagger` | `never` | 0.3 | 3 | [`dark_arrow`](dark-arrow.md) |
| `alexscaves:desolate_dagger` | `desolate_dagger` | `never` | 0.3 | 1 | [`desolate_dagger`](desolate-dagger.md) |
| `alexscaves:forsaken_sonic_boom` | `forsaken_sonic_boom` | `never` | 0.3 | 0 | [`forsaken_sonic_boom`](forsaken-sonic-boom.md) |
| `alexscaves:gumball` | `gumball` | `never` | 0.3 | 0 | [`gumball`](gumball.md) |
| `alexscaves:intentional_game_design` | `intentional_game_design` | `never` | 0.3 | 0 | [`intentional_game_design`](intentional-game-design.md) |
| `alexscaves:nuke` | `nuke` | `never` | 0.1 | 3 | [`nuke`](nuke.md) |
| `alexscaves:radiation` | `radiation` | `never` | 0.1 | 0 | [`radiation`](radiation.md) |
| `alexscaves:raygun` | `raygun` | `never` | 0.3 | 3 | [`raygun`](raygun.md) |
| `alexscaves:spirit_dinosaur` | `spirit_dinosaur` | `never` | 0.3 | 2 | [`spirit_dinosaur`](spirit-dinosaur.md) |
| `alexscaves:tremorzilla_beam` | `tremorzilla_beam` | `never` | 0.3 | 0 | [`tremorzilla_beam`](tremorzilla-beam.md) |

## Advertências de contrato

O recurso `dark_arrow` possui `message_id=desolate_dagger`, igual a `desolate_dagger`; ambos os arquivos possuem o mesmo conteúdo e hash, mas **IDs de dano distintos**. Isso deve ser preservado, sem normalização editorial da fonte.

A tag `minecraft:bypasses_cooldown` trata de classificação de dano no Minecraft, não de cooldown de casting de qualquer feitiço. `minecraft:is_explosion`, `minecraft:is_projectile` e `minecraft:is_fire` são declaradas como memberships **textuais**, não como comprovação da aplicação do `DamageSource` no jogo. A tag `alexscaves:deep_one_ignores` é inventariada, mas não lista diretamente nenhum dos onze IDs.

**PENDENTE:** rastrear bytecode 1.0.10 para cada construtor/uso real do tipo de dano, owner/causa, valores de dano, invulnerabilidade/impactos, proteção PvP, extensão/alteração segura e entradas do sistema de perks. Até isso, `NOT_CERTIFIED` / `NOT_VERIFIED` / `NOT_TESTED`.
