# Wind Blade

- **ID:** `wind_spellbooks:wind_blade`
- **Classe runtime:** `net.raptorzizi.wind_spellbooks.spells.wind.WindBladeSpell`
- **School:** Wind
- **Provider/JAR:** Wind's Spellbooks / `wind_spellbooks-1.0.5.jar`
- **Status:** PRESENTE

## Contract confirmado

Fingerprint ASM: `usesShoot`, `createsEntity`, `createsProjectile`. Wind Blade é um projectile spell disparado pelo provider; flight, hit e settlement pertencem à entity/projectile real do addon.

## NÃO VERIFICADO

Níveis, rarity, mana, cooldown, cast time, projectile speed/count, dano, range/lifetime, piercing, hitbox, friendly-fire/PvP/boss rules e aquisição específica.

## Deduplicação / fail-closed

Não spawnar segundo Wind Blade nem reaplicar dano ao detectar impacto. Bridges devem observar um hook de cast/hit comprovado, se exposto.

## Evidência

Runtime registry + ASM do pack; release oficial 1.0.5.
