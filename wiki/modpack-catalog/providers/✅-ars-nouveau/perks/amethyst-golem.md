# Ars Nouveau — The Amethyst Golem / Knockback Resistance

**✅ Contrato técnico estático documentado; ⛔ `mutating_hook=NOT_VERIFIED`; ⚠️ `physical_qa=NOT_TESTED`.**

- Registry source: `ars_nouveau:thread_amethyst_golem`; classe `com.hollingsworth.arsnouveau.common.perk.KnockbackResistPerk`.
- Família: Thread / perk de equipamento. Slot mínimo **ONE (valor1)** herdado de IPerk; slot não é tier de glyph ou nível de XP.
- Source: `baileyholl/Ars-Nouveau@112920ff774831f204031da75b4c4e73d3765157`, Ars Nouveau **5.13.1**.

## Contrato individual para perks

| Campo | Evidência e limites |
|---|---|
| Identidade e versão | `ars_nouveau:thread_amethyst_golem`, `KnockbackResistPerk`, presente na [registry de produção][registry] e definido na [classe][perk]. A identidade é source-pinned; nenhuma prova de classfile/registro carregado foi atribuída a este Thread. |
| Comportamento e causalidade | `applyAttributeModifiers` devolve um novo `ItemAttributeModifiers` com resistência a knockback. A ação ocorre na construção dos atributos do item, não em um evento de ataque ou em um tick exclusivo deste Thread. [Classe][perk], [aplicador da armadura][apply]. |
| Parâmetros, operação e caps | S é `PerkInstance.slot.value`; contribuição `0,15 × S` em `Attributes.KNOCKBACK_RESISTANCE`, operação `ADD_VALUE` e ID do modificador `ars_nouveau:thread_amethyst_golem`. S=1/2/3 produz0,15/0,30/0,45 por modificador. A classe não define um cap próprio. Default/range do atributo vanilla e a resolução de IDs repetidos entre peças não foram auditados no source Minecraft neste recorte; não anunciar imunidade ou soma universal. [Slots][slot-values], [classe][perk]. |
| Targeting, dano e duração | O alvo funcional é o portador equipado. Não há seleção de terceiro, área, projétil, DamageType, duração, canalização ou cooldown próprios. No consumidor concreto `EffectKnockback.knockback`, uma entidade viva recebe `strength *= 1 − R`; se a força resultante não for positiva, o helper não aplica seu impulso. Isso não prova que todo caminho que chama `setDeltaMovement` consulte resistência. |
| Custos e aquisição | Enchanting Apparatus, Blank Thread como reagent + **3 itens da tag `c:obsidians`**; saída1 Thread e `sourceCost: 0` no [JSON gerado][recipe]. O efeito passivo não define mana por tick/hit, custo de cast, XP de glyph ou cooldown. Instalação é Ars-owned e consome um item com `stack.split(1)` quando o slot é válido [AlterationTile][alteration]. |
| Integração e autoridade | `IPerk.applyAttributeModifiers` é API nativa real e retorna um novo objeto; o aplicador retém esse retorno. Atributo, equipamento e consumo ficam com Ars/engine. Bridge RPG/Black Arcana para atribuição, fase, caps, remoção e deduplicação permanece não verificada; não implica ausência de API. Black Arcana mantém casting, Corruption, Strain e WorldEffectPolicy próprios; RPG mantém progressão por contrato. |
| Evidência e validação | `claim_scope=STATIC_TECHNICAL_CATALOG_ONLY`, `evidence_grade=PINNED_SOURCE_WITH_RELEASE_SHA_ONLY`. Publisher `ars_nouveau-1.21.1-5.13.1.jar`, SHA-1 `02782d071ee5fab3b5c4b8ced67b7e1748277dfd`, é proveniência de release; a auditoria dos109 IDs cobre85 glyphs+24 rituais e não prova este Thread. Source imutável e referências abaixo; config instalada, equivalência de métodos Java/bytecode e modpack físico não testados. |

## Equipamento, slots e persistência

`ArmorPerkHolder` serializa perks, tier e tags no [componente persistente `ARMOR_PERKS`][component]; seu getter ordena slots do maior para o menor. `IPerkHolder.getPerkInstances` emparelha a lista de perks com os slots disponíveis. `AnimatedMagicArmor.getDefaultAttributeModifiers` percorre **cada instância** e passa seu slot ao método da perk; este caminho não usa `PerkUtil.countForPerk`, que calcula o maior slot para outros consumidores [holder][holder], [ordenação][slot-order], [instâncias][instances], [aplicação][apply], [max versus lista][max-versus-all].

O ID do modificador é fixo por perk, sem sufixo do slot/peça. Não há prova aqui de que repetir o Thread resulte numa soma de todos os valores entre equipamentos. O listener de troca de armadura executa no servidor, avisa sobre duplicação e seleciona callbacks de adição/remoção, mas não reescreve o componente para retirar o perk duplicado. Estas quatro classes não implementam estado temporal ou callbacks próprios de equip/unequip; a combinação e retirada dos atributos precisam seguir a infraestrutura nativa, sem um segundo ledger de bônus [evento][equip].

A instalação valida o mínimo do slot e limita a lista ao número de slots/ao teto3 no tile; slots1/2/3 não equivalem à quantidade de cópias equipadas. Ser uma implementação registrada não autoriza ignorar o provider de slots de uma peça externa [gates][slots], [AlterationTile][alteration], [matriz de providers](../systems/perk-slot-providers.md).

### Consumidor de força e limite de interpretação

O [helper de Knockback][knockback] lê o atributo da vítima, reduz a força e só então altera movimento horizontal/vertical; o teto vertical0,4 desse helper pertence ao Effect, não ao Thread. Entidades não vivas não recebem essa leitura. Com apenas esta contribuição e sem outros modificadores, S=1 reduz a força desse caminho para85% da força inicial; isso é um exemplo condicionado, não uma garantia de knockback final no modpack. O ramo de blocos cria falling blocks, que seguem outro tipo de entidade.

Não duplicar a resistência ao traduzir dano, hazards ou deslocamento para Black Arcana: observar o atributo/caminho efetivamente usado. Aumentar range, mudar target para área ou atribuir resistência a uma entidade sem atributo válido exige outro contrato; esses controles não são parâmetros desta classe.

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
[perk]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/perk/KnockbackResistPerk.java#L13-L35
[knockback]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/main/java/com/hollingsworth/arsnouveau/common/spell/effect/EffectKnockback.java#L51-L93
[recipe]: https://github.com/baileyholl/Ars-Nouveau/blob/112920ff774831f204031da75b4c4e73d3765157/src/generated/resources/data/ars_nouveau/recipe/thread_amethyst_golem.json#L1-L23
