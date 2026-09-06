# Raise Dead — Iron's Spells 'n Spellbooks

## Estado
`PROVIDER-NATIVE / SOURCE 3.16.3 AUDITADO / ECONOMIA HEMÁTICA FUTURA AINDA NÃO APLICADA`

## Identidade
- **ID:** `irons_spellbooks:raise_dead`
- **Escola:** Blood
- **Raridade:** Uncommon
- **Max level:** 6
- **Função:** summon de mortos-vivos temporários

## Custo atual
- **Mana base:** 50
- **Mana/level:** +10
- **Cooldown:** 150 s
- **Cast time:** 30 ticks
- **Cast type:** Long
- **Spell power base:** 10
- **Spell power/level:** +3
- **Recast count:** 2

## Efeito
- summon count = `spellLevel + 2`;
- duração dos summons: `20*60*10 = 12.000 ticks` (10 min);
- ~30% dos summons são `SummonedSkeleton`, restantes `SummonedZombie`;
- equipamento é gerado de forma bounded conforme spell power/quality;
- drop chance do equipamento é zerada;
- publica `SpellSummonEvent(caster, undead, spellId, spellLevel)` antes de adicionar a criatura;
- `SummonManager` registra ownership/lifetime/recast.

## Deduplicação
Já ocupa necromancia/summon de mortos-vivos no Iron's. Bruxaria, Infernal e Binding não devem criar `Raise Dead` equivalente; Goety/Eidolon também precisam ser comparados antes de qualquer nova necromancia.

## Migração Blood
Se continuar pertencendo à disciplina Blood no pack, o custo pode migrar para sangue; isso não significa que cadáver/alma seja sangue. Summon authority e `SpellSummonEvent` continuam provider-native.
