# Twilight Perfection — janela de tiro perfeito do Dreadbow (Alex's Caves Continued 1.0.10)

**Estado individual:** ✅ **contrato técnico estático certificado no escopo** `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`, condicionado à CI da revisão. Não é homologação de gameplay, integração mutadora nem de todo o provider. `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `mutation=NO_MUTATION`. Esta propriedade do Dreadbow **não cria um nono cast/raiz mágica**.

**Descrição funcional própria:** enquanto o jogador mantém o Dreadbow carregando, uma janela curta de disparo perfeito aparece ao atingir o limite visual de carga. Se o encantamento estiver presente e o contador ainda for positivo ao soltar, a flecha pode receber uma flag de tiro perfeito ou uma duplicação do dano base, dependendo da factory de munição. O recurso inglês do publisher descreve uma aparência avermelhada e dano dobrado, mas nem o vermelho do modelo nem o multiplicador constituem prova de dano efetivamente recebido pelo alvo.

## 1. Identidade e proveniência exata

| Campo | Prova |
|---|---|
| Provider / mod ID | Alex's Caves Continued / `alexscaves` |
| Registro | `alexscaves:twilight_perfection`; chave `enchantment.alexscaves.twilight_perfection` |
| Objeto equipado | `alexscaves:dreadbow` via `#alexscaves:enchantable/dreadbow` |
| Plataforma | Minecraft **1.21.1**, NeoForge, Java **21** |
| JAR instalado | `alexscaves-1.0.10-neoforge+1.21.1.jar` — **75.279.314 bytes** |
| JAR SHA-1 | `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` |
| JAR SHA-256 | `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| Recurso publisher | `data/alexscaves/enchantment/twilight_perfection.json`, **367 bytes** |
| JSON SHA-256 | `82a8e06c07b66be33a330bdbeb1bc867d03ce13a49ab2505fa06504fe5f044e1` |
| Selo individual | [EXACT-TWILIGHT-PERFECTION-CONTRACT-1.0.10.json](../EXACT-TWILIGHT-PERFECTION-CONTRACT-1.0.10.json) |
| Fonte causal previamente auditada | [Dreadbow 1.0.10](../equipment/dreadbow.md), [Dark Arrow](../damage-types/dark-arrow.md) e [manifesto binário comum](../EXACT-DREADBOW-CONTRACTS-1.0.10.json) |
| Reprodução | [Sonda específica](../../../../../docs/qa/alexscaves_1010_twilight_perfection_probe.py) e [testes individuais](../../../../../docs/qa/alexscaves_1010_twilight_perfection_cards_test.py) |

A fonte pública adjacente `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**; não é autoridade para CFG, fórmulas ou valores do JAR instalado **1.0.10**. O selo resulta da inspeção do binário físico e reutiliza **somente** os classfiles, métodos, recursos e âncoras previamente verificadas no manifesto comum.

## 2. Níveis, custos e elegibilidade do encantamento

| Parâmetro declarativo do JSON | Valor 1.0.10 |
|---|---|
| `description.translate` | `enchantment.alexscaves.twilight_perfection` |
| `supported_items` | `#alexscaves:enchantable/dreadbow` |
| `weight` | **2**; peso de seleção no sistema de encantamentos, não chance de tiro perfeito |
| `max_level` | **3** (I–III) |
| `min_cost` | base **1**, incremento **7** por nível adicional |
| `max_cost` | base **41**, incremento **10** por nível adicional |
| `anvil_cost` | **4** |
| `slots` | `mainhand` |
| `effects` / `exclusive_set` próprios | Não constam do JSON do encantamento |

| Nível publicado | Custo mínimo | Custo máximo | `PerfectShotTicks` concedidos na carga |
|---|---:|---:|---:|
| I | 1 | 41 | **4 ticks** |
| II | 8 | 51 | **7 ticks** |
| III | 15 | 61 | **10 ticks** |

O tag `data/alexscaves/tags/item/enchantable/dreadbow.json` (SHA-256 `f22db4f6335af0cc185f0478c482c3c666a86afa430f06bdabc78ccc662076d5`) contém `alexscaves:dreadbow`. O JSON de **Relentless Darkness** (SHA-256 `94edb103571eba0d0ca503b8a9455d4643a0f414c758b4ca79d49bbcdf9f473e`) inclui `alexscaves:twilight_perfection` em seu `exclusive_set`, junto de Precise Volley e Dark Nock; essa exclusão está declarada **no recurso de Relentless**, não no JSON próprio de Twilight. Datapacks externos e níveis de encantamento forçados não são inferidos como válidos.

**Custos de encantamento não são custos por disparo.** Não há mana, cooldown ou desgaste adicional próprio de Twilight Perfection demonstrado nos métodos auditados.

## 3. Ativação e janela temporal — `DreadbowItem.acInventoryTick`

O mixin `ItemStackTickMixin.ac_inventoryTick` alcança `ACTickingItem.acInventoryTick` do Dreadbow. No `DreadbowItem.class` SHA-256 `b9cd6e843f923877775e38b89214e8649c10d4d5be704ed9dd377900439d44ae`, método `acInventoryTick(ItemStack,Level,Entity,boolean)V`, as escritas de carga desse callback ocorrem **após `Level.isClientSide @39`, com `ifeq @42 → 400`**. O parâmetro `selected` não governa essa lógica; o método verifica o uso do próprio stack por `LivingEntity`.

A ordem causal compilada do trecho de controle é:

1. Lê `UseTime` e concilia `PrevUseTime` no `DataComponents.CUSTOM_DATA` do ItemStack. São campos do provider; não representam o tempo de uso do argumento de `releaseUsing`.
2. Se a entidade está usando o arco e `PerfectShotTicks>0`, decrementa o contador em **1** (`getPerfectShotTicks @91/@99`, `isub @103`, `setPerfectShotTicks @104`) e solicita `UpdateItemTagMessage` ao servidor (`@107–119`).
3. Consulta o nível de `RELENTLESS_DARKNESS @123`, o nível de `TWILIGHT_PERFECTION @140–143` e `M=getMaxLoadTime(stack) @149`. Se usando, `oldUseTime<M` e o incremento do `UseTime` alcança o limite `M`, a janela é concedida apenas quando **Twilight >0**. Os ramos relevantes convergem em `@156`, `@163`, `@189`, `@196`, `@203`.
4. O valor gravado é **`W(L)=4+3×(L−1)`**, conforme `iconst_4 @207`, `iconst_1 @210`, `isub @211`, `iconst_3 @212`, `iadd @214` e `setPerfectShotTicks @215`. Solicita outra sincronização de tag em `@218–230`. Se o ramo de aumento de carga for elegível mas não cruzar `M`, zera o contador (`@237–238`) e sincroniza (`@241–253`).
5. Fora de uso, se `oldUseTime>0`, a carga visual cai para `max(0,oldUseTime−5)` e o contador é zerado (`setPerfectShotTicks @305`). Se o contador já é zero, não há um refresh automático incondicional.
6. O incremento normal da carga visual é **1 por callback**; no modo Relentless é **3**, mas esse modo tem exclusividade declarada e bypass separado no disparo.

Para nível I/II/III, a fórmula dá **4/7/10 ticks de contador**; o nível altera o **tamanho da janela concedida**, não um multiplicador progressivo de dano. São contagens escritas no cliente, não confirmação física de **0,20 / 0,35 / 0,50 s** no servidor sob latência. O helper `getPerfectShotTicks(ItemStack)I` lê o valor da tag, e `setPerfectShotTicks(ItemStack,int)V` grava o inteiro fornecido; **nenhum deles valida nível, lado, origem, tempo ou clamp** por conta própria.

**Carga nominal auxiliar:** `M=5` se Relentless positivo; senão `M=40−8×level(DARK_NOCK)` (40/32/24/16 ticks para níveis normais 0–3 de Dark Nock). O `releaseUsing` usa outro relógio: `t=72000−remainingUseTicks`; `x=t/M`; `p=min(1,(x²+2x)/3)` somente com clamp superior e exige `p>0.1D`. Twilight **não** reduz `M` nem muda a curva `p`. Valores forçados de Dark Nock que tornem `M≤0` não são homologados.

## 4. Consumo no disparo normal — `DreadbowItem.releaseUsing`

O método `releaseUsing(ItemStack,Level,LivingEntity,int)V` primeiro exige um **Player** e desvia se **Relentless Darkness >0** (`@14–20 → 899`). Depois obtém `TWILIGHT_PERFECTION @87` e chama `ACCompat.enchantLevel @90`: a flag de tiro perfeito é **`perfect=(L>0 && getPerfectShotTicks(stack)>0)`** (`@93–108`, resultado no slot local **10**). Se `p≤0.1D`, o corpo retorna (`@113–117 → 899`), mesmo com contador perfeito positivo.

| Ramo da munição | Ação compilada quando `perfect=true` | Limite |
|---|---|---|
| Flecha conversível em Dark Arrow | Instancia `DarkArrowEntity(level,player)`; `setShadowArrowDamage(Precise ? 2F : 3F) @390–402`; `setPerfectShot(perfect) @407–409` | A flag e a potência solicitada pertencem ao projétil criado; não provam hit, spawn ou dano recebido |
| Flecha **não conversível** retornada pela factory de munição | Se `perfect` positivo, acessa `AbstractArrowAccessor.ac$getBaseDamage @431` e faz **`setBaseDamage(danoBaseAnterior×2D) @436–440`** | O tipo de dano, o projeto da flecha e seus demais encantamentos dependem da factory/engine, sem `DarkArrowEntity` próprio |

A conversão nativa é verificada por `isConvertibleArrow`: `instanceof Arrow` e `Arrow.getColor()==−1`. Não se trata de qualquer projétil e nem de garantia de conversão de toda munição. `DreadbowItem.onUseTick` no modo Relentless tem seu **outro** fluxo (`remainingUseTicks %3==0`), cria setas e pode escrever `shadowArrowDamage=2F`, mas **não consulta Twilight nem invoca `setPerfectShot` nesse corpo**. A exclusividade de dados não deve ser substituída pela invenção de um bônus em Relentless.

## 5. Liquidação e alcance — consumidores já certificados do Dreadbow

O consumidor `DarkArrowEntity.onHitEntity(EntityHitResult)V` lê `getShadowArrowDamage @11`, verifica `isPerfectShot @17`, e, se positivo, multiplica a solicitação de dano por **2F** (`@20–27`). Solicita o tipo de dano nativo **`alexscaves:dark_arrow`** via `ACDamageTypes.causeDarkArrowDamage @37` e usa `ACCompat.hurt @82`, condicionado a não atingir owner/aliados e a não estar em fading; apenas um retorno verdadeiro habilita `startFading` (`@85–90`). O valor **solicitado**, não os pontos de vida garantidamente perdidos, resulta em:

| Estado no ramo Dark Arrow | Sem perfect | Com perfect |
|---|---:|---:|
| Sem Precise Volley: `shadowArrowDamage=3F` | 3F | **6F** |
| Com Precise Volley: `shadowArrowDamage=2F` | 2F | **4F** |

`ACCompat.hurt` e o motor podem negar ou modificar a aplicação por armadura, resistência, invulnerabilidade, claims, PvP e outros listeners. Twilight **não adiciona um novo `DamageType`** nem constitui outro cast; a origem e o tratamento de owner pertencem à própria Dark Arrow.

**Targeting nativo compartilhado (não modificado por Twilight):** `releaseUsing` usa raycast de mira `128F×p` e fallback `42F×p` se MISS; o destino é o hit location selecionado, sem autolock persistente. O centro de spawn está sujeito a busca vertical limitada; candidatos de lançamento usam jitter `(16r−8,4r−2,16r−8)`, caixa **16×4×16**, com até seis novas tentativas em certo bloqueio e fallback. As tentativas de criação são `ceil(30F×p)` se conversível e `ceil(8F×p)` senão; velocidade solicitada `0.5F+1.5F×r`, nominal **[0,5; 2)**, sem aumento por Twilight. Hitbox, tamanho de projétil, gravidade, colisão e alcance efetivo permanecem regidos pelas entidades/engine; não confundir distâncias de raycast ou contagem solicitada com AoE, range de voo ou spawns aceitos. `Level.addFreshEntity` tem retorno booleano ignorado.

**Custos nativos do mesmo salvo:** após o fluxo de disparo, fora creative, há solicitação normal de **1 desgaste do Dreadbow** e **1 unidade de munição por salvo**, com exceções específicas de Shaded Respite conforme luz e tipo de flecha. Não é um custo por cada Dark Arrow ou por cada evento perfect. O custo declarativo de bigorna `4` não altera essa regra. O método não instala cooldown independente, mana ou Strain de Black Arcana.

## 6. Estado, rede, sincronização e autoria

A janela usa `UseTime`, `PrevUseTime`, `PerfectShotTicks` em **`DataComponents.CUSTOM_DATA`**. O cálculo/contagem observados estão no ramo **cliente** de `acInventoryTick`. O consumer de rede `UpdateItemTagMessage.handle(UpdateItemTagMessage,ACNetworkContext)V` obtém um sender/contexto (`@8/@15`), usa `entityId` da mensagem para resolver entidade (`@39–42`), exige `LivingEntity` e procura stack da mão principal ou secundária **pelo tipo de item**, não uma validação comprovada de identidade da stack original (`@70–124`). Sob `UpdatesStackTags`, obtém a tag recebida e chama `updateTagFromServer @174`. O corpo não demonstra reconstrução autoritativa de `UseTime`, nível válido ou janela de tiro perfeito no servidor, tampouco vinculação inequívoca `message.entityId == sender.id`.

**Risco de integração:** não promover o pacote `UpdateItemTagMessage` a hook de perk, não aceitar `PerfectShotTicks` arbitrário como direito de lançar proc, e não inferir que o client pode governar legitimamente dano ou Mastery. Essa leitura é **evidência de superfície potencialmente sensível**, não uma exploração demonstrada. O `ACCompat.getTag/setTag` grava o estado no ItemStack; persistência do contador sob save/restart, reconexão, troca de mãos e multiplayer não foi testada fisicamente.

O renderer `ACItemstackRenderer.renderByItem` consulta `getPerfectShotTicks @3191` para escolher a apresentação visual do olho do Dreadbow. **Aparência vermelha não prova dano aplicado.** A autoria do projétil conversível provém de `DarkArrowEntity(level,player)`; o ramo não conversível delega a factory de `ArrowItem`. Sem evidência de aceite e atribuição, não emitir XP, Mastery ou gatilho de perk por cada aparência perfeita, tentativa de spawn ou disparo.

## 7. Eixos de integração para perks, atributos e Mastery

| Eixo | Informação estática disponível | Fronteira de segurança |
|---|---|---|
| Tempo/janela | `W=4+3×(L−1)`; concede após cruzar `UseTime≥M`, decai 1 por callback de uso; ligado a CustomData | ⛔ Sem hook seguro para mudar contador nem validar janela no servidor; risco de manipulação cliente |
| Multiplicador de dano | `DarkArrow ×2F` na flag perfeita; `AbstractArrow.baseDamage×2D` para não conversível | ⛔ Sem mutação em classe de provider aprovada; evitar segundo `hurt`, stack duplo e perda de crédito |
| Target/range/AoE | Raycast `128p`/fallback `42p`; jitter de spawn **16×4×16**; sem novo AoE/perseguição própria | ⛔ Alvos, direção e colisão não são governados pelo valor `PerfectShotTicks` |
| Número/velocidade/tamanho | `ceil(30p)` / `ceil(8p)` tentativas, velocidade nominal `0.5+1.5r`; Twilight não escala essas variáveis | ⛔ Não duplicar salvas, aumentar ticks globais ou variar hitbox sem seam verificada |
| Custos/cooldown | Custo nativo por salvo e Shaded Respite; níveis/custos da mesa/bigorna distintos | ⛔ Não duplicar desgaste/ammo; nenhuma segunda mana, Strain ou cooldown inventado |
| Autoria/persistência/rede | Player constrói DarkArrow; CustomData do arco é sincronizado por mensagem de item | ⛔ Distinguir contador visual, tag server-side, owner válido, PvP, proteção e persistência |
| Mastery/XP | Não foi identificado evento autoritativo de XP ligado ao perfect no trecho próprio | ⛔ Não creditar progresso por renderização, tag sincronizada ou pedido de dano |

**Hooks mutadores reais:** `NOT_VERIFIED`. O Black Arcana mantém autoridade por seu próprio runtime; Dreadbow/Dark Arrow continuam authority dos efeitos nativos, e o RPG Skill Tree fornece apenas perks/Mastery/gates se surgir boundary estável e verificado. Sem isso: **`NO_MUTATION` / fail-closed**.

## 8. Grafo técnico, prova e conclusão

| Classe / consumidor exato | Métodos do manifesto individual (descritores no JSON selado) |
|---|---|
| `server.item.DreadbowItem` — SHA-256 `b9cd6e843f923877775e38b89214e8649c10d4d5be704ed9dd377900439d44ae` | `acInventoryTick`, `releaseUsing`, `getPerfectShotTicks`, `setPerfectShotTicks` |
| `server.entity.item.DarkArrowEntity` — SHA-256 `089f0a65444078ca42fc1da2d5023384314ef5f5283ddf3fe8484bf31d4136ad` | `onHitEntity`, `setPerfectShot`, `isPerfectShot` |
| `server.message.UpdateItemTagMessage` — SHA-256 `bda52d12e8cce7e010b3d4cd2db7d83000e78b35657c55773a8ba91a070478c8` | `handle` |
| `client.render.item.ACItemstackRenderer` — SHA-256 `18e350579f407c7c9509e230aa17b68b1113c166352e812482934ec3fdc1bd7e` | `renderByItem` |
| `server.enchantment.ACEnchantmentRegistry` — SHA-256 `60006fab1b3b29f5f93c8365416815a12770cf8877a059298cb4ee82f7a92f32` | `TWILIGHT_PERFECTION` é lido por `ACCompat.enchantLevel` nos consumers fixados |

**Reprodução SHA-exata:** `python3 docs/qa/alexscaves_1010_twilight_perfection_probe.py --jar <JAR 1.0.10 verificado> --manifest wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-DREADBOW-CONTRACTS-1.0.10.json --seal wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-TWILIGHT-PERFECTION-CONTRACT-1.0.10.json`. O selo fixa o JSON, tag, idioma, exclusividade, cinco hashes de classe e **nove métodos consumidores**, incluindo SHA-256 dos respectivos *conjuntos de âncoras* do manifesto Dreadbow. O digest de âncoras **não** é um hash integral de método; a autoridade da classe é o hash SHA-256 do classfile completo.

**Comprovado estaticamente:** identidade e eligibility, custos, escala de janela I–III, gates cliente/uso e release, dois caminhos de multiplicação, targeting e custos delegados, rede/renderer e risco de integração. **Não verificado fisicamente:** resultado do pacote, sincronização sob latência, dano aceito, dano de outras factories, mundo com outros mods, datapacks e PvP/claims, save/reload e mudança de dimensão; nenhum hook seguro foi declarado.

**Certificação delimitada:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` para o comportamento compilado publisher 1.0.10 descrito; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `provider_universe_closed=false`, `NO_MUTATION`. É a 51ª ficha individual de encantamento do recorte de **51/51 recursos publisher**; isso não encerra o universo mágico total do provider, não autentica a rede nem autoriza perks executáveis.
