# Ars Morph 2.0.0 — matriz causal Identity2 para perks

**Checkpoint 17/10/2026 · PR #825 draft.** `ars_morph` é ponte Identity2 / Ars Nouveau. Esta matriz indexa as sete classes Java de habilidades e as onze atribuições JSON do source. Cada [ficha individual](abilities/) cobre admissão, targets, entidades/efeitos, velocidade, duração, cooldown bruto, passivos, cancelamentos, políticas para perks e testes.

## Proveniência e barras

- Mod ID `ars_morph`, JAR instalado documentado `ars_morph-1.21.1-2.0.0.jar`, SHA-1 `68ff47cc58c0ffe9570bb907f65c2910311ed45f`. [Source de versão 2.0.0](https://github.com/Alexthw46/Ars-Morph/tree/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58). **SOURCE_CAUSALITY** não comprova equivalência binária nem gameplay. Hosts na modlist: Identity2 2.2.4, Ars Nouveau 5.13.1, Ars Elemental 0.7.10.1 (módulo opcional presente) e Gabou's Libs 1.8.7.
- **Barra global: —%**, com piso histórico reconciliado 1.857 semânticos / 1.855 estritos, denominador total não conhecido. **+0 raízes novas** nesta etapa.
- **Barra Ars Morph: ✅ 7/7 classes de habilidade (100% fichas SOURCE_CAUSALITY)** e **11/11 JSONs de atribuição (100% documentados)**. O glifo `ars_morph:glyph_morph` mantém **1/1** no [catálogo próprio](glyphs/morph.md). Runtime/compatibilidade ⚠️ PENDENTE, adapters RPG ⛔ **0 homologados**.
- Campos JSON `cooldown` / `use_duration` são **inteiros literais**; unidade temporal, enforcement, consumo ao cancelar e synchronização cabem ao Identity2 e não foram comprovados no JAR físico.

## Sete habilidades — onze atribuições

| Classe/forma | Ficha | Atribuições JSON | Cooldown / Use duration (brutos) | Causalidade source | Gate de perk |
|---|---|---:|---|---|---|
| Weald Walker | [Weald Walker](abilities/weald-walker.md) | 5 | `100 / 20` | Projectile Ars com velocity 1.0 e inaccuracy 0.8, spell herdada do morph | ⚠️ NBT/target/damage; dedup de cinco variantes |
| Wilden Hunter | [Wilden Hunter](abilities/wilden-hunter.md) | 1 | `800 / 20` | Summon Wolves + Extend Time; retira Summoning Sickness após evento não cancelado | ⚠️ 0/N entidades e owner Ars |
| Wilden Stalker | [Wilden Stalker](abilities/wilden-stalker.md) | 1 | `800 / 100` | Self Launch×2 + Glide + DurationDown; sync server-side de isFlying | ⚠️ movimento/status/tick |
| Starbuncle | [Starbuncle](abilities/starbuncle.md) | 1 | `100 / 20` | Efeito Speed 3000 ticks, amplifier 1; self | ⚠️ buff duration diferente de cooldown |
| Whirlisprig | [Whirlisprig](abilities/whirlisprig.md) | 1 | `400 / 20` | Grow + AOE×3 em bloco abaixo; Jump Boost passivo 40 ticks amp 2 | ⛔ world mutation; passivo não é cast |
| Wixie | [Wixie](abilities/wixie.md) | 1 | `200 / 20` | Splash potion 200 ticks amp 1; lista boa 10, ruim 12, índice sempre nextInt(12) | ⚠️ erro possível se agachado, não reproduzido no JAR |
| Firenando (condicional) | [Firenando (condicional)](abilities/firenando.md) | 1 | `120 / 40` | HomingProjectile Ars Elemental; ignora alvos que não sejam Enemy | ⚠️ conditional host; ⛔ retarget |

As variantes Blazing/Cascading/Flourishing/Vexing/Flashing Weald Walker são **cinco atribuições, uma habilidade Java** com predef compartilhado. Firenando é condicional a presença de Ars Elemental; existência na modlist não atesta execução correta. Nenhuma forma ou efeito derivado foi adicionado ao ledger semântico como nova magia.

## Contratos e QA

1. `MorphBoundAbility.execute` só segue se host for `Player`, morph não nulo e classe compatível. A classe base captura exceptions do callback e registra log. Identity2 permanece dono de aquisição/estado, despacho da habilidade e parâmetros dos JSONs.
2. Ativações que internamente criam um `SpellResolver` Ars, projétil, poção ou efeito formam uma única cadeia causal. Não creditar duas vezes Mastery por 1 ability + 1 cast secundário, nem aplicar mana/cooldown próprio da Black Arcana.
3. Wixie source: ramo crouching usa lista com 10 entradas, mas sorteia índice limitado por 12. Índices 10 e 11 são inválidos naquele ramo. O wrapper captura Throwable; **não afirmar crash físico**. Testar lançamento e cooldown sob erro.
4. Whirlisprig ativa Grow + AOE×3 em bloco abaixo e renova Jump Boost no callback passivo do servidor. Alteração de mundo do provider externo não é automaticamente coberta por `WorldEffectPolicy` Black Arcana; requer claims/survival QA. Passivo não é cast nem XP.
5. Wilden Stalker possui morph-tick handler server que sincroniza isFlying via Identity2; isso não fornece API de perk de voo. Firenando restringe homing para entidades `Enemy` além dos filtros herdados, sem hook de retarget por personagem.
6. Testes pendentes: servidor dedicado e cliente real no pack exato; postEvent cancelado, cada ramo de target, cooldown/use duration do Identity2 2.2.4, possíveis erros Wixie, persistência/relog/respawn/dimensão, claims/PvP, ownership, source de damage, timeouts, passivos e player real.
7. Stage 06.05 🟡 / Stage 09 físico PENDING; source docs completos não promovem Stage nem autorizam adapters.

## Fontes técnicas

- [IdentityReg](https://github.com/Alexthw46/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/java/com/alexthw/ars_morph/identity/IdentityReg.java#L56-L85)
- [ElementalModule](https://github.com/Alexthw46/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/java/com/alexthw/ars_morph/identity/ElementalModule.java#L16-L27)
- [MorphBoundAbility](https://github.com/Alexthw46/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/java/com/alexthw/ars_morph/identity/ability/MorphBoundAbility.java#L15-L62)
- [Inventário original](ABILITIES.md); [glyph Morph](GLYPH-MORPH.md); [matriz do glifo](PERK-ENGINEERING-MATRIX-2.0.0.md)

**Nenhum adapter ou nova magia implementada nesta tranche.**
