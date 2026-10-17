# Wind Shield

**⚠️ Verificação do publisher 2026-10-13:** `aero_additions:wind_shield` e sua classe foram confirmados por `javap` no JAR oficial CurseForge 1.2.8, [Java21 #38431639191](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38431639191). O SHA-1 do arquivo físico instalado **não foi comprovado** (dado histórico de 35 dígitos inválido): esta ficha segue `COUNTED_SOURCE_PINNED`, não `COUNTED_EXACT`; já contabilizada, **+0**. [Provenance/gate](../EXACT-PUBLISHER-SPELLS-1.2.8-PHYSICAL-SHA-BLOCKED.md). Runtime, aquisição e config ⚠️.


- Provider: **SnackPirate's Aeromancy Additions** (`aero_additions`)
- Version: `1.2.8`
- Registry id: `aero_additions:wind_shield`
- Registered class: `WindShieldSpell`
- Provider school: `aero_additions:wind`
- Host registry: **Iron's SpellRegistry**
- Semantic state: `COUNTED_SOURCE_PINNED`
- Strict contribution: `1`

## Identidade semântica

Spell provider-owned ativo no `AASpells` do source pin 1.2.8. A identidade é contada pelo registro ativo do provider, não por nomes de classes, entities, effects ou assets auxiliares.

## Registration evidence

O source pin contém uma chamada ativa `registerSpell(new WindShieldSpell())` para esta identidade. O provider registry é ligado ao event bus sem branch provider-side de configuração que remova este registro.


## Evidence boundary

Esta ficha fecha ID, classe registrada, ownership, escola Wind e estado semântico source-pinned. Mecânica quantitativa, custo, cooldown, acquisition settlement, networking, compatibilidade e comportamento no modpack físico permanecem QA separado quando não explicitamente fechados pelo dossiê.

Source: `../EXACT-1.2.8-SPELL-INVENTORY.md`.

## Engenharia causal para perks — 17/10/2026

**Identidade:** mod ID `aero_additions`, versão `1.2.8`, source fixo `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`. **⚠️ COUNTED_SOURCE_PINNED**: dez registros confirmados em JAR oficial de publicação ([Java 21 #38431639191](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38431639191)), mas SHA-1 do JAR *instalado* na modlist histórica é inválido/incompleto (35 dígitos); **NÃO** promover a COUNTED_EXACT instalada. JAR publisher `aero_additions-1.2.8.jar` SHA-1 `dee32c9fa84a9b3796e39846608f8f77591ea56f`. Todos os números abaixo vêm do source, não de configuração efetiva/QA físico. Iron's governa casting, mana/cooldown; Aero Additions governa efeitos; RPG Skill Tree somente progressão/perks por contrato real.

**Raiz `aero_additions:wind_shield` — Wind Shield.** Source-only; dados de domínio, raio, alvo e duração são mensurados conforme os métodos abaixo, quando aplicáveis.

| Eixo | Observação fonte-fixada | Mutabilidade por perk |
|---|---|---|
| Cast/stats | LONG, níveis 1–5, cooldown 140s, castTime 60, mana 130+30/nível, power 30+8/nível; durationSeconds = `10+5×level+(int)sqrt(10×spellPower)`. | Duração depende do power do caster, não somente spellLevel. |
| Chance real | WindShieldSpell.chanceToDeflect(amplifier)=0.3+amplifier/10, MobEffect amplifier=level−1. Níveis 1–5 resultam em chances nominais **30%,40%,50%,60%,70%** por evento elegível. | Não confundir com +3% dodge por nível descrito no changelog 1.2.8 sem localizar atributo/handler correspondente. |
| Evento de deflexão | AAServerEvents.windShieldDeflection em ProjectileImpactEvent, quando EntityHitResult entity com effect e projectile fora de AAEntityTypeTags.REFLECTION_IMMUNE, sorteia próximo float, cancela evento e chama Projectile.deflect(REVERSE,...). Handler também prevê proteção automática para SUMMONED_BREEZE, identidade não registrada como spell. | ⚠️ evento de impacto não prova dano evitado em todos os outros pipelines; hook é interno ao provider. Não imputar extensão a todos projéteis mágicos. |
| Hitbox/range | Somente o alvo com efeito no EntityHitResult; sem aura de área ou raio per-caster. OnCast aplica status self. | ⛔ aumento de área, shield for all/allies ou target retarget sem contract. |
| Sync | WindShieldEffect apenas repassa add/removal callbacks; flags de efeito locais estão comentadas no arquivo, não são APIs em produção. | QA dedicated/client, authority e C2S. |

**Localizadores:** [WindShieldSpell.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_shield/WindShieldSpell.java#L19-L72) · [AAServerEvents.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAServerEvents.java#L66-L89) · [WindShieldEffect.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_shield/WindShieldEffect.java#L14-L27).

**QA pendente e fail-closed:** Testar invulnerability/dodge em 1..5, reflexão de projectiles imunes, client-server sides, ataque corpo-a-corpo, friendly fire, summoned breeze e possíveis interações de dodge de outro mod. Os valores são defaults ou constantes, não provas de execução em servidor/cliente. **+0 novas magias; +0 adapters aprovados.**
