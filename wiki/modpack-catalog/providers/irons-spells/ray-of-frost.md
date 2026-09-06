# Ray Of Frost

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:ray_of_frost`
- **JAR/versão instalada:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Ice
- **Níveis:** 1–5
- **Raridade:** Common → Legendary
- **Cast:** Instant
- **Mana:** 25–85
- **Cooldown:** 15 s
- **Dano atual:** 12–18
- **Freeze atual:** 4,5–7,5 s
- **Range:** 30 blocos

## O que faz

Dispara um beam de frio por raycast, causando dano e aplicando imediatamente freeze ao alvo atingido.

## Snapshot upstream `e4056af...` — NÃO tratado como tag 3.16.3

- raycast 30 blocos, com blocks e bb inflation 0.15;
- cria `RayOfFrostVisualEntity` entre olhos do caster e hit location;
- damage = `3 + spellPower * 1.5`;
- freeze = `spellPower * 15` ticks, somado ao `ticksRequiredToFreeze` do target via damage source indirect;
- efeitos `ICY_FOG` + snowflakes no impacto;
- som `RAY_OF_FROST`.

## Targets / PvP / bosses / summons

- **Targeting:** primeiro resultado do raycast dentro de 30 blocos.
- **Players em PvP, bosses e summons:** eligibility/imunidade de freeze e damage policy `NÃO VERIFICADO`.
- **Block hit:** gera VFX, sem dano no bloco segundo a spell class auditada.

## Obtenção, requisitos e aprendizado

- pipeline geral de scrolls/spellbooks;
- rotas específicas `NÃO VERIFICADO`;
- requisitos adicionais `NÃO VERIFICADO`;
- itens/focus/rituais específicos `NÃO VERIFICADO`.

## Integrações / QA / fail-closed

- **Damage/freeze authority no snapshot:** `DamageSources.applyDamage` + damage source do spell.
- bridge específica `NÃO VERIFICADO`.
- QA client-real e resistência/imunidade por tipo de entidade `NÃO VERIFICADO`.
- Não executar segundo raycast ou reaplicar freeze/dano.

## Deduplicação

Já cobre instant Ice beam de alcance fixo com dano + freeze imediato.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/` — consulta 2026-09-06.
- Snapshot upstream `e4056af...`: `RayOfFrostSpell.java`.
