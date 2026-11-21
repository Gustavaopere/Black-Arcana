# Hazmat Armor — auditoria causal SHA-exata do JAR 1.0.10

**Estado:** ⚠️ descoberta estática do owner e de seus consumidores diretos, **quatro contratos individuais PARCIAIS**. `STATIC_DISCOVERY_ONLY`, `NO_MUTATION`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `provider_universe_closed=false`. São **quatro itens de armadura**, **zero novos feitiços/casts**. Não há aprovação de perk executável.

## 1. Identidade, reprodução e limite de fonte

A autoridade da modlist sibling `PROJECT-INSTRUCTIONS/modlist/World Gen/✅-alexs-caves-continued v1.0.10.md` registra `alexscaves` **1.0.10**, Minecraft **1.21.1**, **NeoForge**, Java **21**, `alexscaves-1.0.10-neoforge+1.21.1.jar`, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`. O JAR publisher auditado contém **75.279.314 bytes**, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. **Comparação nova com dump local instalado: NOT_VERIFIED**.

Owner `com/github/alexmodguy/alexscaves/server/item/HazmatArmorItem.class`: SHA-256 `289395b93a1a223f2e66a02528ccb4ce3a1a659dd9c82ac071a5b63c32b1c7cb`. O censo tipado conferiu **1.555 classes**, seis métodos executáveis do owner, sete owners consumidores tipados e 28 JSONs com nome contendo hazmat, incluindo decoração de blocos (não contabilizada como armadura).

Reprodução: [sonda read-only](../../../../docs/qa/alexscaves_1010_hazmat_armor_discovery.py), [checker](../../../../docs/qa/alexscaves_1010_hazmat_armor_discovery_checks.py), [workflow](../../../../.github/workflows/alexscaves-1010-hazmat-armor-discovery.yml), [manifesto](EXACT-HAZMAT-ARMOR-DISCOVERY-1.0.10.json), [run #44942542829](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44942542829), job `136962692502` PASS no probe/checker negativo; artefato `14722536050`; `report.json` SHA-256 `3ef6aeeeb37e0768e206b0777d7193a5ac55a0732ff06d568573c3edf923a033`. O manifesto fixa cada método e consumidor sem copiar código-fonte proprietário. Não tratar esse PASS como certificado de gameplay.

## 2. Quatro itens de equipamento e configuração compartilhada

| Resource ID | Slot por registry | Ficha individual |
|---|---|---|
| `alexscaves:hazmat_mask` | `ArmorItem.Type.HELMET` / `EquipmentSlot.HEAD` | [Hazmat Mask](items/hazmat-mask.md) |
| `alexscaves:hazmat_chestplate` | `ArmorItem.Type.CHESTPLATE` / `EquipmentSlot.CHEST` | [Hazmat Chestplate](items/hazmat-chestplate.md) |
| `alexscaves:hazmat_leggings` | `ArmorItem.Type.LEGGINGS` / `EquipmentSlot.LEGS` | [Hazmat Leggings](items/hazmat-leggings.md) |
| `alexscaves:hazmat_boots` | `ArmorItem.Type.BOOTS` / `EquipmentSlot.FEET` | [Hazmat Boots](items/hazmat-boots.md) |

O material nativo `HAZMAT_SUIT_ARMOR_MATERIAL` foi auditado separadamente em [armor-material](systems/armor-material.md): nome `hazmat_suit`, multiplicador de durabilidade **20**; por **ordinal, ainda sem atribuir número a slot**, defesa `[2,4,5,2]` e durabilidade `[260,300,320,220]`; encantabilidade **25**; toughness **0.5F**; resistência a knockback **0F**; reparo associado a `alexscaves:polymer_plate` no `ACItemRegistry.setup`. A criação usa `material.vanilla()`, `material.properties(new Item.Properties(), type)`, `ArmorItem.<init>`; nenhum dos três constrói imunidade por si só. O mapeamento exato de ordinais do enum externo e a aplicação final de armadura/mitigação pela engine permanecem **NÃO VERIFICADOS**.

## 3. Métodos executáveis próprios — todas as entradas de Code

| Método | Instruções | SHA-256 da sequência de instruções |
|---|---:|---|
| `<init>(ACArmorMaterial,ArmorItem.Type)` | 12 | `1c59bef51bc767350a0f79f732eac8355d4c7b6c50b864e6b32197f3a1efabf2` |
| `acArmorTick(ItemStack,Level,Player)` | 158 | `22ce403cc27b77fdb9bfd3402b4afca95eb648290b199f789b9246da65ddd681` |
| `acInventoryTick(ItemStack,Level,Entity,boolean)` | 16 | `ff0bae8a454ba4b5d2f7c0b48a721c45b59e1fc148e9d8f1189b36adf283b0b1` |
| `getArmorTexture(ItemStack,Entity,EquipmentSlot,String)` | 7 | `ab8baef0e1005980872d21af13f7663eadcded42438f6e246db866f4b772aa81` |
| `getWornAmount(LivingEntity)` | 40 | `d546af06a43f1aa99eee96014438b2679d3dda44b33dffdd7b73aacbc7400c69` |
| `initializeClient(Consumer)` | 6 | `241b312ebd6ff1e8ab0719a7fcbfd71c956258d303ba94e3a602770053402fa8` |

**Gatilho de tick do item:** `acInventoryTick @0–30` aceita somente `Player` e passa por `ACCompat.isWornArmor(stack,player)` antes de chamar `acArmorTick`. `acArmorTick` limita o efeito a `stack.is(HAZMAT_MASK)` em `@0–15`; usa `Math.cos(player.tickCount × 0.05F) ≥ 0.8999999761581421D` em `@19–34` e duas escolhas independentes `RandomSource.nextBoolean()` para solicitar partículas `ACParticleRegistry.HAZMAT_BREATHE` em lados opostos da posição dos olhos após `xRot/yRot` (`@38–344`). Os `Vec3` iniciais têm deslocamentos `(+0.25,-0.3000000119,+0.25)` e `(-0.25,-0.3000000119,+0.25)`. O método não guarda cooldown, não desconta mana, não aplica defesa, não chama `hurt` nem muda mundo. Disponibilidade visual em cliente e cadência do dispatcher herdado são **NOT_VERIFIED**.

**Contador de peças:** `getWornAmount(LivingEntity) @0–111` compara exatamente HEAD `HAZMAT_MASK` (`@2–26`), CHEST `HAZMAT_CHESTPLATE` (`@29–53`), LEGS `HAZMAT_LEGGINGS` (`@56–80`) e FEET `HAZMAT_BOOTS` (`@83–107`). Cada `ItemStack.is(Item)` verdadeiro acrescenta 1. Retorno inteiro **n ∈ {0,1,2,3,4}**. Não testa durabilidade residual/encantamento, NBT ou UUID neste corpo. Este é um contador de **identidades em slots**, não uma prova de resistência efetiva em outros mods.

## 4. Consumidores causais nativos verificados

### 4.1. Itens radioativos

`RadioactiveItem.acInventoryTick` e `RadioactiveBlockItem.acInventoryTick` — cada um com 73 instruções e hash `75543b1b405f2225b8ca073341059eeb818715f6043312f7d0802f9056f9639f` — têm guardas server-side `!level.isClientSide()`, `LivingEntity` e exclusão de `Player.isCreative()` (offsets `@0–43`). Computam:

- `b = stack.getCount() × this.randomChanceOfRadiation` (chance nativa do item, **valor por subtipo não auditado nesta sonda**);
- `f = 1.0F − n/4.0F`;
- se ainda não possui `IRRADIATED`, e `random.nextFloat() < b × f`, constroem `MobEffectInstance(IRRADIATED, 1800)` ticks = 90 segundos (`@68–132`).

Chamam `LivingEntity.addEffect` (`@134–141`) e **descartam seu boolean**, seguindo para `UpdateEffectVisualityEntityMessage` via `AlexsCaves.sendMSGToAll`. A mensagem solicitada não comprova aplicação aceita nem apresentação. Não há clamp próprio de `b × f` nesse corpo. Com n=4, `f=0`, logo esta condição de sorteio nativa não solicita um novo efeito. Outros produtores de `IRRADIATED` não estão encerrados.

### 4.2. Efeito Irradiated ativo

`IrradiatedEffect.tick(LivingEntity,int)` — 42 instruções, SHA-256 `16d7936ed5ad148727bc46083451f5329beea0545a46b6d2306c695bc585aed7` — calcula `f=1.0F−n×0.25F` (`@0–12`). Se alvo é Player **e n=0**, chama `causeFoodExhaustion(0.4F)` (`@14–35`). Se não é `RaycatEntity` e `random.nextFloat() < f+0.1F`, solicita `LivingEntity.hurt(causeRadiationDamage(registryAccess), f)` e descarta o boolean (`@38–83`). Com quatro peças, `f=0` mas o limiar ainda é **0.1F**: pode haver chamada `hurt` **com quantidade 0**. A agenda de ticks, supressão pelo engine, dano final aceito, efeitos colaterais de chamadas zero e outras fontes de radiação permanecem não homologados.

### 4.3. Contato com AcidBlock

`AcidBlock.entityInside` — 174 instruções, SHA-256 `cf7110a18f48f7c9c791fb3229b861bbd67eb18c4a2fade3ede48a9d05ae3a8d` — encerra cedo quando a entidade possui tag `RESISTS_ACID` ou `ACFluids.acidHeight(entity) ≤ 0.1D` (`@0–29`). Para `LivingEntity`, percorre `EquipmentSlot.values()`, filtra `isArmor`, `ItemStack.isDamageableItem` e **exclui itens `instanceof HazmatArmorItem`** (`@53–124`). Para cada peça não-Hazmat assim localizada, sorteia chance `0.05F` e, exceto jogador criativo, solicita `ACCompat.hurtAndBreak(stack,1,entity,slot)` (`@124–173`). O simples encontro de peça não-Hazmat aciona um marcador usado no avanço `ENTER_ACID_WITH_ARMOR` (`@192–202`); não depende de desgaste efetivamente aceito.

O fator para LivingEntity é `f=1−n/4` (`@179–190`), para outros Entities mantém `f=1`. O bloco só entra no ramo de dano se `random.nextFloat()<f` (`@205–217`). Nesse ramo, calcula `extra=10F` para entidade `WEAK_TO_ACID`, senão 0; solicita `ACCompat.hurt(entity,causeAcidDamage, f×(peça não-Hazmat detectada?0.01F:1F)+extra)` (`@220–276`), com som condicionado ao boolean retornado. **Com quatro peças Hazmat, f=0, o ramo de dano do próprio bloco não é alcançado**, inclusive a adição condicional de 10. Não extrapolar para outros ácidos/danos do modpack. Desgaste de armadura não-Hazmat é caminho independente do sorteio de dano ácido.

### 4.4. Registro e apresentação

`ACItemRegistry.lambda$static$69..72` (6 instruções cada, referências tipadas) constroem quatro itens com o material Hazmat. `ACArmorRenderProperties.getACArmorModelBase` tem referência tipada e seleção de modelo no cliente, mas não atribui proteção. `getArmorTexture` devolve `alexscaves:textures/armor/hazmat_suit_1.png` para LEGS e `hazmat_suit_0.png` nos demais slots; `initializeClient` usa o proxy de apresentação. Existem modelos JSON individuais e quatro receitas nomeadas `hazmat_*`, mais tag de reparo; foram atestados **nomes, tamanhos e hashes**, não conteúdo integral/condições de obtenção. Os 28 arquivos filtrados incluem blocos decorativos e **não** significam 28 armaduras/ações. Assinaturas, hashes e contagens de consumidores constam do manifesto.

## 5. Targeting, custos, estado e relevância para perks

**Target:** usuário/alvo é a `LivingEntity` que usa os quatro slots; partículas são visuais do Player com máscara. Não há seleção de alvo ofensivo, LOS, cast, alcance, AOE, projétil, invocação, scaling por Mastery, charges ou cooldown nos métodos próprios de armadura (**N/A**, com justificativa de não-cast). O dano ácido é atribuído ao `DamageSource` nativo do bloco; a radiação usa `ACDamageTypes.causeRadiationDamage`; atribuições finais, filtros de PvP e extensões externas exigem engine.

**Custo/estado:** proteção é condicionada à identidade do equipamento no slot, sem custo de mana ou reserva por chamada. Durabilidade máxima é propriedade do material, não gasto no tick Hazmat; o `AcidBlock` pode desgastar **outras** armaduras, não esta por seu filtro de classe. Não foi visto UUID nem persistência própria no owner. `ItemStack` e efeitos possuem persistência/sincronização da engine ou de outros owners **não certificadas** aqui.

**Integração:** uma perk poderia conceitualmente mudar contagem/limiar de proteção, dano ácido, exaustão ou chance de irradiação, mas isso **não equivale a API mutadora**. `getWornAmount` é chamado por consumidores diferentes, com valores locais calculados em cada caminho; sobrescrever o retorno sem contrato real pode afetar efeitos e avanços, inclusive por terceiros. Não duplicar `IRRADIATED`, `hurt`, partículas, cobranças ou XP/Mastery. As interfaces `ACCompat` e `HazmatArmorItem` são **localizadores de investigação**, não autorização para interceptação. Black Arcana mantém a autoridade do runtime mágico, RPG Skill Tree fornece perks/Mastery por contratos reais; até comprovar hook seguro, **`NO_MUTATION` / fail-closed**.

## 6. Limites, testes e próximos gates

O **probe da CI** validou a identidade do publisher, os seis corpos executáveis do owner, sete consumidores tipados e rejeição de JSON malformado; o relatório íntegro é associado ao SHA acima. **Não** verifica todas as fontes de radiação, todos os consumidores dinâmicos/por reflexão, os efeitos ambientais finais, a sequência completa `ACCompat`, a ordem de execução de outros mixins, a ABI ordinal de `ArmorItem.Type`, condições de receitas, regras do pack, descarte, reload, save/restart, multiplayer ou QA física. Não promove nenhum dos quatro itens a ✅.

**Próxima investigação:** auditar `ACCompat.isWornArmor`, `ACTickingItem/ItemStackTickMixin`, `IrradiatedEffect` e suas agendas, demais aplicações de `IRRADIATED`, `AcidBlock` sob interferência de outros mods e a engine exata; confirmar limite do universo antes de certificar as quatro peças individualmente. Nunca usar código de terceiros no runtime sem licença e contrato compatível.
