# Cone Of Cold

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:cone_of_cold`
- **JAR/versão instalada:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Ice
- **Níveis:** 1–10
- **Raridade:** Common → Legendary
- **Cast:** Continuous
- **Mana atual:** 5–14
- **Cooldown:** 12 s
- **Dano atual:** 1–7,75

## O que faz

Mantém um cone de energia fria à frente do caster, causando dano e acumulando freeze em criaturas no caminho.

## Snapshot upstream `e4056af...` — NÃO tratado como tag 3.16.3

- classe `ConeOfColdSpell`;
- cast time 100 ticks;
- cria `ConeOfColdProjectile` e o guarda em `EntityCastData`;
- durante o mesmo cast contínuo, ativa o settlement de dano na entidade cone existente em vez de criar outra;
- fórmula do snapshot: `damage = 1 + spellPower * 0.75`;
- `SpellDamageSource` adiciona 80 freeze ticks;
- som de finish/loop: `CONE_OF_COLD_LOOP`;
- AI deixa de canalizar quando o alvo se afasta além da condição definida pelo spell.

## Targets / PvP / bosses / summons

- **Direção/área:** cone orientado pelo caster via `ConeOfColdProjectile`.
- **Players em PvP, bosses e summons:** friendly-fire/eligibility específica da entidade cone `NÃO VERIFICADO` nesta ficha.
- **Freeze:** 80 ticks no damage source do snapshot; o settlement exato no JAR 3.16.3 permanece sujeito à pinagem do source.

## Obtenção, requisitos e aprendizado

- **Pipeline geral:** scrolls/spellbooks do Iron's.
- **Rotas específicas:** `NÃO VERIFICADO`.
- **Condições/requisitos adicionais:** `NÃO VERIFICADO`.
- **Itens/focus/rituais específicos:** `NÃO VERIFICADO`.

## Integrações / QA / fail-closed

- `EntityCastData` + `ConeOfColdProjectile` representam a ownership contínua no snapshot.
- **Bridge específica:** `NÃO VERIFICADO`.
- **VFX/textura/animação e QA client-real:** `NÃO VERIFICADO` além do som acima.
- Integrações não devem spawnar um segundo cone nem cobrar/aplicar dano por um segundo channel path.

## Deduplicação

Já cobre cone contínuo Ice com dano + freeze. Não duplicar channel, freeze ou dano em bridge externa.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/` — consulta 2026-09-06.
- Snapshot upstream `e4056af...`: `ConeOfColdSpell.java`.
