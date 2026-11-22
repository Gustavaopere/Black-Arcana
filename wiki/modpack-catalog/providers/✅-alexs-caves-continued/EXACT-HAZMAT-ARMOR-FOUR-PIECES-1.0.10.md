# Hazmat Armor — quatro contratos técnicos estáticos individuais (1.0.10)

**Estado das quatro peças:** ✅ `CERTIFIED_STATIC_7_AXES`, estritamente `STATIC_TECHNICAL_CATALOG_ONLY`. **Não** constitui prova de imunidade ambiental universal, aplicação física, hook mutador ou perks executáveis: `NO_MUTATION`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`, `runtime_dispatch=NOT_VERIFIED`, `provider_universe_closed=false`. Quatro itens existentes, **zero** novas raízes mágicas. Os *sete eixos estáticos* são identidade, comportamento, parâmetros, targeting, custos, integração e validação; cada peça possui registro independente no [manifesto](EXACT-HAZMAT-ARMOR-FOUR-PIECES-1.0.10.json).

## 1. Identidade física, hashes e duas provas independentes

A modlist física do sibling `Gustavaopere/neoforge-rpg-skilltree`, item `PROJECT-INSTRUCTIONS/modlist/World Gen/✅-alexs-caves-continued v1.0.10.md`, declara `alexscaves-1.0.10-neoforge+1.21.1.jar` (`alexscaves`), Minecraft 1.21.1 / NeoForge / Java 21. Artefato publisher verificado: **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. O publisher não equivale a novo dump da instalação: `installed_dump_comparison=NOT_VERIFIED`. A árvore fonte pública 1.1.1 não foi usada para inferir o comportamento de 1.0.10.

A classe `com/github/alexmodguy/alexscaves/server/item/HazmatArmorItem` possui classfile SHA-256 `289395b93a1a223f2e66a02528ccb4ce3a1a659dd9c82ac071a5b63c32b1c7cb`, **seis métodos Code**, zero campos próprios e **sete owners consumidores tipados** na varredura de 1.555 classfiles. São quatro **instâncias** de um mesmo owner, não quatro classes distintas de magia. O relatório original de descoberta tem **176.715 bytes**, SHA-256 `3ef6aeeeb37e0768e206b0777d7193a5ac55a0732ff06d568573c3edf923a033` ([Actions #44942542829](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44942542829), artefato 14722536050). O [selo anterior, conservado como descoberta parcial](EXACT-HAZMAT-ARMOR-DISCOVERY-1.0.10.json) não foi reclassificado retroativamente.

A segunda prova vem do cliente e mappings **oficiais Minecraft 1.21.1**, validados por SHA-1/SHA-256 na [auditoria do enum](EXACT-GINGERBREAD-ARMOR-FOUR-PIECES-1.0.10.md) e reproduzidos na CI Hazmat. O cliente oficial tem SHA-256 `499f6897d1837516680f3114072d8106e11c9adcd933fe5cf051b551089b0c99`; mappings SHA-256 `140c47931cccc8fc9e4c22d7603e2d714d1a953a146f51ea7397d95c955536ec`. A classe mapeada `ArmorItem$Type` possui classfile SHA-256 `304d6345c9ed3d0cdeaea281ed1171b98505b266c04e2b25a023dec665197732` e 51 instruções de inicialização, estabelecendo `HELMET=0`, `CHESTPLATE=1`, `LEGGINGS=2`, `BOOTS=3` e `BODY=4`. O relatório oficial estático de referência tem SHA-256 `e83bef57b5efb722a17fefb237edb7288b1668d99d7dae67e51c1905c174ff91`. **O enum vanilla não prova a execução do classfile transformado no modpack.**

## 2. Identidade, slot e atributos configurados **por peça**

As fábricas `ACItemRegistry.lambda$static$69..72` possuem **seis instruções cada**: instanciam `HazmatArmorItem` com `HAZMAT_SUIT_ARMOR_MATERIAL` e a constante literal `ArmorItem.Type` da respectiva peça. `HazmatArmorItem.<init>` passa `material.vanilla()` e `material.properties(new Item.Properties(), type)` a `ArmorItem.<init>`, sem efeito de resistência própria durante o construtor. O [contrato nativo de ACArmorMaterial](EXACT-ARMOR-MATERIAL-1.0.10.md) define o array de defesa `[2,4,5,2]`, índice ordinal `MAX_DAMAGE_ARRAY=[13,15,16,11]`, multiplicador de durabilidade `20`, encantabilidade `25`, toughness `0,5F`, knockback `0F` e ingrediente de reparo configurado `POLYMER_PLATE` / `alexscaves:polymer_plate`.

| Objeto / ID | Fábrica | Enum / ordinal | Slot consultado | Defesa configurada | Durabilidade máxima solicitada |
| --- | ---: | --- | --- | ---: | ---: |
| [Hazmat Mask](items/hazmat-mask.md) `alexscaves:hazmat_mask` | 69 | `HELMET / 0` | `HEAD` | **2** | **260** |
| [Hazmat Chestplate](items/hazmat-chestplate.md) `alexscaves:hazmat_chestplate` | 70 | `CHESTPLATE / 1` | `CHEST` | **4** | **300** |
| [Hazmat Leggings](items/hazmat-leggings.md) `alexscaves:hazmat_leggings` | 71 | `LEGGINGS / 2` | `LEGS` | **5** | **320** |
| [Hazmat Boots](items/hazmat-boots.md) `alexscaves:hazmat_boots` | 72 | `BOOTS / 3` | `FEET` | **2** | **220** |

Os números são parâmetros enviados à construção nativa da armadura, **não** pontos efetivos de armadura no jogador, dano mitigado ou durabilidade observada após consumo. Nenhuma factory Hazmat usa `BODY / 4`; esse quinto ordinal fica fora dos arrays de quatro posições, e `ACArmorMaterial.defense/properties` não tem guard correspondente. Essa fronteira merece fail-closed para usos hipotéticos de BODY, sem afirmar que eles ocorrem.

Cada item tem modelo e JSON de receita individuais verificados por hash no manifesto antecedente; a tag `repairs_hazmat_suit_armor.json` também foi identificada por hash. A existência desses recursos **não** atesta ingredientes atuais de datapack, desbloqueio, craft, reparo físico, permissões de claim nem apresentação final. Texturas solicitadas: `hazmat_suit_1.png` em `LEGS` e `hazmat_suit_0.png` nos outros três slots.

## 3. Gatilho, causalidade e seis métodos próprios do owner

O `getWornAmount(LivingEntity)` do publisher (40 instruções) avalia **exatamente quatro** chamadas independentes `ItemStack.is(exactItem)` em slots:

| Slot | Registry consultado | Janela | Incremento JVM |
| --- | --- | --- | --- |
| HEAD | `HAZMAT_MASK` | @2–26 | `iinc @26` |
| CHEST | `HAZMAT_CHESTPLATE` | @29–53 | `iinc @53` |
| LEGS | `HAZMAT_LEGGINGS` | @56–80 | `iinc @80` |
| FEET | `HAZMAT_BOOTS` | @83–107 | `iinc @107` |

O resultado `n` é um inteiro de 0 a 4, **contribuição unitária por identidade em slot**; o método não verifica desgaste, NBT, owner, mundo ou Mastery. A contribuição de uma peça não significa que todas as condições de todos os consumidores foram satisfeitas. O fator calculado nesses consumidores é `f=1−n/4`, tomando `1;0,75;0,5;0,25;0` para `n=0;1;2;3;4`.

- `<init>` (12 instruções): delegação para `ACArmorMaterial` e `ArmorItem`, sem cast.
- `acInventoryTick` (16): exige `Player` e `ACCompat.isWornArmor` antes de solicitar `acArmorTick`; este helper/dispatcher não foi promovido a runtime verificado.
- `acArmorTick` (158): apenas a **máscara** passa no teste `HAZMAT_MASK`. Com `cos(player.tickCount×0,05) ≥ 0,8999999761581421` e dois sorteios visuais independentes, solicita partículas `HAZMAT_BREATHE` próximas da cabeça. Não adiciona proteção, status ou mana própria; apresentação física não foi executada.
- `getArmorTexture` (7): seleciona variante de pernas `1`, senão `0`.
- `getWornAmount` (40): contagem de quatro identidades em slots, sem escrita.
- `initializeClient` (6): encaminha extensão de renderização, não modifica propriedades mágicas.

O auditor reproduz **cada** método, descriptor, quantidade e SHA-256 de instruções e reconcilia o censo de consumers tipados. Os quatro callbacks de fábrica do registro também são verificados por offsets de material e tipo, sem extrapolar existência de registry carregado ou efeitos herdados na engine transformada.

## 4. Consumidores: parâmetros e consequências distintas

**RadioactiveItem e RadioactiveBlockItem — `acInventoryTick`, 73 instruções cada.** Exigem execução no servidor, portador `LivingEntity`, não estar em modo criativo (quando Player) e ausência de `Irradiated` prévio. Calculam chance local **`p = stack.count × randomChanceOfRadiation × f`** e só solicitam `MobEffectInstance(IRRADIATED, 1800 ticks)` se `nextFloat() < p`. A chamada `addEffect` descarta seu boolean; a mensagem de visualidade posterior não prova aplicação aceita. **Com n=4, f=0 e este sorteio não solicita nova aplicação desse efeito nesses dois métodos.** O valor `randomChanceOfRadiation` é **campo por instância de item**, não foi fechado para todos os subtipos da versão; a proteção de outras fontes de radiação permanece desconhecida.

**IrradiatedEffect.tick — 42 instruções.** Usa `f=1−0,25n`. Apenas `Player` com **n=0** recebe pedido de `causeFoodExhaustion(0,4F)` nessa rotina. Para entidade distinta de `RaycatEntity` e `nextFloat()<f+0,1`, solicita `hurt(causeRadiationDamage, f)`; resultado de `hurt` é descartado. **Com n=4, f=0, ainda existe sorteio de chance 0,1 de chamar `hurt` com argumento zero.** Nem a aceitação do evento, nem a saúde final, nem eventuais efeitos colaterais de `hurt(0)` são provados.

**AcidBlock.entityInside — 174 instruções.** Primeiro exige ausência da tag `RESISTS_ACID` e altura de ácido **maior que 0,1**. Ao inspecionar a armadura do alvo, a rotina exclui `instanceof HazmatArmorItem` do desgaste e pode solicitar `hurtAndBreak(1)` para **outra** armadura danificável com sorteio **0,05** (e guarda adicional de jogador criativo). Esses wear requests são independentes do ramo posterior de dano ácido. Para LivingEntity usa o mesmo `f`; somente com `nextFloat()<f` entra no ramo de dano, cujo argumento solicitado é `f×(outra armadura detectada?0,01:1)+(WEAK_TO_ACID?10:0)`. **Com quatro peças, f=0 e esse ramo do próprio AcidBlock não é alcançado**, sem afirmar imunidade a outros tipos de ácido ou modificadores externos. O método ainda contém efeitos de apresentação/sons, sem autorizar world mutation ao Black Arcana.

**ACArmorRenderProperties e ACItemRegistry:** são consumidores tipados de modelo e construção; não representam um novo poder, damage type ou efeito de combate. Nenhum método do owner possui linha de cast, targeting ofensivo, LOS, raycast, AOE, projétil, summon, cooldown, gasto de mana ou escala por nível de spell. Dano e status são **solicitações feitas pelos consumidores ambientais**, não habilidades ativas do portador.

## 5. Autoridade, custos, estado, persistência e integração

**Owner:** o parâmetro `LivingEntity` é quem veste o equipamento e recebe eventual efeito externo; `Player` é exigido apenas para a rotina visual de máscara. O método de contagem não grava owner UUID. **Custo:** nenhuma avaliação de `getWornAmount`, nem `acInventoryTick` das peças, debita mana, stamina, charge ou durabilidade na classe. A durabilidade do material é um máximo solicitado, não prova de desgaste/reparo transacionado. `AcidBlock` pode solicitar desgaste de outros itens, sem transformar proteção Hazmat em custo próprio.

**Persistência, rede e compatibilidade:** `ItemStack` e efeitos herdados, chamadas `ACCompat`, slots carregados, sincronismo visual, prioridades de eventos, complementos de outros mods, reload e configuração/datapack da instalação **não foram observados fisicamente**. O censo tipado percorreu o publisher e seus consumidores diretos selecionados; **não** garante fechamento reflexivo ou universal de todas as fontes ácidas/radioativas. O quinto ordinal `BODY` permanece caso sem factory suportada. `physical_qa=NOT_TESTED` não significa que o item não funcione; significa ausência de ensaio físico certificado.

**Perks:** alterações na contagem por item afetariam pelo menos três contextos de risco (inicialização de Irradiated, ticks do status e ácido) e poderiam alterar status, dano e exaustão. Um hook genérico de atributo de item não identifica por si um jogador elegível nem fornece autoridade sobre esses consumidores. Não sobrescrever os maps/campos globais de material, aplicar nova imunidade ou duplicar XP/Mastery por tick. O RPG Skill Tree fornece progressão/Mastery apenas se um contrato real e seguro for verificado; Black Arcana retém a autoridade do runtime mágico e da política D007/WorldEffectPolicy. **Sem esse contrato: `NO_MUTATION` e fail-closed.**

## 6. Reprodução, testes negativos e critérios de avanço

O [checker individual](../../../../docs/qa/alexscaves_1010_hazmat_four_cert_checks.py) liga:

1. artefato publisher verificado por tamanho/SHA-1/SHA-256 e relatório nativo reproduzido com a [sonda antecedente](../../../../docs/qa/alexscaves_1010_hazmat_armor_discovery.py);
2. selo anterior de descoberta da classe, seis métodos e sete consumidores, sem mudá-lo retroativamente;
3. contrato de material SHA-exato, fórmula e arrays indexados;
4. cliente e mappings oficiais Minecraft 1.21.1, enumeradores, ordinais e offsets, sem tratá-los como runtime transformado;
5. quatro fichas, factories, recursos, parâmetros e limites do manifesto novo.

Executar [workflow de certificação](../../../../.github/workflows/alexscaves-1010-hazmat-four-static-cert.yml) na mesma HEAD: coleta material/enum oficial e publisher, reproduz relatórios com identidade imutável, valida o checker anterior, verifica **34 controles adversariais em memória, incluindo quatro alterações JVM com hashes internos recalculados**, e testa integração de índices por CI do repositório. O número de controles não implica gameplay QA; os casos mutados são dados sintéticos, nunca chamadas de mundo. A certificação estática é específica para estas quatro peças; não fecha as famílias de outros equipamentos nem o universo do provider.

**Gates ainda abertos:** dump do JAR da instalação real; classfile/mixins efetivamente transformados na versão NeoForge do pack; lista completa de todas as fontes de radiação/ácido e config por item; alterações por datapack, sistema de efeitos, reparos, loot/crafting; save/restart, mundo protegido, PvP/multiplayer; comportamento de partículas e chamadas `hurt` com argumento zero; hook seguro por usuário. Nenhum hook foi implementado, nenhuma Stage avançou e nenhuma QA física foi executada.
