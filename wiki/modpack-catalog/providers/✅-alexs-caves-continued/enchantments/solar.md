# Solar — recarga passiva do Raygun (Alex's Caves Continued 1.0.10)

**Escopo:** contrato técnico **estático individual** do encantamento `alexscaves:solar`, observado no JAR físico/publisher 1.0.10 e delimitado ao callback nativo do Raygun e seus helpers. **Não é um novo feitiço/cast:** atua na mesma carga do equipamento. `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION` / `fail-closed`. A integração com perks continua bloqueada até existir boundary mutador seguro e prova apropriada.

## 1. Identidade, proveniência e descrição

| Campo | Identidade auditada |
|---|---|
| Provider e mod ID | Alex's Caves Continued · `alexscaves` |
| Runtime | Minecraft **1.21.1**, NeoForge, Java **21** |
| JAR da modlist | `alexscaves-1.0.10-neoforge+1.21.1.jar`; **75.279.314 bytes** |
| SHA-1 do JAR | `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` |
| SHA-256 do JAR | `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| Enchantment | `alexscaves:solar`; símbolo `ACEnchantmentRegistry.SOLAR` |
| JSON | `data/alexscaves/enchantment/solar.json`; 353 bytes · SHA-256 `6b89d32889d8da9adfad072c534ae76627b1c620d489951bf1095f1805809b80` |
| Tag elegível | `data/alexscaves/tags/item/enchantable/raygun.json`; 46 bytes · SHA-256 `8e7cb71ff2c706004fba0493f2237e96da3af53dea6e3ae414542b5150cc012d` |
| Item base | `alexscaves:raygun` |
| Descrição publisher `en_us` (paráfrase) | O Raygun recupera carga gradualmente quando o portador está sob luz solar direta |
| Locale `pt_br` no JAR | Nenhuma chave própria de Solar encontrada; descrição em português é interpretação, não tradução oficial |

A [modlist do RPG Skill Tree](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/main/PROJECT-INSTRUCTIONS/modlist/World%20Gen/%E2%9C%85-alexs-caves-continued%20v1.0.10.md) fixa esse JAR como o provider físico. A [auditoria exata anterior](../EXACT-1.0.10-ARTIFACT-AUDIT.md) registra a paridade publisher/físico. O snapshot público adjacente de código em versão 1.1.1 **não** é autoridade para valores da versão instalada. Os dados abaixo provêm do JAR 1.0.10 e do [manifesto de Solar](../EXACT-SOLAR-STATIC-1.0.10.json).

## 2. JSON, aquisição, níveis e custos declarativos

| Campo | Valor extraído | Consequência |
|---|---|---|
| `description.translate` | `enchantment.alexscaves.solar` | Chave do idioma |
| `supported_items` | `#alexscaves:enchantable/raygun` | Tag que contém `alexscaves:raygun` |
| `weight` | **10** | Peso declarativo, não probabilidade de recarga |
| `max_level` | **1** | Solar I; o consumidor testa **nível positivo** |
| `min_cost` | base **1**, per-level **14** | Aquisição declarativa `1+14×(L−1)`; nível I = 1 |
| `max_cost` | base **41**, per-level **10** | Aquisição declarativa `41+10×(L−1)`; nível I = 41 |
| `anvil_cost` | **1** | Custo de encantamento, não débito de mana por callback |
| `slots` | `mainhand` | Metadado de equipamento; não é condição testada pelo callback do inventário |
| `exclusive_set` | Não declarado neste recurso | Não certifica compatibilidade efetiva com todos os encantamentos/datapacks |

Não há taxa extra de mana, stamina, cooldown ou consumível próprio cobrado pela **recarga Solar** no callback auditado. A aquisição real em mesa, loot, comércio e datapacks ativos não foi validada por teste físico. Um nível artificialmente superior a I não aumenta a recarga no corpo observado, pois `enchantLevel > 0` é teste booleano e não multiplicador.

## 3. Despacho exato e guardas do callback

A execução passa pelo `ItemStackTickMixin.ac_inventoryTick(Level,Entity,int,boolean,CallbackInfo)`, que testa `item instanceof ACTickingItem` e encaminha `stack, level, entity, selected` ao `ACTickingItem.acInventoryTick`. O `RaygunItem` implementa o consumidor `acInventoryTick(ItemStack,Level,Entity,boolean)`. Esse despacho foi auditado estática e independentemente no [contrato anterior de Seapairing](../EXACT-SEAPAIRING-CONTRACT-1.0.10.md); aqui os classfiles e métodos foram novamente selados por hash. A presença do mixin no binário **não** substitui medição da cadência exata do callback na instância completa.

No início de `RaygunItem.acInventoryTick`, o código calcula `usingThisStack`: para `entity instanceof LivingEntity`, compara `living.getUseItem().equals(stack)`; caso contrário, o valor é `false`. É uma comparação `Object.equals` realizada no método, não um teste explícito de `isUsingItem`, seleção de hotbar ou mainhand. O parâmetro `selected` não participa dos guardas da recarga no corpo auditado.

O ramo de recarga tem a seguinte sequência, com offsets JVM do JAR instalado:

1. **Somente servidor:** `Level.isClientSide() == false` (`@38–42`); a rota cliente `@146–230` executa outras atualizações de `PrevUseTime/UseTime`.
2. **Encantamento presente:** `ACCompat.enchantLevel(stack,SOLAR)>0` (`@45–52`). Solar I é o único nível declarado no JSON, mas o teste não exige igualdade com I.
3. **Item não em uso:** `usingThisStack == false` (`@55–57`); não recarrega neste ramo enquanto a stack é a de uso calculada.
4. **Débito prévio positivo:** `getCharge(stack)>0` (`@60–68`); o zero não é modificado.
5. **Sorteio:** `Level.getRandom().nextFloat() < 0.02F` (`@71–83`). Sorteio ocorre **antes** dos testes ambientais; `0.02F` é a probabilidade por **callback elegível**, e não por segundo já certificado.
6. **Céu visível:** consulta `Level.canSeeSky(entity.blockPosition().above())` (`@86–101`), com posição do argumento Entity mais um bloco.
7. **Condições temporais:** requer `Level.isDay()` (`@104–108`), `!Level.dimensionType().hasFixedTime()` (`@111–118`) e `ACCompat.sunAboveHorizon(level,positionAbove)` (`@121–127`). São gates distintos, cumulativos.
8. **Efeito solicitado:** `setCharge(stack,chargeAnterior-1)` (`@130–135`) e `setUseTime(stack,0)` (`@138–140`). O setter não retorna confirmação transacional da alteração persistida.

O helper `ACCompat.sunAboveHorizon(Level,BlockPos)` consulta `Level.getTimeOfDay(1F)` e devolve verdadeiro para os trechos `t<0.259F` ou `t>0.74F`, conforme ramos JVM `@7–27`. Valores exatamente nos limites são avaliados pelos operadores de comparação do bytecode, não devem ser arredondados como ângulos astronômicos ou duração real em segundos. **A exigência cumulativa `isDay()` é preservada**. O `BlockPos` não é lido pelo corpo do helper observado; a checagem de céu já recebe explicitamente a posição acima da entidade. O helper não verifica chuva/tempestade por chamada própria nesse corpo; efeitos ambientais da engine continuam fora do contrato.

## 4. Fórmula de recarga, limites e precisão

`RaygunItem.getCharge(stack)` lê o inteiro `ChargeUsed` da custom data da stack; se a tag está ausente, devolve **0**. O método `hasCharge(stack)` retorna verdadeiro enquanto `ChargeUsed < 1000`. Portanto **`ChargeUsed` registra consumo acumulado**, não quantidade disponível. Solar reduz esse contador:

`D_novo = D_anterior - 1` se e somente se todos os guardas acima forem verdadeiros, com `D_anterior>0`; fora disso não solicita mudança de carga.

| Estado antes do proc | Solicitação Solar | Implicação limitada |
|---|---|---|
| `ChargeUsed=0` | Não altera | Já está na posição lógica de carga plena |
| `ChargeUsed=1` | Solicita `setCharge(0)` | Última unidade de consumo pode ser restaurada |
| `ChargeUsed=1000` | Solicita `setCharge(999)` | Pode voltar a satisfazer `hasCharge` se a escrita for aceita |
| `ChargeUsed>1000` (estado forçado) | Solicita `D−1` | Não existe clamp para `1000` nesse ramo; o estado anômalo ainda exige análise |

A chance `0.02F` é **por invocação que alcance o RNG**, sem prova de independência estatística entre chamadas ou de frequência efetiva de ticks recebidos pelo item. Não declarar “uma carga a cada 50 ticks”, “1 por segundo”, “permanent unlimited ammo” ou taxa física fixa. No bytecode Solar não modifica o literal `1000` do limite do Raygun nem adiciona ticks extras; reduz `ChargeUsed` de uma unidade por proc, sem escala por nível.

## 5. Grafo técnico, hashes e consumidores

A varredura SHA-exata de **1.555 classfiles** encontrou o token direto `SOLAR` em apenas dois: `ACEnchantmentRegistry.class` e `RaygunItem.class`. `ItemStackTickMixin` aciona a interface sem mencionar o nome do encantamento; `ACCompat` executa o helper de horário e os acessos aos dados da stack. Este censo de símbolo não descarta reflection, mixins posteriores, datapacks nem consumidores de outros mods.

| Classfile relevante | SHA-256 da classe instalada |
|---|---|
| `server/item/RaygunItem.class` | `3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c` |
| `server/enchantment/ACEnchantmentRegistry.class` | `60006fab1b3b29f5f93c8365416815a12770cf8877a059298cb4ee82f7a92f32` |
| `mixin/ItemStackTickMixin.class` | `260fff4418e426eb5b3b9a02032cc0d5ebb73444aa1b16d7d578f4660e33a6b6` |
| `server/item/ACTickingItem.class` | `a96fc5427180e594aa59c3272395c207f3570f49165e33af0fdfa429a9922a1e` |
| `server/misc/ACCompat.class` | `333738f324e6e9d77a488e14b7e81b169c2b2d4f6db5171206a016ad0271f57b` |

A [sonda individual](../../../../../docs/qa/alexscaves_1010_solar_static_probe.py) registra hashes completos de métodos compilados, descritores JVM, janelas reduzidas de instruções e confronto com as provas anteriores do Raygun e de `sunAboveHorizon`. Métodos decisivos:

| Método / descritor abreviado | Instruções | SHA-256 compilado |
|---|---:|---|
| `RaygunItem.acInventoryTick(ItemStack,Level,Entity,boolean)V` | **109** | `7dd6613ef567ab79f0065253788e6ee9156bb86908b63907808599d5e3b560d2` |
| `RaygunItem.getCharge(ItemStack)I` | 11 | `c69c154524dbe4b4e46ed589438f7548cc39658305072a59b7c6a7dc9ec25baa` |
| `RaygunItem.setCharge(ItemStack,int)V` | 11 | `cedf012dbfb8edf1ca2171c57001dc8937f2982e3755a156da058a74d260993e` |
| `RaygunItem.hasCharge(ItemStack)Z` | 8 | `0b89217b97ca4f3d1c155c01b4170d1f0cb9141e4ee854ccf0c72892cd3b1db7` |
| `ACCompat.sunAboveHorizon(Level,BlockPos)Z` | **16** | `e56a191d33a1ab462518d5113e1df101c98663bafa1b263da092cf46a9767da7` |
| `ItemStackTickMixin.ac_inventoryTick(...)` | **19** | `ceeb91a726e908df227666b823d9811552dc84032df23dcc1570add5a11698d6` |

O compilado de `RaygunItem` tem 26 métodos declarados; o manifesto também sela `use`, `onUseTick`, `releaseUsing`, `getUseTime` e `setUseTime`. O digest de `onUseTick` foi reaproveitado de [controle Raygun preexistente](../EXACT-RAYGUN-CONTROL-1.0.10.json), mas nenhum aumento de dano, alcance, targeting, tamanho ou projétil é atribuído ao efeito Solar.

## 6. Efeitos, dano, targeting, duração e custos

- **Efeito primário:** alteração de estado de carga de um `ItemStack` pelo callback de inventário. **Sem dano direto, cura, efeito de status, projétil, summon, AOE, knockback ou alteração de blocos próprios de Solar:** `N/A` neste caminho.
- **Targeting:** o “alvo” relevante é a **stack** entregue ao callback e o **Entity** que carrega esse contexto; não seleciona `LivingEntity` para ataque, não faz ray trace próprio, não amplia alcance e não cria um cast. A seleção de vítimas do raio pertence ao [Raygun](../damage-types/raygun.md).
- **Geometria:** `entity.blockPosition().above()` é posição de consulta `canSeeSky`, não raio AOE ou deslocamento de projétil. `getTimeOfDay` pertence à engine, sem conversão arbitrária para graus de sol.
- **Duração:** passive proc condicionado a cada callback; nenhum timer independente de Solar em ticks no corpo auditado. A renovação de carga e a alteração de `UseTime` são eventos locais, não duração permanente de um status.
- **Cooldown e custos:** o proc Solar não consome Uranium Rod nem aplica cooldown próprio. O Raygun tem consumo de carga durante `onUseTick`, pode recarregar via insumo nativo `URANIUM_ROD` e usa o limite 1000 no predicado `hasCharge`; são contratos separados e não autorizam segunda cobrança Black Arcana.
- **RNG:** o nível não multiplica `0.02F` e não são verificadas probabilidades de terceiros, eficácia do RNG entre instâncias ou frequência exata em cliente/servidor carregado.

Os fluxos de feixe, dano e status `Irradiated` estão na [ficha Raygun](../damage-types/raygun.md) e nos manifestos de condicionais/consumidores nativos. Solar **não** acrescenta raiz mágica, `DamageSource` nem proc ofensivo contável.

## 7. Owner, persistência e autoridade de rede

A escrita `setCharge` passa por `ACCompat.getOrCreateTag` → `CompoundTag.putInt("ChargeUsed",D)` → `ACCompat.setTag`. O setter de `UseTime` também atualiza marcadores de tempo na stack. O Solar usa o `Entity` entregue ao callback para checar posição/céu; **não exige explicitamente Player** no ramo de recarga e não cria seu próprio registro de caster/UUID. O teste de uso usa `LivingEntity` apenas quando essa instância de Entity o é. Itens soltos ou inventários de terceiros não são automaticamente confirmados como recebedores do callback sem prova do despacho efetivo.

O ramo Solar observado é **server-side**, mas o Raygun possui outros ramos que enviam `UpdateItemTagMessage` do cliente para o servidor. As provas dos receptores, validação de identidade e autenticação dessas mensagens pertencem ao [dossiê de rede do Raygun](../EXACT-RAYGUN-RECEIVER-1.0.10.json) e continuam com limites. **Não presumir que a escrita Solar seja definitiva contra sincronizações concorrentes, rollback, cliente malicioso ou reload.** O NBT/CustomData nativo existe, mas persistência efetiva por save/reload, troca de dimensão e múltiplos usuários não foi testada aqui.

## 8. Integração com perks, atributos e Mastery

| Ideia de perk | Parâmetro nativo pertinente | Condição para implementação segura |
|---|---|---|
| Recarga Solar mais frequente | `nextFloat()<0.02F` por callback elegível | Hook real, comprovado no servidor, para alterar probabilidade sem repetir callback |
| Maior recuperação por proc | `setCharge(D−1)` e guarda `D>0` | Clamp e invariante de carga, tratamento de estados forçados e transação server-owned |
| Recarga sob outras condições climáticas | `canSeeSky`, `isDay`, `hasFixedTime`, `sunAboveHorizon` | Respeitar autoridade de dimensão, PvP/world safety e custo; nenhum bypass existe certificado |
| Desbloquear recarga enquanto dispara | `usingThisStack` e consumo do feixe | Evitar corrida entre cobrança de carga e recarga; ausência de hook seguro |
| Redução de consumo de energia | `onUseTick` e Energy Efficiency | É outro contrato: não confundir chance Solar com custo de disparo |
| XP e Mastery | Proc passivo de recuperação de carga | Não contar cada tick/roll como cast, hit ou XP ofensivo; creditação exige evento estável e deduplicado |
| Salvamento e multiplayer | `ChargeUsed`, `UseTime`, pacote de atualização | Validar ownership, net handler, antirreplay, reload e compensação de concorrência |

O **Black Arcana** mantém autoridade sobre seu próprio runtime mágico; o **RPG Skill Tree** pode consumir contratos de atributos/perks por boundary real. `RaygunItem` e o sistema de carga pertencem ao provider. **Não foi identificada API pública mutadora segura apenas por observar campos/métodos compilados.** `mutating_hook=NOT_VERIFIED`, `NO_MUTATION`, `physical_qa=NOT_TESTED`.

## 9. Prova, reprodução e pendências

- [Manifesto SHA-exato individual](../EXACT-SOLAR-STATIC-1.0.10.json): JSON, tag, locales, classes, censo de 1.555 classes, digests e janelas JVM limitadas, retorno do helper solar.
- [Relatório reproduzível](../EXACT-SOLAR-STATIC-1.0.10.md), [sonda read-only](../../../../../docs/qa/alexscaves_1010_solar_static_probe.py), [testes de drift](../../../../../docs/qa/alexscaves_1010_solar_static_probe_test.py), [workflow dedicado](../../../../../.github/workflows/alexscaves-1010-solar-static.yml).
- Executar em checkout do Black Arcana com Java 21 e o JAR SHA-exato: `python3 docs/qa/alexscaves_1010_solar_static_probe.py --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar --javap javap --seal wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-SOLAR-STATIC-1.0.10.json`.
- A sonda falha se o hash/size do JAR, a classe Raygun, os digest de métodos previamente selados, as âncoras numéricas de `sunAboveHorizon`, os ramos booleanos do helper ou o manifesto divergem.

**Limites finais:** a certificação é `STATIC_TECHNICAL_CATALOG_ONLY`. Não fecha todos os 51 encantamentos nem o provider integral, não verifica frequência real do tick, comportamento com datapacks, presença/ausência de outras mutações por mods, aceitação efetiva da recarga, segurança do pacote C2S, reload/save, cliente real, PvP/world safety, latência ou hook mutador. Até QA específica e API segura, **⛔ nenhuma perk que muta recarga ou ignora os gates pode ser ativada**.
