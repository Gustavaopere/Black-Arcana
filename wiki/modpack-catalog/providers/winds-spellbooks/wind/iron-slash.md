# Iron Slash

- **ID:** `wind_spellbooks:iron_slash`
- **Classe runtime:** `net.raptorzizi.wind_spellbooks.spells.wind.IronSlashSpell`
- **School:** Wind
- **Provider/JAR:** Wind's Spellbooks / `wind_spellbooks-1.0.5.jar`
- **Status:** PRESENTE

## Contract confirmado

Fingerprint ASM: `usesPotentiation`, `createsEntity`, `usesImpulseCastData`, `usesTeleport`, `usesAddEffect`. Isso prova que Iron Slash combina lógica de potentiation do ecossistema, entity provider-native, impulso, teleport e effect dentro do mesmo spell contract.

## NÃO VERIFICADO

Níveis, rarity, mana, cooldown, cast time, weapon contribution, dano, teleport destination/range, impulse magnitude, effect, target rules, invulnerability frames, PvP/friendly-fire e aquisição.

## Deduplicação / fail-closed

É um espaço já ocupado de ataque Wind + mobilidade/teleporte/potentiation. Black Arcana não deve recriar um dash-slash equivalente nem executar segundo teleport/impulse/effect fora dos hooks do provider.

## Evidência

Runtime registry + ASM do pack; release oficial 1.0.5.
