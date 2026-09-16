# Wind Jump

- **ID:** `wind_spellbooks:wind_jump`
- **Classe runtime:** `net.raptorzizi.wind_spellbooks.spells.wind.WindJumpSpell`
- **School:** Wind
- **Provider/JAR:** Wind's Spellbooks / `wind_spellbooks-1.0.5.jar`
- **Status:** PRESENTE — registration observado no runtime
- **Upgradable:** sim, conforme descrição oficial do conjunto de sete spells

## Contract confirmado

O bytecode carregado no pack foi classificado com `createsEntity`, `usesImpulseCastData`, `createsProjectile` e `usesAddEffect`. Portanto Wind Jump é um contract de mobilidade/impulso que também instancia conteúdo provider-native e aplica effect; o comportamento fino da entity/projectile permanece authority do addon.

## NÃO VERIFICADO

Níveis exatos, rarity, mana, cooldown, cast time, magnitude/direção do impulso, projectile purpose, damage, duração do effect, fall-damage behavior, target rules, PvP e aquisição específica.

## Deduplicação / fail-closed

Não criar um segundo impulso/projectile/effect para o mesmo cast. Uma perk/bridge deve reagir a causalidade comprovada do cast, nunca inferir Wind Jump apenas por alteração brusca de velocidade.

## Evidência

Release 1.0.5 (CurseForge file 8485822) + logs runtime do pack/ASM FundamentalPrinciples.
