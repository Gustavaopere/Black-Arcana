# Extinction Spear — `alexscaves:extinction_spear`

**Contrato técnico estático** ✅ `STATIC_TECHNICAL_CATALOG_ONLY`, grau `SHA_EXACT_BINARY_BEHAVIOR`. Hook mutador `NOT_VERIFIED`, QA física `NOT_TESTED`, perk executável `NOT_CERTIFIED`, política `NO_MUTATION`. Esta ficha cobre o equipamento e seus callbacks de uso, acerto e defesa, com **zero novas raízes mágicas**. Dano, movimento das entidades e estado dos espíritos têm contrato próprio. [Spirit Dinosaur](../damage-types/spirit-dinosaur.md)

## Identidade e atributos

`ACItemRegistry.<clinit>()V @1120–1134` liga o campo `EXTINCTION_SPEAR` ao ID e ao supplier `lambda$static$49()Lnet/minecraft/world/item/Item;`, com Code SHA-256 `b05a5a0d5218ba481b9ca05220fb579000fa64c3e2af6ac8878b39e1ea0105e8`. A factory declara **1.300 de durabilidade**, raridade `DEMONIC` e `fireResistant`. `ExtinctionSpearItem.<init>(Item.Properties) @0–8` chama `SpearItem.<init>(Item.Properties,double)` com **8D**. A implementação própria da lança tem SHA-256 `846709940e9e400c4d6e894ec07887b762598b0d8f116fff951fa5585245bfd8`. [Registro](../systems/item-registry.md) · [Manifesto do binário](../EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.json)

`SpearItem.acModifiers @0–15` entrega o mapa fixo em `MAINHAND` e `null` nos demais slots. O mapa pede `ATTACK_DAMAGE +8D` e `ATTACK_SPEED −3D`, ambos `ADD_VALUE`. `getDefaultAttributeModifiers @0–17` passa pelo bridge `ACCompat.itemAttributes`. A composição efetiva depende da stack, da entidade, da engine e de modificadores externos. O JSON `data/alexscaves/weapon_attributes/extinction_spear.json` contém o parent `bettercombat:spear`, sem distância ou animação numérica própria. [Atributos dinâmicos](../systems/dynamic-attributes.md)

## Uso, carga e arremesso

`SpearItem.use(Level,Player,InteractionHand) @0–46` pega a stack da mão informada. Retorna `PASS` se for danificável e `damageValue >= maxDamage−1`. Nos demais casos pede `startUsingItem(hand)` e retorna `CONSUME` como resultado da interação. O ato de iniciar uso não remove a stack. A animação herdada é `UseAnim.SPEAR` e a duração de uso é **72.000 ticks**.

`ExtinctionSpearItem.releaseUsing(ItemStack,Level,LivingEntity,int) @0–175` exige `Player`. Calcula `t=72000−timeLeft`, `x=t/20F` e `p=(x²+2x)/3F`, com teto de `1F` em `SpearItem.getPowerForTime(I)F @0–26`. O ramo de arremesso compara `p` alargado a double com **`0.1D`** e exige `p > 0.1D`. Na faixa normal de carga não negativa, o primeiro arremesso passa aos **3 ticks** e a carga chega ao teto aos **20 ticks**. O helper não aplica um piso geral para entradas fora desse domínio.

| Trecho | Operação compilada |
| --- | --- |
| `releaseUsing @42–62` | Pede desgaste **1** com o slot de quebra `MAINHAND`, constrói `ExtinctionSpearEntity` com a stack após essa solicitação. A entidade copia a stack para o próprio estado de impacto. |
| `@64–85` | `shootFromRotation(player,XRot,YRot,0,3.5F×p,1F)` usa rotação do jogador, argumento de velocidade dependente da carga e dispersão (`inaccuracy`) `1F`. O item não busca alvo antes de disparar. |
| `@88–165` | `instabuild` escolhe pickup `CREATIVE_ONLY`. A inserção na Level descarta o retorno, então seguem som, shrink de **1** fora de `instabuild` e `ITEM_USED`. O corpo não estorna o débito diante de inserção recusada. |
| `@168–175` | Em release de Player, chama `killGrottoGhostsFor(player,false)`, inclusive com carga insuficiente. |

O registry declara a entidade da lança com **0,5 × 0,5 bloco**. A colisão consulta o caminho herdado de `AbstractArrow` enquanto `dealtDamage` ainda está falso. No impacto de entidade, `onHitEntity` pede **10F + bônus de encantamento** se a vítima é `LivingEntity` e **10F** nos demais casos, com `alexscaves:spirit_dinosaur`. A carga altera o argumento de lançamento, enquanto a fórmula de impacto tem outros operandos. Um acerto aceito com owner disponível pode produzir Subterranodon. Um acerto aceito em Enderman encerra o método antes dessa etapa. [Colisão, bônus e vínculo da lança](../damage-types/spirit-dinosaur.md#impacto-de-extinction-spear)

O impacto em bloco ativa `WIGGLING`. A lógica própria de retorno processa o owner quando a lança está no chão ou com `noPhysics`. O ramo de oscilação pode pedir `TephraExplosion` de raio **1,5F**, modo `KEEP`, em servidor. O retorno usa `0.95×delta + 0.3×normalize(owner.eyePosition−posição)` e pickup herdado, com checagem de owner. Esses caminhos têm limites de engine e persistência próprios. [Explosão e retorno](../damage-types/spirit-dinosaur.md#bloco-wiggling-explosão-e-retorno)

## Ataque corpo a corpo e defesa em uso

`SpearItem.hurtEnemy @0–7` despacha `acHurtEnemy(stack,vítima,atacante)`. A sobrescrita solicita ignição da vítima por **5 s** e tenta criar **um Tremorsaurus**, no ponto médio horizontal do atacante e da vítima e em `Y=atacanteY+1`. Transfere UUID do atacante, ID da vítima, nível de `CHOMPING_SPIRIT` e delay de **5 ticks**. O golpe chega ao callback com a vítima definida. A tentativa de spawn antecede o desgaste herdado de **1** na `MAINHAND`. No consumidor Tremorsaurus, o dano solicitado é `3+2×nível` ao alvo vinculado e quando `distanceTo(alvo) < larguraDoAlvo+3.5D`, com os demais guards detalhados na ficha de dano. [Chomping Spirit](../enchantments/chomping-spirit.md)

`onUseTick(Level,LivingEntity,ItemStack,int) @0–132` exige `timeLeft == getUseDuration(stack,null)` para pedir som e `N=3+HERD_PHALANX` criações de Grottoceratops. Cada espírito recebe posição/UUID do usuário e offset de órbita `i×(360F/N)`. A órbita usa `DinosaurSpiritEntity` e seu Player resolvido. O loop não limita diretamente o nível lido, guarda lado lógico ou valida os retornos de inserção. [Herd Phalanx](../enchantments/herd-phalanx.md)

`killGrottoGhostsFor(Player,boolean) @0–149` procura dentro da caixa do Player expandida em **30 blocos por eixo**, filtrando UUID, tipo Grottoceratops e `!fading`. `false` pede fading para todos os elegíveis. `true` seleciona uma instância pela comparação `closest.distanceTo(player) > candidate.distanceTo(closest)` quando já existe candidata selecionada. `CommonEvents.acCancelDamage @91–143` usa o segundo modo quando a vítima é um Player em uso desta lança. Se o helper retorna verdadeiro, o handler solicita som de escudo e a ponte NeoForge pede `LivingDamageEvent.Pre.setNewDamage(0F)`. Isso documenta uma solicitação de defesa, com aceitação e ordem de eventos em jogo ainda por testar. [Seleção e consumo defensivo](../damage-types/spirit-dinosaur.md#grottoceratops-seleção-e-consumo-defensivo)

## Custos, reparo e aquisição

- O publisher declara a receita shaped ` T ` / `TST` / `ABA`, com três Tectonic Shards, uma Limestone Spear, duas Amber Curiosities e um Heavy Bone. A validação de reparo aceita `TECTONIC_SHARD` por `ACRepairableItem.isExtraRepairMaterial` ou delega à superclasse. Há pedido de desgaste **2** no callback herdado `mineBlock` quando a velocidade de destruição difere de zero. [Receita e dados de encantamento](../EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.md) · [Reparo](../systems/repairable-item.md)
- `getEnchantmentValue()` retorna **1** e `isEnchantable(ItemStack)` exige **stack count 1**. A tag `#alexscaves:enchantable/extinction_spear` inclui este ID. Além de Chomping Spirit e Herd Phalanx, [Plummeting Flight](../enchantments/plummeting-flight.md) modifica duração e movimento do Subterranodon criado por impacto. Seus níveis e custos vêm dos JSONs individuais. Os métodos do item não declaram custo próprio de mana, stamina, munição separada ou cooldown para esses caminhos.

## Integração e validação

Uma perk de duração precisa distinguir tempo de uso, carga, delay do Tremorsaurus, tempo de transporte de Subterranodon e janela de retorno. Para dano, Mastery ou troca de alvo, o contrato exige preservar o callback único da arma, a colisão da entidade, o ID local da vítima, o UUID de autoria e a resolução de dano/defesa do provider. O modificador de ataque, a fórmula de impacto e a do espírito têm consumidores próprios. Black Arcana, Enshrouded e RPG Skill Tree têm aqui uma referência estática. Atributos e perks executáveis nesses mods dependem de uma fronteira de integração verificada.

Autoridade binária **Alex's Caves Continued 1.0.10 / NeoForge 1.21.1**, CurseForge `8856293`, **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. O replay `alexscaves_1010_action_contract_audit.py --profile spirit_dinosaur` verifica o manifesto existente SHA-256 `a5820b815e80c566832691e2d80290ecfd23d21b4bb36d21be922f794f7605aa`, que inclui os **9** corpos próprios do item, **12** da base `SpearItem` e **18** da lança arremessada. A verificação reutiliza a evidência compilada e os recursos ligados à ficha de dano. Permanecem pendentes testes físicos de troca de mão, quebra/recuperação, recusa de spawn/dano, compatibilidade de combate, proteção PvP e defesa em multiplayer. [Reprodução e limites](../EXACT-SPIRIT-DINOSAUR-CONTRACT-1.0.10.md)
