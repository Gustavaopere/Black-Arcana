# Ars Nouveau — Magic Capacity

**✅ Contrato técnico estático documentado; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.**

- Registry source: `ars_nouveau:thread_magic_capacity`; classe `com.hollingsworth.arsnouveau.common.perk.MagicCapacityPerk`.
- Família: Thread / perk de equipamento. Slot mínimo **ONE (valor1)** herdado de IPerk; slot não é tier de glyph ou nível de XP.
- Source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, Ars Nouveau **5.13.1**.

## Contrato individual para perks

| Campo | Evidência e limites |
|---|---|
| Identidade e versão | `ars_nouveau:thread_magic_capacity`, `MagicCapacityPerk`, presente na [registry de produção][registry] e definido na [classe][perk]. A identidade é source-pinned; nenhuma prova de classfile/registro carregado foi atribuída a este Thread. |
| Comportamento e causalidade | `applyAttributeModifiers` acrescenta o multiplicador de capacidade ao item. A classe não chama `setMana`, não regenera nem transfere mana. O efeito depende do cálculo Ars que transforma o atributo em limite da capability. [Classe][perk], [aplicador da armadura][apply]. |
| Parâmetros, operação e caps | S é `PerkInstance.slot.value`; contribuição `0,1 × S` em `PerkAttributes.MAX_MANA`, operação `ADD_MULTIPLIED_TOTAL` e ID do modificador `ars_nouveau:thread_magic_capacity`. S=1/2/3 gera contribuição0,1/0,2/0,3 para ADD_MULTIPLIED_TOTAL. O atributo Ars é syncable, default0 e range0…10000; registry source `ars_nouveau:ars_nouveau.perk.max_mana`. O Thread não define cap adicional, preenchimento imediato ou desconto de cast. [Slots][slot-values], [classe][perk]. |
| Targeting, dano e duração | Portador com atributo/capability Ars; sem target, dano, raio, projétil ou duração próprios. A capacidade é de mana de jogador, separada de Source de mundo. Reserva, eventos e casts continuam no provider, não são um segundo pool Black Arcana. |
| Custos e aquisição | Enchanting Apparatus, Blank Thread como reagent + **3 `ars_nouveau:sourceberry_bush` +3 `ars_nouveau:magebloom`**; saída1 Thread e `sourceCost: 0` no [JSON gerado][recipe]. O efeito passivo não define mana por tick/hit, custo de cast, XP de glyph ou cooldown. Instalação é Ars-owned e consome um item com `stack.split(1)` quando o slot é válido [AlterationTile][alteration]. |
| Integração e autoridade | `IPerk.applyAttributeModifiers` é API nativa real e retorna um novo objeto; o aplicador retém esse retorno. Atributo, equipamento e consumo ficam com Ars/engine. Bridge RPG/Black Arcana para atribuição, fase, caps, remoção e deduplicação permanece não verificada; não implica ausência de API. Black Arcana mantém casting, Corruption, Strain e WorldEffectPolicy próprios; RPG mantém progressão por contrato. |
| Evidência e validação | `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`, `evidence_grade=PINNED_SOURCE_WITH_RELEASE_SHA_ONLY`. Publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`, é proveniência de release; a auditoria dos109 IDs cobre85 glyphs+24 rituais e não prova este Thread. Source imutável e referências abaixo; config instalada, equivalência de métodos Java/bytecode e modpack físico não testados. |

## Equipamento, slots e persistência

`ArmorPerkHolder` serializa perks, tier e tags no [componente persistente `ARMOR_PERKS`][component]; seu getter ordena slots do maior para o menor. `IPerkHolder.getPerkInstances` emparelha a lista de perks com os slots disponíveis. `AnimatedMagicArmor.getDefaultAttributeModifiers` percorre **cada instância** e passa seu slot ao método da perk; este caminho não usa `PerkUtil.countForPerk`, que calcula o maior slot para outros consumidores [holder][holder], [ordenação][slot-order], [instâncias][instances], [aplicação][apply], [max versus lista][max-versus-all].

O ID do modificador é fixo por perk, sem sufixo do slot/peça. Não há prova aqui de que repetir o Thread resulte numa soma de todos os valores entre equipamentos. O listener de troca de armadura executa no servidor, avisa sobre duplicação e seleciona callbacks de adição/remoção, mas não reescreve o componente para retirar o perk duplicado. Estas quatro classes não implementam estado temporal ou callbacks próprios de equip/unequip; a combinação e retirada dos atributos precisam seguir a infraestrutura nativa, sem um segundo ledger de bônus [evento][equip].

A instalação valida o mínimo do slot e limita a lista ao número de slots/ao teto3 no tile; slots1/2/3 não equivalem à quantidade de cópias equipadas. Ser uma implementação registrada não autoriza ignorar o provider de slots de uma peça externa [gates][slots], [AlterationTile][alteration], [matriz de providers](../systems/perk-slot-providers.md).

### Cálculo consumido e atualização

[`ManaUtil.calcMaxMana`][mana-calc] calcula `raw = baseMax + glyphBonus×glyphmax + bookTier×tierMax`; os defaults são **100**, **15** e **50** [config][mana-config]. Insere ou substitui o modificador aditivo transitório `ars_nouveau:max_mana_mod` quando esse raw muda, depois lê `MAX_MANA`. Assim a base0 declarada do atributo não significa que a perk sempre multiplica zero. Armadura adiciona separadamente30×(tier+1) e outros itens podem contribuir; não atribuir todo bônus ao Thread.

O valor é convertido para int antes de [`MaxManaCalcEvent`][max-event]; o resolver relê `getMax/getReserve` e `getRealMax` devolve `int(Max×(1−Reserve))`. O evento tem setters reais, mas não constitui uma bridge RPG já validada. [`ManaCapEvents`][mana-tick] recalcula no servidor no intervalo configurado (default5 ticks), atualiza max/reserve e sincroniza; mana corrente é adicionada/clampada por operações de [`ManaCap`][mana-cap], não por este Thread. Mudar o máximo não é um cast nem um depósito instantâneo garantido.

Defaults não são configuração instalada. Não somar outro bônus de10% no RPG após ler o máximo já calculado; também não aplicar o fator sobre mana corrente ou Source por analogia.

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
[perk]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/perk/MagicCapacityPerk.java#L13-L34
[attributes]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/perk/PerkAttributes.java#L19-L28
[mana-calc]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/util/ManaUtil.java#L52-L101
[mana-config]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/setup/config/ServerConfig.java#L35-L45
[max-event]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/api/event/MaxManaCalcEvent.java#L11-L36
[mana-tick]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/event/ManaCapEvents.java#L20-L47
[mana-cap]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/capability/ManaCap.java#L26-L61
[curio]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/items/curios/AbstractManaCurio.java#L17-L31
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/generated/resources/data/ars_nouveau/recipe/thread_magic_capacity.json#L1-L32
