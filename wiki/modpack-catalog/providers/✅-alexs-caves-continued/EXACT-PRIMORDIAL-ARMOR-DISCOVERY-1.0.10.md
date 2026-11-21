# Primordial Armor — contrato causal parcial da versão SHA-exata 1.0.10

**Estado:** ⚠️ **descoberta estática**, sem certificação individual integral. `STATIC_DISCOVERY_ONLY` / `static_contract=NOT_CERTIFIED` / `NO_MUTATION` / `mutating_hook=NOT_VERIFIED` / `physical_qa=NOT_TESTED`. Três equipamentos `Primordial`, **zero novas magias/casts** e universo integral do provider **OPEN**. A contagem de peças afeta argumentos de nutrição/saturação de dois consumidores nativos; não constitui API de perk.

## 1. Fonte da verdade e reprodução

A modlist física documentada no sibling `neoforge-rpg-skilltree/PROJECT-INSTRUCTIONS/modlist/World Gen/✅-alexs-caves-continued v1.0.10.md` fixa `alexscaves-1.0.10-neoforge+1.21.1.jar` (mod ID `alexscaves`, Minecraft **1.21.1**, NeoForge, Java **21**), SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`. Publisher de **75.279.314 bytes**, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. **Dump da instância instalado e paridade de outras revisões-fonte não foram novamente verificados.**

Owner `com/github/alexmodguy/alexscaves/server/item/PrimordialArmorItem.class`, SHA-256 `8833c162d1507aba795b1ff809f5a6f6ddb846da308d809795cf80e69be5d09e`. Censo tipado do JAR: **1.555 classes**, quatro métodos Code do owner, **cinco owners referenciadores** (incluindo autorreferência sem callsite executável), zero campos próprios, zero ancestrais internos nesse recorte, oito recursos JSON filename-matched.

Prova reproduzível: [sonda](../../../../docs/qa/alexscaves_1010_primordial_armor_discovery.py), [checker fail-closed](../../../../docs/qa/alexscaves_1010_primordial_armor_discovery_checks.py), [workflow](../../../../.github/workflows/alexscaves-1010-primordial-armor-discovery.yml) e [manifesto imutável](EXACT-PRIMORDIAL-ARMOR-DISCOVERY-1.0.10.json). Primeira execução read-only [GitHub Actions #44951722588](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44951722588), job `136990914383` **PASS**, artefato `14725074259`, `report.json` SHA-256 `659f60f17d549d8c795becc4d7fa7e6b8968cb546b8af002099b44abb65e4f75`. O primeiro PASS antecede o selo mais estrito; uma segunda execução deve confirmá-lo. Report válido não significa jogo/engine/QA física aprovados.

## 2. Equipamentos, registries e parâmetros compartilhados

| ID de recurso | Item registry | Tipo declarado | Slot verificado no contador | Ficha |
|---|---|---|---|---|
| `alexscaves:primordial_helmet` | `PRIMORDIAL_HELMET` | `ArmorItem.Type.HELMET` | `EquipmentSlot.HEAD` | [Primordial Helmet](items/primordial-helmet.md) |
| `alexscaves:primordial_tunic` | `PRIMORDIAL_TUNIC` | `ArmorItem.Type.CHESTPLATE` | `EquipmentSlot.CHEST` | [Primordial Tunic](items/primordial-tunic.md) |
| `alexscaves:primordial_pants` | `PRIMORDIAL_PANTS` | `ArmorItem.Type.LEGGINGS` | `EquipmentSlot.LEGS` | [Primordial Pants](items/primordial-pants.md) |

No `ACItemRegistry`, `lambda$static$42..44` instanciam o owner com `PRIMORDIAL_ARMOR_MATERIAL`. O `<init>` do item entrega `material.vanilla()` e `material.properties(new Item.Properties(),type)` ao construtor de `ArmorItem`. O [contrato estático antecedente](systems/armor-material.md) comprova material **`primordial`**, multiplicador de durabilidade **20**, defesa por índice ordinal `[3,4,3,2]`, durabilidade por ordinal `[260,300,320,220]`, encantabilidade **25**, toughness **0F**, knockback resistance **0F**, reparo configurado via `alexscaves:tough_hide`. **Não atribuir índices desse array aos slots sem ABI do enum externo.** Esses parâmetros não comprovam mitigação final, stamina, cooldown, resistência mágica ou integração de perks.

Foram identificados modelos JSON dos três itens, receitas `data/alexscaves/recipe/primordial_{helmet,tunic,pants}.json`, advancement `primordial_armor.json` e tag `repairs_primordial_armor.json`. O manifesto registra **hash e tamanho**, não copia seus conteúdos; desbloqueio/craft/reparo/loot efetivos são **NOT_VERIFIED**. `getArmorTexture` seleciona `alexscaves:textures/armor/primordial_armor_1.png` quando slot `LEGS` e `primordial_armor_0.png` caso contrário. `initializeClient` entrega o proxy de extensões visuais. O consumidor `ACArmorRenderProperties` escolhe `PRIMORDIAL_ARMOR_MODEL` por `instanceof`; rendering físico não foi executado.

## 3. Quatro métodos próprios da classe — censo integral Code

| Método JVM | Instruções | Fingerprint SHA-256 das instruções |
|---|---:|---|
| `<init>(ACArmorMaterial, ArmorItem.Type)` | 12 | `1c59bef51bc767350a0f79f732eac8355d4c7b6c50b864e6b32197f3a1efabf2` |
| `getArmorTexture(ItemStack,Entity,EquipmentSlot,String)` | 7 | `cda97c121e4aa31e0c82fbedb73ce9589c322d3bdefbaa0c7091e474dc815e5a` |
| `getExtraSaturationFromArmor(LivingEntity)` | 31 | `2fb7d7a8c00bc1a5b33c525f7da5b7c80d04b373b9c24bed3412fe4d04cc8317` |
| `initializeClient(Consumer)` | 6 | `241b312ebd6ff1e8ab0719a7fcbfd71c956258d303ba94e3a602770053402fa8` |

O contador `getExtraSaturationFromArmor`, `@0–84`, inicia `n=0` e avalia exclusivamente **HEAD** com `PRIMORDIAL_HELMET` (`@2–26`), **CHEST** com `PRIMORDIAL_TUNIC` (`@29–53`) e **LEGS** com `PRIMORDIAL_PANTS` (`@56–80`). Cada `ItemStack.is(exactItem)` verdadeiro executa `iinc 1,1` (`@26,53,80`), retorna n em **`{0,1,2,3}`**. Não consulta boots, durabilidade, upgrade, enchant, UUID, fome, mundo, time ou Mastery. Apesar do nome, o método **retorna contagem inteira**, não valor absoluto de saturação.

## 4. Consumidores de alimentação (distinguir argumentos de efeito engine)

### PlayerMixin.ac_eat — alimentos em RAW_MEATS

O método `com/github/alexmodguy/alexscaves/mixin/PlayerMixin.ac_eat` (31 instruções, SHA-256 `3f928fd639c0d5e62a849fdf302ba373fc304d4a4c8fff7cfd65e11a9a2abffd`) consulta `ItemStack.is(ACTagRegistry.RAW_MEATS)` (`@0–8`); somente nesse ramo solicita `n=getExtraSaturationFromArmor(player)` (`@11–15`). Fora da tag, n=0.

Se **n>0 e FoodProperties != null** (`@19–27`), invoca `FoodData.eat(int,float)` com os argumentos:
- **nutrição solicitada:** `ACCompat.nutrition(foodProperties) + n` (`@30–37`);
- **saturationModifier solicitado:** `ACCompat.saturationModifier(foodProperties) + 0.125F×n` (`@38–49`).

Se algum gate falha, usa `FoodData.eat(FoodProperties)` sem a alteração (`@55–60`). Os números `+1` e `+0.125F` são por peça em **argumentos entregues**, não crescimento comprovado de pontos reais de fome/saturação após clamps, status, eventos ou outras modificações da engine. O report verifica o método consumidor, mas não o ponto de injeção efetivamente aplicado, cancelamento de terceiros, sincronização ou as implementações de `ACCompat` e `FoodData`.

### DinosaurChopBlock.eat — alimentação por bloco específico

`com/github/alexmodguy/alexscaves/server/block/DinosaurChopBlock.eat` (89 instruções, SHA-256 `4e2b75751d124247a814dc386551010171bbfdc157b96a80f01c36c74cc4058c`) exige `player.canEat(false)`; caso contrário retorna `InteractionResult.PASS` (`@0–12`). Registra pedido de `Stats.EAT_CAKE_SLICE` (`@13–18`). Consulta `n=getExtraSaturationFromArmor(player)` **somente se** a instância do bloco é a `ACBlockRegistry.DINOSAUR_CHOP` (`@21–42`), n=0 para outra instância.

A chamada `FoodData.eat(int,float)` recebe `foodAmount + n` e `saturationAmount + 0.125F×n` (`@44–68`). Prossegue solicitando `GameEvent.EAT`; se `BITES<3`, prepara `setBlock` com incremento; caso contrário solicita `removeBlock`, conversão para `THIN_BONE` e `GameEvent.BLOCK_DESTROY` (`@71–202`). Retorna `InteractionResult.SUCCESS`; resultado efetivamente aceito pelo mundo/engine, permissões e proteção de claims permanecem **NOT_VERIFIED**. Esse caminho é diferente da tag de carne crua; não duplicar o bônus e os eventos como dois novos casts.

## 5. Custos, target, autoria, estado e integração com perks

**Target:** a entidade viva consultada pelo contador, concretamente o Player nos dois consumidores nativos; não há inimigo, seleção de alvo, raycast, LOS, alcance, AOE, projetil, dano ofensivo, tipo de dano, knockback, summon, modificação de bloco pelo *item* ou spell cast (**N/A no owner**). O consumidor `DinosaurChopBlock` pode modificar o bloco após alimentação; autoria/permissions persistem no sistema de interação do mundo, não no item de armadura.

**Ativação:** equipar as identidades exatas nos slots definidos; a contagem é **reativa** quando consumidores de comida invocam o método, sem timer/charge do item, mana, cooldown, perda própria de durabilidade ou desgaste acionado pelo cálculo. Para comida há requisitos distintos de tag e fome; chamadas de engine não são garantias de alimentação aceita.

**Estado/persistência:** owner e contador não gravam NBT/componente nem UUID. Modificações reais no `FoodData`, estados de bloco, eventos, sincronização, recuperação após login/restart e efeitos de outros mods pertencem à engine/consumers e **não foram testados fisicamente**.

**Perks/Mastery:** candidatos conceituais são bônus de nutrição e parâmetros de saturação condicionados por equipamentos, tags e alimentos. Não existe **hook mutador per-player certificado** nestes quatro métodos; mexer em `getExtraSaturationFromArmor` muda simultaneamente dois consumidores e pode colidir com outros módulos. Não duplicar `FoodData.eat`, alimentação, GameEvents, bônus de XP/Mastery ou aplicar modificador genérico sem boundary verificável. Black Arcana mantém runtime mágico, RPG Skill Tree recebe autoridade somente sobre progressão/perks por contratos reais. Política: **`NO_MUTATION` / fail-closed**.

## 6. Validação, pendências e critérios de avanço

O publisher foi inspecionado por CI com autenticação do SHA exato; os quatro métodos próprios, consumidores `PlayerMixin`, `DinosaurChopBlock`, `ACItemRegistry`, `ACArmorRenderProperties` e autorreferência, 8 recursos JSON filename-matched estão listados com hashes reproduzíveis. A prova é **parcial** até verificar também chamada/injeção real do mixin, ABI da engine `FoodData` e dos ordinais de equipamento, suporte `ACCompat`, outros produtores/consumidores de efeitos alimentares, condições das recipes, prioridade de mixins, atualizações de dados/packet, compatibilidade com outros perks, world safety e testes em cliente/servidor.

O universo integral do provider permanece aberto; **nenhuma das três fichas individuais recebe ✅ apenas por existir manifesto ou método compartilhado**. O próximo gate técnico depende de investigação causal e execução dos verificadores SHA-exatos da HEAD final. A QA física continua `NOT_TESTED` mesmo que a CI termine em PASS. Não foi copiado código ou asset para o runtime Black Arcana.
