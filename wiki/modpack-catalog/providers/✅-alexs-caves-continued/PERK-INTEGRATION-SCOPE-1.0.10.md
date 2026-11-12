# Alex's Caves Continued 1.0.10 — escopo de integrações ainda aberto

Os recortes das oito ações mágicas e dos oito efeitos registrados têm contratos estáticos próprios. Eles **não cobrem todo o conteúdo integrável por perks** do mod. A classificação histórica `EXCLUDED` em [42 classes de interação](ITEM-ACTION-DISPOSITION-1.0.10.md) significa exclusão do denominador de magia, não exclusão do trabalho de integração.

Autoridade: JAR 1.0.10, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`, 75.279.314 bytes. O [inventário JSON](INTEGRATION-SCOPE-INVENTORY-1.0.10.json) enumera os nomes exatos abaixo a partir do artefato, sem importar os parâmetros da fonte 1.1.1. [Limites e reprodução](EXACT-TECHNICAL-CONTRACTS-1.0.10.md).

| Família | Universo exato identificado | Trabalho necessário antes de fechar o provider |
|---|---|---|
| Ações sobrenaturais | Oito raízes já contadas | Sete campos estáticos documentados nas oito fichas; hooks e QA física separados |
| Itens / equipamento | 81 classes externas de itens; 42 com assinaturas de interação já classificadas semanticamente | [Dreadbow](equipment/dreadbow.md), [Desolate Dagger](equipment/desolate-dagger.md) e [Shot Gum](equipment/shot-gum.md) documentados individualmente; demais armas, movimento, comida, defesa e helpers precisam de disposição própria. Classes e fichas não são denominadores equivalentes |
| Enchantments | 51 JSONs em `data/alexscaves/enchantment/` ([índice nominal e pendências por encantamento](ENCHANTMENT-PERK-CROSSWALK-1.0.10.md)) | Ficha por contrato: nível/custo/slots/exclusividade e consumidor real de cada modifier, inclusive tecnologia/armas |
| Damage types | 11 JSONs, 11 factories e seus consumidores diretos localizados no JAR | **9/11 contratos estáticos documentados:** [Acid](damage-types/acid.md), [Dark Arrow](damage-types/dark-arrow.md), [Desolate Dagger](damage-types/desolate-dagger.md), [Forsaken Sonic Boom](damage-types/forsaken-sonic-boom.md), [Gumball](damage-types/gumball.md), [Radiation](damage-types/radiation.md), [Intentional Game Design](damage-types/intentional-game-design.md), [Nuke](damage-types/nuke.md), [Spirit Dinosaur](damage-types/spirit-dinosaur.md). Restam Raygun e Tremorzilla Beam. [Prova nuclear](EXACT-NUCLEAR-CONTRACTS-1.0.10.md), preservando o mismatch de tickets e toda QA física pendente |
| Mob effects | Oito campos de registro de efeitos | **8/8 contratos estáticos documentados**, incluindo aplicações e consumidores; [fichas](effects/INDEX.md) e [prova exata](EXACT-EFFECT-CONTRACTS-1.0.10.md). Hooks e QA física pendentes |
| Potions | 12 campos de registro de poções | Conteúdo, níveis/tempo e aquisição, sem contar variantes como novas magias |
| Config servidor | 40 campos em `ACServerConfig` | Defaults/bounds, momento de leitura, autoridade global/por jogador e consumidores; não presumir valores em execução |
| Config cliente | 15 campos em `ACClientConfig` | Distinguir HUD, luz, shader, som e câmera de comportamento servidor e atributos |
| Rede | 18 classes externas sob `server/message/`, incluindo transporte/helpers | Direção, registro/protocolo, autenticação, seleção de entidade, limites, autoridade e lifecycle |
| Mobs/montarias e eventos | Classes e interfaces inventariadas, sem denominador final de fichas | Atributos, dano, targeting, domesticação/reputação, medidores e skills de montaria; separar AI de raiz mágica do jogador |
| Mundo, dados e compatibilidade | Registries, block entities, tags, loot, crafting e mixins | Disposição explícita por consumidor ou suporte; aquisição, proteção e persistência não podem ser inferidas de assets |

Essas famílias se sobrepõem. Não somar 81+51+11 etc. como denominador final: um item pode ser owner de uma ação existente, uma classe base pode atender vários registros e um efeito pode ter vários consumidores. Os números descrevem superfícies identificadas, não novas fichas concluídas ou novos spells.

## Contratos não mágicos que não podem ser descartados

Dreadbow, spears, Ortholance, Desolate Dagger e Primitive Club oferecem combate e modifiers. Galena Gauntlet, Raygun, Quarry Smasher e Remote Detonator oferecem controle magnético, energia, mineração e explosivos. Candy Cane Hook, Floater e Submarine oferecem mobilidade. Armor passiva, comida e itens como Sack of Sating, Gazing Pearl e Holocoder também precisam de disposição de integração. Os nomes e assinaturas estão no inventário; ainda não constituem revisão completa de seus corpos.

As interfaces de montaria `FlyingMount`, `KeybindUsingMount` e `RidingMeterMount`, assim como `CommonEvents`, progresso de Cave Book e reputação Deep One, são candidatos a contratos de sistemas. Uma assinatura de API não é, sozinha, um hook seguro. A próxima catalogação deve documentar o consumidor, os parâmetros e os limites de autoridade antes de marcar essas superfícies completas.

## Estado dos índices

As oito ações, oito efeitos, os três equipamentos e os nove contratos de dano somam 28 contratos estáticos. Com os trinta e dois contratos individuais de encantamentos do [crosswalk](ENCHANTMENT-PERK-CROSSWALK-1.0.10.md), o provider registra **60 contratos estáticos certificados entre 81 fichas observadas**: 51 são dossiers de encantamentos, sendo dezenove parciais e trinta e dois estáticos completos. Contratos de encantamentos: [Arrow Inducting](enchantments/arrow-inducting.md), [Astral Transferring](enchantments/astral-transferring.md), [Heavy Slam](enchantments/heavy-slam.md), [Herd Phalanx](enchantments/herd-phalanx.md), [Humungous Hex](enchantments/humungous-hex.md), [Impending Stab](enchantments/impending-stab.md), [Lasting Morale](enchantments/lasting-morale.md), [Multiple Mint](enchantments/multiple-mint.md), [Peppermint Punting](enchantments/peppermint-punting.md), [Plummeting Flight](enchantments/plummeting-flight.md), [Precise Volley](enchantments/precise-volley.md), [Rapid Possession](enchantments/rapid-possession.md), [Relentless Darkness](enchantments/relentless-darkness.md), [Sated Blade](enchantments/sated-blade.md), [Sea Swing](enchantments/sea-swing.md), [Seapairing](enchantments/seapairing.md), [Second Wave](enchantments/second-wave.md), [Seekcandy](enchantments/seekcandy.md), [Shaded Respite](enchantments/shaded-respite.md), [Sharp Cane](enchantments/sharp-cane.md), [Sightless](enchantments/sightless.md), [Soak Seeking](enchantments/soak-seeking.md), [Solar](enchantments/solar.md), [Spell Lasting](enchantments/spell-lasting.md), [Straight Hook](enchantments/straight-hook.md), [Swiftwood](enchantments/swiftwood.md), [Targeted Ricochet](enchantments/targeted-ricochet.md), [Taxing Bellow](enchantments/taxing-bellow.md), [Triple Splash](enchantments/triple-splash.md), [Triple Split](enchantments/triple-split.md), [Tsunami](enchantments/tsunami.md), [Twilight Perfection](enchantments/twilight-perfection.md). As provas individuais descrevem consumidores nativos em recortes SHA-exatos, sem autorizar hooks ou QA física. Raygun e Tremorzilla Beam continuam parciais. O provider inteiro continua aberto; a fila alfabética permanece em **Alex's Caves Continued**.

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
