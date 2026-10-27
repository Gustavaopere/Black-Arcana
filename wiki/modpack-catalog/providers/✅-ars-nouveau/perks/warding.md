# Ars Nouveau — Warding

**✅ Contrato técnico estático documentado; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.**

- Registry source: `ars_nouveau:thread_warding`; classe `com.hollingsworth.arsnouveau.common.perk.MagicResistPerk`.
- Família: Thread / perk de equipamento. Slot mínimo **ONE (valor1)** herdado de IPerk; slot não é tier de glyph ou nível de XP.
- Source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, Ars Nouveau **5.13.1**.

## Contrato individual para perks

| Campo | Evidência e limites |
|---|---|
| Identidade e versão | `ars_nouveau:thread_warding`, `MagicResistPerk`, presente na [registry de produção][registry] e definido na [classe][perk]. A identidade é source-pinned; nenhuma prova de classfile/registro carregado foi atribuída a este Thread. |
| Comportamento e causalidade | O equipamento gera WARDING; `EventHandler.entityHurt(LivingDamageEvent.Pre)` consulta o valor da vítima e reduz o dano no container. O Thread não cancela diretamente evento, não produz uma barreira/entidade e não altera armor vanilla por si. [Classe][perk], [aplicador da armadura][apply]. |
| Parâmetros, operação e caps | S é `PerkInstance.slot.value`; contribuição `2 × S` em `PerkAttributes.WARDING`, operação `ADD_VALUE` e ID do modificador `ars_nouveau:thread_warding`. S=1/2/3 gera+2/+4/+6 no atributo syncable; default0 e range0…1024. Registry source `ars_nouveau:ars_nouveau.perk.warding`. A classe não oferece percentual, consumo por hit, tempo de recarga ou cap próprio além do atributo. [Slots][slot-values], [classe][perk]. |
| Targeting, dano e duração | Entidade portadora/vítima com atributo e dano cuja fonte satisfaz `net.neoforged.neoforge.common.Tags.DamageTypes.IS_MAGIC`. É tag, não somente o DamageType vanilla `MAGIC`, e seus membros efetivos podem ser alterados por datapacks. Sem alcance, área, projétil ou duração próprios; dano sem essa tag não passa por esta subtração. |
| Custos e aquisição | Enchanting Apparatus, Blank Thread como reagent + **8 `ars_nouveau:magebloom_fiber`**; saída1 Thread e `sourceCost: 0` no [JSON gerado][recipe]. O efeito passivo não define mana por tick/hit, custo de cast, XP de glyph ou cooldown. Instalação é Ars-owned e consome um item com `stack.split(1)` quando o slot é válido [AlterationTile][alteration]. |
| Integração e autoridade | `IPerk.applyAttributeModifiers` é API nativa real e retorna um novo objeto; o aplicador retém esse retorno. Atributo, equipamento e consumo ficam com Ars/engine. Bridge RPG/Black Arcana para atribuição, fase, caps, remoção e deduplicação permanece não verificada; não implica ausência de API. Black Arcana mantém casting, Corruption, Strain e WorldEffectPolicy próprios; RPG mantém progressão por contrato. |
| Evidência e validação | `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`, `evidence_grade=PINNED_SOURCE_WITH_RELEASE_SHA_ONLY`. Publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`, é proveniência de release; a auditoria dos109 IDs cobre85 glyphs+24 rituais e não prova este Thread. Source imutável e referências abaixo; config instalada, equivalência de métodos Java/bytecode e modpack físico não testados. |

## Equipamento, slots e persistência

`ArmorPerkHolder` serializa perks, tier e tags no [componente persistente `ARMOR_PERKS`][component]; seu getter ordena slots do maior para o menor. `IPerkHolder.getPerkInstances` emparelha a lista de perks com os slots disponíveis. `AnimatedMagicArmor.getDefaultAttributeModifiers` percorre **cada instância** e passa seu slot ao método da perk; este caminho não usa `PerkUtil.countForPerk`, que calcula o maior slot para outros consumidores [holder][holder], [ordenação][slot-order], [instâncias][instances], [aplicação][apply], [max versus lista][max-versus-all].

O ID do modificador é fixo por perk, sem sufixo do slot/peça. Não há prova aqui de que repetir o Thread resulte numa soma de todos os valores entre equipamentos. O listener de troca de armadura executa no servidor, avisa sobre duplicação e seleciona callbacks de adição/remoção, mas não reescreve o componente para retirar o perk duplicado. Estas quatro classes não implementam estado temporal ou callbacks próprios de equip/unequip; a combinação e retirada dos atributos precisam seguir a infraestrutura nativa, sem um segundo ledger de bônus [evento][equip].

A instalação valida o mínimo do slot e limita a lista ao número de slots/ao teto3 no tile; slots1/2/3 não equivalem à quantidade de cópias equipadas. Ser uma implementação registrada não autoriza ignorar o provider de slots de uma peça externa [gates][slots], [AlterationTile][alteration], [matriz de providers](../systems/perk-slot-providers.md).

### Ordem do consumidor e resultado efetivo

O [listener][mitigation] parte de `container.getNewDamage()`, aplica primeiro os acréscimos de Shocked/Hex e a redução condicional de Defence; depois, se a fonte está em `IS_MAGIC`, subtrai WARDING. O caso FALL aplica ainda Feather e o final usa `container.setNewDamage(max(0,amount))`. Logo `final=max(0,current−WARDING)` descreve só o trecho sem outros ramos, não toda a engine de dano. A classe não faz teste local de lado servidor, prioridade customizada ou controle dos listeners de outros mods; a execução/ordem global precisa de QA.

[`PerkUtil.valueOrZero`][attribute-read] devolve0 quando o atributo não existe. Não inferir que uma entidade arbitrária recebe o atributo automaticamente: o registro Ars adiciona os atributos somente ao tipo PLAYER neste recorte [registro][attributes]. A existência de um modifier no item não prova que um receptor sem atributo possa consumi-lo.

Para novas perks, usar a fonte/tag e o valor efetivamente consumidos. Não subtrair novamente uma cópia de Warding depois que Ars já alterou o container, nem converter os pontos em uma porcentagem genérica de Arcane Danger.

## Validade

O ✅ cobre a documentação estática do recorte. Mudança de release, configuração, registry, item de armadura, atributos, recipes, tags ou listeners exige reauditoria. Persistência real após unload/reload, equip/unequip, servidor/cliente e combinação com addons permanecem pendentes; `mutating_hook=NOT_VERIFIED` e `physical_qa=NOT_TESTED`. Nenhuma perk RPG, magia, adapter, limite executável ou Stage foi implementado por esta ficha.

[registry]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/APIRegistry.java#L166-L185
[native-map]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/registry/PerkRegistry.java#L19-L49
[slots]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/IPerk.java#L26-L74
[slot-values]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/PerkSlot.java#L29-L36
[instances]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/IPerkHolder.java#L19-L28
[holder]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/ArmorPerkHolder.java#L16-L21
[component]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/registry/DataComponentRegistry.java#L19-L28
[slot-order]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/data/ArmorPerkHolder.java#L54-L67
[apply]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/armor/AnimatedMagicArmor.java#L112-L125
[equip]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/PerkEvents.java#L37-L85
[alteration]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/block/tile/AlterationTile.java#L99-L150
[max-versus-all]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/PerkUtil.java#L50-L82
[perk]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/perk/MagicResistPerk.java#L13-L34
[attributes]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/PerkAttributes.java#L19-L54
[mitigation]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/EventHandler.java#L259-L300
[attribute-read]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/PerkUtil.java#L26-L33
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/generated/resources/data/ars_nouveau/recipe/thread_warding.json#L1-L38
