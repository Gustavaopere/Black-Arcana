# Almighty Push

- **ID:** `wind_spellbooks:almighty_push`
- **Classe runtime:** `net.raptorzizi.wind_spellbooks.spells.wind.AlmightyPushSpell`
- **School:** Wind
- **Provider/JAR:** Wind's Spellbooks / `wind_spellbooks-1.0.5.jar`
- **Status:** PRESENTE

## Contract confirmado

Fingerprint ASM: `createsEntity` e `usesAddEffect`. O nome/provider indicam um spell de push, mas a geometria, força e seleção de targets **não são inferidas** sem bytecode exato. O que está comprovado é que o cast cria entity e aplica effect provider-native.

## NÃO VERIFICADO

Níveis, rarity, mana, cooldown, cast time, radius/range, force, dano, entity/effect concretos, target/friendly-fire/PvP/boss rules e aquisição.

## Deduplicação / fail-closed

Reservar o contract de push-themed Wind e não criar entity/effect paralelo. Qualquer integração numérica aguarda source/JAR extraction.

## Evidência

Runtime registry + ASM do pack; release oficial 1.0.5.
