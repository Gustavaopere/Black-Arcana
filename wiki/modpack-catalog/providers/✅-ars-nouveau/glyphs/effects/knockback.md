# Knockback

- Registry ID: `ars_nouveau:glyph_gust`
- Source class: `EffectKnockback`
- Display name: `Knockback`
- School: Elemental Air
- Default tier: **1**
- Default mana: **15**
- Default strength config: **1.5** base + **1.0** per amplification unit
- Exact source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`

## Source-pinned behavior

Knocks entities according to provider caster orientation/position and target knockback resistance. On blocks it can convert affected blocks into Ars enchanted falling-block entities and move them. Sensitive prevents the block-moving path. Extract changes entity knockback direction to be away from the caster rather than following the caster look direction.

Compatible augments: Amplify, Dampen, AOE, Pierce, Sensitive, Extract. Sensitive is limited to 1 by default.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:air_essence` + `minecraft:piston` ×3.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Boundary

Ars owns `glyph_gust` motion/block conversion. Black Arcana movement remains server-validated and block movement remains subject to its own world-safety policy and bounded work.

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME+CONFIG QA PENDING`.

## Engenharia para perks — caminho causal individual

- **Source exato:** [`EffectKnockback.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectKnockback.java), `com.hollingsworth.arsnouveau.common.spell.effect.EffectKnockback` no Ars Nouveau 5.13.1.
- **Registry real:** `ars_nouveau:glyph_gust`, embora a ficha se chame Knockback e a classe seja `EffectKnockback`. Preservar esse ID na documentação/implementação.
- **Magnitude:** `strength=GENERIC_DOUBLE.get()+AMP_VALUE.get()*getAmpMultiplier()` com defaults 1.5 e 1.0. Para LivingEntity, multiplica por `1-KNOCKBACK_RESISTANCE`; se strength<=0 não aplica o impulso. No horizontal usa metade da velocidade atual menos vetor normalizado*strength. No vertical para alvo no chão usa `min(0.4,vy/2+strength)`, senão mantém vy.
- **Direção:** se `AugmentExtract` presente, vetor de `caster.getPosition().subtract(target.position())`; outro branch depende da rotação do `LivingCaster`, `RotatingTurretTile`, `BasicSpellTurretTile` ou `RuneTile`. O cálculo muda por tipo de invocador, portanto não adotar apenas yaw do jogador.
- **Blocos:** Sensitive faz abort; sem Sensitive seleciona AOE/Pierce por `SpellUtil.calcAOEBlocks` e cria `EnchantedFallingBlock.fall`, aplica knockback e `ShapersFocus.tryPropagateEntitySpell` em cada sucesso. Direitos sobre blocos pertencem ao provider; adapter não duplica entidades.
- **Estado:** ✅ classe/fórmulas source-pinned; ⚠️ outcomes downstream, config física e Survival pendentes; ⛔ nenhuma alteração por RPG Skill Tree implementada ou testada. Avaliar a interface `EffectResolveEvent.Pre` per-effect com clamps e causalidade.

## Certificação estática de Effect — 25/10/2026

**✅ Documentação técnico-causal estática completa deste Effect; ⛔ hook de mutação por perks `NOT_VERIFIED`; ⚠️ QA físico/config `NOT_TESTED`.** O ✅ não concede implementação de perk; aplica-se ao source fixo do Ars Nouveau 5.13.1 e identidade binária do glyph, não à equivalência integral dos métodos do JAR instalado.

| Campo para implementação de perks | Prova / fronteira de autoridade |
|---|---|
| ID, versão e classe | `ars_nouveau:glyph_gust`, classe `EffectKnockback`, escola Elemental Air, tier padrão 1. [Implementação em commit exato](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectKnockback.java); [ID/class no JAR SHA-exato](../../EXACT-BINARY-GLYPH-RITUAL-IDS-5.13.1.md). |
| Ação, ramo, consumidor e settlement | `onResolveEntity` calcula `strength=GENERIC_DOUBLE+AMP_VALUE*amp` e aplica `knockback` conforme `IWrappedCaster`; marca `hurtMarked`. Em `onResolveBlock`, `Sensitive` retorna sem mover blocos; caso contrário calcula posições `SpellUtil.calcAOEBlocks` e para cada entidade `EnchantedFallingBlock.fall` não nula aplica impulso e `ShapersFocus.tryPropagateEntitySpell`. |
| Parâmetros/fórmulas/compatibilidade/caps | Config defaults força base 1.5 e amp +1.0; para LivingEntity escala por `(1 - KNOCKBACK_RESISTANCE)` e só executa se `strength>0`. Movimento horizontal aplica `delta/2` menos direção normalizada*strength; eixo vertical no chão `min(0.4,vy/2+strength)`, no ar mantém vy. Com Extract a direção vem do vetor caster→target (subtração source posição do caster menos target); sem Extract deriva rotação do player/turret/rune. Compatíveis Amplify, Dampen, AOE, Pierce, Sensitive, Extract; Sensitive cap default 1. |
| Alvo, área, projétil, tipo de dano e duração | EntityHitResult move entidade alvo por impulso; BlockHitResult pode converter blocos em entidades móveis, caminho com impacto e World mutation. O `glyph_gust` é ID real, não `glyph_knockback`. Não há DamageType ou duração própria comprovados neste glyph; geometry de blocos deriva `SpellUtil.calcAOEBlocks`. |
| Mana, cast, cooldown, aquisição e aprendizado | Mana default 15, tier I, 27 XP recipe `ars_nouveau:air_essence` + `minecraft:piston` ×3. Starter default não. Múltiplos falling blocks/partículas não geram pagamento ou cast separado. [Inventário de acquisition 85/85](../../ACQUISITION.md). |
| Integração e policy | Não supor claim check local na classe nem taxa de spawn bem sucedida para todos os blocos. Não duplicar `EnchantedFallingBlock`, knockback, efeitos de ShapersFocus ou settlement da magia Ars. Ars Novo detém `SpellResolver`, `SpellStats`, custos, targets e resultado; RPG Skill Tree é sibling de progresso/perks, não proprietário de runtime. A existência de API de evento pública do Ars não prova um adapter RPG/Black Arcana seguro. Efeitos independentes Black Arcana têm seu próprio `WorldEffectPolicy`. |
| Evidência e limites | Source `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, JAR publisher Ars 5.13.1 SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` para **identidade registrada**; métodos/consumidores **somente source-pinned**, checksum de instalação corrente e configuração em jogo **não auditados** nesta etapa, gameplay Survival/cliente/servidor `NOT_TESTED`. |

**Fail-closed:** mudança de build/config, hooks efetivos, ordem de eventos e contrapartes de addons precisam de prova antes de mutar mana/alcance/alvo/duração/hitbox ou interpretar FX/estados persistentes como casts extras. Este Effect não aumenta o número de objetos do catálogo — sua ficha já existia.
