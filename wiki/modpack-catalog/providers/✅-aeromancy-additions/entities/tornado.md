# Tornado — entidade registrada, magia inativa

- Registro: `aero_additions:tornado`, `EntityType<TornadoEntity>`, categoria `MISC`, builder **10×6**, tracking **64**. A entidade sobrescreve dimensões dinamicamente.
- Ativação: entidade **REGISTERED** e renderer ativo; única magia produtora localizada `TornadoSpell` **NOT_REGISTERED**. A lógica pode rodar se entidade for criada externamente; não é uma 11ª magia ativa. Contribuição estrita de magias **0**.
- Estado: `documentary=SOURCE_PINNED`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; identidade instalada **NOT_VERIFIED**; certificação **0**.

Source `snackerpirater/aero-additions@ae282b32d25ad76ef8d01c637ec05566a767ae4c`, versão `1.2.8`. [Prova comum](../SOURCE-CONTRACTS-1.2.8.md) · [manifesto](../SOURCE-CATALOG-MANIFEST-1.2.8.json) · [limites](../SOURCE-CATALOG-CLOSURE-1.2.8.md). SHA-1 instalado histórico de 35 caracteres continua inválido/desconhecido. [Magia inativa](../systems/unregistered-spell-code.md).

## Tamanho, seleção e duração

`TornadoEntity extends Projectile implements AntiMagicSusceptible,GeoAnimatable`. O construtor com owner chama `setOwner`. Sincroniza `DATA_SIZE` Float default **1** e `DATA_EFFECT` Int default **0**. `setSize` só escreve no server, aplica teto **48**, sem piso; atualização de size refresca dimensões e descarta se `<0.1`. `getDimensions` produz largura **1.5×S**, altura **S**, mantendo posição ao refresh. O builder 10×6 não é a dimensão dinâmica final. A magia inativa calcularia S=`4+2×level` (6–16 nos níveis default), independente de spell power.

Após `super.tick`, atualiza lista de tracking a cada `U=max((int)(S/2),2)` ticks, buscando entidades na **AABB atual inflada em 1**. Em cada tick percorre a lista e exclui owner, friendly fire pelo helper Iron's e spectators. Distância horizontal à coluna é comparada com `R=boundingBox.getXsize()` (**largura completa**, nominalmente 1.5×S); a seleção AABB é uma restrição adicional e a lista pode ficar desatualizada entre pulsos. Esse R não prova aquisição circular livre até R em todas as direções. Não faz raycast/LOS por entidade.

No server descarta quando `tickCount>20×160×2` = **6400 ticks**; branch de som em loop a cada 320 existe mas seus comandos de som estão comentados. `onAntiMagic` é **vazio**: implementar a interface não prova dissipação. Não há override local de movimento da própria coluna além do `Projectile` herdado.

## Movimento e variantes de dano

Para entidade elegível a distância horizontal `d<=R`, define `f=1−d/R`, `q=f⁴×0.25`, `h=max(entityY−bbMinY,1)/3`. Vetor de sucção `I=normalize(centerAtEntityY−entityPos)×q×h`; vetor de giro `G=rotateY(I,270°)×q×2×h`. Perto do topo (`entityY>bbMaxY−1.5`), multiplica G por **4** e, para LivingEntity ainda sem AIRBORNE, aplica AIRBORNE **200 ticks**, amplifier `(int)S`. Resistência `r=clamp(1−KNOCKBACK_RESISTANCE,0.3,1)` para living, ou 1 para demais; bosses tagados recebem `b=0.5`, demais 1. Empurra por **`I+G+(0,q×r×b×0.7,0)`** e zera fall distance. Resistência/boss só escalam o componente vertical explícito, não I/G.

Quando `d<2`, identifica tipos de projétil e muda a variante; não consome/descarta esses projéteis. A cada `tickCount%10==0`, somente LivingEntity com `d<2` recebe a tentativa específica abaixo. Não há guard server-only em volta do loop de movimento/dano; somente parte do lifecycle/partículas tem guards explícitos.

| ID da variante | Tipo de entidade que ativa | Tentativa de dano no núcleo |
|---|---|---|
| 0 DEFAULT | `aero_additions:magic_wind_charge` | Nenhum dano local. |
| 1 FIRE | Iron's `FIRE_BREATH_PROJECTILE` | 2 via damage source de `FIRE_BREATH_SPELL`, tornado/owner. |
| 2 ENDER | Iron's `DRAGON_BREATH_PROJECTILE` | 2 via `DRAGON_BREATH_SPELL`, tornado/owner. |
| 3 NATURE | Iron's `POISON_BREATH_PROJECTILE` | 2 via `POISON_BREATH_SPELL`; se `applyDamage` true, POISON **100 ticks**, amplifier 0. |
| 4 LIGHTNING | Iron's `ELECTROCUTE_PROJECTILE` | 2 via `ELECTROCUTE_SPELL`; partículas de eletricidade no server. |

A ordem de entidades rastreadas pode determinar a última variante escrita. `BY_ID` usa fallback ZERO para IDs fora da enum. O campo `spell` de `TornadoEffect` tem getter, mas o dano seleciona spells explicitamente no switch; não é despachado genericamente por esse getter.

## NBT e apresentação

Salva `Size` Float, `Age` Int e `Effect` Int, além de superclass. Lê Age/Effect; restaura Size somente se **`getInt("Size")>0`**, embora salve Float e depois leia o valor como Float. Conversão/truncamento depende de NBT do host: tamanhos positivos abaixo de 1 podem falhar nesse gate. Não há versão/migração local. Cache/lista de entidades rastreadas não é persistida.

`TornadoRenderer` usa texturas base/top, `breezeWind` com offset `age×0.02`, escala visual **S/6.5**, alpha `0xd0`; cores default branca, fire laranja, ender magenta, nature verde, lightning ciano. `TornadoModel` aponta `geo/tornado.geo.json`, `textures/entity/tornado.png`, `animations/tornado.animation.json`; controlador repete animação `spin`. Visual não é hitbox nem teste de dano.

## Matriz para perks

| Eixo | Consumidor real | Fronteira de mutação |
|---|---|---|
| Ativação/size | Registry ativo, único spell produtor inativo; `setSize` server com teto 48 | Não ativar Tornado via contagem ou catálogo. API/setter não é seam de perk certificado; **NOT_VERIFIED**. |
| Seleção/força | Tracking AABB/cache, fórmulas I/G/q e push | S altera dimensões, cadence e seleção; custo de entidade grande precisa orçamento/QA. |
| Dano/variantes | Switch de `applyDamage`, absorção por tipo de projectile | Dano de outras escolas/spells, default sem dano; não creditar Wind genericamente ou por troca de cor. |
| Persistência/antimagia | NBT Size/Age/Effect, callback anti-magic vazio | Guard Int/Float e dissipação não fechados fisicamente. |
| Causalidade | Owner e `DamageSources`, retorno só usado no poison | Mastery exige efeito/dano aceito, server authority e crédito de dono demonstrados. |

QA: entidade criada externamente, client/server push, cache, dimensões e S extremos, NBT fracionário, owner/friendly fire, variante simultânea, poison, expiração e antimagia. Nenhum adapter certificado.

## Localizadores fixos

- [AASpells.java — registro L108–112](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L108-L112); [spell comentado L74–78](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/AASpells.java#L74-L78).
- [TornadoEntity.java — dados/tamanho L42–105](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/tornado/TornadoEntity.java#L42-L105); [NBT/antimagia L108–135](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/tornado/TornadoEntity.java#L108-L135); [dimensões/força/lifecycle L163–232](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/tornado/TornadoEntity.java#L163-L232); [dano/tipos/tracking L233–290](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/tornado/TornadoEntity.java#L233-L290).
- [TornadoRenderer.java L17–58](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/tornado/TornadoRenderer.java#L17-L58); [TornadoModel.java L7–27](https://github.com/snackerpirater/aero-additions/blob/ae282b32d25ad76ef8d01c637ec05566a767ae4c/src/main/java/com/snackpirate/aeromancy/spells/tornado/TornadoModel.java#L7-L27).
