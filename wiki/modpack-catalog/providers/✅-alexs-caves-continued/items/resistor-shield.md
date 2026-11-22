# Resistor Shield — escudo de Alex's Caves

**Estado:** ⚠️ **PARCIAL — identidade e encantabilidade documentadas**, sem contrato estático individual completo. `static_contract=NOT_CERTIFIED` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION` · provider `OPEN`. A catalogação deste item adiciona **uma ficha observada**, mas **nenhum cast, certificado ou hook**.

## Identidade, versão, autoridade e descrição

- **Nome editorial:** Resistor Shield. **Item ID da versão exata:** `alexscaves:resistor_shield`; campo `ACItemRegistry.RESISTOR_SHIELD`. Não presumir tipo de dano, redução, propriedades elétricas ou mecânica de shield apenas pelo nome.
- **Factory nativa:** `com/github/alexmodguy/alexscaves/server/item/ACItemRegistry.lambda$static$20:()Lnet/minecraft/world/item/Item;`, que referencia `new com/github/alexmodguy/alexscaves/server/item/ResistorShieldItem`; **Code SHA-256 do corpo da factory** `6be6cb4de8570768436590ecdd12cfd11e44f1c9b8e76b7eb58a324d6b4d63ce` (não é o SHA das instruções resolvidas), bootstrap offset `650` no escopo auditado de `ACItemRegistry`. **Contrato da factory não prova o resultado do registro na engine**, nem certifica todo o item.
- **Provider físico:** Alex's Caves Continued, `alexscaves` **1.0.10**, Minecraft **1.21.1**, **NeoForge**, Java **21**. O [registro da modlist sibling](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/main/PROJECT-INSTRUCTIONS/modlist/World%20Gen/%E2%9C%85-alexs-caves-continued%20v1.0.10.md) identifica `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`; JAR publisher auditado nos suportes anteriores SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, **75.279.314 bytes**, **1.555 classfiles**. A comparação física do JAR da instância com esse publisher e o teste do bootstrap são **NOT_VERIFIED** nesta etapa.
- **Hierarquia publisher verificada:** `ResistorShieldItem.class`, SHA-256 `ffd3fddd74f8d44049886e9013de2e3d67cbd2a721015369175e8442c5044741`, **estende `net.minecraft.world.item.ShieldItem`** e declara `ACClientExtensionItem`, `ACEnchantableItem`, `ACRepairableItem` e `ACTickingItem` como interfaces diretas. Isso comprova herança/declaração, **não** o resultado efetivo de bloqueios, ticks, reparos e client callbacks. Requer exame da implementação herdada e dos overrides no JAR exato.
- **Descrição funcional derivada do escopo certificado:** é um item do tipo `ShieldItem` com contrato de consulta de encantabilidade `ACEnchantableItem`. Efeitos de defesa, absorção, eletricidade, redirecionamento, ataques ou bloqueio ainda não foram provados no bytecode específico nem no gameplay e **não são atribuídos aqui**.
- **Manifesto desta ficha parcial:** [identidade de classe, interfaces e dois métodos pinados no JAR 1.0.10](../EXACT-RESISTOR-SHIELD-PARTIAL-EVIDENCE-1.0.10.json), com todos os demais efeitos e consumers explicitamente pendentes.

**Provas reutilizadas, sem transferir selo:** [item registry](../systems/item-registry.md), [contrato SHA-exato de registro](../EXACT-ITEM-REGISTRY-CONTRACT-1.0.10.md), [interface ACEnchantableItem](../systems/enchantable-item.md) e [contrato SHA-exato dessa interface](../EXACT-ENCHANTABLE-ITEM-CONTRACT-1.0.10.md). São contratos de suporte **✅ em seus limites**, não um certificado de `ResistorShieldItem`.

## Ativação e condições comprovadas

**Encantabilidade local:** a auditoria individual anterior da interface `ACEnchantableItem` identificou `ResistorShieldItem` entre **13 implementadores diretos** na versão publisher. O método `getEnchantmentValue()I` retorna literalmente **1**, com duas instruções; `isEnchantable(ItemStack)Z` contém a guarda **`stack.getCount()==1`**. Isso se aplica à consulta de elegibilidade. O inteiro `1` **não** é o nível do encantamento, potência, dano, chance de proc, custo de XP nem índice Mastery.

**Prova bytecode pré-existente, extraída do publisher:** o relatório nativo da [CI #44312413309](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44312413309), job `134829679393`, contém `report.json` (97.832 bytes, SHA-256 `d34a655d06d65a771ea9237ef222635e159ffcfa6fe8b454ee6826ee14979e73`). Nesse relatório, `getEnchantmentValue()I`: `iconst_1 @0` → `ireturn @1`, **2 instruções**, code SHA `95ef737cd8a13db65e3eb3c18e8816a5179dcbdf341309522ab00e95d5aae6d2`, instruction SHA `d943c5fe0bd38038ce70963c73b8759ba3d76c8c00d31c1a2141268dc4e0ee0a`. `isEnchantable(ItemStack)Z`: `ItemStack.getCount() @1`, `iconst_1 @4`, `if_icmpne 12 @5`, `true/false` → retorno, **8 instruções**; code SHA `c1c39189ff601291bec7533e758094d6e935147c1308db53adfe374b3a117a58`, instruction SHA `9cd84b0255be269f2bf50fce0095c14fa5d484831fd35063e71f4c9814aa6b4f`. Esses hashes e a classe completa pertencem ao **mesmo publisher 1.0.10**, não a uma reconstrução em outra versão. O arquivo verifica **somente os dois métodos de interface selecionados**, não os demais overrides.

**Gates externos diferentes:** `ItemStack.isEnchantable()` considera componentes de encantamentos; `IItemExtension.supportsEnchantment`, `isPrimaryItemFor`, mesa e bigorna possuem regras próprias documentadas na prova de suporte. Uma stack elegível pela guarda local pode ainda ser recusada em outros gates. Os 51 encantamentos do provider são objetos distintos e não são acrescidos neste item.

**Gatilhos de defesa/uso:** `use`, `useOn`, ataque recebido, `getUseAnimation`, `getUseDuration`, `inventoryTick`, efeitos ativos/passivos, condicionais de equipamento, guardas client/server, ataque/block events, callbacks de proteção e critério de cancelamento: **NÃO VERIFICADOS para `ResistorShieldItem`**. É incorreto inferir que o comportamento nativo equivale ao `ShieldItem` vanilla sem confirmar hierarquia e overrides físicos. Nenhuma ordem de execução de bloqueio ou cooldown foi certificada.

## Efeitos, parâmetros, danos e custos

| Campo técnico | Situação nesta ficha |
|---|---|
| Targeting | ⚠️ **NÃO VERIFICADO** para mecânica defensiva/ofensiva; não presumir um alvo ou raio |
| Tipo, valor e fonte de dano | ⚠️ **NÃO VERIFICADOS**; não presumir que o item inflige dano |
| Redução/mitigação de dano, ângulo de bloqueio e knockback | ⚠️ **NÃO VERIFICADOS**; nome e herança aparente não estabelecem fórmula |
| AOE, partículas, projéteis, entidades invocadas | ⚠️ **NÃO VERIFICADOS**; presença ou ausência exige inspeção dos métodos |
| Duração, use ticks, cooldown, recarga | ⚠️ **NÃO VERIFICADOS** |
| Durabilidade, stack size, custo de reparo/uso, mana, XP | ⚠️ **NÃO VERIFICADOS** para o item, exceto o **count == 1** como condição de consulta de encantabilidade, **não como débito** |
| Fórmulas/multiplicadores de defesa/atributos/efeitos | ⚠️ **NÃO VERIFICADOS** |
| Valor retornado por `getEnchantmentValue()` | **1**, escopo da interface e owner auditado, não nível do enchant |
| `isEnchantable(stack)` local | **`stack.getCount()==1`**, sem certificar aceite final por mesa ou bigorna |
| Ownership, multiplayer, side, permissões, PvP | ⚠️ **NÃO VERIFICADOS** |
| Persistência, NBT, componentes, transição de dimensão, death/drop | ⚠️ **NÃO VERIFICADOS** |

## Grafo de classes, consumidores e recursos

**Provenientes da auditoria já certificada de suporte:** a classe declara superclasse `ShieldItem` e quatro interfaces diretas (client extension, encantabilidade, reparo e tick); o relatório nativo de encantabilidade trouxe fingerprints de **dois** métodos selecionados. `ACItemRegistry.RESISTOR_SHIELD` → factory `lambda$static$20` → `ResistorShieldItem`; `ResistorShieldItem` implementa `ACEnchantableItem` e expõe `getEnchantmentValue()I` / `isEnchantable(ItemStack)Z`. No roster da auditoria de encantabilidade, foram observados **2 recursos JSON relacionados a esse item**, mas sua identidade completa, conteúdo e semântica não foram identificados individualmente por esta ficha.

**Auditoria física própria em andamento:** [sonda SHA-exata da classe](../../../../../docs/qa/alexscaves_1010_resistor_shield_discovery.py), [gate fail-closed](../../../../../docs/qa/alexscaves_1010_resistor_shield_discovery_checks.py), [workflow](../../../../../.github/workflows/alexscaves-1010-resistor-shield-discovery.yml), PR #1148. A sonda deverá enumerar **todos os métodos executáveis declarados, assinatura JVM, code hash/instruction hash, campos, superclasse/interfaces, ancestrais e descendentes no JAR, owners com referências tipadas, bodies consumidores e recursos filename-matched**. Esses dados ainda **não constam de um censo completo e individual verificado de ResistorShield**; a prova restrita dos dois métodos de encantabilidade acima não supre a auditoria de todos os overrides e seus efeitos.

**Boundary externo:** o contrato de `ACEnchantableItem` é um **suporte de elegibilidade**. Não representa hook mutador por jogador no ponto de impacto, bloqueio, escudo ou buff. O código físico da classe pode chamar sistemas de eventos/atributos/entidades que precisam de fichas e provas próprias.

## Interoperabilidade, Mastery e design futuro

Candidatos conceituais para perks: alterar parâmetros de mitigação, condições de proteção, custo/durabilidade ou vantagens defensivas. Todos são **HIPÓTESES**, condicionadas à descoberta de mecânicas reais e a um boundary seguro por jogador. **Nenhuma API/hook mutador do Resistor Shield foi verificada.** Não alterar `getEnchantmentValue` globalmente a partir do rank de um player sem prova de contexto/authority e compatibilidade com o provider. Não duplicar eventos de dano, settlement de recursos ou procs do escudo.

Black Arcana continua autoridade do runtime mágico; RPG Skill Tree é apenas provider de progressão/perks/gates quando a boundary real existir. Integrações inseguras devem encerrar em `NO_MUTATION` / fail-closed.

## Certificação, reprodução e pendências

**Evidência positiva:** JAR publisher 1.0.10 autenticado nas auditorias anteriores de `ACItemRegistry` e `ACEnchantableItem`; binding `RESISTOR_SHIELD` e os dois métodos de encantabilidade foram documentados e certificados **somente no escopo de suporte**, com hashes nos manifestos já integrados. A auditoria específica do owner `ResistorShieldItem` ainda aguarda seu próprio relatório integral, consumers tipados e hashes dos demais métodos, replay do gate, análise dos ramos e CI completa da HEAD final. **Não contar como contrato estático individual certificado.**

**Próximos gates:** obter `report.json` do workflow da PR #1148; conferir SHA/size do arquivo e de seu JAR, enumerar métodos/consumers, inspecionar bytecode relevante, abrir JSONs associados, identificar fórmula e parâmetros de eventual defesa/dano, verificar side e lifecycle, criar manifesto SHA-exato, completar dossiê causal e submeter validadores. Depois revisar índices e CI integral. Qualquer QA de shield no cliente/servidor real, integração com hit/hurt eventos e outros mods permanece pendente.

`static_contract=NOT_CERTIFIED; mutating_hook=NOT_VERIFIED; physical_qa=NOT_TESTED; mutation=NO_MUTATION; magic_roots_delta=0; provider_universe_closed=false`.
