# Gamma Ray — dano, radiação e feedback da Raygun (Alex's Caves Continued 1.0.10)

**Estado:** ⚠️ ficha individual **parcial/condicionada**. Reúne evidências de bytecode já verificadas no **JAR publisher SHA-exato 1.0.10** para o consumidor `RaygunItem.onUseTick`, sem alegar um novo fechamento de CFG, extração individual do JSON deste encantamento, autorização de alteração do comportamento ou QA física. `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED` · `mutation=NO_MUTATION`.

**Definição:** `alexscaves:gamma_ray` é um encantamento nativo da Raygun, não uma magia/cast criado pelo Black Arcana. A classe compilada consulta seu nível para selecionar variantes de dano solicitado, intensidade do efeito *Irradiated* e feedback visual. Dano, seleção de alvos, consumo de carga, atribuição e status permanecem sob a autoridade do provider.

## 1. Identidade e fontes de autoridade

| Campo | Estado observado |
|---|---|
| Mod instalado | Alex's Caves Continued, mod ID `alexscaves`, versão `1.0.10`; [modlist física sibling](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/main/PROJECT-INSTRUCTIONS/modlist/modlist.md), entrada 019 |
| Plataforma | Minecraft 1.21.1, NeoForge, Java 21 |
| JAR exato já selado | `alexscaves-1.0.10-neoforge+1.21.1.jar`; 75.279.314 bytes; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| Identidade | `alexscaves:gamma_ray`, listada entre os 51 nomes do [inventário publisher](../INTEGRATION-SCOPE-INVENTORY-1.0.10.json); símbolo `ACEnchantmentRegistry.GAMMA_RAY` observado no consumer |
| Consumer compilado | `com/github/alexmodguy/alexscaves/server/item/RaygunItem.class`, SHA-256 `3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c` |
| Método principal | `onUseTick(Level,LivingEntity,ItemStack,int):void`; descritor `(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;I)V` |
| Digest do método compilado | `b037276094928625e501d13fddd11829e3fe5540d585f7d8213f37b098c39bc5` (523 instruções extraídas na auditoria de branches) |
| JSON individual do encantamento | **Pendente de extração e selagem individual**. Não atribuir `max_level`, `weight`, `exclusive_set`, `supported_items` ou custos de mesa/anvil à versão 1.0.10 com base apenas na wiki ou em fonte 1.1.1. |

**Prova já existente:** [controle e constantes](../EXACT-RAYGUN-CONTROL-1.0.10.json), [branches de X-Ray e Gamma Ray](../EXACT-RAYGUN-CONDITION-BRANCHES-1.0.10.json), [consumidores de branches](../EXACT-RAYGUN-BRANCH-CONSUMERS-1.0.10.json), [guardas de radiação](../EXACT-RAYGUN-RADIATION-GUARDS-1.0.10.json) e [ficha Raygun](../damage-types/raygun.md). Esta ficha **reutiliza** esses manifestos e não afirma que eles sejam uma auditoria integral de `gamma_ray.json`.

A [wiki comunitária da Raygun](https://alexscaves.wiki.gg/wiki/Raygun#Enchantments) descreve o encantamento, suas cores e a incompatibilidade com X-Ray. É fonte de comportamento de referência; **não** substitui a definição JSON ou os classfiles exatos do publisher 1.0.10. A fonte pública `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara versão 1.1.1 e não constitui autoridade numérica para esta versão.

## 2. Parâmetros e branches compilados

O método `RaygunItem.onUseTick` consulta `ACCompat.enchantLevel(stack, GAMMA_RAY)` em `@332–338`. O resultado condicional é armazenado em um inteiro do slot JVM 18 (`istore @346`); as janelas posteriores o testam por `iload` seguido de `ifeq`. A leitura de slot, isoladamente, não é prova de atribuição única em todos os caminhos do CFG.

| Seleção compilada 1.0.10 | Operand(os) / resultado solicitado | Limite de prova |
|---|---|---|
| `slot 18 @367 → ifeq @369` | Ramo de partículas `BLUE_RAYGUN_EXPLOSION` | Variante visual selecionada; não é novo projétil nem dano |
| `slot 18 @402 → ifeq @404` | Ramo visual `BLUE_HAZMAT_BREATHE` | Efeito visual condicionado; não certifica hit |
| `slot 18 @922 → ifeq @924` | `iconst_4` / `iconst_0` guardados como `int slot 23 @932` | Amplifier do status, não quantidade de alvos |
| `slot 18 @1029 → ifeq @1031` | `2.0f` quando não zero; `1.5f` quando zero, antes de `ACCompat.hurt @1041` | **Dano solicitado**, não dano efetivamente aceito, mitigado ou aplicado por tick |
| `slot 18 @1138 → ifeq @1140` | `4` / `0` no payload visual | Dados de mensagem, não uma segunda aplicação do status |

**Radiação:** o consumer passa `sipush 800 @1111` e `iload 23 @1114` a `MobEffectInstance.<init>(Holder,int,int) @1116` e chama `LivingEntity.addEffect @1119`. Assim, a solicitação observada usa **800 ticks** e amplifier **4** no ramo Gamma, versus **0** no alternativo; na nomenclatura do jogo, amplifier 4 corresponde a *Irradiated V*, e 0 a *Irradiated I*. **Não** significa aplicação garantida a todos os alvos.

**Guarda do provider:** o método testa `ACTagRegistry.RESISTS_RADIATION @1082` e `Holder$Reference.is(TagKey) @1085`; o salto `ifne @1088` evita a solicitação nativa de status no ramo resistente. Após `addEffect`, `ifeq @1122` condiciona também o caminho visual `UpdateEffectVisualityEntityMessage.<init>(IIII) @1151` / `sendMSGToAll @1154`. O estado final depende do alvo, da tag resolvida em execução, da aceitação da chamada e do contexto do servidor.

## 3. Geometria, targeting, custo e causalidade

**Range e seleção de alvos.** O consumidor tem o produto compilado `25.0f × local float 7` (`@35–41`) e usa a distância calculada em `ProjectileUtil.getHitResultOnViewVector @69` e `LivingEntity.pick @80`. O ramo de `X_RAY` controla seleções adicionais em `@105/@122/@569`, inclusive `ProjectileUtil.getEntityHitResult @640`. A região de dano inclui `Level.getEntities @943`, exclusões `isAlliedTo` e `isPassengerOfSameVehicle`, e um ramo específico para `TremorzillaEntity`. **Nenhum desses fragmentos certifica que Gamma Ray amplia alcance, transforma a busca em AoE, altera line-of-sight ou permite atravessar proteção de território**. A expressão de 25 unidades tampouco é distância final garantida.

**Dano e autoria.** O caminho de dano referencia `ACDamageTypes.causeRaygunDamage(registryAccess,caster) @1026`, solicita `ACCompat.hurt @1041` e testa o retorno em `@1044`. O dono da fonte de dano, filtros de aliados, mitigação e evento de acerto devem permanecer nativos. Não criar um segundo `hurt`, nova fonte de dano, proc de Mastery ou callback de cast só porque o encantamento selecionou `2.0f`.

**Energia e duração.** `RaygunItem` mantém `ChargeUsed`, `hasCharge` com limite observado `1000`, e consulta `ENERGY_EFFICIENCY` separadamente em `onUseTick @246`. A recarga e sua munição nativa fazem parte do contrato da Raygun. Não atribuir a Gamma Ray economia de carga, custo extra, cadência fixa de dano, cooldown próprio ou número de raios sem dataflow e testes adicionais.

**Compatibilidade.** A wiki comunitária menciona exclusividade com `X_RAY`; a exclusão precisa ser comprovada no JSON/datapack de 1.0.10 e na registry resolvida antes de ser aplicada como gate de perks. A seleção `GAMMA_RAY` e `X_RAY` no mesmo consumer não autoriza presumir coexistência legal nem incompatibilidade no runtime.

## 4. Implicações para perks e lacunas

Campos potencialmente relevantes para planejamento: `damage_request_amount` (1.5f/2.0f), `effect_duration_request_ticks` (800), `effect_amplifier_request` (0/4), `visual_variant`, `target_selection`, `resistance_tag`, `charge_state` e `native_damage_source`. São **pontos de observação**, não parâmetros expostos por API ou mutadores aprovados.

Qualquer futura alteração de dano, amplitude, duração, range, cor, cadência ou multialvo exige demonstração de hook suportado e ajuste com limites explícitos, deduplicação causal, autorização server-side, proteção PvP/claims, imutabilidade de custos nativos e validação no modpack. O RPG Skill Tree só pode fornecer perks/gates por um contrato real; Black Arcana não assume a Raygun nem duplica o seu pipeline.

**Pendente para ficha integral:** extrair e selar `data/alexscaves/enchantment/gamma_ray.json` (campos, SHA-256 e eventual `exclusive_set`/tag); rastrear completamente a origem e o destino do slot 18, os gates de hit e consumo, a compatibilidade com X-Ray e a autorização dos efeitos; mapear hooks realmente acessíveis; testar em cliente/servidor, multiplayer, resistência à radiação, PvP, claims, datapacks, troca de item, recarga e reload. Sem essas provas, **⚠️ parcial/condicionado**, nunca ✅ `COMPLETE_PERK_READY`.

**Escopo de alteração nesta revisão:** documentação e índices, sem cópia de implementação do provider, nenhuma mudança em runtime/Stage, nenhum hook, nenhum cast ou nova raiz mágica.
