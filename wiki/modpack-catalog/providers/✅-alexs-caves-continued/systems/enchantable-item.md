# ACEnchantableItem — consulta de encantabilidade (1.0.10)

**Contrato técnico estático:** ✅ CERTIFIED_STATIC_7_AXES / STATIC_TECHNICAL_CATALOG_ONLY (candidato ao merge #1119). **Hook:** NOT_VERIFIED. **Runtime:** NOT_VERIFIED. **QA física:** NOT_TESTED. **Perk:** NOT_CERTIFIED. **Política:** NO_MUTATION. Provider OPEN; +0 raízes mágicas.

## 1. Identidade e proveniência

Interface de suporte a equipamentos que declara o inteiro de encantabilidade e uma consulta por ItemStack; não é um cast, encantamento individual ou objeto registrado. Descrição editorial própria. Mod ID alexscaves; Minecraft 1.21.1, Java 21, NeoForge físico 21.1.250. Publisher `alexscaves-1.0.10-neoforge+1.21.1.jar`, CurseForge 1645389/8856293, 75.279.314 bytes; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Owner `com.github.alexmodguy.alexscaves.server.item.ACEnchantableItem`, class SHA-256 `3e2b29f7d1d11f066d4d2e54141a90561edcf76a8c550a32746ee4a23f1f4786`. Zero campos/superinterfaces; getEnchantmentValue()I abstrato público access 1025; isEnchantable(ItemStack)Z default público access 1. [Prova](../EXACT-ENCHANTABLE-ITEM-CONTRACT-1.0.10.md) e [selo](../EXACT-ENCHANTABLE-ITEM-CONTRACT-1.0.10.json). A fonte adjacente 1.1.1 não determina comportamento de 1.0.10.

## 2. Ativação e condições

Treze implementadores diretos, zero herdados adicionais no censo de 1555 classes. Todos declaram getEnchantmentValue()I de duas instruções retornando **1**, Code SHA-256 `95ef737cd8a13db65e3eb3c18e8816a5179dcbdf341309522ab00e95d5aae6d2`. O default da interface e **doze overrides explícitos** de isEnchantable têm 14 bytes e oito instruções: consulta getCount @1, compara 1 @4–5, true @8, false @12, retorno @13. Hash do default `64da4f2b791e5e23d69c3ca524d113b15372ce159dc6deca49aa5f1e6b0ef074`. Os hashes de overrides diferem pelo constant pool, não pela guarda.

**Ortholance é a exceção**: declara valor 1, não declara isEnchantable; pai Item. Pela precedência do método concreto de classe, a referência vanilla 1.21.1 resolve a Item.isEnchantable: exige getMaxStackSize()==1 e componente MAX_DAMAGE presente, não count==1. A fábrica solicita Properties.durability(340), e o construtor encaminha Properties para Item. Não garante componentes finais da stack carregada. Referências userdev/universal 21.1.250 e vanilla são independentes do runtime transformado.

**Camada adicional:** ItemStack.isEnchantable vanilla primeiro consulta Item.isEnchantable(stack) virtualmente; depois exige ENCHANTMENTS não nulo e ItemEnchantments.isEmpty(). O guard local dos 12 itens não verifica esse componente.

## 3. Registro, parâmetros e elegibilidade

| Owner | ID de item | lambda$static$ | Offset de bootstrap | JSONs publisher | Guarda local |
|---|---|---:|---:|---:|---|
| CandyCaneHookItem | alexscaves:candy_cane_hook | 179 | 3166 | 3 | count==1 |
| DreadbowItem | alexscaves:dreadbow | 137 | 2503 | 5 | count==1 |
| ExtinctionSpearItem | alexscaves:extinction_spear | 49 | 1126 | 3 | count==1 |
| GalenaGauntletItem | alexscaves:galena_gauntlet | 19 | 633 | 3 | count==1 |
| MagicConchItem | alexscaves:magic_conch | 107 | 2027 | 3 | count==1 |
| OrtholanceItem | alexscaves:ortholance | 110 | 2078 | 4 | Item (externo) |
| PrimitiveClubItem | alexscaves:primitive_club | 40 | 973 | 3 | count==1 |
| RaygunItem | alexscaves:raygun | 76 | 1568 | 4 | count==1 |
| ResistorShieldItem | alexscaves:resistor_shield | 20 | 650 | 2 | count==1 |
| SeaStaffItem | alexscaves:sea_staff | 108 | 2044 | 5 | count==1 |
| ShotGumItem | alexscaves:shot_gum | 176 | 3115 | 4 | count==1 |
| SugarStaffItem | alexscaves:sugar_staff | 184 | 3251 | 5 | count==1 |
| TotemOfPossessionItem | alexscaves:totem_of_possession | 126 | 2316 | 4 | count==1 |

13 bindings de ACItemRegistry: literal imediatamente anterior ao handle de fábrica, register e putstatic posteriores. Não são novos casts. Os 51 JSONs publisher de encantamento apontam 14 tags de supported_items, cada qual com um único item literal e replace=false; nenhuma declara primary_items. As 13 tags acima somam **48 recursos**; outros três pertencem a Desolate Dagger, que não integra o roster da interface. A interface não é censo de todos os itens encantáveis.

O valor 1 não é nível I, potência, multiplicador ou chance de êxito. Pesos, custos e níveis dos 51 encantamentos estão em suas [fichas individuais](../ENCHANTMENT-PERK-CROSSWALK-1.0.10.md). Nenhum efeito direto de dano, cura, status, movimento, invocação, alteração de mundo ou projétil. Dano/tipo, alcance, LOS, AOE, targeting de entidade, HP, velocidade, ticks, duração, recarga e escala Mastery são N/A para esta consulta.

## 4. Grafo e consumidores externos

- IItemStackExtension.getEnchantmentValue() delega virtualmente a Item.getEnchantmentValue(ItemStack) @15; IItemExtension default chama Item.getEnchantmentValue() sem argumento @6.
- EnchantmentHelper userdev altera duas consultas de Item para ItemStack.getEnchantmentValue; referência vanilla identifica getEnchantmentCost e selectEnchantment como consumidores. Não se certifica a fórmula de seleção/custo de toda a engine.
- IItemExtension.supportsEnchantment default: ENCHANTED_BOOK ou Enchantment.isSupportedItem(stack). isPrimaryItemFor default: BOOK ou supportsEnchantment e (primaryItems ausente ou stack membro do HolderSet). As variantes da stack delegam ao Item.
- Patch AnvilMenu usa supportsEnchantment; EnchantmentMenu preserva guarda stack.isEnchantable. Suporte, primário, encantabilidade e custo não são equivalentes.
- O censo dos nomes da interface no publisher não encontrou referências de método internas; ausência não confirma dispatch externo. A regressão específica verifica ausência de outras variantes de encantabilidade/suporte/primary nos treze owners.

## 5. Custos, autoria, estado e persistência

Os corpos apenas retornam constante ou leem count, sem cobrança de XP, lapis, mana, stamina, durabilidade ou cooldown; count é input, não custo. Sem campos, NBT, rede, persistência ou efeito de mundo próprios; não recebem player, caster ou alvo vivo. Owner, kill credit, Mastery, mudança de dimensão e lifecycle de entidade são N/A no callback. Estado de componentes, aplicação/reload e custos da mesa/bigorna permanecem externos e não verificados fisicamente.

## 6. Perks e boundaries

Black Arcana conserva autoridade mágica; RPG Skill Tree fornece progressão por boundaries reais. Possibilidades conceituais: controle de elegibilidade, custo/seleção, support e primary; não alterar valor globalmente nem confundir valor com nível do encanto. As APIs de referência recebem stack/holder, sem player explícito. Hook mutador por jogador, ordem de outros mods, datapack merge, XP transacional e QA permanecem pendentes. NO_MUTATION/fail-closed.

## 7. Validação

[Auditor nativo](../../../../../docs/qa/alexscaves_1010_enchantable_item_probe.py), [referência](../../../../../docs/qa/alexscaves_1010_enchantable_item_boundary.py), [regressões](../../../../../docs/qa/alexscaves_1010_enchantable_item_probe_test.py), [prova](../EXACT-ENCHANTABLE-ITEM-CONTRACT-1.0.10.md), [selo](../EXACT-ENCHANTABLE-ITEM-CONTRACT-1.0.10.json). Relatórios SHA-256 `d34a655d06d65a771ea9237ef222635e159ffcfa6fe8b454ee6826ee14979e73` e `2666fde10c15277042eea741f770c0bab4e1487ac0d0730b37494e47a45adf5d`. CI final obrigatória antes do merge. Dispatch instalado/transformado, resultado físico, compatibilidade por item e resolução após reload não comprovados; nenhum hook liberado.
