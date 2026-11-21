# Gingerbread Armor — auditoria nativa SHA-exata 1.0.10

**Estado:** ⚠️ descoberta binária completa do owner `GingerbreadArmorItem`, porém **contratos estáticos individuais das quatro peças PARCIAIS**. `STATIC_DISCOVERY_ONLY`, `NO_MUTATION`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, provider `OPEN`. Quatro equipamentos, **zero** novas raízes mágicas.

## Proveniência e reprodução

Modlist sibling: `alexscaves-1.0.10-neoforge+1.21.1.jar`, Minecraft 1.21.1, NeoForge, Java 21, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`. JAR publisher de **75.279.314 bytes**, 1.555 classes, SHA-256 **`36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`**. Novo dump da instalação **NÃO VERIFICADO**. Classfile `com/github/alexmodguy/alexscaves/server/item/GingerbreadArmorItem` SHA-256 **`918cc76cd122605e6ba7aa2e8d26e1f4891b3ad8f26554b960e9b07412884a27`**: **8** métodos executáveis, 7 campos, três owners consumidores tipados.

A sonda [read-only](../../../../docs/qa/alexscaves_1010_gingerbread_armor_discovery.py) extraiu corpo, descriptor, instruções, hashes, consumers e resources. [Manifesto](EXACT-GINGERBREAD-ARMOR-DISCOVERY-1.0.10.json) guarda oito métodos, 142 arquivos JSON filename-matched (somente hashes/tamanhos, sem copiar conteúdo do publisher) e limites. [Verificador fail-closed](../../../../docs/qa/alexscaves_1010_gingerbread_armor_static_checks.py); [workflow](../../../../.github/workflows/alexscaves-1010-gingerbread-armor-discovery.yml). [Run #44937619871](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44937619871), job 136947609057 **PASS**, relatório SHA-256 `4b6a0709a167e49ffb4bd04b2949facfc3c7b0e55dad80c28842eaf26f1fbae1`, artefato 14720561081, ZIP SHA-256 `a92ea9a51f710e040e54adba19a0eca512d8a0284854564a0be58509fed390cc` (expira em 05/12/2026). O verificador de manifesto e os demais gates do novo commit aguardam CI própria.

## Registro e recursos

`ACItemRegistry` possui quatro consumidores/fábricas `lambda$static$187..190` e oito sites de referência tipada ao item, representando as quatro peças `gingerbread_helmet/chestplate/leggings/boots`. A associação de ordinal efetivo de `ArmorItem.Type` com os índices de material deve ser verificada na versão engine; **não** equiparar ordinal a posição na lista editorial.

O material `GINGERBREAD_ARMOR_MATERIAL` usa [contrato anterior](systems/armor-material.md): nome `gingerbread`, multiplicador de durabilidade **10**, `MAX_DAMAGE_ARRAY[ordinal]×10` = **[130,150,160,110]** por ordinal, defesa **[2,4,5,2]** por ordinal, encantabilidade **25**, toughness **0**, knockback resistance **0** e ingrediente de reparo `gingerbread_crumbs`. Essas sequências não são diretamente rotuladas BOOTS/LEGGINGS/CHEST/HEAD sem ABI externo do enum.

Recursos de modelo observados: `assets/alexscaves/models/item/gingerbread_helmet.json`, `_chestplate.json`, `_leggings.json`, `_boots.json`; tag `data/alexscaves/tags/item/repairs_gingerbread_armor.json` lista `alexscaves:gingerbread_crumbs`; avanço `gingerbread_armor.json` possui critérios para as quatro peças. O filename census de 142 JSONs inclui **blocos e receitas de construção Gingerbread que não são equipamentos**; não equivale a 142 armaduras, magias, receitas próprias ou closed universe. Não foi identificada receita `gingerbread_helmet/chestplate/leggings/boots` entre os JSONs de nome diretamente correspondente, mas **obtenção integral é NOT_VERIFIED**.

## Grafo de oito métodos

| Método nativo | Instruções | Evidências/efeitos locais |
|---|---:|---|
| `<clinit>()` | 24 | Quatro UUIDs de modifier, array ARMOR_MODIFIERS; IDs concretos no relatório |
| `<init>(ACArmorMaterial,ArmorItem.Type)` | 62 | Chama vanilla/properties, guarda acSlot/acDefense; constrói ARMOR com `ADD_VALUE` e MOVEMENT_SPEED `0.1D ADD_MULTIPLIED_BASE` no campo defaultAttributes |
| `acModifiers(EquipmentSlot,ItemStack)` | 14 | Compara slot com acSlot.getSlot(), consulta stack.getDamageValue/getMaxDamage, delega cache; em outro slot retorna `ImmutableMultimap.of()` **vazio, não null** |
| `getOrCreateDurabilityAttributes(int,int)` | 73 | Usa cache por inteiro **damage**, sem maxDamage na chave; em miss calcula velocidade `0.1D + 0.9D × ((float)damage/maxDamage)`; retorna mapa com ARMOR ADD_VALUE e MOVEMENT_SPEED ADD_MULTIPLIED_BASE |
| `getDefaultAttributeModifiers(ItemStack)` | 8 | Entrega `this::acModifiers` e supplier fallback ao `ACCompat.itemAttributes`, sem aplicar/modificar diretamente atributo final do Player |
| `lambda$getDefaultAttributeModifiers$0(ItemStack)` | 4 | Supplier chama super ArmorItem.getDefaultAttributeModifiers(ItemStack) |
| `getArmorTexture(ItemStack,Entity,EquipmentSlot,String)` | 7 | LEGS retorna `alexscaves:textures/armor/gingerbread_armor_1.png`; outros slots retornam `..._0.png` |
| `initializeClient(Consumer)` | 6 | getArmorProperties do proxy, consumer.accept; apenas apresentação |

O método `getOrCreateDurabilityAttributes` usa conversão float ao calcular a fração, coeficientes double, e mapa `Integer.valueOf(damage)`. O **cache por damage ignora maxDamage e identidade da stack/jogador**. Não presumir que cada item tenha ciclo próprio independente de equipamentos de mesmo tipo. O mapa `defaultAttributes` inicial tem bônus **0.1**; o caminho `acModifiers` usa o mapa reconstruído por dano. Essa distinção é relevante para evitar bônus duplicados, bugs de atualização e uso de fallback incorreto.

## Eixos de segurança e integração

**Targeting, alcance, projéteis, AOE, custo de mana, casting, owner de dano, summons, efeitos de mundo e cooldown:** **N/A no owner nativo**, que é equipamento e construtor de modificadores. Atributos de defesa e velocidade são calculados mas **não garantem** efeito aceito no jogador ou redução de dano final; a engine NeoForge, configuração, outros mods, eventos e prioridade de modifiers condicionam o resultado.

**Custo e durabilidade:** a durabilidade do item é propriedade do material; **acModifiers não desconta desgaste**. Quebra/reparo, persistência de desgaste, equipamentos encantados e compatibilidade de terceiros dependem da engine/consumers. **Hook mutador por usuário NÃO VERIFICADO**: alterar o mapa cacheado do item compartilhado pode contaminar stacks/jogadores. Não modificar `DEFAULT_ATTRIBUTES`, cache global, material, nem duplicar modifiers para perks de velocidade sem boundary real. RPG Skill Tree só deve fornecer atributos/perks por contrato seguro; Black Arcana preserva world safety e sua autoridade mágica. Nenhuma XP/Mastery por cálculo de atributos.

**Pendências:** ordinal engine para slot, aceitação final de modificadores em NeoForge 21.1.250, ciclo de desgaste e cache sob variação de maxDamage, reparo/crafting em mundo, overlays/renderer, save/reload, cliente/servidor, PvP, QA física, regras de outros providers e hooks. O contrato anterior de [ACDynamicAttributeItem](systems/dynamic-attributes.md) e [ACArmorMaterial](systems/armor-material.md) é reutilizado **sem promover** os quatro itens a ✅. Clean-room: sem código/asset copiado ao runtime; somente descrições originais e localizadores.
