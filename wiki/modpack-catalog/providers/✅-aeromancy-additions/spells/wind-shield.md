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

Estado documental: `documentary=SOURCE_PINNED`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; identidade instalada **NOT_VERIFIED**; certificação **0**. [Contrato comum](../SOURCE-CONTRACTS-1.2.8.md) · [manifesto](../SOURCE-CATALOG-MANIFEST-1.2.8.json) · [fechamento](../SOURCE-CATALOG-CLOSURE-1.2.8.md).

Esta ficha fecha ID, classe registrada, ownership, escola Wind e estado semântico source-pinned. Mecânica quantitativa, custo, cooldown, acquisition settlement, networking, compatibilidade e comportamento no modpack físico permanecem QA separado quando não explicitamente fechados pelo dossiê.

Source: `../EXACT-1.2.8-SPELL-INVENTORY.md`.

## Engenharia causal para perks — 17/10/2026

**Identidade:** mod ID `aero_additions`, versão `1.2.8`, source fixo `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`. **⚠️ COUNTED_SOURCE_PINNED**: dez registros confirmados em JAR oficial de publicação ([Java 21 #38431639191](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38431639191)), mas SHA-1 do JAR *instalado* na modlist histórica é inválido/incompleto (35 dígitos); **NÃO** promover a COUNTED_EXACT instalada. JAR publisher `aero_additions-1.2.8.jar` SHA-1 `dee32c9fa84a9b3796e39846608f8f77591ea56f`. Todos os números abaixo vêm do source, não de configuração efetiva/QA físico. Iron's governa casting, mana/cooldown; Aero Additions governa efeitos; RPG Skill Tree somente progressão/perks por contrato real.

**Raiz `aero_additions:wind_shield` — Wind Shield.** Source-only; dados de domínio, raio, alvo e duração são mensurados conforme os métodos abaixo, quando aplicáveis.

Os pares **base/per-level** abaixo são campos literais entregues a `AbstractSpell`; não significam `base + per-level×level`. Avaliação de nível, atributos/config e custo/cooldown efetivo pertencem ao host.

| Eixo | Observação fonte-fixada | Mutabilidade por perk |
|---|---|---|
| Cast/stats | LONG, níveis 1–5, cooldown 140s, castTime 60, mana base/per-level **130/30**, power base/per-level **30/8**; durationSeconds = `10+5×level+(int)sqrt(10×spellPower)`. | Duração depende do power do caster, não somente spellLevel. |
| Dodge nativo | `AASpells.MobEffects.WIND_SHIELD` registra `IronsLibRegistries.AttributeRegistry.DODGE_CHANCE`, modifier `aero_additions:wind_shield_dodge`, base **+0.03 ADD_VALUE**. O produtor usa amplifier `level−1`; com escala de `MobEffect` Minecraft 1.21.1, o modifier nominal é **+0.03/+0.06/+0.09/+0.12/+0.15**. | A definição existe no source. [Escala do host](../SOURCE-CONTRACTS-1.2.8.md#host-minecraft-1211); settlement/stacking de dodge pertence ao IronsLib e não foi certificado. |
| Chance de reflexão | WindShieldSpell.chanceToDeflect(amplifier)=0.3+amplifier/10f. Níveis 1–5 resultam em chances nominais **30%,40%,50%,60%,70%** por evento elegível, sem clamp local. | Reflexão de projétil e atributo de dodge são mecanismos separados; não somar probabilidades nem equiparar ao dano evitado. |
| Evento de deflexão | AAServerEvents.windShieldDeflection em ProjectileImpactEvent, quando EntityHitResult de LivingEntity com effect e projectile fora de AAEntityTypeTags.REFLECTION_IMMUNE, sorteia, cancela evento e chama Projectile.deflect(REVERSE,...). O `else if` de SUMMONED_BREEZE usa o summoner como owner, sem repetir o filtro de imunidade. Breeze com efeito/projétil elegível entra no primeiro ramo e não recebe fallback se o sorteio falhar. | Cancelar impacto não prova dano evitado em todos os pipelines; deflect pode ter política própria da entidade/host. O summon está registrado como entidade, mas sua magia produtora está inativa. |
| Hitbox/range | Somente o alvo com efeito no EntityHitResult; sem aura de área ou raio per-caster. OnCast aplica status self. | ⛔ aumento de área, shield for all/allies ou target retarget sem contract. |
| Sync | WindShieldEffect apenas repassa add/removal callbacks; flags de efeito locais estão comentadas no arquivo, não são APIs em produção. | QA dedicated/client, authority e C2S. |

**Localizadores:** [WindShieldSpell.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_shield/WindShieldSpell.java#L19-L73) · [AASpells.java — dodge L150–153](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L150-L153) · [AAServerEvents.java — ramos completos L68–90](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/AAServerEvents.java#L68-L90) · [WindShieldEffect.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_shield/WindShieldEffect.java#L14-L27).

**QA pendente e fail-closed:** Testar invulnerability/dodge em 1..5, reflexão de projectiles imunes, client-server sides, ataque corpo-a-corpo, friendly fire, summoned breeze e possíveis interações de dodge de outro mod. Os valores são defaults ou constantes, não provas de execução em servidor/cliente. **+0 novas magias; +0 adapters aprovados.**

## Contratos de suporte — 28/10/2026

Registro ativo e vínculo ao event bus: [AASpells.java L53–78](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L53-L78). Consumidores documentados: [Wind Shielded](../effects/wind-shield.md) e [tags de reflexão](../data-contracts/entity-type-tags.md). Auxiliares não criam raízes adicionais: esta ficha preserva contribuição estrita **1**, enriquecimento **+0**.
