# Energy Efficiency — consumo de carga do Raygun (publisher 1.0.10)

**Estado:** ⚠️ **ficha individual parcial/condicionada** para `alexscaves:energy_efficiency`. O ID está no inventário dos 51 recursos da versão publisher 1.0.10, e a referência ao encantamento aparece no `RaygunItem.onUseTick` compilado. O controle de carga foi rastreado em manifestos SHA-exatos **parciais**, mas a expressão completa, o JSON físico de encantamento e a validação em jogo **não** foram fechados para esta ficha. `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `perk_certification=NOT_CERTIFIED` · `NO_MUTATION`.

**Descrição funcional, com limite de prova:** o encantamento é consultado durante o uso contínuo do **Raygun** em uma região que também calcula e atualiza a carga usada do item. Sua intenção aparente é alterar o consumo/intervalo de gasto de energia. **Não** há evidência suficiente para atribuir à build 1.0.10 a fórmula completa ou percentuais de economia por nível. O encantamento não constitui uma nova magia, novo tipo de dano ou projétil independente: é um modificador do fluxo do equipamento nativo.

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

Esses manifestos já haviam sido gerados a partir do JAR publisher e validados pelos workflows relacionados. **Nesta revisão não houve nova leitura binária completa do método.** A tentativa de obter novamente o JAR por `edge.forgecdn.net` falhou por resolução DNS no ambiente de trabalho; portanto, não se eleva a precisão das conclusões existentes. Hashes de métodos e offsets são **reutilização de evidência histórica selada**, não resultado de um novo probe.

## 2. Dados declarativos: conhecido versus ainda não equiparado ao publisher

**Confirmado para o publisher 1.0.10:** o inventário exato enumera o recurso `energy_efficiency`; o método `RaygunItem.onUseTick` contém referência simbólica ao campo `ACEnchantmentRegistry.ENERGY_EFFICIENCY` em `@246`. A enumeração de nomes e um callsite **não verificam o JSON físico completo, sua exclusividade, os slots resolvidos ou a disponibilidade efetiva em mesa/bigorna**.

**Fonte pública adjacente, apenas para investigação:** `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara **1.1.1**, não a versão instalada. Nessa fonte, `src/main/resources/data/alexscaves/enchantment/energy_efficiency.json` contém:

| Campo na fonte **1.1.1** | Valor adjacente — **não certificado para 1.0.10** |
|---|---|
| `description.translate` | `enchantment.alexscaves.energy_efficiency` |
| `supported_items` | `#alexscaves:enchantable/raygun` |
| `weight` | 10 |
| `max_level` | 3 |
| `min_cost` | `base=1`, `per_level_above_first=5` |
| `max_cost` | `base=41`, `per_level_above_first=10` |
| `anvil_cost` | 1 |
| `slots` | `mainhand` |
| `exclusive_set` | Não declarado nesse JSON adjacente |

**Não importar esses valores ao contrato do publisher** sem conferir o ZIP `data/alexscaves/enchantment/energy_efficiency.json`, a tag `enchantable/raygun`, seus hashes e a resolução de dados. Peso/custos de encantamento não constituem custo por tick, combustível consumido, mana ou limite de charge.

## 3. Fluxo nativo observado no binário 1.0.10

**Owner:** `RaygunItem.onUseTick`, descritor JVM `(Lnet/minecraft/world/level/Level;Lnet/minecraft/world/entity/LivingEntity;Lnet/minecraft/world/item/ItemStack;I)V`. A [auditoria de controle](../EXACT-RAYGUN-CONTROL-1.0.10.json) registrou 26 métodos declarados no classfile, 18 selecionados e o digest do método acima.

| Região / método | Evidência delimitada da versão exata | O que não comprova |
|---|---|---|
| `onUseTick @246` | Consulta simbólica a `ACEnchantmentRegistry.ENERGY_EFFICIENCY`, com `ACCompat.enchantLevel` na região de consumo | Valor do nível ativo, máximo efetivo, fórmula completa ou execução por tick |
| `onUseTick @246–319` | Região já inventariada com `Math.floor`, `Math.min`, `getCharge`, `setCharge`, limite **1000** e literal **1.5F** | Ordem de todas as condições, taxa de descarga por nível e garantias de lado/autoridade |
| `hasCharge(ItemStack)Z @4` | Compara o valor de `getCharge` com **1000**, deixando de considerar carga disponível no limite observado | Que `ChargeUsed` mede energia restante; a semântica observada é **carga usada** |
| `getCharge` / `setCharge` | Lêem/escrevem `ChargeUsed` via componente/tag do `ItemStack`; leitura ausente tem fallback zero | Persistência, autorização do servidor ou validação de valores anômalos |
| `getUseDuration` | Valor compilado **72000 ticks** | Taxa de consumo, cooldown de arma ou duração obrigatória de ataque |
| `use` / `findAmmo` | Recarga nativa envolve `URANIUM_ROD`, guardas de Creative e possível `shrink(1)`; `setCharge(...,0)` em caminho de recarga | Consumo de uma unidade a cada disparo, recarga incondicional ou custo de mana |

**Sequência causal parcial:** a verificação de carga e os caminhos de `use`/recarga pertencem ao **Raygun**. Energy Efficiency é consultado dentro de `onUseTick`; após esse trecho seguem caminhos próprios de targeting, dano e `GAMMA_RAY`. O método só deve ser interpretado como **equipamento com consumo nativo**, não como `ArcanaCast` com custos transacionais inventados. O literal 1000 é o limite observado do estado `ChargeUsed`; 72000 é a duração máxima do item em uso, **não** um intervalo de consumo.

### Pista da fonte 1.1.1, explicitamente não certificada

O `RaygunItem.java` público na mesma revisão 1.1.1 sugere, **apenas como hipótese para comparação de bytecode**, uma periodicidade candidata `divisor = 2 + floor(level * 1.5)` para uma condição de atualização de `ChargeUsed`, com filtros de tempo de uso e jogador Creative. Naquela **fonte adjacente**, o incremento é limitado ao teto com `Math.min`. Embora a estrutura explique por que `Math.floor`, `1.5F` e `Math.min` aparecem no recorte exato, **coincidência de operandos não certifica expressão, branch, periodicidade, lado de execução ou percentuais na versão publisher 1.0.10**. Proibido usar a fórmula candidata para parametrizar uma perk sem CFG/validação específica do binário instalado.

## 4. Rede, autoria e autoridade de charge

A inspeção de `RaygunItem` observa `UpdateItemTagMessage` em `onUseTick` e `releaseUsing`. As auditorias de [pacote](../EXACT-RAYGUN-PACKET-AMMO-1.0.10.json), [receptor](../EXACT-RAYGUN-RECEIVER-1.0.10.json) e [ABI de rede](../EXACT-RAYGUN-NETWORK-ABI-1.0.10.json) já localizaram o envelope NeoForge bidirecional e o caminho que seleciona um item em uma das mãos para receber atualização de `CUSTOM_DATA`.

Os guards compilados do receptor conferem entidade, tipo de item, mão e presença de tag; porém **não foi certificado saneamento semântico de `ChargeUsed`**, vínculo do `entityId` à sessão remetente, integridade do `ItemStack`, antirreplay ou execução compatível com todos os mods do pack. Um pacote aceito, animação ou indicador de charge **não comprova** custo autenticado pelo servidor. Não interceptar/reemitir `UpdateItemTagMessage` como substituto de um hook seguro.

O indicador visual do Raygun usa referência a **13** e **1000** em `getBarWidth`; essa barra mede uma representação local do estado do item, não concede autoridade sobre mana ou balanceamento Black Arcana. `PrevUseTime` e `UseTime` pertencem ao estado/animação do equipamento; sua presença não prova uma taxa de gasto.

## 5. Targeting, dano e demais eixos de perks

| Eixo | Papel observado do Energy Efficiency | Boundary para perks |
|---|---|---|
| **Consumo / eficiência / frequência** | Referência ao encantamento junto de `floor`, `min` e `ChargeUsed`; fórmula 1.0.10 incompleta | ⛔ Não aplicar multiplicador externo nem alterar `ChargeUsed` sem hook verificado |
| **Mana / combustível / durabilidade** | `URANIUM_ROD` e charge do Raygun são recursos nativos; não há segunda mana no consumidor observado | ⛔ Não introduzir novo settlement ou cobrança duplicada por tick |
| **Alvo / range / área / LOS** | Não foi demonstrado que Energy Efficiency altere os ramos `X_RAY`, ray trace, AABB ou filtros de aliados | ⛔ Manter filtros nativos; qualquer expansão exige auditoria própria |
| **Dano / tipo de dano** | `causeRaygunDamage` e `ACCompat.hurt` aparecem mais tarde em `onUseTick`; `GAMMA_RAY` tem outro ramo | ⛔ Não atribuir 1.5F de eficiência como dano; não duplicar hits nem reclassificar `raygun` |
| **Projétil / hitbox / trajetória** | Raygun usa caminhos de trace e consulta de entidades; não há tamanho/projétil próprio comprovado para este encantamento | N/A na região auditada; ⛔ sem mutação externa |
| **Duração / cooldown** | `getUseDuration=72000`; condição de gasto dependente de uso ainda incompleta | ⛔ Não inferir cooldown, tempo de tiro ou taxa efetiva do consumo |
| **Mastery / perks / autoria** | O Raygun continua produtor do efeito; recepção de estado por rede carece de homologação de autorização | ⛔ Não emitir XP ou proc repetido a cada tick, pacote ou atualização de HUD |

**Causalidade:** os registros de dano, `Irradiated`, `X_RAY` e `GAMMA_RAY` pertencem ao mesmo item, mas são **consumidores distintos**. Energy Efficiency não é uma segunda arma/cast nem uma origem nova de `DamageType`. A ficha [Raygun](../damage-types/raygun.md) continua ⚠️ parcial para dano, targeting, rede e autorização, sem promoção automática pela catalogação deste encantamento.

## 6. Pendências e critérios de aceite

1. Obter o **JAR publisher 1.0.10** pelos fingerprints já registrados e extrair `energy_efficiency.json` e a tag real `enchantable/raygun`; registrar hashes, nível máximo, peso, custos, slots e exclusividades de **1.0.10**.
2. Selar **janela completa e CFG de `onUseTick`** em torno de `@246–319`, incluindo pilha, locais, comparações, frequência, restrição de lado, Creative, valores negativos/anômalos e branches que evitam débito. Não confundir hipótese 1.1.1 com contrato real.
3. Testar nativamente em servidor dedicado/modpack níveis permitidos, nível 0, combinações com `GAMMA_RAY`/`X_RAY`, alteração de stack/mão, recarga, interrupção, save/reload, lag e reconexão; aferir consumo real e aceitação dos pacotes.
4. Homologar **autorização e integridade C2S**, caps de `ChargeUsed`, deduplicação de eventos/XP e coexistência de outros mods antes de permitir alteração por perks.
5. Exigir boundary provider-native, proteção contra replay e respeito à autoridade de cada sistema. Black Arcana continua dono do seu runtime mágico; RPG Skill Tree fornece progressão/Mastery/perks/gates somente por contratos verificados; Enshrouded não recebe controle implícito do item.

**Estado final desta ficha:** `RESOURCE_ID_IN_EXACT_INVENTORY` + `SHA_EXACT_SELECTED_CONSUMER_REFERENCES` + `ADJACENT_SOURCE_NOT_VERSION_EQUIVALENT`. **Sem** fechamento de JSON/CFG integral, hooks mutadores, teste físico, certificação perk-ready, novo spell, Stage promotion ou alteração do JAR. **Contabilidade:** +1 ficha individual **parcial**, +0 fichas certificadas, +0 raízes mágicas, +0 providers fechados. **Próximo recurso alfabético:** `alexscaves:enveloping_bubble`.
