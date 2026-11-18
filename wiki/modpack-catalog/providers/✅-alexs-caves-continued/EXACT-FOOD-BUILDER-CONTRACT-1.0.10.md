# ACFoodBuilder — contrato estático SHA-exato 1.0.10

**Escopo:** sete eixos do helper e referência de construção/consumo oficial. A ficha não certifica alimentos completos; candidato #1120, NO_MUTATION, hook NOT_VERIFIED, runtime NOT_VERIFIED, QA NOT_TESTED, perk NOT_CERTIFIED, provider OPEN, zero raízes novas.
[Ficha](systems/food-builder.md) · [Manifesto](EXACT-FOOD-BUILDER-CONTRACT-1.0.10.json).

## Sete eixos

**identity:** Publisher 1.0.10 SHA-exato: ACFoodBuilder 14 métodos/9 campos e record Effect 6 métodos/2 campos; censo de 1555 classfiles; separa ACFoods, ACFoodPropertiesItem e equipamentos.

**behavior:** Fluent setters, list append, resolve cria FoodProperties.Builder e resolve suppliers imediatamente; build registra identidade em BUILT, food encaminha para Item.Properties; meat/sound não são lidos neste recorte.

**parameters:** Nutrição int, saturationMod float, flags alwaysEat/fast/bowl, probabilidade float por supplier; referência oficial vanilla: saturação (float)N*m*2F, 1.6/0.8 s -> 32/16 ticks, clamps de FoodData, sorteio servidor u<p.

**targeting:** Não há cast: o consumidor externo é a LivingEntity que come; nenhum alvo hostil, AOE, projétil ou LOS próprio. O record de efeito não recebe entidade/stack.

**costs:** Builder não debita recursos; referência vanilla solicita consume(1,this), preserva materiais infinitos, retorno de recipiente no Player; não é taxa de mana, cooldown ou cobrança de perk.

**integration:** NeoForge físico 21.1.250: getFoodProperties(stack,living) e patch food/eat, PossibleEffect copy, eventos Start/Tick e Finish após finishUsingItem; superfícies de referência, não hooks mutadores homologados. NO_MUTATION.

**validation:** Dois relatórios SHA-exatos e auditores independentes com Mojang client/mappings verificados, testes de roster, pivôs, parâmetros e ledger; consumo externo referencial, sem QA física.

## Referência de fórmulas, identidade e custo

Mojang client 1.21.1 SHA-1 `30c73b1c5da787909b2f73340419fdf13b9def88`, SHA-256 `499f6897d1837516680f3114072d8106e11c9adcd933fe5cf051b551089b0c99`; mappings SHA-256 `140c47931cccc8fc9e4c22d7603e2d714d1a953a146f51ea7397d95c955536ec`. NeoForge 21.1.250 universal e userdev verificados, os mesmos do [manifesto engine](EXACT-DESTROYED-ITEM-ENGINE-REFERENCE-21.1.250.json).

| Método | Pivôs de referência |
|---|---|
| ACFoodBuilder.resolve | nutrição e saturação @11/18; alwaysEdible @30; fast @42; bowl @57; Supplier.get @95, probability @104, effect(instance,F) @107 e build @115. |
| ACFoodBuilder.build | resolve @1, IdentityHashMap via Map.put @10; não lookup; construção clinit @0–7. |
| FoodConstants.saturationByModifier | Code SHA  ce66e1e9569b83c93667549d1b5c4f76d3df1da5a0423ba9c6902adcfed3cb9a; i2f, fmul, fconst_2, fmul; sem clamp nessa função. |
| FoodProperties.Builder | init 1.6F @5, fast 0.8F @1, build chama saturationByModifier @8. |
| FoodProperties.eatDurationTicks | 20F @4, fmul @6, f2i @7. |
| FoodData.add | clamp int @10, float @29, usa foodLevel atualizado. |
| LivingEntity.addEatEffect | server guard @4–10, random @47, probability @54, fcmpg/ifge @57–58, addEffect @67, pop @70; sem aceitação garantida. |
| LivingEntity.eat/ItemStack.consume | addEatEffect @53 antes de consume(1,this) @59; materials infinite @5–8 ou shrink @13. |
| Player.eat | FoodData.eat @5, super @87, Optional recipiente @93, infinite @107, cópia como retorno @129 ou Inventory.add @158 no servidor. |
| NeoForge FoodProperties patch | Possível efeito por supplier; sobrecarga instância cria supplier que retorna essa instância e effect() executa cópia. ACFoodBuilder já resolveu seu supplier, portanto não o transfere intacto. |
| NeoForge EventHooks.onItemUseFinish | Finish ctor @8, EVENT_BUS.post @18, getResultStack @26; patch LivingEntity passa finishUsingItem como argumento. |

As expressões são descrições analíticas de fatos de interoperabilidade, não implementação copiada. Os relatórios não constatam transformações do pack. A presença de ACFoods e de fieldrefs delimita construção; não autoriza fechar os 63 campos como objetos mágicos. A ausência de leituras tipadas de meat/sound e de leitores externos do mapa não exclui reflexão, transformações ou outras versões.

## Reprodução

[JAR probe](../../../../docs/qa/alexscaves_1010_food_builder_probe.py), [referência vanilla/NeoForge](../../../../docs/qa/alexscaves_1010_food_builder_reference.py), [testes](../../../../docs/qa/alexscaves_1010_food_builder_probe_test.py), [workflow](../../../../.github/workflows/alexscaves-1010-food-builder-probe.yml). JDK21, publisher SHA-exato, universal/userdev oficiais e download oficial Mojang verificado. Comandos no workflow.

- [Execução nativa](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44318572341/job/134851123940): `e6453ae5631a104314f67c9d9e337cced60da511e56f226b2b13fb4f39054a77`.
- [Execução ampliada](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44319361784/job/134853907680): referência `7eeb6cfcb82dbe38406c5c5241d6955a10826a66610fe8d1d732e7906189fb50` [artefato temporário](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44319361784/artifacts/14433293321).
- Testes do selo exigem a reprodução de ambos os hashes, rosters, pivôs, limites e ledger; CI atual obrigatória antes de merge. Nenhum JAR ou código-fonte externo versionado.
