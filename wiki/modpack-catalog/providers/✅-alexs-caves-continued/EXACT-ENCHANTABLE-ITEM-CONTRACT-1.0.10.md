# ACEnchantableItem — contrato individual SHA-exato 1.0.10

**Escopo:** sete eixos estáticos da interface e fronteiras de consulta, candidato ao merge #1119. NO_MUTATION, hook NOT_VERIFIED, QA NOT_TESTED, perk NOT_CERTIFIED, runtime NOT_VERIFIED, provider OPEN. [Ficha](systems/enchantable-item.md) · [Manifesto](EXACT-ENCHANTABLE-ITEM-CONTRACT-1.0.10.json).

## Sete eixos

**identity:** Publisher 1.0.10 SHA-exato; interface pública, duas assinaturas, zero campos/superinterfaces, 13 implementadores diretos, zero herdados, 13 bindings.

**behavior:** 13 valores constantes 1; 12 overrides e default da interface com count==1; Ortholance sem override, referência Item.isEnchantable exige max stack 1/MAX_DAMAGE; guarda adicional da ItemStack.

**parameters:** Inteiro 1, quantidade da stack, 51 JSONs e 14 tags locais de supported_items; 48 recursos dos 13 itens e 3 de Desolate Dagger fora do roster, zero primary_items explícitos.

**targeting:** N/A para cast, vítima, LOS, AOE, projétil: consulta ItemStack e elegibilidade de encantamento por holder/tag no consumidor externo, sem alvo vivo/caster.

**costs:** N/A para custo de cast, mana, XP, lapis, débito de durabilidade, cooldown e duração: corpos somente leem count ou retornam constante; cálculo de custos mesa/bigorna é externo.

**integration:** Mojang 1.21.1 e NeoForge 21.1.250 pinados: precedência de método de classe, bridge stack-aware, EnchantmentHelper, supports/primary e anvil/table; sem autoridade por jogador ou hook seguro. NO_MUTATION.

**validation:** Censo de 1555 classes, dois relatórios SHA-exatos, bindings por handles, testes de corpo/offset/roster/recursos e ledger. Referência não é execução instalada.

## Pivôs externos versionados

Mojang client 1.21.1 SHA-1 `30c73b1c5da787909b2f73340419fdf13b9def88`, SHA-256 `499f6897d1837516680f3114072d8106e11c9adcd933fe5cf051b551089b0c99`; mappings SHA-1 `2244b6f072256667bcd9a73df124d6c58de77992`, SHA-256 `140c47931cccc8fc9e4c22d7603e2d714d1a953a146f51ea7397d95c955536ec`; metadata SHA-1 `ff7ef54488da4a711f3c8a781a9f79105bbe801a`. NeoForge 21.1.250 universal/userdev pinados no [manifesto de referência](EXACT-DESTROYED-ITEM-ENGINE-REFERENCE-21.1.250.json). Não são um Minecraft transformado observado.

| Referência | Pivôs |
|---|---|
| Item vanilla cul.a(Lcuq;)Z | 12 instruções, SHA Code 801002b78fdcb3657282d200a5e63cbb17c65c05ad4b038454e1c186099b30a1. getMaxStackSize @1, compara 1 @4–5, MAX_DAMAGE @9, consulta de componente @12, guarda @15; true @18, false @22. |
| ItemStack vanilla cuq.z()Z | 21 instruções, SHA Code 726c744f1e31404ae4b3e285569fbcdc280f3d94b64416fc6e44aa8bbe28dd0f. Item.isEnchantable @5, guarda @8, ENCHANTMENTS @12, consulta @15, não nulo @23, ItemEnchantments.isEmpty @27, guarda @30. |
| EnchantmentHelper | getEnchantmentCost 56 instruções (valor @8); selectEnchantment 104 (valor @13); userdev substitui duas chamadas pelo getEnchantmentValue de ItemStack. |
| IItemStackExtension.getEnchantmentValue | 7 instruções, bridge stack-aware @15. |
| IItemExtension.getEnchantmentValue | 4 instruções, getter sem argumento @6. |
| supportsEnchantment | 14 instruções; ENCHANTED_BOOK @1–7, isSupportedItem @20. |
| isPrimaryItemFor | 30 instruções; BOOK @4–11, primaryItems @24, supportsEnchantment @31, ItemStack.is(HolderSet) @54. |
| IItemStackExtension support/primary | 8 instruções cada, virtual para Item @16. |
| Userdev AnvilMenu/EnchantmentMenu | Adição de supportsEnchantment na bigorna; guarda da mesa no contexto do patch. |

Precedência de método concreto de classe sobre default (referências [JVMS 5.4.3.3](https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-5.html#jvms-5.4.3.3), [JLS 8.4.8](https://docs.oracle.com/javase/specs/jls/se21/html/jls-8.html#jls-8.4.8)). A classe Ortholance não declara isEnchantable. Sua fábrica lambda$static$110 solicita durability(340) @11–14, UNCOMMON @17–20 e construtor @23, que encaminha Properties a Item @2. Faz-se derivação estática, não afirmação sobre comportamento final após transformação ou modificação da stack. A prova cobre as consultas, não custos efetivos/rolls/XP da mesa, nem os efeitos integrais de equipamentos. Os 51 recursos têm próprios certificados, e seus dados literais não provam a união de datapacks.

## Reprodução

[Auditor](../../../../docs/qa/alexscaves_1010_enchantable_item_probe.py), [auditor externo](../../../../docs/qa/alexscaves_1010_enchantable_item_boundary.py), [testes](../../../../docs/qa/alexscaves_1010_enchantable_item_probe_test.py), [workflow](../../../../.github/workflows/alexscaves-1010-enchantable-item-probe.yml). JDK 21 e artefatos oficiais; a segunda sonda baixa metadata e valida os hashes oficiais Mojang. Comandos no workflow.

- [Execução nativa](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44312413309/job/134829679393): `d34a655d06d65a771ea9237ef222635e159ffcfa6fe8b454ee6826ee14979e73`.
- [Execução de referência/recursos](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44313906227/job/134834846277): `2666fde10c15277042eea741f770c0bab4e1487ac0d0730b37494e47a45adf5d`, [artefato temporário](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44313906227/artifacts/14431392225).
- O selo fixa os dois relatórios; as regressões conferem identidade, guardas, bindings, recursos e estado independente. CI final obrigatória; não versionar JARs, mappings ou implementação de terceiros.

**Limites:** dispatch transformado, efeitos finais, custos reais, reload, mistura de tags e mods, ownership e segurança por jogador não verificados. Não habilita perk, hook ou nova raiz; NO_MUTATION.
