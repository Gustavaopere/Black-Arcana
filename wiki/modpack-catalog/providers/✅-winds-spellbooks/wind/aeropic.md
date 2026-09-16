# Aeropic

- **ID:** `wind_spellbooks:aeropic`
- **Classe runtime:** `net.raptorzizi.wind_spellbooks.spells.wind.AeropicSpell`
- **School:** Wind
- **Provider/JAR:** Wind's Spellbooks / `wind_spellbooks-1.0.5.jar`
- **Status:** PRESENTE

## Contract confirmado

Fingerprint ASM: `hasRecasts`, `usesImpulseCastData`, `usesAddEffect`. Aeropic é portanto um spell Wind com janela/lifecycle de recasts, mobilidade por impulso e effect provider-native.

## NÃO VERIFICADO

Número de recasts, janela, níveis, rarity, mana, cooldown, cast time, impulso por recast, effect, dano, target rules, cancel/finish semantics e aquisição específica.

## Deduplicação / fail-closed

Não implementar contador paralelo de recasts nem um segundo impulse ledger. O recast state do provider deve permanecer autoridade causal.

## Evidência

Runtime registry + ASM do pack; release oficial 1.0.5.
