# Explosion

- Registry ID: `ars_nouveau:glyph_explosion`
- Source class: `EffectExplosion`
- School: Elemental Fire
- Default tier: **2**
- Default mana: **200**
- Default source config: intensity **0.75**, amplification intensity **0.5**, AOE intensity **1.5**, damage **6.0**, damage per Amplify **2.5**
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Creates Ars Nouveau's custom explosion at the resolved position. AOE raises blast size without directly raising the configured damage term; Amplify affects size and damage; Dampen reduces size/damage. Extract changes block interaction from decay-style destruction to full-destroy/drop behavior. NeoForge's explosion-start hook can veto execution.

Compatible augments: Amplify, Dampen, AOE, Extract. Amplify is limited to 2 by default.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:fire_essence` + `minecraft:tnt` ×3 + `minecraft:fire_charge`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

This is a destructive provider-native capability. Black Arcana must never route its own explosions through this as a way around `WorldEffectPolicy`; its destructive effects remain independently budgeted and policy-controlled.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / HIGH-RISK WORLD EFFECT / RUNTIME+CONFIG QA PENDING`.

## Dossiê de engenharia para perks — causalidade exata

- **Código versionado:** [`EffectExplosion.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectExplosion.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectExplosion` no Ars 5.13.1, método `onResolve`.
- **Raio/intensidade:** `BASE.get()+AMP_VALUE.get()*ampMultiplier+AOE_BONUS.get()*aoeMultiplier-0.5*count(Dampen)`; defaults BASE=0.75, AMP=0.5, AOE_BONUS=1.5. **Dano:** `ANExplosion.baseDamage=DAMAGE.get()` (default 6.0) e `ampDamageScalar=AMP_DAMAGE.get()` (default 2.5), dano por entidade definido downstream em `ANExplosion`, não diretamente nesta classe. **Blocos:** Extract escolhe `DESTROY`, senão `DESTROY_WITH_DECAY`; `EventHooks.onExplosionStart` pode cancelar a explosão. Pacote enviado a jogadores dentro de distância quadrada 4096 é sincronização e **não** raio de explosão. **Perks:** intensidade, dano, proteção e drops são eixos separados; sem API de mutação comprovada.
- **Limite de integração:** ✅ fonte estática identificada; ⚠️ parâmetros condicionados à configuração carregada; ⛔ nenhum hook externo de mutação verificado. Mana, targeting e settlement pertencem a Ars; RPG Skill Tree não substitui o resolver. Gameplay/Survival e adapter real: PENDING.

## Auditoria do executor secundário — limitações verificáveis

- **Java:** [`api/util/ANExplosion.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/ANExplosion.java).
- **Executor `ANExplosion` — prova de fórmula downstream:** `ANExplosion.explode` calcula distância normalizada `d12=distance/(2*radius)`, exposição `d14=getSeenPercent`, `d10=(1-d12)*d14`, e dano `min(max(0,(int)(((d10*d10+d10)/2)*7*(2*radius)+1)), baseDamage + amps*ampDamageScalar)`. O cast inicial define `amps=spellStats.getAmpMultiplier()`; defaults do cap configurado `baseDamage=6` e `ampDamageScalar=2.5`. Knockback usa `d10` e `EXPLOSION_KNOCKBACK_RESISTANCE`. A geometria de entidades usa AABB central de extensão `2*radius` por eixo, com filtro por distância `d12<=1`; a coleta de blocos é por raios de resistência do mundo e não por essa mesma lista. **Hook real:** `EventHooks.onExplosionDetonate` ocorre na lista de entidades dentro de `ANExplosion.explode`; a presença do evento não comprova que o RPG Skill Tree possa ajustar dano/radius/caster sem quebrar a causalidade.

**Limite:** fatos lidos do source pin, não prova de comportamento no JAR físico ou de adapter RPG. QA no modpack ainda pendente.

## Certificação estática por pipeline e consumidores — 25/10/2026

**✅ COMPLETE_PERK_READY apenas no escopo `STATIC_TECHNICAL_CATALOG_ONLY` — NÃO é certificação de perk jogável. ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.** O ID e a classe no JAR publisher foram auditados separadamente da semântica lida no commit de source.

| Campo exigido | Contrato source-pinned, limites e classificação para perks |
|---|---|
| Identidade/versionamento | Ars Nouveau `5.13.1`; `ars_nouveau:glyph_explosion`; classe `EffectExplosion`; escola Elemental Fire, tier II. [Source imutável](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectExplosion.java) e [registry do publisher SHA-exato](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Comportamento, causalidade e settlement | `onResolve(HitResult)` computa a intensidade e chama seu wrapper `explode`. Constrói `ANExplosion`, grava `baseDamage` e `ampDamageScalar`, consulta `EventHooks.onExplosionStart` que pode **cancelar** a execução, depois chama `explode()`/`finalizeExplosion(false)` e envia pacote a jogadores num raio de sincronização definido por **distanceToSqr < 4096**. O pacote não define o raio de dano. |
| Parâmetros, escalas e caps | Raio/intensidade nominal = `BASE+AMP_VALUE*ampMultiplier+AOE_BONUS*aoeMultiplier−0.5×count(Dampen)`; defaults **0,75 + 0,5×amp + 1,5×aoe − 0,5×dampen**. Executor `ANExplosion` calcula `d12=dist/(2×radius)`, exposição `getSeenPercent`, `d10=(1−d12)×exposure` e dano proposto `min(max(0,int(((d10²+d10)/2)×7×(2radius)+1)),baseDamage+amps×ampDamageScalar)`; baseDamage **6,0** e escalar por amp **2,5** por config. Mobs/armadura/claims/eventos downstream podem alterar resultado, não são damage fixo. Cap default Amplify=**2**. |
| Targeting, geometria, projétil, tipo e duração | Explosão na posição resolvida pelo HitResult; `ANExplosion` considera entidades em AABB de `2×radius` e limita por distância normalizada; blocos por ray-marching/resistência separados. Com Extract: `Explosion.BlockInteraction.DESTROY`; sem: `DESTROY_WITH_DECAY`; não afirmar drops garantidos. O raio passado é intensidade de explosão, não comprimento em blocos do projectile da Form. |
| Custos, aprendizagem e limites da receita | Mana default **200**; tier II; XP receita default 55; starter default não; recipe `ars_nouveau:fire_essence` + `minecraft:tnt` ×3 + `minecraft:fire_charge`. [Acquisition 85/85](../../ACQUISITION.md). Cast/cooldown e mana efetiva da composição são autoridade/config Ars Nouveau. Augments: Amplify, Dampen, AOE, Extract. AOE escala intensidade/radius mas **não** muda `baseDamage`/`ampDamageScalar` diretamente; dano ainda varia pela exposição e geometria. `EventHooks.onExplosionDetonate` do executor recebe lista de entidades filtráveis. |
| Integração e segurança | **⛔** Modificação genérica de raio/dano ou replay de explosão proibidos sem bounds, confirmação de hook real e política de mundo. `WorldEffectPolicy` rege explosões próprias do Black Arcana, não cancela automaticamente mutação Ars. Validar proteção, griefing, multiplayer e performance fisicamente. Contrato de perks RPG Skill Tree e hook mutador para este caminho não verificados. Não trocar target, type, raio, mana nem recipients com API presumida. Black Arcana conserva seu runtime, hazards e `WorldEffectPolicy` para efeitos próprios. |
| Grau de evidência/testes | Source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`; JAR publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` prova **ID/classe registrada**, não todos os métodos do classfile ou gameplay atual. Config final, order de eventos, integrações de outros mods, PvP/claims, servidor e cliente: **NOT_TESTED**. |

**Regra de reauditoria:** alterações de JAR/source, config, modificadores, geometria/ordem de eventos ou consumidor downstream exigem nova verificação técnica antes de liberar qualquer hook. Efeitos/raios/VFX não são eventos novos de cast/Mastery.
