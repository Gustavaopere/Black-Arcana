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

As oito ações, oito efeitos, os três equipamentos e os nove contratos de dano somam 28 contratos estáticos. Com os doze contratos individuais de encantamentos do [crosswalk](ENCHANTMENT-PERK-CROSSWALK-1.0.10.md), o provider registra **40 contratos estáticos certificados entre 62 fichas observadas**: 32 são dossiers de encantamentos, sendo vinte parciais e doze estáticos completos, incluindo [Sea Swing](enchantments/sea-swing.md). Seu manifesto agora contempla métodos e construtores completos do recorte JAR SHA-exato, sem autorizar hook ou QA física. Raygun e Tremorzilla Beam continuam parciais. O provider inteiro continua aberto, incluindo os demais equipamentos, encantamentos e sistemas, e a fila alfabética permanece em **Alex's Caves Continued**.

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
