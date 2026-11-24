# Holocoder, Hot Chocolate Bottle, Ink Bomb e Glow Ink Bomb — descoberta publisher 1.0.10

Publisher `alexscaves-1.0.10-neoforge+1.21.1.jar` (CurseForge file 8856293), 75.279.314 bytes, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c32e9f2e95bffae0e7c`. Minecraft 1.21.1, Java 21; modlist física #001 registra NeoForge 21.1.250, gradle do sibling 21.1.248. Sem novo dump instalado.

## Evidência e escopo

[Run inicial 45462812701](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45462812701), job 138689710380, artifact 14952534565, relatório 113.270 bytes SHA-256 `b1b37e98304c6a38c2eacd1167580a2ec843c1768a3dfcd9b84fa32396a224d5`: três classes, oito corpos próprios, sete JSONs filename-matched. [Run expandido 45464509190](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45464509190), job 138695690486, artifact 14953084290, relatório 645.624 bytes SHA-256 `0ab600a51b26fd3da5e7360ad461deabf629f053817f1e210fe1e4a280821dac`: 18 owners, censo de 1555 classfiles. Inicial expandido falhou por budget de referências tipadas (run 45464158574); correção mantém limites de 180 referências/90 branches/30 terminais na análise completa, com janelas diretas para consumidores amplos. Escopo não é totalidade de métodos de todos os 18 owners. A CI reproduz os dois selos; final-head replay exigido.

[Sonda inicial](../../../../docs/qa/alexscaves_1010_holocoder_hot_chocolate_ink_bomb_probe.py) · [Sonda causal](../../../../docs/qa/alexscaves_1010_holocoder_hot_chocolate_ink_bomb_consumers.py) · [Workflow](../../../../.github/workflows/alexscaves-1010-holocoder-hot-chocolate-ink-bomb.yml).

## Fichas individuais e fronteiras

| ID | Classe e factory | Ficha |
|---|---|---|
| alexscaves:glow_ink_bomb | InkBombItem, lambda$static$106, true | [Glow Ink Bomb](items/glow-ink-bomb.md) |
| alexscaves:holocoder | HolocoderItem, lambda$static$17, stacksTo(1) | [Holocoder](items/holocoder.md) |
| alexscaves:hot_chocolate_bottle | HotChocolateBottleItem, lambda$static$164, stacksTo(16) no construtor | [Hot Chocolate Bottle](items/hot-chocolate-bottle.md) |
| alexscaves:ink_bomb | InkBombItem, lambda$static$105, false | [Ink Bomb](items/ink-bomb.md) |

ACItemRegistry class SHA `114e4a3576d56cb66d240fa9df9db7693b1df576ebfa86631ef751dd1e7b5bb1`, putstatic offsets 607/2001/2018/2970 respectivamente HOLOCODER/INK_BOMB/GLOW_INK_BOMB/HOT_CHOCOLATE_BOTTLE. [Contrato de registry](systems/item-registry.md) resolve causalmente IDs/factories. ACEntityRegistry initializer literal ink_bomb @758, invokedynamic @761, register @766, INK_BOMB @769; factory de tipo downstream ainda precisa projeção específica de handle e parâmetros. Não confundir classe de item com entidade ou duas variantes com duas novas raízes semânticas certificadas.

Holocoder: CommonEvents.acPlayerEntityInteract é produtor de UUID/BoundEntityTag e HologramProjectorBlock.acUse é consumidor. Totem usa as mesmas chaves em outros fluxos; não vincular objetos por igualdade de literal. O evento tem guardas de tipo e vida, serialização de alvo via ACPlatform e nova stack, não prova settlement ou autorização. A camada do projetor precisa análise própria.

Hot Chocolate: perfil ACFoods já certificado em seu recorte, herança de DrinkableBottledItem reaproveitada. Override próprio só solicita TIME_SINCE_REST reset para ServerPlayer após retorno ancestral. Sem prova de efeitos sobre spawn/sono, eventos ou stats efetivas.

Ink Bomb: 14 corpos executáveis da entidade compartilhada, incluindo dois caminhos de impacto, synced flag e persistência. O pedido de dano thrown é 0F, retorno ignorado; status e nuvem não condicionados a dano aceito. onHit cria nuvem com radius 2, duration 60, raio/tick -r/d; cloud aplica efeitos conforme variante, não há owner explicitamente definido nesse corpo. Dispenser e AI Deep One são produtores separados; não atribuir a Player sem prova.

## Recursos diretamente observados

| Recurso | SHA-256 | Bytes |
|---|---|---:|
| assets/alexscaves/models/item/glow_ink_bomb.json | 034db87e4bc47cd578294ed7d862d0acac9e03792f5e6afd3718e77928fc9f76 | 109 |
| assets/alexscaves/models/item/holocoder.json | 49d22813ee22ba3e07c49f7f790c4d18e09ee73f77e5bce195b9dd389a52de0e | 237 |
| assets/alexscaves/models/item/holocoder_bound.json | 1faa8ec9f31d450f423bdd758e8902001c44eef706454928c53ba04423a7f3fa | 111 |
| assets/alexscaves/models/item/hot_chocolate_bottle.json | ad66cf2db8f7cbcc2c5810f006cb1a5001978a1b862c93235ce991b437900fef | 116 |
| assets/alexscaves/models/item/ink_bomb.json | 51d0f510cbcb05fe51754a5715f983eb46592ca32b50ce115241ac0f406631ff | 104 |
| data/alexscaves/recipe/holocoder.json | b35d6d2b47e967ebae4c13a0e5f6fa1701aa486eec8b1dc9405290bc36f345cd | 424 |
| data/alexscaves/recipe/hot_chocolate_bottle.json | d9973d88982f4e0d3cefa31987dd087d56250a79a5f6da7a32bb2d9bd1d3ff49 | 415 |

Filename match is not complete resource reference enumeration. All four cards are partial; observed card denominator +4, static numerator +0, semantic roots +0. The historical 37-class contiguous certified prefix remains unchanged, with Galena still first incomplete; later discoveries do not close that prefix. Full provider OPEN. `NO_MUTATION`, `static_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`.

## Cardinalidade da projeção expandida

52 projeções de métodos em 18 owners: 44 corpos com projeção delimitada completa e 8 janelas diretas. InkBombEntity: 14 métodos próprios. O censo não representa fechamento de todos os métodos dos 18 owners.
