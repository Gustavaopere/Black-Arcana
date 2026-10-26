# Ars Nouveau — Cut

Status: `SOURCE-PINNED 5.13.1 / SEMANTICS+ACQUISITION AUDITED / RUNTIME CONFIG QA PENDING`

- Registry id: `ars_nouveau:glyph_cut`
- Display name: Cut
- School: Manipulation
- Default tier: 1
- Default mana cost: 0
- Compatible augments: Extract, Fortune, Amplify, Dampen
- Default Amplify limit: 2
- Source default base damage: 1
- Source default Amplify scalar: +1 damage

## Provider-native behavior

Cut simulates shears on shearable entities/blocks. Against non-shearable entities it deals small spell damage. Amplify changes block interaction to an axe-like strip/use path; Extract/Fortune apply tool enchantment semantics where supported. The source includes explicit duplicate-prevention checks around item-handler/container block entities before fake-player tool interaction.

## Acquisition / learning

- Provider-generated Glyph recipe: `ars_nouveau:manipulation_essence` + `minecraft:shears` + `minecraft:iron_sword`.
- Source-default recipe XP: **27 XP** (Tier I).
- Starter default: **no**.
- Learning is Ars-owned and consumes the Glyph in survival after a successful server-side unlock; runtime config may change enabled/starter/tier behavior.
- Full 85/85 acquisition table: [`ACQUISITION.md`](../../ACQUISITION.md).

## Authority / deduplication

Ars Nouveau owns this magical shearing/stripping utility. Black Arcana should not add a generic duplicate zero-cost cutting/shearing spell or double-spawn shear drops.

Source checkpoint: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157` (`EffectCut`).

## Engenharia de perks — evidência de execução individual

- **Classe versionada:** [`EffectCut.java`](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectCut.java) no Ars Nouveau 5.13.1.
- **Alvo vivo:** se é `IShearable`, usa `isShearable/onSheared` com shears e lança os itens retornados; demais entidades recebem `IDamageEffect.attemptDamage` com dano `DAMAGE.get()+AMP_VALUE.get()*getAmpMultiplier()`, defaults 1.0 e 1.0.
- **Blocos:** usa `SpellUtil.calcAOEBlocks` mas `getCompatibleAugments` inclui somente Extract, Fortune, Amplify e Dampen; Amplify count >0 aciona `doStrip` (diamond axe), senão `doShear` (shears). `dupeCheck` recusa block entities com capability `ItemHandler.BLOCK` ou `Container` para interação por fake player. **Aviso de fonte:** há comentários TODO sobre Fortune em shear; não afirmar bônus concluído em todas as superfícies.
- **Perks:** dano e extração não são mesmo resultado; nenhuma dupla geração de drops por callback externo.
- **Status:** ✅ code pin/identidade; ⚠️ downstream, config e Survival pendentes; mutação por RPG perk só pode ocorrer via [eventos reais](../../VERIFIED-EVENT-SURFACES-5.13.1.md) e adapter validado, não por inferência temática.

## Certificação técnica estática — Cut (25/10/2026)

**✅ `STATIC_TECHNICAL_CATALOG_ONLY` · ⛔ `mutating_hook=NOT_VERIFIED` · ⚠️ `physical_qa=NOT_TESTED`.** Publisher `ars_nouveau-1.21.1-5.13.1.jar` SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd` fixa classe/ID `EffectCut` ↔ `ars_nouveau:glyph_cut`, sem comprovar equivalência dos métodos compilados. Fonte imutável `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`: [EffectCut.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectCut.java), [SpellUtil.java](https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/SpellUtil.java).

| Eixo de perk | Contrato da execução no source e riscos |
|---|---|
| Seleção e dano | `onResolveEntity` separa `entity instanceof IShearable` do ramo ofensivo. Quando é `IShearable`, gera `Items.SHEARS`, aplica `applyEnchantments`, exige `isShearable` e coleta drops de `onSheared` para `world.addFreshEntity(new ItemEntity(...))`. Caso contrário usa `IDamageEffect.attemptDamage` com `damage=DAMAGE.get()+AMP_VALUE.get()*spellStats.getAmpMultiplier()`, defaults `DAMAGE=1.0` e `AMP_VALUE=1.0`. `canDamage` também exclui todo `IShearable`. Não tratar shear como dano/kill; não contar HP reduzido como garantido após `attemptDamage`. |
| AOE/Pierce e augments | `onResolveBlock` itera `SpellUtil.calcAOEBlocks(...,getAoeMultiplier(),count(AugmentPierce))`, porém `getCompatibleAugments` da classe lista **somente** `AugmentExtract`, `AugmentFortune`, `AugmentAmplify`, `AugmentDampen`. Assim, `AOE/Pierce` são parâmetros **consumidos no helper**, não augments autorizados diretamente para o glyph; a origem/compatibilidade de qualquer bônus externo depende do resolver/config. Amplify com `getBuffCount(AugmentAmplify)>0` muda o modo para `doStrip` (`Items.DIAMOND_AXE`); sem Amplify chama `doShear` (`Items.SHEARS`). Amplify default max 2. |
| Bloqueio de inventário | `dupeCheck(world,p)` só retorna true para `BlockEntity` com `Capabilities.ItemHandler.BLOCK` não nulo ou `be instanceof Container`. Em `doStrip` aplica `dupeCheck` **antes** das interações fake-player; em `doShear`, o ramo `IShearable` executa `onSheared` e spawn dos drops **antes** de `dupeCheck`; depois simula `BlockState.useItemOn` e `axe/shears.useOn` mediante `ANFakePlayer`. Portanto essa barreira impede interações simuladas em certos containers, **não garante bloquear shear inicial** em todo bloco com inventário. |
| Mutação e observabilidade | O bloco `doShear` pode ter **dois caminhos consecutivos** de atuação: interface `IShearable.onSheared` seguida de tool-use vanilla/provider. `doStrip` também chama `useItemOn` seguido de `axe.useOn`, sem verificar `InteractionResult` ou outro retorno antes da segunda chamada. Não assumir unicidade de drops ou stripping, nem um único callback causal por posição sem QA de provider e blocos modded. |
| Fortune/Extract e custos | `applyEnchantments` prepara stack de ferramenta; comentários `TODO: restore fortune bonus on augment` aparecem nos ramos `onSheared`, portanto não certificar Fortune nas espécies/blocos shearable só por estar em `getCompatibleAugments`. `getDefaultManaCost()=0` é default, **não prova ausência de custo total de cast, cooldown ou gate carregado**; o resolver Ars possui autoridade de mana/cast. Sem método de dano de bloco próprio, seu `WorldEffectPolicy` do Black Arcana não intercepta automaticamente a tool-use Ars. |
| Integração | Black Arcana mantém `WorldEffectPolicy` para world effects próprios; RPG Skill Tree é sibling de Mastery/perks/atributos/gates apenas mediante adapter verificado. Cut não autoriza reproduzir shear, dano, drops ou `useOn` por perk sem budget e deduplicação. |

**QA pendente:** handler fake player, `dupeCheck` em blocos com e sem capabilities, proteção/claims para `onSheared` e tool-use, Fortune efetivo, mods `IShearable`, respostas de `useItemOn`/`useOn`, lado de execução, configs de dano/mana e multiplayer. `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`. Não promover Stage 06.05 ou 09.
