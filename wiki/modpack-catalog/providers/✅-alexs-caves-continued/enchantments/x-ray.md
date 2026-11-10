# X-Ray — `alexscaves:x_ray` (Alex's Caves Continued 1.0.10)

**Catalogação individual:** ⚠️ **PARCIAL / CONDICIONADA**, baseada em evidências JVM SHA-exatas previamente produzidas para o Raygun. **Contrato técnico estático individual:** `NOT_CERTIFIED`. **Hook mutador:** `NOT_VERIFIED`. **QA física:** `NOT_TESTED`. **Mutação:** `NO_MUTATION` / fail-closed.

> Este dossiê reúne e interpreta provas já presentes na `main`; **não** é uma nova execução independente do JAR nem a certificação integral de X-Ray. Um consumer compartilhado com Raygun ou Gamma Ray não transfere sua certificação ao encantamento.

## Identidade, versão e escopo

- **Provider:** Alex's Caves Continued; **mod ID** `alexscaves`; **recurso de encantamento inventariado:** `alexscaves:x_ray`.
- **Ambiente da modlist:** Minecraft **1.21.1**, NeoForge e Java **21**; artefato físico identificado como `alexscaves-1.0.10-neoforge+1.21.1.jar` (entrada #19 da modlist).
- **JAR publisher examinado nas sondas anteriores:** 75.279.314 bytes; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Consumidor compilado selecionado:** `com/github/alexmodguy/alexscaves/server/item/RaygunItem.class`, SHA-256 `3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c`.
- **Descrição funcional própria, condicionada:** X-Ray altera a seleção de extremos/traçados do Raygun quando seu nível é positivo. As janelas JVM comprovam comutação de caminhos; **a possibilidade efetiva de atingir entidades atrás de blocos, o alcance final e o conjunto completo de alvos ainda não estão certificados**. Não tratar o nome do encantamento como prova de atravessar qualquer obstáculo.
- **Recurso `data/alexscaves/enchantment/x_ray.json`:** a identidade consta no inventário histórico de 51 JSONs publisher. **Bytes individuais, digest, `max_level`, `weight`, `min_cost`, `max_cost`, `anvil_cost`, `slots`, tags de elegibilidade e `exclusive_set`: NÃO VERIFICADOS neste dossiê.** A leitura nominal de `ACEnchantmentRegistry.X_RAY` não comprova esses campos.

## Cadeia compilada e escolhas observadas

O método selecionado é `RaygunItem.onUseTick(Level,LivingEntity,ItemStack,int):void`, descritor JVM `(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;I)V`. A extração anterior registrou **523 instruções** e digest da representação do método `b037276094928625e501d13fddd11829e3fe5540d585f7d8213f37b098c39bc5`. Não é um grafo de fluxo de controle integral, sobretudo para exceções e origens de todas as variáveis.

| Região JVM | Evidência fixada pelo manifesto | Interpretação limitada |
|---|---|---|
| `@35–41` | `25.0f × local7` alimenta `local8` | Valor de distância intermediário; **não** publicar alcance de 25 blocos como contrato final |
| `@44–58` | `getstatic X_RAY @44`, `ACCompat.enchantLevel @47`, `ifle @50→57`; `1` ou `0` armazenado em `local9 @58` | Encantamento **presente com nível > 0** produz flag booleana nessa região; não há escala por nível demonstrada |
| `@69`, `@80` | `ProjectileUtil.getHitResultOnViewVector` e `LivingEntity.pick` recebem operandos derivados de `local8` | Dois traçados de visão; prioridade e oclusão global requerem CFG |
| `@105–120` | `iload 9; ifeq @107→115`: escolhe `local12` ou `HitResult.getLocation()` para `local13` | Dois caminhos para um extremo, com decisão imediata comprovada |
| `@122–137` | `iload 9; ifeq @124→132`: escolhe `local12` ou `HitResult.getLocation()` para `local14` | Segundo extremo condicionado pela mesma flag; sem extrapolar causalidade de todos os usos |
| `@569–669` | `iload 9; ifeq @571→669`; usa `LivingEntity.getBoundingBox`, `AABB.inflate`, `getEyePosition`, `getViewVector` e `ProjectileUtil.getEntityHitResult @640` | Caminho adicional de traçado de entidade sob a flag; **AABB, passo e range finais não certificados** |
| `@595–663` | `local23` float inicia em `1`, é comparado com `local8`, pode avançar por `+1` e saltar de volta a `@595` | Laço selecionado de procura, mas sem provar número de iterações/hits ou todos os caminhos de entrada/saída |
| `@689–721` | `BlockHitResult.getBlockPos`, `Level.getBlockState` e `BlockState.isFaceSturdy` aparecem no consumidor | A interação com a superfície de blocos existe; regras globais de bloqueio/piercing não certificadas |
| `@875–943` | Guarda de `Level.isClientSide` no recorte e `Level.getEntities(source,AABB,Predicate) @943` | Enumeração de alvos no fluxo observado; não transforma resultado de cliente em autoridade de servidor |
| `@978–1008` | `Entity.is`, `Entity.isAlliedTo`, `LivingEntity.isAlliedTo`, `isPassengerOfSameVehicle` precedem o ramo de dano | Não suprimir filtros de self, aliados ou ocupantes do mesmo veículo numa perk |
| `@1026–1044` | `causeRaygunDamage(registryAccess,caster)`; pedido `ACCompat.hurt` com **2.0f ou 1.5f** condicionado por outra flag local | Dano pertence ao caminho Raygun; **não está provado** que X-Ray o aumente, nem que `hurt` seja aceito |
| `@1076–1154` | Guard de `RESISTS_RADIATION`, possível `IRRADIATED` (800 ticks solicitados), pacote visual posterior | Efeito é outro ramo do Raygun/Gamma; nenhum buff/debuff exclusivo de X-Ray comprovado |

**Limites centrais:** `local9` é a flag observada para nível de X-Ray, mas o fluxo inteiro que conecta cada extremidade do raio a dano, entidades finais, obstáculos, callbacks e efeitos depende de reconstrução de CFG/def-use ainda não realizada. Um `ProjectileUtil` ou `AABB` encontrado não define, por si, raio de área, quantidade de hits ou alvo efetivamente atingido.

## Parâmetros operacionais e custos

| Campo exigido para perk | Resultado documentável neste checkpoint |
|---|---|
| Nível e escalonamento X-Ray | **`level > 0`** seleciona o caminho booleano observado; teto de nível e custos de obtenção: **NÃO VERIFICADOS** |
| Range, LOS, atravessamento de bloco | `25.0f × local7` e traçados distintos observados; **alcance efetivo, barreiras e LoS: NÃO CERTIFICADOS** |
| AOE, targeting, filtros e alvos máximos | AABB/predicados, `getEntityHitResult`, `getEntities` e exclusões observados; **volume numérico final, múltiplos hits e seleção completa: NÃO CERTIFICADOS** |
| Dano/tipo e críticos | Factory `alexscaves:raygun` e valores **1.5f/2.0f** em ramo compartilhado; **dano extra de X-Ray, críticos, aceitação e mitigação: NÃO VERIFICADOS** |
| Projétil, velocidade, tamanho, homing | Nenhuma entidade nova identificada diretamente nas janelas selecionadas de `onUseTick`; ausência universal de spawn indireto: **NÃO VERIFICADA** |
| Duração e cooldown | `RaygunItem.getUseDuration = 72000` ticks, limite declarativo da arma, **não** duração/cooldown de X-Ray; cooldown X-Ray: **NÃO VERIFICADO** |
| Carga, munição e desgaste | `RaygunItem.hasCharge` consulta `ChargeUsed < 1000`; recarga nativa usa `URANIUM_ROD` e ramo `ItemStack.shrink(1)`. Consumo por tick, redução por `ENERGY_EFFICIENCY` e custo adicional de X-Ray: **NÃO VERIFICADOS** |
| Persistência e replicação | `ChargeUsed`, `UseTime`, `PrevUseTime` e mensagem `UpdateItemTagMessage` identificados no Raygun; ownership/validação, save/reload e sincronização efetiva: **NÃO VERIFICADOS** |
| Autoria e XP/Mastery | O caster alimenta a factory de `DamageSource` na janela de dano; kill credit, XP, deduplicação e regras PvP: **NÃO VERIFICADOS** |

## Dependências de consumo e boundaries

- [Ficha parcial do Raygun](../damage-types/raygun.md): comportamento compartilhado de charge, payload C2S, filtro de entidade, dano/status e limites de autoridade.
- [Gamma Ray](gamma-ray.md) e [Energy Efficiency](energy-efficiency.md) permanecem **objetos separados**: flags, custo, dano e `Irradiated` não podem ser atribuídos automaticamente a X-Ray.
- O Raygun é **provider-native**; Black Arcana não assume sua execução, criação do `DamageSource`, custo ou seleção de alvo. RPG Skill Tree controla progressão/perks/Mastery por contratos reais. **Não existe hook mutador seguro confirmado para X-Ray neste checkpoint.**
- Futuras perks poderiam *conceitualmente* mudar distância efetiva, predicados de entidade, custo/charge ou permeabilidade a obstáculos, **somente** após identificar e validar um seam real com authority server-side, segurança PvP/claims e deduplicação de hits/custos/XP. **`NO_MUTATION`**.

## Provas reproduzíveis herdadas e pendências

**Fonte física previamente auditada, sem execução nova nesta entrega:**

- [Manifesto JVM de X-Ray e targeting](../EXACT-RAYGUN-XRAY-TARGET-1.0.10.json): hash do JAR e da classe, descritor/digest de `onUseTick`, seis janelas e seus offsets.
- [Ramos condicionais X-Ray/Gamma](../EXACT-RAYGUN-CONDITION-BRANCHES-1.0.10.json): seleção de `local9` e usos imediatos de `@105`, `@122`, `@569`.
- [Consumidores de branches](../EXACT-RAYGUN-BRANCH-CONSUMERS-1.0.10.json): `@569–669`, laço por `local23`, traçados, efeitos e limites de CFG.
- [Controle do Raygun](../EXACT-RAYGUN-CONTROL-1.0.10.json): referências de classe, custo, parâmetros e fingerprints selecionados.
- [Crosswalk dos 51 recursos publisher](../ENCHANTMENT-PERK-CROSSWALK-1.0.10.md): identidade `alexscaves:x_ray` e separação entre universo de JSON e fichas certificadas.
- [Sonda de X-Ray no GitHub Actions](../../../../../.github/workflows/alexscaves-1010-raygun-xray-target.yml) e [workflow de consumidores](../../../../../.github/workflows/alexscaves-1010-raygun-branch-consumers.yml), quando presentes na `main`. A existência desses arquivos não demonstra, por si, que a revisão atual executou as sondas.

**Para elevar a ✅ estática:** (1) selar o JSON individual exato, tags/slots/custos/níveis/exclusões e suas hashes; (2) cobrir integralmente as definições/uso das variáveis e o CFG de `onUseTick` incluindo caminhos de bloco, entidade e erro; (3) fechar range, LOS, AABB, quantidade de hits, persistência/autoria e todos os consumidores X-Ray, separando Raygun/Gamma; (4) produzir testes semânticos negativos e manifesto individual SHA-exato do JAR 1.0.10; (5) repetir as verificações e validar índices antes de certificar. **QA física permanece independente:** níveis, obstáculos e diferentes entidades, servidores dedicados, multiplayer, PvP, claims, troca de mãos, reuso de stack, save/reload e configs/datapacks.

**Estado final desta ficha:** ⚠️ documentação técnica individual parcial; `contract_static=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. Nenhuma nova raiz de cast, código de perk ou runtime alterado.
