# Woodwalkers SpellBooks 0.3.1-BETA — auditoria técnica

## Proveniência

- Pack: `woodwalkers_spellbooks-0.3.1-BETA.jar` / mod id `woodwalkers_spellbooks`.
- Release pública 1.21.1: CurseForge file `8052198`; página do arquivo expõe filename interno `woodwalkers_spellbooks-0.3.1-BETA.jar`.
- Source pin exato: `jo-devnull/woodwalkers-spellbooks@fd52733f6ba6e00028492ba1fa945f6a851de1fd`.
- Branch source: `1.21.1`.
- `gradle.properties`: `mod_version=0.3.1-BETA`, Minecraft 1.21.1, NeoForge 21.1.227.
- Dependência de desenvolvimento do pin: Iron's Spells `1.21.1-3.15.6`.
- Pack atual: Iron's Spells `1.21.1-3.16.3`.

Conclusão: inventário, config e contrato estático do addon podem ser fechados pelo source exato; integração runtime contra Iron's 3.16.3 permanece gate de QA.

## Registry

`SpellRegistry` registra exatamente:

- `woodwalkers_spellbooks:shapeshifting` → `ShapeshiftingSpell`.

Não há segundo spell registrado no source pin.

## Spell config

`ShapeshiftingSpell`:

- School: `irons_spellbooks:evocation`;
- min rarity: Rare;
- max level: 6;
- cooldown: 40 s;
- cast type: LONG;
- cast time: 60 ticks;
- base mana: 40;
- mana/level: +10;
- base spell power: 8;
- spell power/level: +1.

Mana neutra por nível: `40 / 50 / 60 / 70 / 80 / 90`.
Spell power neutro por nível: `8 / 9 / 10 / 11 / 12 / 13` antes dos multiplicadores do Iron's.

## Config comum

`woodwalkers-spellbooks.toml` usa defaults:

- `Requires XP = true`;
- `Requires XP On Creative = false`;
- `Infinity Spell = false`;
- `Infinity Spell On Creative = true`;
- `Spells while Transformed = false`;
- `Spell Duration per Level = [30,45,75,90,120,240]` segundos;
- `Xp Level Cost = [6,5,4,3,2,1]` níveis.

## Fluxo de transformação

1. `checkPreCastConditions` resolve alvo via cast data ou raycast fallback.
2. Se há alvo e o jogador não está transformado, o addon verifica XP e usa `Utils.preCastTargetHelper(..., 16, .25f, false)`.
3. `onCast` grava `ShapeType.from(target)` como segunda forma por `PlayerShapeChanger.change2ndShape`.
4. `Shapeshifting.doShapeshift` chama `PlayerShape.updateShapes` para aplicar a forma.
5. Em modo não infinito, aplica `woodwalkers_spellbooks:shapeshifter` pelo tempo configurado.
6. Cast sem alvo, com segunda forma existente, reutiliza a segunda forma sem débito de XP.
7. O tick handler sincroniza expiração do effect com a forma e chama `doShapeshift` para voltar ao normal quando necessário.

## Spellcast enquanto transformado

`SpellPreCastEvent` é cancelado quando:

- entity é `ServerPlayer`;
- `Spells while Transformed = false`;
- `Shapeshifting.isTransformed(player)` é verdadeiro.

Esse cancelamento é provider-native. Black Arcana não deve registrar um segundo gate equivalente.

## Targeting — divergência estática a testar

Há dois alcances no source:

- `preCastTargetHelper`: 16 blocos;
- fallback `Utils.raycastForEntity`: 32 blocos.

O helper é chamado depois de `getTarget` já ter tentado resolver o alvo. O comportamento efetivo na borda 16–32 deve ser validado em runtime; não normalizar silenciosamente um dos valores.

## Aquisição

O spell não chama `setAllowCrafting(false)` e o repositório não define custom boss-scroll/loot provider para ele. Portanto a auditoria não cria uma rota de boss drop própria. A disponibilidade efetiva via crafting/loot genérico do Iron's deve ser validada no runtime/JEI antes de documentar receita/peso específico.

## Authority / integração

- cast/mana/cooldown/school/spell level: Iron's;
- shape state/second shape/entity representation: Woodwalkers;
- XP gate, duration config, infinite mode, transformed-spell gate: Woodwalkers SpellBooks;
- Black Arcana: somente observar ou integrar em hooks comprovados; nunca duplicar transformação, XP, timer ou spell cancellation.

## QA obrigatório

1. Iron's 3.15.6→3.16.3 compatibility smoke;
2. client + dedicated-server cast;
3. target range 16 vs fallback 32;
4. XP debit exatamente uma vez no unlock;
5. recast sem target sem novo XP;
6. duration 1–6;
7. infinity survival/creative;
8. spell-precast cancellation while transformed;
9. second-shape lifecycle em logout/login, dimensão, morte e respawn;
10. generic Iron's acquisition path/JEI.

## Estado

`SOURCE-PINNED 0.3.1-BETA / CATÁLOGO 1/1 COMPLETO / RUNTIME QA PENDENTE`
