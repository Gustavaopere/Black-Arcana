# Saeptum

- ID: `ypfundamentals:saeptum`
- escola registrada: Fundamentalism; domain escolhe a escola elemental dominante do caster quando Player
- rarity: Legendary
- nível: 1
- cast: LONG, 80 ticks / 4 s
- mana: 600
- cooldown: 300 s
- loot/crafting: desabilitados
- `requiresLearning=true`

## Unlock

Requer simultaneamente:
- Concentratio >=12
- Locus >=10
- Perceptio >=12
- Apparitio >=10

O próprio attachment aprende o spell e o SpellSelectionEvent adiciona `domain_slot`.

## Domain contract

`DomainEntity` estende `AbstractDomainEntity` do Ace's Spell Utils. Source pin:
- radius 20;
- duração interna inicial 60 s;
- refinement deriva do spell power dominante + Principles;
- prende living entities na área com `TRAPPED_EFFECT` durante construção;
- constrói uma barreira esférica, registra blocos originais e restaura no cleanup;
- registra posições originais e retorna entidades ao destruir o domínio;
- possui domain clashes/refinement;
- adiciona region ticket provider-native durante ativação;
- aplica Burnout ao owner por 160 s no destroy path mostrado.

Dano periódico/sure-hit e todos os edge cases do domain completo: **NÃO VERIFICADO** nesta ficha até auditoria integral da entity/runtime.

## Authority / dedup

Não force-load, não construa barrier, não teleporte/restore e não implemente clash em paralelo. O lifecycle do `DomainEntity`/Ace's Spell Utils é authority.