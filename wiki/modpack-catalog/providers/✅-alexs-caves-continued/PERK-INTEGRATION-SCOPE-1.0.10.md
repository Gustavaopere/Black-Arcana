# Alex's Caves Continued 1.0.10 — escopo de integrações ainda aberto

**ACSwingControlItem — contrato estático delimitado (candidato #1126):** [ficha](systems/swing-control-item.md), [prova](EXACT-SWING-CONTROL-ITEM-CONTRACT-1.0.10.md) e [selo](EXACT-SWING-CONTROL-ITEM-CONTRACT-1.0.10.json). Dois predicados do clube e fronteira oficial auditados. **91/91 contratos estáticos**, **10/10 suportes** no recorte candidato; +1 ficha, +0 raízes. Próximo `server/item/ACTickingItem`, reservado #1127. Provider OPEN, NO_MUTATION; checkpoints anteriores são históricos.

**ACRepairableItem — contrato estático delimitado (checkpoint histórico #1124 integrado):** [ficha](systems/repairable-item.md), [prova](EXACT-REPAIRABLE-ITEM-CONTRACT-1.0.10.md) e [selo](EXACT-REPAIRABLE-ITEM-CONTRACT-1.0.10.json). Cinco implementadores, seis materiais, predicate e boundaries de referência auditados. **90/90 contratos estáticos** e **9/9 suportes** no recorte candidato; +1 ficha, +0 raízes. Próximo `server/item/ACSwingControlItem`. Provider OPEN, NO_MUTATION; checkpoints anteriores são históricos.

**ACItemRegistry — contrato estático delimitado (checkpoint histórico):** [ACItemRegistry](systems/item-registry.md), [prova](EXACT-ITEM-REGISTRY-CONTRACT-1.0.10.md) e [selo](EXACT-ITEM-REGISTRY-CONTRACT-1.0.10.json) documentam bindings declarados, registro diferido e callbacks nativos locais, com fronteira de `ACDeferredRegister` delimitada. A classe declaradora possui 200 campos e 208 métodos no publisher 1.0.10; os 188 bindings de campos `Supplier` e 43 declarações adicionais de spawn eggs representam 231 pedidos estáticos de registro, sem certificação individual dos itens, projéteis ou efeitos completos. **+1 ficha/certificado de suporte, +0 raízes:** **89/89 contratos estáticos** e **8/8 suportes** no recorte observado. Próximo símbolo sem disposição: `server/item/ACRepairableItem`, reservado à PR #1124 sem promoção de status. Provider **OPEN**, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`, `NO_MUTATION`. Os checkpoints anteriores são históricos.

**Continuidade #1122 (checkpoint histórico):** [ACFoods](systems/foods.md) — [contrato estático candidato](EXACT-FOODS-CONTRACT-1.0.10.md) e [selo](EXACT-FOODS-CONTRACT-1.0.10.json), 63 campos, 46 suppliers, 121 sites, boundary nativo e referência vanilla. +1 ficha/certificado de suporte, +0 raízes. Naquele checkpoint, o recorte candidato era **88/88 contratos estáticos**, **7/7 suportes**; `server/item/ACItemRegistry` era o próximo símbolo, reservado na #1123. Provider OPEN, NO_MUTATION; checkpoints abaixo são históricos.

**Continuidade #1121 (checkpoint histórico):** [ACFoodPropertiesItem](EXACT-FOOD-PROPERTIES-ITEM-MARKER-1.0.10.md) — marcador vazio, disposição de suporte SHA-exata ([manifesto](EXACT-FOOD-PROPERTIES-ITEM-MARKER-1.0.10.json)); 0 campos, 0 métodos, 1 implementador direto (BiomeTreatItem), sem referências tipadas a membros. +0 fichas/certificados/raízes. Recorte 87/87, suportes 6/6; próximo símbolo sem disposição: `server/item/ACFoods`. BiomeTreatItem continua aberto; provider OPEN, NO_MUTATION.

**Continuidade #1120 (checkpoint histórico):** [ACFoodBuilder](systems/food-builder.md) recebe [contrato estático](EXACT-FOOD-BUILDER-CONTRACT-1.0.10.md) e [selo](EXACT-FOOD-BUILDER-CONTRACT-1.0.10.json), builder/record e parâmetros de alimentação, consumers tipados e referência vanilla/NeoForge. Recorte **87/87 certificados**, **6/6 suportes**, +1 ficha/certificado, zero raízes. Provider OPEN, NO_MUTATION, hook NOT_VERIFIED, QA NOT_TESTED, perk NOT_CERTIFIED. Próximo símbolo sem disposição: `server/item/ACFoodPropertiesItem`; ACFoods permanece aberto. Checkpoints abaixo são históricos.

**Continuidade #1119 (checkpoint histórico):** [ACEnchantableItem](systems/enchantable-item.md) recebe [contrato estático](EXACT-ENCHANTABLE-ITEM-CONTRACT-1.0.10.md) e [selo](EXACT-ENCHANTABLE-ITEM-CONTRACT-1.0.10.json), 13 owners, 13 bindings, exceção Ortholance e 51 recursos/14 tags. Naquele checkpoint **86/86 certificados**, **5/5 suportes**, +1 ficha/certificado, +0 raízes. Provider OPEN, NO_MUTATION, hook NOT_VERIFIED, QA NOT_TESTED, perk NOT_CERTIFIED. Próximo símbolo sem disposição: `server/item/ACFoodBuilder`. Checkpoints abaixo são históricos.

**Certificação incremental — PR #1118:** [ACDynamicAttributeItem](systems/dynamic-attributes.md) conclui seu [contrato estático individual](EXACT-DYNAMIC-ATTRIBUTE-CONTRACT-1.0.10.md) e [selo](EXACT-DYNAMIC-ATTRIBUTE-CONTRACT-1.0.10.json), abrangendo construtores, callbacks, 15 bindings, atributos e cache nativos, mais a referência do builder NeoForge 21.1.250. Naquele checkpoint: **85/85 contratos estáticos**, quatro fichas de suporte; **+1 certificado, +0 candidatos, +0 raízes mágicas**. Provider **OPEN**, `NO_MUTATION`, hooks `NOT_VERIFIED`, QA física `NOT_TESTED`, perks `NOT_CERTIFIED`. Próximo símbolo sem disposição: `server/item/ACEnchantableItem`. Os checkpoints anteriores são históricos.

**Continuidade reconciliada — PR #1116 (checkpoint histórico):** [ACDynamicAttributeItem](systems/dynamic-attributes.md) possui ficha individual ⚠️ parcial e [prova binária](EXACT-DYNAMIC-ATTRIBUTE-DISCOVERY-1.0.10.md). Naquele checkpoint o recorte era **84/85 contratos estáticos certificados (98,8%)**, com **3/4 suportes certificados**; o certificado de ACDestroyedItem integrado pela #1117 permanece intacto. Próxima classe sem disposição: `server/item/ACEnchantableItem`; ACDynamicAttributeItem permanece sem certificado. Zero novas raízes mágicas, `NO_MUTATION`, hook `NOT_VERIFIED`, QA física `NOT_TESTED`, provider OPEN. Os números 84/84 abaixo registrados como checkpoint da #1117 são históricos.

**Conclusão incremental — 18/11/2026:** a ficha existente [ACDestroyedItem](systems/destroyed-item.md), acrescentada parcialmente pela PR #1115, tem agora [contrato técnico estático certificado](EXACT-DESTROYED-ITEM-CONTRACT-1.0.10.md) e [selo reproduzível](EXACT-DESTROYED-ITEM-CONTRACT-1.0.10.json). Naquele checkpoint, o recorte observado alcançava **84/84 contratos estáticos (100%)**, com **3/3 fichas de suporte**: **+1 certificado, +0 candidatos e +0 raízes mágicas**. O certificado delimita ABI, implementação, bindings nativos e fronteiras externas; aceitação de efeitos, World Safety, hook e QA física conservam seus estados próprios. `STATIC_TECHNICAL_CATALOG_ONLY`, `NO_MUTATION`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`; provider **OPEN**. O próximo escopo sem certificado é `server/item/ACDynamicAttributeItem`.

Os recortes das oito ações mágicas e dos oito efeitos registrados têm contratos estáticos próprios. Eles **não cobrem todo o conteúdo integrável por perks** do mod. A classificação histórica `EXCLUDED` em [42 classes de interação](ITEM-ACTION-DISPOSITION-1.0.10.md) significa exclusão do denominador de magia, não exclusão do trabalho de integração.

Autoridade: JAR 1.0.10, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes. O [inventário JSON](INTEGRATION-SCOPE-INVENTORY-1.0.10.json) enumera os nomes exatos abaixo a partir do artefato, sem importar os parâmetros da fonte 1.1.1. [Limites e reprodução](EXACT-TECHNICAL-CONTRACTS-1.0.10.md).

| Família | Universo exato identificado | Trabalho necessário antes de fechar o provider |
|---|---|---|
| Ações sobrenaturais | Oito raízes já contadas | Sete campos estáticos documentados nas oito fichas; hooks e QA física separados |
| Itens / equipamento | 81 classes externas de itens; 42 com assinaturas de interação já classificadas semanticamente | Os oito contratos de suporte incluem [ACArmorMaterial](systems/armor-material.md), [ACClientExtensionItem](systems/client-extension.md), [ACDestroyedItem](systems/destroyed-item.md), [ACDynamicAttributeItem](systems/dynamic-attributes.md), [ACEnchantableItem](systems/enchantable-item.md), [ACFoodBuilder](systems/food-builder.md), [ACFoods](systems/foods.md) e [ACItemRegistry](systems/item-registry.md); `ACArmorTickItem` e `ACFoodPropertiesItem` são marcadores vazios com disposição explícita, sem ficha própria. [Dreadbow](equipment/dreadbow.md), [Desolate Dagger](equipment/desolate-dagger.md) e [Shot Gum](equipment/shot-gum.md) documentados individualmente; demais armas, movimento, comida, defesa e helpers precisam de disposição própria. Classes e fichas não são denominadores equivalentes |
| Enchantments | 51 JSONs em `data/alexscaves/enchantment/` ([índice nominal e pendências por encantamento](ENCHANTMENT-PERK-CROSSWALK-1.0.10.md)) | Ficha por contrato: nível/custo/slots/exclusividade e consumidor real de cada modifier, inclusive tecnologia/armas |
| Damage types | 11 JSONs, 11 factories e seus consumidores diretos localizados no JAR | **11/11 contratos estáticos documentados (100% do recorte de JSONs publisher):** [Acid](damage-types/acid.md), [Dark Arrow](damage-types/dark-arrow.md), [Desolate Dagger](damage-types/desolate-dagger.md), [Forsaken Sonic Boom](damage-types/forsaken-sonic-boom.md), [Gumball](damage-types/gumball.md), [Radiation](damage-types/radiation.md), [Intentional Game Design](damage-types/intentional-game-design.md), [Nuke](damage-types/nuke.md), [Spirit Dinosaur](damage-types/spirit-dinosaur.md), [Raygun](damage-types/raygun.md), [Tremorzilla Beam](damage-types/tremorzilla-beam.md). [Prova Raygun](EXACT-RAYGUN-CONTRACT-1.0.10.md) e [prova nuclear](EXACT-NUCLEAR-CONTRACTS-1.0.10.md), preservando o mismatch de tickets e toda QA física pendente |
| Mob effects | Oito campos de registro de efeitos | **8/8 contratos estáticos documentados**, incluindo aplicações e consumidores; [fichas](effects/INDEX.md) e [prova exata](EXACT-EFFECT-CONTRACTS-1.0.10.md). Hooks e QA física pendentes |
| Potions | 12 campos de registro de poções | Conteúdo, níveis/tempo e aquisição, sem contar variantes como novas magias |
| Config servidor | 40 campos em `ACServerConfig` | Defaults/bounds, momento de leitura, autoridade global/por jogador e consumidores; não presumir valores em execução |
| Config cliente | 15 campos em `ACClientConfig` | Distinguir HUD, luz, shader, som e câmera de comportamento servidor e atributos |
| Rede | 18 classes externas sob `server/message/`, incluindo transporte/helpers | Direção, registro/protocolo, autenticação, seleção de entidade, limites, autoridade e lifecycle |
| Mobs/montarias e eventos | Classes e interfaces inventariadas, sem denominador final de fichas | Atributos, dano, targeting, domesticação/reputação, medidores e skills de montaria; separar AI de raiz mágica do jogador |
| Mundo, dados e compatibilidade | Registries, block entities, tags, loot, crafting e mixins | Disposição explícita por consumidor ou suporte; aquisição, proteção e persistência não podem ser inferidas de assets |

Essas famílias se sobrepõem. Não somar 81+51+11 etc. como denominador final: um item pode ser owner de uma ação existente, uma classe base pode atender vários registros e um efeito pode ter vários consumidores. Os números descrevem superfícies identificadas, não novas fichas concluídas ou novos spells.

## Contratos não mágicos que não podem ser descartados

Dreadbow, spears, Ortholance, Desolate Dagger e Primitive Club oferecem combate e modifiers. Galena Gauntlet, Raygun, Quarry Smasher e Remote Detonator oferecem controle magnético, energia, mineração e explosivos. Candy Cane Hook, Floater e Submarine oferecem mobilidade. Armor passiva, comida e itens como Sack of Sating, Gazing Pearl e Holocoder também precisam de disposição de integração. Os nomes e assinaturas estão no inventário; isoladamente não constituem revisão completa de seus corpos. Os contratos individuais já certificados, incluindo o recorte nativo de Raygun, mantêm os limites descritos em suas próprias fichas.

As interfaces de montaria `FlyingMount`, `KeybindUsingMount` e `RidingMeterMount`, assim como `CommonEvents`, progresso de Cave Book e reputação Deep One, são candidatos a contratos de sistemas. Uma assinatura de API não é, sozinha, um hook seguro. A próxima catalogação deve documentar o consumidor, os parâmetros e os limites de autoridade antes de marcar essas superfícies completas.

## Estado dos índices

As oito ações, oito efeitos, os três equipamentos e os onze contratos de dano somam 30 contratos estáticos. Com os 51 contratos individuais de encantamentos do [crosswalk](ENCHANTMENT-PERK-CROSSWALK-1.0.10.md) e os dez contratos de suporte de [ACArmorMaterial](systems/armor-material.md), [ACClientExtensionItem](systems/client-extension.md), [ACDestroyedItem](systems/destroyed-item.md), [ACDynamicAttributeItem](systems/dynamic-attributes.md), [ACEnchantableItem](systems/enchantable-item.md), [ACFoodBuilder](systems/food-builder.md), [ACFoods](systems/foods.md), [ACItemRegistry](systems/item-registry.md), [ACRepairableItem](systems/repairable-item.md) e [ACSwingControlItem](systems/swing-control-item.md), o provider registra **91/91 contratos estáticos certificados entre as fichas do recorte observado (100% desse recorte)**. Os **51/51 dossiers de encantamentos estão concluídos no recorte estático publisher (100%)**, sem fichas parciais dessa família. Contratos: [Arrow Inducting](enchantments/arrow-inducting.md), [Astral Transferring](enchantments/astral-transferring.md), [Bonking](enchantments/bonking.md), [Bouncing Bolt](enchantments/bouncing-bolt.md), [Bouncy Ball](enchantments/bouncy-ball.md), [Charting Call](enchantments/charting-call.md), [Chomping Spirit](enchantments/chomping-spirit.md), [Crystallization](enchantments/crystallization.md), [Dark Nock](enchantments/dark-nock.md), [Dazing Sweep](enchantments/dazing-sweep.md), [Detonating Death](enchantments/detonating-death.md), [Double Stab](enchantments/double-stab.md), [Energy Efficiency](enchantments/energy-efficiency.md), [Enveloping Bubble](enchantments/enveloping-bubble.md), [Explosive Flavor](enchantments/explosive-flavor.md), [Far Flung](enchantments/far-flung.md), [Ferrous Haste](enchantments/ferrous-haste.md), [Field Extension](enchantments/field-extension.md), [Flinging](enchantments/flinging.md), [Gamma Ray](enchantments/gamma-ray.md), [Heavy Slam](enchantments/heavy-slam.md), [Herd Phalanx](enchantments/herd-phalanx.md), [Humungous Hex](enchantments/humungous-hex.md), [Impending Stab](enchantments/impending-stab.md), [Lasting Morale](enchantments/lasting-morale.md), [Multiple Mint](enchantments/multiple-mint.md), [Peppermint Punting](enchantments/peppermint-punting.md), [Plummeting Flight](enchantments/plummeting-flight.md), [Precise Volley](enchantments/precise-volley.md), [Rapid Possession](enchantments/rapid-possession.md), [Relentless Darkness](enchantments/relentless-darkness.md), [Sated Blade](enchantments/sated-blade.md), [Sea Swing](enchantments/sea-swing.md), [Seapairing](enchantments/seapairing.md), [Second Wave](enchantments/second-wave.md), [Seekcandy](enchantments/seekcandy.md), [Shaded Respite](enchantments/shaded-respite.md), [Sharp Cane](enchantments/sharp-cane.md), [Sightless](enchantments/sightless.md), [Soak Seeking](enchantments/soak-seeking.md), [Solar](enchantments/solar.md), [Spell Lasting](enchantments/spell-lasting.md), [Straight Hook](enchantments/straight-hook.md), [Swiftwood](enchantments/swiftwood.md), [Targeted Ricochet](enchantments/targeted-ricochet.md), [Taxing Bellow](enchantments/taxing-bellow.md), [Triple Splash](enchantments/triple-splash.md), [Triple Split](enchantments/triple-split.md), [Tsunami](enchantments/tsunami.md), [Twilight Perfection](enchantments/twilight-perfection.md), [X Ray](enchantments/x-ray.md). Raygun e Tremorzilla Beam possuem certificados estáticos individuais; os 11/11 JSONs de dano também estão concluídos no recorte estático publisher. Hooks mutadores, QA física e universo integral do provider continuam abertos; a fila alfabética permanece em **Alex's Caves Continued**, com `server/item/ACTickingItem` como próximo escopo sem disposição, reservado à PR #1127. O prefixo revisado possui doze entradas, de ACArmorMaterial a ACSwingControlItem, incluindo as duas disposições de marcador vazio; as onze entradas anteriores e o inventário físico permanecem preservados. Completar 91 fichas observadas não fecha esse universo.

## Dreadbow e Dark Arrow — contrato consolidado

A [prova conjunta](EXACT-DREADBOW-CONTRACTS-1.0.10.md) e as duas fichas acompanham o contador de tiro perfeito, a duração real de uso, a sincronização de `CUSTOM_DATA`, os caminhos de disparo, a fórmula solicitada de dano e os filtros de colisão. Defaults, setters e decisões anteriormente inventariados permanecem nos manifestos de apoio imutáveis; sua existência isolada não homologa API de perks.

Uma perk de duração, alcance, dano, tipo de alvo ou frequência precisa escolher o consumidor correto e preservar a autoridade nativa. **`mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`**. Não há nova raiz mágica, adapter executável ou promoção de Stage.

## Acid — dois emissores com contratos distintos

A [prova de Acid](EXACT-ACID-CONTRACT-1.0.10.md) acompanha a fórmula ambiental probabilística, a contagem de peças Hazmat, o contato do drum, seu movimento e os guards de colocação/limpeza de fluido. Esses caminhos compartilham o tipo de dano, mas mantêm filtros e parâmetros próprios. Corrosão, o sistema completo de fluidos e toda a AI do Brainiac continuam superfícies separadas; o recorte de dano não encerra esses sistemas nem o provider.

## Desolate Dagger — equipamento e entidade separados

A [prova conjunta](EXACT-DESOLATE-DAGGER-CONTRACTS-1.0.10.md) relaciona o callback de ataque do item, a produção de entidades, os dados sincronizados, órbita/stab, solicitação de dano e descarte. O produtor nativo não preenche o ID de jogador usado pela entidade; autoria e benefícios condicionados a Player mantêm essa fronteira explícita. Os dois contratos não encerram todos os equipamentos, encantamentos ou sistemas de combate.

## Forsaken Sonic — contrato consolidado do ataque

A [prova consolidada](EXACT-FORSAKEN-CONTRACT-1.0.10.md) liga seleção de alvo, início/encerramento do goal, temporização, animações, produtor/consumo de carga, geometria e dano solicitado. Os cinco manifestos parciais anteriores permanecem preservados como evidências históricas; suas flags não homologam runtime. O contrato da ficha é estático e delimitado: não encerra toda a IA do Forsaken nem habilita intervenção em `LivingEntity.hurt`, `SynchedEntityData`, animação ou `knockback`. Hooks mutadores e QA física seguem pendentes.

## Shot Gum e Gumball — equipamento, projétil e emissores

A [prova consolidada](EXACT-GUMBALL-CONTRACTS-1.0.10.md) acompanha os métodos próprios do item e da entidade, os emissores Gumbeeper e os recursos de encantamento. A munição e o estado da arma, os parâmetros do mob, a fábrica dos descendentes, o dano de impacto e a explosão mantêm consumidores próprios. Esses contratos não encerram o mob inteiro, a configuração de rede ou o universo do provider, nem concedem hooks mutadores.

## Intentional Game Design e Nuke — dois modos, um consumidor

A [prova consolidada](EXACT-NUCLEAR-CONTRACTS-1.0.10.md) relaciona os 20 membros próprios da entidade, quatro emissores, dano, movimento, radiação, blocos e tickets. A seleção de fonte não duplica a chamada de dano. A certificação é apenas estática: o mismatch de categorias de ticket permanece, e NT-01…NT-07 continuam NOT_TESTED.

## Spirit Dinosaur — consumidores e autoria distintos

A [prova consolidada](EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.md) fecha a ficha existente dos espíritos/lança: os três tipos têm funções diferentes, a flag de dano é atualizada em ordem distinta nos dois consumidores e a explosão Tephra usa outro mecanismo nativo. Custos, produção, defesa Grotto, targeting e persistência continuam com seus owners próprios. Naquele checkpoint, o índice passou a 28/30 contratos observados; o universo do provider, hooks e QA física permanecem abertos.

## Heavy Slam — primeiro contrato estático individual de encantamento

A [ficha](enchantments/heavy-slam.md) e o [manifesto reproduzível](EXACT-HEAVY-SLAM-CONTRACT-1.0.10.md) documentam JSON, custos/slots, dano inicial 6+3L, pulsos posteriores2F, área/targeting e as fronteiras de knockback, dois lados lógicos e durabilidade. A conclusão não certifica todo Resistor Shield, não transforma relâmpagos visuais em DamageType elétrico e não concede hook mutador ou QA física.

## Herd Phalanx — quantidade e defesa Grotto

A [ficha individual](enchantments/herd-phalanx.md) e o [selo](EXACT-HERD-PHALANX-CONTRACT-1.0.10.md) reaproveitam a cadeia Spirit Dinosaur para documentar 3+L tentativas de criação, órbita, UUID, consumo e limpeza. Pedido de dano zero no Pre e marcação fading não equivalem a imunidade ou descarte instantâneo medidos. O contrato é estático; hooks, QA física e universo do provider permanecem abertos.

## Impending Stab — espera e dano em momentos diferentes

A [ficha](enchantments/impending-stab.md) e o [selo](EXACT-IMPENDING-STAB-CONTRACT-1.0.10.md) reaproveitam Desolate Dagger: nível positivo escolhe 40–49 no produtor; dano `2+2L` é relido no stab. Stack sem cópia própria, PLAYER_ID não preenchido, exclusividade declarada e descarte após tentativa são limites explícitos. Somente o contrato estático individual é concluído; hooks e QA física continuam pendentes.

## Lasting Morale — tempo compartilhado e persistência condicionada

A [ficha](enchantments/lasting-morale.md) e a [prova](EXACT-LASTING-MORALE-CONTRACT-1.0.10.md) distinguem carga/custo, leitura de `1200+400L`, contador e cooldown por Item, tentativas de spawn, fade e UUID/NBT. Somente o contrato estático individual é concluído; não se alteram as ações existentes, ataques dos mobs, hooks mutadores ou QA física.

## Multiple Mint — quantidade e distribuição ligadas

A [ficha](enchantments/multiple-mint.md) e a [prova](EXACT-MULTIPLE-MINT-CONTRACT-1.0.10.md) acompanham `3+L` no loop e no denominador angular, pedidos de inserção/custo/cooldown, dimensões, movimento, dano, owner e NBT. Essa conclusão é estática e individual; não certifica inserções aceitas, DPS, hooks ou QA física.

## Relentless Darkness — cadência e carga visual separadas

A [ficha](enchantments/relentless-darkness.md) e a [prova](EXACT-RELENTLESS-DARKNESS-CONTRACT-1.0.10.md) acompanham o desvio do release para onUseTick, o módulo do timer restante, o M5/incremento3 visual cliente e custos/dano por seus consumidores nativos. A conclusão é estática e individual; não homologa frequência física, DPS, rede ou perks mutadoras.

## Sated Blade — saturação e atribuição condicionais

A [ficha](enchantments/sated-blade.md) e a [prova](EXACT-SATED-BLADE-CONTRACT-1.0.10.md) acompanham hurt aceito, leitura tardia, fonte Player e gate anterior à soma de saturação. O produtor não preenche PLAYER_ID; posição copiada e stack não estabelecem beneficiário. A conclusão é apenas estática, sem corrigir runtime, promover hook ou substituir QA física.

## Seapairing — manutenção passiva e limite da engine

A [ficha](enchantments/seapairing.md) e a [prova](EXACT-SEAPAIRING-CONTRACT-1.0.10.md) cobrem o despacho via interface, callback completo, selected ignorado, uso comparado por equals, RNG antes do ambiente e pedido literal `Math.min(0,D−1)`. O valor armazenado e a distribuição do callback a inventários externos não são resultados certificados. Nenhum hook, crédito de Mastery, mudança de runtime ou QA física foi promovido.

## Shaded Respite — luz, desgaste e munição separados

A [ficha](enchantments/shaded-respite.md) e a [prova](EXACT-SHADED-RESPITE-CONTRACT-1.0.10.md) acompanham o predicado de luz na posição do veículo raiz, nível positivo, gate inicial de munição/creative e custos dos caminhos release/Relentless. A isenção de munição exige o item `Items.ARROW`, enquanto conversibilidade do projétil e factories seguem contratos distintos. A conclusão estática não torna o release inteiro auditado nem homologa execução exclusiva no servidor, hook mutador ou QA física.

## Sharp Cane — snapshot, busca e colisão separados

A [ficha](enchantments/sharp-cane.md) e a [prova](EXACT-SHARP-CANE-CONTRACT-1.0.10.md) ligam `3F×L` capturado na criação ao pedido de dano no ramo de busca do tick. UUID anterior ao hurt e retorno descartado não são recibos de dano aceito; o callback `onHitEntity` não contém esse hurt. O prefixo 256/546 permanece parcial, e persistência herdada, engine, hooks mutadores e QA física não são homologados.

## Triple Splash — quantidade solicitada e resultado separados

A [ficha](enchantments/triple-splash.md) e a [prova](EXACT-TRIPLE-SPLASH-CONTRACT-1.0.10.md) ligam o nível positivo à seleção de três tentativas de Water Bolt, com geometria e parâmetros nativos por instância. O custo posterior ao loop não cria um débito por projétil; inserção, targeting, homing, ricochete, hits e dano aplicado conservam contratos próprios. O tick parcial permanece delimitado; hooks mutadores e QA física não são homologados.

## Triple Split — snapshot, dano e filhos separados

A [ficha](enchantments/triple-split.md) e a [prova](EXACT-TRIPLE-SPLIT-CONTRACT-1.0.10.md) ligam o nível positivo ao flag capturado no disparo do Shot Gum. O callback tenta três filhos após o ramo de dano, sem usar aceitação do hurt como recibo; a factory do laço não atribui owner. Parâmetros correntes copiados, máximo de bounces, custos e NBT conservam autoridades próprias. O método de disparo parcial permanece delimitado; hooks mutadores e QA física não são homologados.

## Tsunami — onda e ataque direto separados

A [ficha](enchantments/tsunami.md) e a [prova](EXACT-TSUNAMI-CONTRACT-1.0.10.md) ligam o nível positivo e carga elegível no servidor a uma tentativa de onda escala 5. O salto nativo pula a consulta Second Wave e chega ao ataque direto separado; fontes, filtros, volumes, dano e knockback conservam autoridades próprias. Espera 2 e lifespan 20 não são duração física garantida; owner por campo/getter e NBT próprio mantêm fronteiras distintas. Métodos parciais continuam delimitados; hooks mutadores e QA física não são homologados.

## Arrow Inducting — conversão e herança delimitadas

A [ficha](enchantments/arrow-inducting.md) e a [prova](EXACT-ARROW-INDUCTING-CONTRACT-1.0.10.md) consolidam o contrato do evento, os 12 membros comportamentais da flecha e seu inicializador estático, filtros e movimento, custos e campos próprios. A herança permanece identificada como binário de compilação; aceitação de spawn/dano, runtime transformado, PvP/claims, hook mutador, crédito de Mastery e QA física continuam sem homologação. Não há nova raiz mágica nem fechamento do provider.

## Astral Transferring — transferência, custo e identidade separados

A [ficha](enchantments/astral-transferring.md) e a [prova](EXACT-ASTRAL-TRANSFERRING-CONTRACT-1.0.10.md) documentam o ramo servidor de transferência por saúde/cadência, o laço que conserva o controlado original, os filtros e os marcadores. Desgaste solicitado no cliente, estado sincronizado/UUID, serialização e pacote não equivalem a custo ou resultado autorizado. Hooks, runtime transformado, crédito Mastery e QA física continuam pendentes; os recortes parciais permanecem explícitos.

## Bonking — oportunidade, contexto de loot e resultado separados

A [ficha](enchantments/bonking.md) e a [prova](EXACT-BONKING-CONTRACT-1.0.10.md) consolidam o evento completo, ator direto e arma atual, a chance nominal e as entidades temporárias não inseridas no mundo. Backup/zero/restore de equipamento e bridge de loot não são recibos de drop, coleta ou Mastery. Exceções, callbacks/mixins, hooks e QA física conservam seus limites; não há novo cast nem dano adicional.

## Flinging — movimento, geometria de ataque e consequências separados

A [ficha](enchantments/flinging.md) e a [prova](EXACT-FLINGING-CAUSAL-1.0.10.md) fecham o contrato estático individual: carga e fórmula de impulso, vetor anterior ao bônus vertical, caixa de consulta e gate de servidor, custos e ondas nativas. Velocidade solicitada não é distância percorrida, chamada de spawn não é inserção aceita e pedido de dano não é recibo de Mastery. Nenhum novo cast, hook ou QA física foi homologado.

## Gamma Ray — dano, status, visual e carga separados

A [ficha](enchantments/gamma-ray.md) e a [prova](EXACT-GAMMA-RAY-CAUSAL-1.0.10.md) fecham a documentação estática do encantamento a partir dos recursos e consumidores compilados. A exceção Tremorzilla, a resistência e as chamadas de hurt/addEffect conservam seus limites; feedback visual não é recibo de dano. Rede e custos da Raygun não se tornam autorização de perk ou Mastery. Nenhum novo cast ou hook foi homologado.

## X-Ray e fechamento dos 51 recursos publisher

A [prova](EXACT-XRAY-CAUSAL-1.0.10.md) combina o contrato individual de targeting com o censo SHA-exato dos 51 JSONs e a correspondência das 51 fichas certificadas. O fechamento é do catálogo estático desse recorte; não é prova de execução de perks, autorização C2S, atravessamento universal de obstáculos, aceitação de dano ou descoberta de todos os sistemas do mod.

## Raygun — item nativo e tipo de dano consolidados

A [ficha](damage-types/raygun.md) e a [prova](EXACT-RAYGUN-CONTRACT-1.0.10.md) fecham o contrato estático individual dos 26 métodos próprios do item, factory, carga/munição, targeting, dano/status, lifecycle e UI. Os checkpoints parciais anteriores permanecem preservados e as fronteiras de rede/anvil mantêm limites próprios. No checkpoint histórico Raygun, a conclusão levou o recorte de dano a 11/11 e o das fichas observadas a 81/81 (100% estático), sem certificar autorização C2S, efeitos físicos, hooks mutadores, nova raiz mágica ou fechamento integral do provider. `NO_MUTATION`.

## ACArmorMaterial e marcador ACArmorTickItem — primeiro suporte de integração

A [ficha de ACArmorMaterial](systems/armor-material.md), o [selo nativo](EXACT-ARMOR-MATERIAL-1.0.10.json) e a [prova](EXACT-ARMOR-MATERIAL-1.0.10.md) encerram somente o contrato estático dessa classe de suporte e seus bindings. A durabilidade usa `MAX_DAMAGE_ARRAY[type.ordinal()] × durabilityFactor`, com base 13/15/16/11; a cópia para tipos vanilla possui guard de ordinal, enquanto getters de defesa e propriedades não acrescentam guard universal. O array de defesa é mantido por referência, knockback é público, o setter de reparo é bruto e supplier nulo retorna `Ingredient.EMPTY`. Os seis materiais e cinco bindings de reparo são documentados sem inferir um sexto binding para Rainbounce nem impossibilidade global de reparação. Defesa, toughness e knockback usados nos bindings têm snapshots próprios; o supplier de reparo mantém leitura tardia. Esses parâmetros não são um hook seguro por jogador nem um certificado de item de armadura completo.

O censo tipado das 1.555 classes encontra somente a própria interface `ACArmorTickItem` e a declaração `implements` em DarknessArmorItem; não encontra dispatcher ou chamadas de API do marcador. A interface vazia recebe disposição de suporte, **+0 fichas**, e não é habilidade independente. O caminho relevante é `DarknessArmorItem.acInventoryTick` → método privado `acArmorTick`, acionado pela interface diferente `ACTickingItem`. O inventário físico original permanece preservado em `remaining_family_inventory.item_outer_classes`. Nesse checkpoint histórico, o prefixo revisado abrangia ACArmorMaterial e ACArmorTickItem, com 82/82 fichas observadas. O contrato adicionou **+1 ficha de suporte e +0 raízes mágicas**. Provider **OPEN**, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`.

## ACClientExtensionItem — ABI e inicializadores de suporte cliente

A [ficha de ACClientExtensionItem](systems/client-extension.md), o [selo nativo](EXACT-CLIENT-EXTENSION-1.0.10.json) e a [prova](EXACT-CLIENT-EXTENSION-1.0.10.md) encerram o contrato técnico estático da ABI declarada e dos 19 corpos `initializeClient` dos implementadores diretos, 18 nativos e um Citadel realocado. O censo tipado abrange as 1.555 classes do artefato e encontra 20 owners que referenciam a interface, incluindo ela própria. Não há `Methodref` ou `InterfaceMethodref` chamado `initializeClient` em qualquer owner ou descriptor do artefato. Os outputs de extensão cliente têm disposição delimitada; isso não certifica todos os métodos dos renderers ou os itens implementadores completos.

A ausência de consumidor nativo não prova desuso global nem incompatibilidade em runtime: registro, bootstrap/evento, execução e rotas externas ou reflexivas permanecem **NOT_VERIFIED**. O contrato não promove a assinatura a hook seguro por jogador, targeting, dano ou custo de cast próprios. O incremento histórico foi **+1 ficha de suporte e +0 raízes mágicas**, com **83/83 contratos estáticos entre fichas observadas** e dois contratos na família de suporte naquele checkpoint. O prefixo então revisado abrangia ACArmorMaterial, ACArmorTickItem e ACClientExtensionItem; `server/item/ACDestroyedItem` era o próximo escopo descoberto sem disposição. Provider **OPEN**, `registration_execution=NOT_VERIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`, `NO_MUTATION`.


## ACDestroyedItem — callback e ponte externa delimitados

A [ficha existente](systems/destroyed-item.md), o [selo SHA-exato](EXACT-DESTROYED-ITEM-CONTRACT-1.0.10.json) e a [prova](EXACT-DESTROYED-ITEM-CONTRACT-1.0.10.md) concluem o contrato estático de suporte introduzido parcialmente pela PR #1115. A ABI declarada, o implementador direto único `RadioactiveOnDestroyedBlockItem`, o corpo completo de 170 bytes, os delegates e o censo tipado das 1.555 classes recebem disposição própria. O binding nativo é exclusivamente `waste_drum`, selector 5 em `ACBlockRegistry`; `radrock_uranium_ore`, `block_of_uranium` e `unrefined_waste` são selector 4 e usam `RadioactiveBlockItem` comum. O bridge/delegate externo tem referência NeoForge versionada própria, separada do runtime transformado instalado.

O supermétodo é chamado antes dos guards de Creative e remoção. Após retorno normal e guards elegíveis, o callback solicita descarte, nuvem Irradiated de 9600 ticks/amplifier 1 com raio 2F, duração 12000 e espera 0, e explosão 1.8F com fonte null, `y+0.5` e interação `BLOCK`. O retorno do spawn é descartado e não condiciona a explosão; não há guarda local de servidor nem atribuição explícita de owner. Targeting, dano/status aceitos, proteção do mundo, cancelamento, ownership, persistência, rede e Mastery conservam fronteiras externas e QA pendente. A certificação não homologa World Safety nem um hook por jogador e não autoriza repetir os efeitos.

O [histórico parcial](systems/EXACT-DESTROYED-ITEM-HISTORICAL-CARD-1.0.10.md), o inventário físico original e as três disposições anteriores do prefixo permanecem preservados. Nesse checkpoint histórico, ACDestroyedItem era a quarta classe revisada e a terceira ficha certificada de suporte: **+1 certificado da ficha existente, +0 candidatos e +0 raízes mágicas**, com **84/84 contratos estáticos observados**. O próximo escopo sem certificado era `server/item/ACDynamicAttributeItem`; a ficha parcial da PR #1116 não recebeu promoção de status naquele incremento. Provider **OPEN**, `STATIC_TECHNICAL_CATALOG_ONLY`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`, `NO_MUTATION`.
