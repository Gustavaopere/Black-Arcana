# Energy Efficiency — consumo de carga do Raygun (publisher 1.0.10)

**Estado:** ✅ **contrato técnico estático individual certificado** de `alexscaves:energy_efficiency` no publisher **1.0.10**, `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`, `evidence_grade=SHA_EXACT_BINARY_BEHAVIOR`. A auditoria individual reproduziu o JSON/tag físicos, os quatro métodos relevantes do `RaygunItem` e o CFG direto do `onUseTick`, preservando a distinção entre escrita de charge no cliente e autoridade de rede/servidor. **Sem hook mutador ou QA física homologada:** `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `executable_perk_certification=NOT_CERTIFIED` · `NO_MUTATION`.

**Descrição funcional verificada estaticamente:** Energy Efficiency aumenta o intervalo entre tentativas de incrementar o indicador de **carga usada** (`ChargeUsed`) durante o uso sustentado do Raygun, conforme `P(L)=2+floor(1.5×L)`. Após o aquecimento de 15 ticks, o consumidor calcula no **ramo cliente** a periodicidade e solicita `setCharge(stack,min(ChargeUsed+1,1000))` nas iterações elegíveis. Não é uma nova magia, novo tipo de dano nem um projétil separado; integração mutadora e consumo realmente aceito pelo servidor continuam sem homologação.

## 1. Versão instalada, identidade e fontes

| Objeto | Prova e classificação |
|---|---|
| Modpack | [Modlist do sibling](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/main/PROJECT-INSTRUCTIONS/modlist/modlist.md), linha #019: `alexscaves-1.0.10-neoforge+1.21.1.jar`, versão **1.0.10** (entrada revisada em 22/10/2026) |
| Provider / mod ID | Alex's Caves Continued / `alexscaves`; Minecraft 1.21.1 / NeoForge |
| Publisher JAR | 75.279.314 bytes; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570` |
| SHA-256 do JAR | `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| Identidade semântica | `alexscaves:energy_efficiency`, um dos 51 recursos em `data/alexscaves/enchantment/`, segundo [inventário físico](../INTEGRATION-SCOPE-INVENTORY-1.0.10.json) |
| Consumer binário | `com/github/alexmodguy/alexscaves/server/item/RaygunItem.class`; SHA-256 `3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c` |
| Método selecionado | `onUseTick(Level,LivingEntity,ItemStack,int)V`; digest de parse `b037276094928625e501d13fddd11829e3fe5540d585f7d8213f37b098c39bc5` |
| Manifestos canônicos reutilizados | [Controle Raygun](../EXACT-RAYGUN-CONTROL-1.0.10.json), [rede](../EXACT-RAYGUN-NETWORK-ABI-1.0.10.json), [pacote e munição](../EXACT-RAYGUN-PACKET-AMMO-1.0.10.json), [receptor](../EXACT-RAYGUN-RECEIVER-1.0.10.json), [ficha de dano](../damage-types/raygun.md) |

Os manifestos anteriores permanecem intactos. **Nesta certificação houve nova execução do JAR publisher exato em GitHub Actions**, com revalidação do SHA-1, SHA-256, tamanho, hash do `RaygunItem` e registry, leitura de `energy_efficiency.json` e `enchantable/raygun.json`, métodos JVM, 57 branches diretos e selo individual [Energy Efficiency](../EXACT-ENERGY-EFFICIENCY-CAUSAL-1.0.10.json). A inspeção local fora da CI tem bloqueio DNS, sem prejuízo do resultado reproduzível da CI. Nenhum teste físico do modpack foi executado.

## 2. JSON físico e elegibilidade — publisher 1.0.10

O ZIP exato possui o recurso `data/alexscaves/enchantment/energy_efficiency.json`, SHA-256 `c5771a00e6dd2dd0a693369a110a943354b074dde27b9f3c9d1dcb4a8440cf3a`; e `data/alexscaves/tags/item/enchantable/raygun.json`, SHA-256 `8e7cb71ff2c706004fba0493f2237e96da3af53dea6e3ae414542b5150cc012d`. A tag física declara somente `alexscaves:raygun`. O varrimento de classfiles pelo token compilado `ENERGY_EFFICIENCY` identificou `ACEnchantmentRegistry.class` e `RaygunItem.class`; caminhos por reflexão ou mixins externos não foram excluídos.

| Campo do publisher | Valor estático verificado |
|---|---|
| `description.translate` | `enchantment.alexscaves.energy_efficiency` |
| `supported_items` | `#alexscaves:enchantable/raygun` |
| `weight` | `10`, peso declarativo; não probabilidade de gasto |
| `max_level` | `3` (I/II/III) |
| `min_cost` | `base=1`, `per_level_above_first=5` (1/6/11) |
| `max_cost` | `base=41`, `per_level_above_first=10` (41/51/61) |
| `anvil_cost` | `1` |
| `slots` | `mainhand` |
| `exclusive_set` | **Ausente** no JSON específico |

Esses custos são do sistema de encantamento, não de mana, combustível ou custo por disparo. A resolução final de tags, encantamento em bigorna, datapacks e níveis forçados não foi validada em jogo. A fonte pública 1.1.1 permanece referência não autoritativa para a versão física 1.0.10.

## 3. Causalidade JVM completa do consumo do Raygun

**Classe:** `com/github/alexmodguy/alexscaves/server/item/RaygunItem.class`, SHA-256 `3fc60cb7ff8be2744becf8ac9e524799349996972708845a124f02650bfb344c`. O método `onUseTick(Level,LivingEntity,ItemStack,int)V` possui **523 instruções JVM** e **57 branches diretos** com alvos verificados; SHA-256 canônico do parse `b037276094928625e501d13fddd11829e3fe5540d585f7d8213f37b098c39bc5`. Foram reconciliados os métodos `hasCharge`, `getCharge` e `setCharge` pelos digests já publicados.

**Entrada e aquecimento:** `onUseTick @0–9` calcula `elapsed=getUseDuration(stack,null)-remainingUseTicks`, armazenado no local inteiro 5. Em `@11–33`, o progresso `f7` é `elapsed/15F` enquanto `elapsed<15`, e **1F** caso contrário. O valor não tem clamp inferior próprio nesse trecho; `getUseDuration` retorna o literal **72000 ticks**. Distância do raio (outros branches) não deve ser confundida com o contador de consumo.

**Guardas anteriores ao débito:** `@139–143` executa `hasCharge(stack)`; o helper retorna verdadeiro enquanto `getCharge(stack)<1000`. Se a carga usada já ultrapassou ou atingiu o limite, o ramo `@146–209` solicita, **no cliente**, `UpdateItemTagMessage` por `sendMSGToServer`, chama `stopUsingItem`, pede som de esgotamento e retorna. Um pacote enviado não certifica identidade do remetente, valor autorizado nem aceitação do estado no servidor.

**Ramo que solicita o gasto:** `@210–214` testa `Level.isClientSide()` e salta diretamente para `@322` no servidor. Assim, toda a sequência `@245–319` de atualização de `ChargeUsed` é **client-side nesse método**. No cliente:

1. `@245–268` lê `ACCompat.enchantLevel(stack,ENERGY_EFFICIENCY)` e calcula, sem clamp próprio, `P(L)=2+floor(1.5F×L)`.
2. `@270–274` exige `f7 >= 1F` (para o fluxo normal: **15 ticks de uso**). `@277–282` exige `elapsed % P(L) == 0`; se não, salta sobre a escrita.
3. `@285–299` ignora o gasto se o usuário for `Player` em Criativo. Entidades `LivingEntity` não-Player não recebem essa isenção no ramo próprio.
4. `@302–319` lê `ChargeUsed`, soma **1**, usa `Math.min(valor+1,1000)` e solicita `setCharge`. O método não prova aceitação/autorização remota desse valor.

| `L` lido do stack | `P(L)`: periodicidade nominal após o aquecimento | Condição de débito |
|---|---:|---|
| 0 — sem encantamento | 2 ticks | `elapsed % 2 == 0` |
| I | 3 ticks | `elapsed % 3 == 0` |
| II | 5 ticks | `elapsed % 5 == 0` |
| III | 6 ticks | `elapsed % 6 == 0` |

**Casos anômalos e riscos:** o JSON limita níveis normais a III, mas `ACCompat.enchantLevel` lê um inteiro sem clamp demonstrado nesse consumidor. Para `L=-1`, a expressão dá `P=0` e a operação `irem @281` pode lançar divisão por zero **se** o caminho cliente alcançar a condição após o aquecimento. Para níveis extraordinários, podem surgir valores inesperados/overflow; não reinterpretar a tabela normal como extrapolação livre. `Math.min(used+1,1000)` aplica apenas teto, não piso zero. A ficha não aprova injeção de níveis nem reescrita desse contador.

**Não é fórmula de dano:** `GAMMA_RAY` é lido mais adiante (começando `@332`); `X_RAY` e ray traces possuem consumidores distintos, incluindo `ProjectileUtil` e `ACCompat.hurt`. O número `1.5F` aqui pertence à multiplicação do **intervalo de gasto**, enquanto outro `1.5F` posterior pode ser operando de dano Raygun, sem relação causal com Energy Efficiency.

## 4. Rede, autoria e autoridade de charge

A inspeção de `RaygunItem` observa `UpdateItemTagMessage` em `onUseTick` e `releaseUsing`. As auditorias de [pacote](../EXACT-RAYGUN-PACKET-AMMO-1.0.10.json), [receptor](../EXACT-RAYGUN-RECEIVER-1.0.10.json) e [ABI de rede](../EXACT-RAYGUN-NETWORK-ABI-1.0.10.json) já localizaram o envelope NeoForge bidirecional e o caminho que seleciona um item em uma das mãos para receber atualização de `CUSTOM_DATA`.

Os guards compilados do receptor conferem entidade, tipo de item, mão e presença de tag; porém **não foi certificado saneamento semântico de `ChargeUsed`**, vínculo do `entityId` à sessão remetente, integridade do `ItemStack`, antirreplay ou execução compatível com todos os mods do pack. Um pacote aceito, animação ou indicador de charge **não comprova** custo autenticado pelo servidor. Não interceptar/reemitir `UpdateItemTagMessage` como substituto de um hook seguro.

O indicador visual do Raygun usa referência a **13** e **1000** em `getBarWidth`; essa barra mede uma representação local do estado do item, não concede autoridade sobre mana ou balanceamento Black Arcana. `PrevUseTime` e `UseTime` pertencem ao estado/animação do equipamento; sua presença não prova uma taxa de gasto.

## 5. Targeting, efeitos e matriz de interoperabilidade

Energy Efficiency não produz uma nova entidade, impacto, hitbox, AOE, escola ou `DamageType` no método auditado. O Raygun é a ação base, com ray traces, seleção e dano nativos. `X_RAY` e `GAMMA_RAY` são encantamentos adjacentes e não devem ter seus parâmetros atribuídos a Energy Efficiency. A ficha [Raygun](../damage-types/raygun.md) mantém **⚠️ partial** para seus próprios eixos ainda não fechados; certificar esta fórmula de consumo não a certifica automaticamente.

| Eixo para perks/Mastery | Contrato da versão 1.0.10 | Boundary e risco |
|---|---|---|
| Intervalo de consumo | `2+floor(1.5×L)`, após 15 ticks; normal 2/3/5/6 | ⛔ Sem mutação de nível/intervalo sem seam real, caps, side e autorização |
| Carga/custos | `ChargeUsed` é **carga usada**, limite comparado 1000; escrita cliente `min(used+1,1000)` | ⛔ Não duplicar gasto, refund, combustível ou segunda mana |
| Duração e cooldown | `getUseDuration=72000` é limite do item em uso, não cooldown de cast | ⛔ Não inventar cooldown/custo por tiro |
| Targeting/range/LOS/AOE | Não alterados pelo ramo de eficiência; caminho nativo do Raygun usa outros controles | ⛔ Não mudar filtros, claims, aliados ou PvP a partir do custo |
| Dano/tipo | `ACDamageTypes.causeRaygunDamage`/`ACCompat.hurt` em consumidor separado; `GAMMA_RAY` participa de ramo próprio | ⛔ O 1.5 de periodicidade não é dano ou multiplicador de dano |
| Projéteis, tamanho, velocidade | Nenhum projétil do encantamento isolado; valores de raio/render do Raygun são externos ao ramo | N/A para Energy Efficiency; downstream do item continua provider-owned |
| Autoria/rede/persistência | ItemStack e `UpdateItemTagMessage`, lado cliente de charge; autorização de receptor não homologada | ⛔ Sem hook mutador seguro e recibo idempotente; bloqueio de replay/pacote |
| Mastery / XP | Atualizações de charge podem se repetir durante um mesmo uso | ⛔ Não contabilizar cada tick/pacote como cast, proc ou vitória confirmada |

**Autoridade:** Alex's Caves mantém o consumo e os efeitos Raygun. Black Arcana continua autoritativo sobre sua própria magia. RPG Skill Tree fornece progressão, atributos, Mastery, perks e gates apenas por adapters/contratos reais, não recebe automaticamente o estado `ChargeUsed`. **`NO_MUTATION` / fail-closed** para qualquer proposta de alteração de eficiência.

## 6. Selo individual, reprodução e pendências

**Contrato estático certificado:** há prova física SHA-exata do JAR, hash de JSON e tag, dois classfiles tokenizados, quatro métodos Raygun com digests e a sequência integral de operandos da região de charge. O selo [`EXACT-ENERGY-EFFICIENCY-CAUSAL-1.0.10.json`](../EXACT-ENERGY-EFFICIENCY-CAUSAL-1.0.10.json) fixa o SHA-256 do relatório canônico `0bb9e77b51908adaf6b679f483c484d5b4da5169cd4cb440e0c7a31b9c6dcfb3`, 57 branches e projeção da fórmula em quatro níveis normais. Ver [sonda SHA-exata](../../../../docs/qa/alexscaves_1010_energy_efficiency_probe.py), [testes negativos](../../../../docs/qa/alexscaves_1010_energy_efficiency_probe_test.py) e workflow `alexscaves-1010-energy-efficiency-causal.yml`.

**Reprodução local, somente read-only, Java 21:**

```sh
python3 docs/qa/alexscaves_1010_energy_efficiency_probe_test.py -v
python3 docs/qa/alexscaves_1010_energy_efficiency_probe.py \
  --jar /caminho/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --javap /caminho/jdk-21/bin/javap \
  --seal 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-ENERGY-EFFICIENCY-CAUSAL-1.0.10.json' \
  --output /tmp/alexscaves-energy-efficiency.json
```

**QA física `NOT_TESTED`:** intervalos medidos no cliente/servidor real, inventário Creative/Survival, carga negativa/excedente, nível anômalo, disponibilidade/recarga com `URANIUM_ROD`, troca de mãos, interrupções e tick delay, divergência C2S, replays, save/reload, sincronização após morte/desconexão, outros mods, `GAMMA_RAY` e `X_RAY`, proteção PvP e claims. Não testar se o receptor valida semanticamente `ChargeUsed` a partir do corpo de `RaygunItem`; isso pertence a outro contrato. Nenhuma linha de QA foi promovida por CI estática.

**Estados:** `individual_static_certification=STATIC_TECHNICAL_CATALOG_ONLY`, `evidence_grade=SHA_EXACT_BINARY_BEHAVIOR`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `network_authorization=NOT_VERIFIED`, `NO_MUTATION`, `provider_universe_closed=false`.

**Contabilidade:** +0 fichas novas, **+1 contrato técnico estático individual certificado**, +0 raízes mágicas, +0 hooks validados, +0 QA física e +0 providers integralmente concluídos. Próximo encantamento **parcial** alfabético: `alexscaves:enveloping_bubble`.
