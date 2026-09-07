# Silence

- **ID:** `discerning_the_eldritch:silence`
- **School:** Eldritch
- **Levels:** 1–5
- **Min rarity:** Legendary
- **Cast:** Long, 80 ticks base
- **Mana neutral:** 100–180
- **Spell power neutral:** 1–5
- **Cooldown:** 200 s
- **Target range:** 32 blocks

## Contract

Aplica `SILENCE_POTION_EFFECT` ao target. Duração = `clamp(getSpellPower*20, 20, 140)` ticks: 1–7 s hard bounds; neutral levels dão 1–5 s.

O efeito não adiciona cures em `fillEffectCures`. O bloqueio real é server-authoritative: DTE escuta Iron's `SpellPreCastEvent`; se o jogador possui Silence, cancela o cast, mostra tempo restante e toca feedback de falha.

`King's Effigy` torna o cast de Silence não-interruptível; sem ele, o cast pode ser interrompido.

## Dedup / gates

- authority anti-cast: `SILENCE_POTION_EFFECT` + `SpellPreCastEvent`;
- não cancelar casts por polling de HUD/animação;
- não aplicar segundo cooldown/punição ao cast cancelado;
- PvP/boss/summon eligibility do target helper: detalhes adicionais `NÃO VERIFICADO`;
- acquisition específica: `NÃO VERIFICADO`.

## Presentation

Finish sound `SILENCE_SPELL_CAST`, Iron's long-cast animations.

## Source

`SilenceSpell.java`, `SilencePotionEffect.java`, DTE `ServerEvents`, branch `1.21@7bbd81f...`.
