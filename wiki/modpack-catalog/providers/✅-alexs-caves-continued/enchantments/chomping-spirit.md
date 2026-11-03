# Chomping Spirit — dano do espírito Tremorsaurus da Extinction Spear (1.0.10)

**Estado:** ⚠️ ficha individual técnica **parcial/condicionada** baseada no JAR publisher SHA-exato, no manifesto previamente integrado de Spirit Dinosaur e no JSON cuja igualdade byte a byte foi confirmada pelo SHA-256. `NO_MUTATION` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED`. Não há homologação de uma perk que altere a entidade, o dano, a área ou o fluxo de ataque.

O encantamento **não constitui um novo feitiço ou cast**. É um modificador consumido pela ação nativa de **acerto corpo a corpo com a Extinction Spear**: transfere seu nível a um `DinosaurSpiritEntity` de tipo `TREMORSAURUS`. O ataque do espírito pode solicitar dano `alexscaves:spirit_dinosaur`. Não confundir essa variante com os espíritos `SUBTERRANODON` (lançamento/impacto, `plummeting_flight`) e `GROTTOCERATOPS` (`herd_phalanx`, uso sustentado). A [ficha raiz já certificada](../damage-types/spirit-dinosaur.md) documenta a causalidade comum e deve ser reutilizada, sem contabilizar três novos casts.

## 1. Identidade e proveniência

- **Provider:** Alex's Caves Continued, `alexscaves`; Minecraft **1.21.1**, NeoForge.
- **Identidade:** `alexscaves:chomping_spirit`; chave `enchantment.alexscaves.chomping_spirit`.
- **Publisher físico:** `alexscaves-1.0.10-neoforge+1.21.1.jar`, **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Manifesto binário reutilizado:** [EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json](../EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json); nele, o `data/alexscaves/enchantment/chomping_spirit.json` físico tem SHA-256 **`f0fb73c3e1c564831375009736264848190a6a6edd126b36bb3802ff356fa6e7`**.
- **Verificação adicional de conteúdo:** o JSON público do [commit fonte fixado](https://github.com/Codx-org/AlexsCavesContinued/blob/523308608422ab8e31974befa7111ecdf495dd37/src/main/resources/data/alexscaves/enchantment/chomping_spirit.json) tem **372 bytes** e SHA-256 **`f0fb73c3e1c564831375009736264848190a6a6edd126b36bb3802ff356fa6e7`**, idêntico ao hash do membro do JAR 1.0.10 já selado. Portanto, **somente o conteúdo deste recurso específico** pode ser tratado como byte-idêntico; a árvore fonte adjacente declara versão **1.1.1** e não certifica os outros métodos da versão 1.0.10.
- **Limite clean-room:** descrição original própria, sem incorporar classes, trechos de código, assets ou efeitos proprietários ao Black Arcana.

## 2. Definição exata do recurso JSON

| Campo físico `data/alexscaves/enchantment/chomping_spirit.json` | Valor |
|---|---|
| `description.translate` | `enchantment.alexscaves.chomping_spirit` |
| `supported_items` | `#alexscaves:enchantable/extinction_spear` |
| `weight` | `2` — peso de encantamento; **não** probabilidade de ativação |
| `max_level` | `2` — nível máximo II no recurso |
| `min_cost` | `base=1`; `per_level_above_first=10` |
| `max_cost` | `base=41`; `per_level_above_first=10` |
| `anvil_cost` | `4` |
| `slots` | `mainhand` |
| `exclusive_set` | **Não declarado** no JSON auditado |

Esses custos são de **enchanting/bigorna**, não de mana, stamina, disparo, cooldown ou durabilidade da Extinction Spear. A tag indicada é uma condição declarativa do recurso; alterações por datapacks, compatibilidades de mesa, níveis adulterados e disponibilidade real em loot **não foram verificadas em jogo**. Não extrapolar incompatibilidades ausentes do arquivo.

## 3. Produtor exato — impacto corpo a corpo

A classe compilada `com/github/alexmodguy/alexscaves/server/item/ExtinctionSpearItem.class` tem SHA-256 **`846709940e9e400c4d6e894ec07887b762598b0d8f116fff951fa5585245bfd8`**. Método `acHurtEnemy(ItemStack,LivingEntity,LivingEntity)Z`, descritor JVM `(Lnet/minecraft/world/item/ItemStack;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/entity/LivingEntity;)Z`. Os offsets abaixo são do manifesto estático **1.0.10**, não inferidos do código da versão 1.1.1.

1. `@0–3` solicita `igniteForSeconds(5F)` na **vítima**, antes de criar o espírito. Essa ignição é uma ação própria do callback da lança; **não** é multiplicador de Chomping Spirit.
2. `@6–24` pede a criação de um `DinosaurSpiritEntity` provider-native. A posição inicial usa a média das posições horizontalmente e Y do atacante + 1; `@71–74` configura o tipo `TREMORSAURUS`.
3. `@79–83` grava o UUID do **atacante**; `@88–95` lê `ACEnchantmentRegistry.CHOMPING_SPIRIT` por `ACCompat.enchantLevel(stack,key)` e escreve o inteiro `E` através de `setEnchantmentLevel(E)` na entidade.
4. `@100–104` grava o **entity ID da vítima** como alvo do espírito, `@109–116` orienta sua visão e `@121–122` configura delay inicial de **5 ticks**.
5. `@125–134` chama `Level.addFreshEntity` e descarta o booleano de retorno. Uma **tentativa** de inserção não é garantia de entidade aceita ou dano subsequente. `@135–142` delega ao `SpearItem.acHurtEnemy` (custo nativo de durabilidade).

Não há segundo `DamageSource`, cast de Black Arcana ou custo de mana criado por este encantamento. O método não apresenta guarda **local** de `isClientSide` nem verificação de sucesso de `addFreshEntity`; isso delimita a evidência e **não** demonstra duplicação física entre lados. Não interpretar o nome do callback como confirmação de dano líquido ou hit aceito pela engine.

## 4. Consumidor exato — espírito Tremorsaurus

A classe compilada `com/github/alexmodguy/alexscaves/server/entity/item/DinosaurSpiritEntity.class` possui SHA-256 **`c4f6bbf7dab4aeeb2abd5b8cd227759d2ea1692115d1b3d14b62598a0b3900d7`**. O campo de nível `ENCHANTMENT_LEVEL` é dado sincronizado da entidade, com getter/setter próprio, não um hook público de integração para mods terceiros.

`tick()` não despacha o subtipo durante os cinco primeiros ticks de delay; na passagem que reduz o delay a zero o método também retorna. Após o delay, o dispatcher chama `tickTremorsaurus(Player)V` quando consegue resolver o `Player` do UUID. Isso é distinto de apenas ter um atacante `LivingEntity` no produtor.

No corpo de `tickTremorsaurus`:

- **Targeting:** lê `getAttackingEntity()`, usando o ID da vítima na `Level` local, sem um novo raycast/consulta global. Faz `lookAt` nos olhos do alvo. O intervalo de contato é **`distanceTo(target) < target.getBbWidth() + 3.5D`** (`@25–49`). Esse limiar **não** é tamanho de hitbox, raio de AoE ou alcance inicial da lança.
- **Movimento:** quando fora do intervalo, deriva direção para o alvo, normaliza somente quando comprimento `>1D` e solicita delta proporcional a **`0.15000000596046448D`** (`@54–93`). Não há upgrade de velocidade associado ao nível do encantamento neste trecho.
- **Preparação de ataque:** marca `usingAbility=true`; exige `abilityProgress >= 5F` e `dealtDamage=false` (`@96–119`). Esse progresso é mantido em `tick`, sujeito a delay, fade e demais condições nativas.
- **Dano pedido:** `@122–143` seleciona `ACDamageTypes.causeSpiritDinosaurDamage(registryAccess,player)` e chama `ACCompat.hurt(target,source,(float)(3+2*E))`. O inteiro `E` é lido por `getEnchantmentLevel()`; as operações de soma/multiplicação são inteiras antes da conversão a float.
- **Liquidação limitada:** só se o helper devolver `true` define `dealtDamage=true` (`@146–151`). Em seguida solicita `fading=true` (`@154–156`). Uma recusa não marca `dealtDamage`; podem existir novas tentativas enquanto o ciclo continuar elegível. Não há token de deduplicação global de eventos nem garantia de dano efetivo.
- **Duração:** `duration++ > 20` solicita fading, também quando o alvo não está ao alcance; com valor inicial zero, o limite é alcançado na **22ª avaliação** do ramo, não em vinte ticks absolutos desde a criação. A entidade controla fade e descarte independentemente (`tick`), com necessidade de validação física.

**Tabela aritmética solicitada pelo consumidor**, sem garantir hit:

| Nível `E` | Dano base pedido `(float)(3+2E)` |
|---:|---:|
| 0 | `3.0F` |
| I (1) | `5.0F` |
| II (2) | `7.0F` |

Esses valores **não** são HP removidos garantidamente nem números de hits, e não incluem armadura, resistência, outros eventos, políticas PvP, proteção de claims ou mods terceiros. Níveis `E>2` ou negativos não foram certificados; não extrapolar escala segura apenas porque a fórmula foi encontrada.

## 5. Fronteiras de perks e integração

| Eixo | Dado aproveitável para o projeto | Estado da intervenção |
|---|---|---|
| Dano | Pedido do Tremorsaurus `3+2E`; `alexscaves:spirit_dinosaur`, factory do provider | ⛔ Sem hook seguro para alterar `E`/dano, substituir `DamageSource` ou duplicar `hurt` |
| Targeting/alcance | ID da vítima no corpo a corpo; limiar `BbWidth+3.5D`; perseguição em entidade nativa | ⛔ Sem redirecionamento, troca por AoE, LOS novo, raio estendido ou hit extra |
| Projétil/quantidade | Variante `TREMORSAURUS` é gerada no callback melee; Extinction Spear arremessada é outra cadeia | ⛔ Não transformar nível II em quantidade de espíritos, nem criar spawns extras |
| Tempo/velocidade | Delay 5; progresso de habilidade 5; `duration++>20` e fading; delta ≈0.15 | ⛔ Não alterar NBT, ticks, velocidade, spawn ou vida de entidades externas |
| Custo e cooldown | Delegação ao custo de durabilidade de `SpearItem`; `weight`/`anvil_cost` são metadados de enchanting | ⛔ Sem segundo débito, refund, mana, cooldown ou alteração de custos provider-native |
| Autoria/Mastery | UUID do atacante e entity ID da vítima; consumidor resolve `Player`; `hurt` pode ser recusado | ⛔ Sem atribuição de XP por summon, tentativa, hit recusado ou proc; faltam settlement, autoria e dedupe verificados |
| Autoridade/rede | `ENCHANTMENT_LEVEL` é sincronizado pela entidade; callbacks não são uma API pública estável | ⛔ Sem escrita direta nos dados sincronizados, rerun de callback, execução client-authoritative ou bridge inferida |

**Autoridade:** Black Arcana mantém casting, efeitos próprios, world safety, Arcane Danger e persistência; RPG Skill Tree fornece progressão/atributos/Mastery/perks/gates somente através de boundaries comprovadas. O fluxo de espíritos e dano da Extinction Spear continua inteiramente provider-native. Aplicar `NO_MUTATION` e fail-closed na ausência de contrato de hook.

## 6. Evidência, limitações e contabilidade

**Verificado:** membro JSON com hash idêntico ao JAR 1.0.10; campo de nível e registry; métodos `acHurtEnemy`, `tick` e `tickTremorsaurus` com offsets/operandos JVM selados no manifesto preexistente; fórmula inteira de dano solicitado, origem de owner/alvo, delays, limiar de contato e ordem das solicitações.

**Não verificado:** execução em cliente/dedicated server com níveis 0/I/II; real chance de spawn e acerto, custos líquidos, comportamento quando `getUsingPlayer()==null`, loader + mixins, level/claim/PvP, gameplay simultâneo, dados modificados por datapacks, persistência/reconnect, empilhamento com outros efeitos, hooks versionados, atribuição de kills/Mastery, igualdade de `Entity.hurt` com dano líquido e aceitação física. Nenhum desses campos é marcado `PASS`.

**Estado final:** `VERIFIED_EXACT_BINARY_SELECTED_CONSUMERS` para o recorte; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`, `NO_MUTATION`. Não promover Stage 06, não homologar perks mutadoras nem inventar integração.

**Contabilidade:** +1 **ficha individual parcial** de encantamento; +0 contratos estáticos certificados pelo ledger; +0 raízes mágicas; +0 providers com catálogo encerrado. Próximo recurso alfabético: `alexscaves:crystallization`.
