# Tailwind

- **ID:** `wind_spellbooks:tailwind`
- **Classe runtime:** `net.raptorzizi.wind_spellbooks.spells.wind.TailwindSpell`
- **School:** Wind
- **Provider/JAR:** Wind's Spellbooks / `wind_spellbooks-1.0.5.jar`
- **Status:** PRESENTE

## Contract confirmado

Fingerprint ASM: `usesAddEffect`. O changelog 1.0.1 registra um fix específico de **fall damage de Tailwind**, provando que o effect participa de uma interação de mobilidade/queda na linha incorporada pela 1.0.5.

## NÃO VERIFICADO

Níveis, rarity, mana, cooldown, cast time, exact effect, velocidade/movimento, duração, magnitude de redução/negação de fall damage, stacking, target rules e aquisição específica.

## Deduplicação / fail-closed

Tailwind ocupa um buff/effect Wind com interação de queda. Não adicionar segundo listener de fall damage ou modifier de movimento sem identificar o effect/hook provider-native exato.

## Evidência

Runtime registry + ASM do pack; release 1.0.5; changelog 1.0.1.
