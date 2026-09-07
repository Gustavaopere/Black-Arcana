# Tornado

- **ID:** `wind_spellbooks:tornado`
- **Classe runtime:** `net.raptorzizi.wind_spellbooks.spells.wind.TornadoSpell`
- **School:** Wind
- **Provider/JAR:** Wind's Spellbooks / `wind_spellbooks-1.0.5.jar`
- **Status:** PRESENTE

## Contract confirmado

Fingerprint ASM: `createsEntity`, `createsProjectile`, `usesRaycast`. O cast resolve alguma forma de alvo/posição por raycast e instancia entity/projectile provider-native. A release 1.0.3 registrou especificamente um fix de crash de Tornado em servidor, reforçando que o lifecycle server é parte sensível do contract.

## NÃO VERIFICADO

Níveis, rarity, mana, cooldown, cast time, raycast range, entidade concreta, duração, pull/knockback/damage, area, target/friendly-fire/PvP/boss rules e aquisição específica.

## Deduplicação / fail-closed

Não criar segundo tornado, scan, force solver ou projectile. Tratar o provider como authority do alvo resolvido, entity lifecycle e damage/force settlement.

## Evidência

Release 1.0.5 + changelog 1.0.3 + runtime ASM do pack.
