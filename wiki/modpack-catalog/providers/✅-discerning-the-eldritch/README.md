# Discerning The Eldritch — provider canônico

## Prova binária exata 1.4.4-1.21 — 2026-10-13

✅ [Dossiê de 22/22 IDs/classes físicos](EXACT-BINARY-SPELLS-1.4.4-1.21.md): [Java 21 #38455449207](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38455449207) **SUCCESS**. CurseForge file `8816497`, JAR **22.098.930 bytes**, SHA-1 `cf35c225aced23b705d1e0fd1bc5c62d96540e0c` = modlist física #220. `DiscerningTheEldritch → SpellRegistries` com **22/22** instâncias `AbstractSpell` registradas incondicionalmente, 9 Eldritch / 1 Blood / 2 Evocation / 2 Fire / 1 Holy / 2 Ice / 5 Ritual. IDs e escolas padrão verificados em cada classe. `COUNTED_EXACT` apenas quanto ao registro estático, campanha **22/39 exatos / 17/39 pendentes**, +0 raízes, mínimos **1857/1855** inalterados. Insanity/Exorcism, gates Ritual, config, Survival e compatibilidade runtime ⚠️.


Status: `INSTALLED 1.4.4-1.21 / COUNTED_EXACT 22/22 STATIC REGISTRY / RUNTIME QA PENDING`

- **JAR do pack:** `discerning_the_eldritch-1.4.4-1.21.jar`
- **Mod ID:** `discerning_the_eldritch`
- **Version authority:** modlist atual + upstream branch `1.21`
- **Source pin auditado:** `AceTheEldritchKing/Discerning_The_Eldritch@7bbd81f902c65a4452f47656ebd948cae8cd5833`
- **Upstream `gradle.properties`:** `mod_version=1.4.4-1.21`
- **Casting authority:** Iron's Spells 'n Spellbooks

## Cobertura de fichas existentes: **22/22**

A antiga página pública dizia “15 spells” e enumerava 14. O registry exato 1.4.4 resolve a discrepância: são **22 registrations reais**.

| School/classificação | Registrations | Fichas |
|---|---:|---:|
| Eldritch | 9 | 9 |
| Blood | 1 | 1 |
| Evocation | 2 | 2 |
| Fire | 2 | 2 |
| Holy | 1 | 1 |
| Ice | 2 | 2 |
| Ritual (`discerning_the_eldritch:ritual`) | 5 | 5 |
| **Total** | **22** | **22** |

Comentários de ideias futuras no registry não são spells ativos e não inflam a contagem.

## Inventário exato

### Eldritch
`silence`, `conjure_forsaken_aid`, `esoteric_edge`, `conjure_gaoler`, `otherworldly_presence`, `mend_flesh`, `rift_walker`, `abracadabra`, `esoteric_strike`.

### Blood
`vein_ripper`.

### Evocation
`boogie_woogie`, `guardians_gaze`.

### Fire
`soul_slice`, `soul_set_ablaze`.

### Holy
`exorcism`.

### Ice
`glacial_edge`, `crystalline_carver`. Public-facing “Glacial Cleave” maps to registry ID `glacial_edge` / class `GlacialEdgeSpell`.

### Ritual
`call_ascended_one`, `blades_of_rancor`, `zealous_harbinger`, `ravenous_revenant`, `libras_judgement`.

## Escola Ritual própria

`DTESchoolRegistry` registra `discerning_the_eldritch:ritual` com focus tag, Ritual Power, Ritual Resist, sound e Ritual damage type próprios.

`AbstractRitualSpell` estabelece:

- crafting proibido;
- complex rituals não entram no loot genérico;
- super-complex: bloqueado via SPELLBOOK e SWORD;
- complex non-super: bloqueado via SPELLBOOK;
- casts ritual base não são interruptíveis.

Overrides individuais estão nas fichas.

## Systems provider-native relevantes

- Silence e Metaphysical cancelam Iron's `SpellPreCastEvent` server-side.
- Insanity é opcional, default off; max default 15.
- Mend Flesh reactive healing é config-driven.
- Abracadabra possui damage-cap e harmful-effect gate configuráveis.
- Summons usam `SpellSummonEvent` / `SummonManager` quando são summons controlados.
- Soul Fire attacks consomem `SOUL_FIRE_STACKS` da arma.
- Frostbite combo usa `FROSTBITE_LEVEL` attachment + `CHILLED`.
- Exorcism existe como cleanse específico do próprio Insanity system.

## Deduplicação

O provider ocupa anti-cast, damage-cap defense, harmful-effect immunity gate, metaphysical teleport lockout, entity-position swap, weapon-scaled Eldritch attacks, controlled/feral summons, Blood lifesteal engage, Soul Fire stack spending, Insanity cleanse, Frozen Weapon bonus, Frostbite combo, boss ritual summon, cursor-homing ritual blades, Predator/Prey hunting state e HP-threshold judgement.

Black Arcana não deve duplicar esses contracts por rename/VFX.

## QA blockers estáticos

- Ravenous Revenant: branch Predator+Prey de 25 damage é logicamente inalcançável e não adiciona a jaw ao level.
- Zealous Harbinger: primeira posição `z+i` é imediatamente sobrescrita por `z-i` em cada projectile.
- Guardian's Gaze: block-particle `else if` está aninhado sob `ENTITY`, portanto é inalcançável.
- Crystalline Carver: `isFinalCast` é campo mutável na instância do spell registrada; possível shared-state entre casters exige GameTest/runtime QA.
- Otherworldly Presence: anti-cast e veto de incoming foram localizados no source; `ServerEvents#livingIncomingDamageEvent` cancela se vítima ou causingEntity Living têm Metaphysical. Aceite no pack continua PENDING.

Esses itens são observações de source 1.4.4, não correções runtime deste chat.

## Reauditoria de parâmetros e perks — 24/10/2026

[22 fichas e contratos comuns](SPELL-PERK-BOUNDARIES-1.4.4-1.21.md) agora rastreiam parâmetros até consumers, com dano/tipo, alvo/área, projéteis/hitbox, tempos/custos/recasts, summons, estados e persistência. **22/22 é somente este recorte documental**, sem encerrar todos os itens/Curios/sistemas do provider. +0 identidades/+0 strict; configs/hosts, Mastery Ritual, hooks integrados, Survival e QA permanecem PENDING.

Publisher CF8816497 revalidado nesta sessão: 22098930 bytes, SHA-1 `cf35c225aced23b705d1e0fd1bc5c62d96540e0c`, SHA-256 `77e53df3fe020572626593ca9f6b955abce1dd4b49697084c2226019dcf2ef14`. Não é nova leitura do perfil original nem prova integral de método/source. As contagens 1857/1855 e campanha22/39 do cabeçalho datado13/10 são históricas; o [painel atual](../../meta/PROGRESSO-CATALOGO-ATUAL.md) preserva mínimos1856/1854, campanha38/39 e universo global aberto.

A normalização da escola Ritual custom no RPG produz um token com `/`, rejeitado pelo validador de lanes consultado; reprodução isolada do método consta no dossiê comum, sem afirmar crash em jogo ou corrigir runtime neste lote.
