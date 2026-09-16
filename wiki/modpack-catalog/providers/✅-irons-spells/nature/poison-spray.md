# Poison Spray

- **Status:** PRESENTE — ativo
- **Nome interno histórico:** Poison Breath
- **Spell ID real:** `irons_spellbooks:poison_breath`
- **Classe:** `PoisonBreathSpell`
- **Provider/JAR:** Iron's Spells / `1.21.1-3.16.3`
- **Escola:** Nature
- **Níveis/raridade:** 1–10 / Common → Legendary
- **Cast:** Continuous
- **Cast-time field:** 100 ticks
- **Mana/cooldown:** 5–14 / 12 s
- **Dano player-facing atual:** 1–7,75

## Alias histórico

O changelog oficial registra que **Poison Breath foi renomeado para Poison Spray sem outras mudanças**. O registry ID e a classe permanecem `poison_breath` / `PoisonBreathSpell`; integrações devem usar o identificador real, não inferir `poison_spray`.

## Source audit 3.16.3

- base spell power 0, +1 por nível após o primeiro;
- damage = `1 + spellPower*0.75`;
- durante o mesmo cast, se `EntityCastData` ainda aponta para `AbstractConeProjectile`, reutiliza o cone e ativa novo settlement de dano;
- caso contrário cria `PoisonBreathProjectile`, posiciona próximo à altura dos olhos, injeta damage e salva a entity no cast data;
- loop sound `POISON_BREATH_LOOP`;
- AI stop threshold baseado em target > ~10 blocos com margem interna.

## Authority / dedup

`PoisonBreathProjectile` + `EntityCastData` são authority. Não spawnar um cone por tick, não contar cada pulse como novo cast e não reaplicar Poison por fora.

Geometry, cadence, poison duration, friendly-fire, PvP/boss/summon policy: `NÃO VERIFICADO` nesta ficha.

## Verificação obrigatória

- damage type fino: `NÃO VERIFICADO`;
- range/area/duração do cone: provider-native, números exatos `NÃO VERIFICADO`;
- scaling: `1 + 0.75*spellPower`;
- obtenção/itens/focus/rituais: específicos `NÃO VERIFICADO`;
- VFX/textura/QA client-real: `NÃO VERIFICADO` além do loop sound;
- fail-closed: preservar o cone único do provider.

## Fonte

- `https://iron.wiki/spells/` — nome atual, consulta 2026-09-06.
- changelog oficial: rename Poison Breath → Poison Spray sem mudança mecânica.
- `PoisonBreathSpell.java` — source 3.16.3.
