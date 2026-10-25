# Heal

- Registry ID: `ars_nouveau:glyph_heal`
- Source class: `EffectHeal`
- School: Abjuration
- Default tier: **2**
- Default mana: **50**
- Default heal config: **3.0** base + **3.0** per amplification unit
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Heals a living target, with randomized stats able to alter the heal amount. Healing a Player causes provider-side food exhaustion. Targets using inverted heal/harm semantics instead receive provider-owned magic damage for the same computed amount.

Compatible augments: Amplify, Dampen, Fortune, Randomize.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:abjuration_essence` + `minecraft:glistering_melon_slice` ×4 + `minecraft:golden_apple`.
- Source-default recipe XP: **55 XP** (Tier II).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars Nouveau owns healing, food exhaustion, undead/inverted-heal damage and configured values. Black Arcana must not create duplicate healing settlement, damage procs or progression awards from the same provider event.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Localizadores e parâmetros para Codex — fonte exata

- **Java:** [`EffectHeal.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectHeal.java) no commit `112920ff774831f204031da75b4c4e73d3765157` correspondente ao catálogo Ars 5.13.1.
- **Alvo:** `onResolveEntity` requer `LivingEntity` válida e `ServerLevel`; ignora removidos ou saúde <=0.
- **Cálculo:** `healVal = GENERIC_DOUBLE.get() + AMP_VALUE.get()*spellStats.getAmpMultiplier()`, defaults configuráveis 3.0 base e 3.0 per amplifier. `Randomize` aplica rolagem somente na branch de cura, após seleção do destino.
- **Alvo de cura invertida:** `isInvertedHealAndHarm` muda para dano de `DamageTypes.MAGIC` via `attemptDamage`; não tratar a magia como heal-only para todas as entidades.
- **Alvo player:** `causeFoodExhaustion(2.5f)` antes de `heal`; custos de fome não podem ser ignorados por perks.
- **Augments:** Amplify, Dampen, Fortune, Randomize. Hook específico para trocar amount/target ainda **não comprovado**; sem duplicar cura/dano.

**Estado:** prova estática de parâmetros por leitura de código; habilidade de mutação por hook externo não verificada. Ars controla composição, execução, mana/Source e configurações; RPG Skill Tree controla perks/Mastery/gates; Black Arcana é autoridade somente de seu runtime próprio. [Padrão universal](../../../../meta/PERK-READY-TECHNICAL-STANDARD.md).

## Certificação estática de Effect — 25/10/2026

**✅ Documentação técnico-causal estática completa deste Effect; ⛔ hook de mutação por perks `NOT_VERIFIED`; ⚠️ QA físico/config `NOT_TESTED`.** O ✅ não concede implementação de perk; aplica-se ao source fixo do Ars Nouveau 5.13.1 e identidade binária do glyph, não à equivalência integral dos métodos do JAR instalado.

| Campo para implementação de perks | Prova / fronteira de autoridade |
|---|---|
| ID, versão e classe | `ars_nouveau:glyph_heal`, classe `EffectHeal`, escola Abjuration, tier padrão 2. [Implementação em commit exato](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectHeal.java); [ID/class no JAR SHA-exato](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Ação, ramo, consumidor e settlement | `onResolveEntity` requer `LivingEntity` e `ServerLevel`, e ignora alvo removido/sem saúde. O cálculo de heal é `GENERIC_DOUBLE.get()+AMP_VALUE.get()*stats.getAmpMultiplier()`. Em target com `isInvertedHealAndHarm()`, chama `attemptDamage` por `DamageTypes.MAGIC` (contrato `IDamageEffect`); em target comum aplica `entity.heal`. Se o **alvo** é `Player`, chama `player.causeFoodExhaustion(2.5f)` antes da cura. **Não assumir que sempre cobra fome do caster**, apesar do texto descritivo upstream. |
| Parâmetros/fórmulas/compatibilidade/caps | Defaults configurados base heal 3.0 e incremento 3.0 por amp; `Randomize` altera a cura não invertida com `randomRolls`, sem duplicar a rolagem em `attemptDamage`. Para dano invertido, o pipeline de dano adiciona modifiers/eventos e pode cancelar; `healVal` não é garantidamente dano liquidado. Compatíveis Amplify, Dampen, Fortune e Randomize. |
| Alvo, área, projétil, tipo de dano e duração | Alvo vivo server-side; ramo cura versus dano invertido, sem área ou projétil próprios e sem duração aplicada pela classe. A Form carrega seleção e delivery. Alteração de target não autoriza duplicar `attemptDamage`, healing ou eventos de XP. |
| Mana, cast, cooldown, aquisição e aprendizado | Mana default 50, tier II, 55 XP recipe default; `ars_nouveau:abjuration_essence` + `minecraft:glistering_melon_slice` ×4 + `minecraft:golden_apple`. O desgaste de fome 2.5 é efeito no alvo Player no ramo de cura, **não** desconto da mana. [Inventário de acquisition 85/85](../../ACQUISITION.md). |
| Integração e policy | Não somar bônus de cura e dano magic como duas resoluções; inversão de heal/harm e eventos Pre/Post precisam preservar deduplicação, cancelamento, atribuição e limites. Ars Novo detém `SpellResolver`, `SpellStats`, custos, targets e resultado; RPG Skill Tree é sibling de progresso/perks, não proprietário de runtime. A existência de API de evento pública do Ars não prova um adapter RPG/Black Arcana seguro. Efeitos independentes Black Arcana têm seu próprio `WorldEffectPolicy`. |
| Evidência e limites | Source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, JAR publisher Ars 5.13.1 SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` para **identidade registrada**; métodos/consumidores **somente source-pinned**, checksum de instalação corrente e configuração em jogo **não auditados** nesta etapa, gameplay Survival/cliente/servidor `NOT_TESTED`. |

**Fail-closed:** mudança de build/config, hooks efetivos, ordem de eventos e contrapartes de addons precisam de prova antes de mutar mana/alcance/alvo/duração/hitbox ou interpretar FX/estados persistentes como casts extras. Este Effect não aumenta o número de objetos do catálogo — sua ficha já existia.
