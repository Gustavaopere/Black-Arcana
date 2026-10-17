# Wind Charge

**⚠️ Verificação do publisher 2026-10-13:** `aero_additions:wind_charge` e sua classe foram confirmados por `javap` no JAR oficial CurseForge 1.2.8, [Java21 #38431639191](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38431639191). O SHA-1 do arquivo físico instalado **não foi comprovado** (dado histórico de 35 dígitos inválido): esta ficha segue `COUNTED_SOURCE_PINNED`, não `COUNTED_EXACT`; já contabilizada, **+0**. [Provenance/gate](../EXACT-PUBLISHER-SPELLS-1.2.8-PHYSICAL-SHA-BLOCKED.md). Runtime, aquisição e config ⚠️.


- Provider: **SnackPirate's Aeromancy Additions** (`aero_additions`)
- Version: `1.2.8`
- Registry id: `aero_additions:wind_charge`
- Registered class: `WindChargeSpell`
- Provider school: `aero_additions:wind`
- Host registry: **Iron's SpellRegistry**
- Semantic state: `COUNTED_SOURCE_PINNED`
- Strict contribution: `1`

## Identidade semântica

Spell provider-owned ativo no `AASpells` do source pin 1.2.8. A identidade é contada pelo registro ativo do provider, não por nomes de classes, entities, effects ou assets auxiliares.

## Registration evidence

O source pin contém uma chamada ativa `registerSpell(new WindChargeSpell())` para esta identidade. O provider registry é ligado ao event bus sem branch provider-side de configuração que remova este registro.


## Evidence boundary

Esta ficha fecha ID, classe registrada, ownership, escola Wind e estado semântico source-pinned. Mecânica quantitativa, custo, cooldown, acquisition settlement, networking, compatibilidade e comportamento no modpack físico permanecem QA separado quando não explicitamente fechados pelo dossiê.

Source: `../EXACT-1.2.8-SPELL-INVENTORY.md`.

## Engenharia causal para perks — 17/10/2026

**Identidade:** mod ID `aero_additions`, versão `1.2.8`, source fixo `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`. **⚠️ COUNTED_SOURCE_PINNED**: dez registros confirmados em JAR oficial de publicação ([Java 21 #38431639191](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38431639191)), mas SHA-1 do JAR *instalado* na modlist histórica é inválido/incompleto (35 dígitos); **NÃO** promover a COUNTED_EXACT instalada. JAR publisher `aero_additions-1.2.8.jar` SHA-1 `dee32c9fa84a9b3796e39846608f8f77591ea56f`. Todos os números abaixo vêm do source, não de configuração efetiva/QA físico. Iron's governa casting, mana/cooldown; Aero Additions governa efeitos; RPG Skill Tree somente progressão/perks por contrato real.

**Raiz `aero_additions:wind_charge` — Wind Charge.** Source-only; dados de domínio, raio, alvo e duração são mensurados conforme os métodos abaixo, quando aplicáveis.

| Eixo | Observação fonte-fixada | Mutabilidade por perk |
|---|---|---|
| Cast e custos | INSTANT, nível 1–5, cooldown default 1 s; castTime=0, baseMana=20 e +8 por nível; baseSpellPower=10 e +3 por nível (antes dos multiplicadores do caster). | Iron's authority; não instituir custo duplicado. |
| Spawn/direção | Cria um MagicWindCharge por cast em Y do olho menos metade da altura da hitbox; owner caster, direção getLookAngle, velocidade base 1.5 (getSpeed), isNoGravity=true. | Quantidade/velocity/hitbox per-caster ⛔ sem seam. |
| Dano de explosão | Spell passa `charge.damage=0.2×sqrt(getSpellPower)/0.6324555` (aprox `0.31623×sqrt(power)`); MagicWindCharge.explode usa SimpleExplosionDamageCalculator com `1.22×charge.damage` como parâmetro de dano e explosão raio 1.5, `Level.ExplosionInteraction.TRIGGER`. | Não afirmar dano HP exato sem engine/armor; raio de explosão ≠ range de projétil; WorldEffectPolicy BA não controla provider-native. |
| Impacto/tipo | Em hit de entidade chama `entity.hurt(damageSources().windCharge(this,owner),1.0F)` e, se true, pós-efeitos de enchant; então explode. Em hit de bloco explode no server e descarta. Anti-magic também dispara explode + discard. | Hit direto fixo 1.0 e explosão são caminhos distintos; não somar hits/creditar Mastery na emissão. |
| Persistência | Save NBT escreve Damage e Age; read restaura ambos. Caster desconectado/damageSource em reload ainda precisa QA. | Sem hook seguro para escala por player. |

**Localizadores:** [WindChargeSpell.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_charge/WindChargeSpell.java#L22-L84) · [MagicWindCharge.java](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/wind_charge/MagicWindCharge.java#L49-L164).

**QA pendente e fail-closed:** Verificar raio/WorldEffectPolicy no modpack, blockTags WIND_CHARGE_EXPLOSIONS, anti-magic, owner/logout, PvP, impacto direto + explosão e diferenças lado cliente/servidor. Os valores são defaults ou constantes, não provas de execução em servidor/cliente. **+0 novas magias; +0 adapters aprovados.**
