# Chomping Spirit — dano do espírito Tremorsaurus da Extinction Spear (1.0.10)

**Estado:** ✅ **contrato técnico estático individual certificado** (`STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`) no recorte nativo do JAR publisher 1.0.10. Verificações de identidade, nível, produtores, targeting, fluxo de dano, branches JVM, autoria, NBT, custos e limites estão ligadas ao manifesto causal individual e à prova já certificada de Spirit Dinosaur. `NO_MUTATION` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED`. **Não** há homologação de uma perk que altere a entidade, o dano, a área ou o fluxo de ataque.

O encantamento **não constitui um novo feitiço ou cast**. É um modificador consumido pela ação nativa de **acerto corpo a corpo com a Extinction Spear**: transfere seu nível a um `DinosaurSpiritEntity` de tipo `TREMORSAURUS`. O ataque do espírito pode solicitar dano `alexscaves:spirit_dinosaur`. Não confundir essa variante com os espíritos `SUBTERRANODON` (lançamento/impacto, `plummeting_flight`) e `GROTTOCERATOPS` (`herd_phalanx`, uso sustentado). A [ficha raiz já certificada](../damage-types/spirit-dinosaur.md) documenta a causalidade comum e deve ser reutilizada, sem contabilizar três novos casts.

## 1. Identidade e proveniência

- **Provider:** Alex's Caves Continued, `alexscaves`; Minecraft **1.21.1**, NeoForge.
- **Identidade:** `alexscaves:chomping_spirit`; chave `enchantment.alexscaves.chomping_spirit`.
- **Publisher físico:** `alexscaves-1.0.10-neoforge+1.21.1.jar`, **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **Manifesto binário reutilizado:** [EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json](../EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json); nele, o `data/alexscaves/enchantment/chomping_spirit.json` físico tem SHA-256 **`f0fb73c3e1c564831375009736264848190a6a6edd126b36bb3802ff356fa6e7`**.
- **Revalidação causal individual:** [EXACT-CHOMPING-SPIRIT-CAUSAL-1.0.10.json](../EXACT-CHOMPING-SPIRIT-CAUSAL-1.0.10.json), selo compacto com SHA-256 de relatório JVM completo, reproduzido pela [sonda read-only](../../../../../docs/qa/alexscaves_1010_chomping_spirit_causal_probe.py), [regressões sintéticas](../../../../../docs/qa/alexscaves_1010_chomping_spirit_causal_probe_test.py) e [workflow dedicado ao JAR 1.0.10](../../../../../.github/workflows/alexscaves-1010-chomping-spirit-causal.yml). Selo do relatório completo: `44e8552ba4a803a2c8735fe78803795f37c63ac66e56624acc519167d29ab814` (hash sobre JSON canônico ordenado).
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

## 6. Reconciliação causal completa no recorte de classes do JAR

A sonda comparou o SHA-1, SHA-256 e tamanho do artefato físico, os hashes de classfiles/recursos e **todos os anchors de bytecode publicados no manifesto técnico anterior** para quatro classes relevantes. O relatório completo de auditoria é reproduzido deterministamente pelo workflow e vinculado por SHA-256 ao novo selo compacto; não contém implementação copiada de outro mod.

| Classe / método produtor ou consumidor | Instruções JVM | Branches diretos `if/goto` | Switch nativo |
|---|---:|---:|---|
| `ExtinctionSpearItem.acHurtEnemy` | 64 | 0 | nenhum |
| `SpearItem.acHurtEnemy` (custo herdado da lança) | 7 | 0 | nenhum |
| `DinosaurSpiritEntity.tick` | 230 | 20 | `tableswitch @279` |
| `DinosaurSpiritEntity.tickTremorsaurus` | 96 | 10 | nenhum |
| `ExtinctionSpearEntity.onHitEntity` (trajetória distinta da lança arremessada) | 140 | 8 | nenhum |

São **38 desvios condicionais/goto** e a tabela de `tick` possui quatro destinos diretos validados: ordinal `0 → 304` (Subterranodon), `1 → 312` (Grottoceratops), `2 → 320` (Tremorsaurus) e `default → 325`. O inventário observado possui **71 métodos declarados** entre `ExtinctionSpearItem` (9), `SpearItem` (12), `DinosaurSpiritEntity` (32, incluindo o inicializador estático) e `ExtinctionSpearEntity` (18). Essa contagem é apenas dessas quatro classes, não do universo do provider.

O caminho `acHurtEnemy` não faz branches diretos próprios no corpo compilado: solicita ignição da vítima, criação do espírito, tipo `TREMORSAURUS`, UUID do atacante, nível `CHOMPING_SPIRIT`, ID da vítima e atraso inicial de cinco ticks. `addFreshEntity` em `@131` tem seu retorno booleano descartado por `pop @134`; em seguida o método delega o desgaste ao `SpearItem`. Portanto, **spawn e dano bem-sucedidos não são pressupostos**.

O dispatcher `tick` só encaminha `TREMORSAURUS` após resolver um `Player` do UUID de autoria; `tickTremorsaurus` lê a entidade-alvo, exige contato geométrico e progresso de habilidade, e passa `(float)(3+2E)` com `ACDamageTypes.causeSpiritDinosaurDamage` a `ACCompat.hurt`. Se o helper retorna `true`, marca `dealtDamage=true`; a rotina solicita `fading` conforme o fluxo original. A chamada de dano de `ExtinctionSpearEntity.onHitEntity` é um **emissor causal distinto** da variante melee de Chomping Spirit e não justifica atribuir dois hits ao mesmo efeito.

**Persistência importante para perks:** os overrides `DinosaurSpiritEntity.addAdditionalSaveData` e `readAdditionalSaveData` possuem **15 instruções cada** e gravam/leem `UsingPlayerUUID` e `DinosaurType`. Não serializam explicitamente nesses próprios corpos `ENCHANTMENT_LEVEL`, `ATTACKING_ENTITY_ID` ou `DELAY_SPAWN`; campos sincronizados não se tornam automaticamente campos de NBT. Isso **não comprova perda de estado após reload**, já que persistência herdada, reconstrução por pacotes e ciclo físico de descarregamento/recarregamento permanecem `NOT_VERIFIED` / `NOT_TESTED`.

O token binário direto `CHOMPING_SPIRIT` ocorre em `ACEnchantmentRegistry.class` e `ExtinctionSpearItem.class` no JAR observado; pesquisas por token não excluem reflexão, transformações/mixins ou consumidores de outros JARs. A validação cobre os branches intramétodo selecionados, não todo CFG interprocedural/exceções. Nenhum hook mutador foi encontrado e homologado. `NO_MUTATION` e `fail-closed` continuam obrigatórios.

## 7. Evidência, limitações e contabilidade

**Verificado:** membro JSON com hash idêntico ao JAR 1.0.10; campo de nível e registry; métodos `acHurtEnemy`, `tick` e `tickTremorsaurus` com offsets/operandos JVM selados no manifesto preexistente; fórmula inteira de dano solicitado, origem de owner/alvo, delays, limiar de contato e ordem das solicitações.

**Não verificado:** execução em cliente/dedicated server com níveis 0/I/II; real chance de spawn e acerto, custos líquidos, comportamento quando `getUsingPlayer()==null`, loader + mixins, level/claim/PvP, gameplay simultâneo, dados modificados por datapacks, persistência/reconnect, empilhamento com outros efeitos, hooks versionados, atribuição de kills/Mastery, igualdade de `Entity.hurt` com dano líquido e aceitação física. Nenhum desses campos é marcado `PASS`.

**Estado final:** ✅ **contrato técnico estático individual** `COMPLETE_PERK_READY` / `STATIC_TECHNICAL_CATALOG_ONLY`, com manifestos SHA-exatos e branches diretos certificados no recorte selecionado; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. Este status do ledger não certifica perk executável, não comprova reload nem permite avançar Stage 06.

**Contabilidade do fechamento:** +0 fichas novas; **+1 contrato técnico estático individual certificado**, +0 raízes mágicas e +0 providers integralmente catalogados. Encantamentos identificados: **37/51 certificados**, **14 parciais**, nenhuma identidade sem ficha individual. Contratos estáticos do provider no recorte observado: **65/81**; o universo completo ainda não foi comprovado. Próximo objeto parcial em ordem alfabética: `alexscaves:crystallization`.
