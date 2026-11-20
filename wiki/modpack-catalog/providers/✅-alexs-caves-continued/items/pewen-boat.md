# Pewen Boat — recurso `alexscaves:pewen_boat`

**Catálogo:** ⚠️ ficha individual detectada, contrato técnico estático `PARTIAL`; hook `NOT_VERIFIED`; QA física `NOT_TESTED`; `NO_MUTATION`. Objeto utilitário de transporte, **não** raiz de magia ou feitiço independente.

## 1. Identidade e versão
- Nome: Pewen Boat; resource ID `alexscaves:pewen_boat`; provider Alex's Caves Continued, `alexscaves` 1.0.10, Minecraft 1.21.1, NeoForge 21.1.250 no último snapshot documental e Java 21.
- Fonte física publisher: `alexscaves-1.0.10-neoforge+1.21.1.jar`, 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. A paridade com novo dump instalado não foi verificada.
- Factory exata `ACItemRegistry.lambda$static$25()Item`, Code SHA-256 `bdcdd27b8688b4c77b965a94ae39cde059587468e45dcc27f4329ee79552537c`: `new CaveBoatItem(false, PEWEN, Item.Properties.stacksTo(1))`. A enum `PEWEN` usa ordinal 0. A factory ativa o caminho de embarcação convencional.
- Classe compartilhada `CaveBoatItem`, SHA-256 `92fc0840e49f71306bbcafbd3e5f4f5814acbf87846846430007310a2577c18d`; caminho `com/github/alexmodguy/alexscaves/server/item/CaveBoatItem`. Grafo e método completo em [auditoria causal comum](../EXACT-CAVE-BOAT-CAUSAL-1.0.10.md).

## 2. Descrição e ativação
Item que solicita colocar uma embarcação de transporte herdada de Boat no ponto atingido pelo raio de visão do usuário. Descrição funcional produzida da auditoria, não transcrição de tooltip oficial. `use(Level,Player,InteractionHand)` usa a mão corrente e `ClipContext.Fluid.ANY`; MISS, uma obstrução envolvendo o olho do jogador ou hit não-BLOCK retornam PASS; colisão de bounding box retorna FAIL. A seleção de possíveis obstruções percorre `AABB.expandTowards(viewVector*5.0).inflate(1.0)`, com predicado sem espectadores e apenas entidades pickable. **Não inferir alcance final da colocação nem AOE desse envelope.**

## 3. Efeito, custo e consumidores
- Em BLOCK sem colisão: `new AlexsCavesBoatEntity(level,hitPos,PEWEN)`, `setYRot(player.getYRot())`; no servidor solicita `addFreshEntity` **sem verificar o Boolean de sucesso**, `GameEvent.ENTITY_PLACE` e `shrink(1)` se o usuário não possui `instabuild`; depois solicita estatística de uso e `useSidedSuccess`. O consumo é solicitado mesmo quando o retorno de spawn indica falha, desde que o código alcance esse ramo.
- Entidade concreta `AlexsCavesBoatEntity`: herda Boat e resolve drops com getDropSupplier; recebe tipo customizado `PEWEN` por `DATA_ID_TYPE` sincronizado. O construtor usa `ACEntityRegistry.BOAT`; execução real, ciclo de passageiros, controle e conteúdo do baú são herdados e NÃO VERIFICADOS.
- Custo inventarial direto: stack máxima 1 e débito solicitado de 1 item em Survival no ramo de colocação. Sem mana, cooldown, níveis ou dano direto no corpo do item: **N/A local**; modos de jogo, efeitos herdados, claims, PvP e alterações externas NÃO VERIFICADOS.

## 4. Aquisição/receita
Recurso publisher `data/alexscaves/recipe/pewen_boat.json` com SHA-256 `64f7a3e16af2501636904a74c9e79c8cf07ddb4fd89885d388c4207bed6e3e4a`, tipo `minecraft:crafting_shaped` e ingredientes identificados `alexscaves:pewen_planks`; output ID `alexscaves:pewen_boat`. Quantidade exata de tábuas no shaped recipe, receitas adicionadas por datapacks, critérios de desbloqueio e acesso Survival no pack: **NÃO VERIFICADOS**.

## 5. Estado, persistência, queda e drops
- `AlexsCavesBoatEntity` salva o campo nativo `ACBoatType` no override próprio de `addAdditionalSaveData` e o restaura com `Type.byName` se presente. Ambos os overrides locais não invocam explicitamente a superclasse. A sequência de persistência/slot de armazenamento herdado não foi testada após restart; não inferir perda ou segurança de inventário sem teste.
- `getVariant()` fornece `Boat.Type.OAK` e `setVariant(Boat.Type)` é no-op neste classfile; o tipo PEWEN/THORNWOOD é gerido separadamente por `getACBoatType` e `setACBoatType`. Tipo inválido por nome/ordinal cai no enum inicial PEWEN no corpo local.
- No caminho da queda em solo (`fallDistance>3.0F`, `Boat.Status.ON_LAND`, servidor, não removido e game rule `RULE_DOENTITYDROPS`), a entidade solicita três tábuas do fornecedor da enum e dois `Items.STICK`, após solicitar dano por queda e `kill()`. O enum PEWEN usa `PEWEN_PLANKS` no `plankSupplier`. A concessão dos drops continua condicionada ao caminho de queda, gamerule e engine. O retorno das tentativas de dano/drops não demonstra resultado aceito.

## 6. Integração, validação e pendências
Esta ficha referencia [manifesto SHA-exato](../EXACT-CAVE-BOAT-DISCOVERY-1.0.10.json) e [contrato causal comum](../EXACT-CAVE-BOAT-CAUSAL-1.0.10.md). Candidatos **somente conceituais** a perks: custo de item, tipos, física, drops e armazenamento. Nenhum hook/ABI mutador seguro foi certificado; manter `NO_MUTATION` e não duplicar spawn, consumo, inventário ou premiação por tentativa. Faltam confirmação de registry runtime, receita integral, hitbox/raycast efetivos, persistência+reconexão, escolha de alvo, permissões, claims, colisão, efeitos reais e QA do modpack/servidor. Evidência estática não fecha o universo do provider.
