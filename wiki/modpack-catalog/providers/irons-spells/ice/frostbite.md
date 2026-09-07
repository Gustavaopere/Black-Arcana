# Frostbite

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:frostbite`
- **JAR/versão instalada:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Ice
- **Níveis:** 1–5
- **Raridade:** Epic → Legendary
- **Cast:** Instant
- **Mana:** 80–120
- **Cooldown:** 60 s
- **Shatter damage atual:** 6–10
- **Duração atual:** 30 s

## O que faz

Imbui o caster com Frostbitten Strikes. Durante o efeito, criaturas totalmente congeladas mortas pelo caster tornam-se Ice Shadows, que depois se estilhaçam em icicles.

## Source audit 3.16.3 — commit `e4056af...`

- aplica `MobEffectRegistry.FROSTBITTEN_STRIKES` ao caster;
- spell power base 30, duração `spellPower * 20` ticks;
- amplifier = `spellLevel + 4`;
- shatter damage é resolvido por `FrostbiteEffect.getDamageForAmplifier`;
- VFX: `SNOW_DUST` + `SwirlingParticleOptions(SNOWFLAKE, ...)`;
- animação `SELF_CAST_ANIMATION`.

O changelog oficial 3.16.2 registra cast effects adicionados a Frostbite.

## Targets / PvP / bosses / summons

- **Target inicial:** self-buff no caster.
- **Conversão de vítimas congeladas em Ice Shadows:** elegibilidade exata de players, bosses e summons `NÃO VERIFICADO` nesta ficha; não inferir que qualquer kill é elegível.
- **Causalidade:** manter o effect/provider como authority do proc de kill.

## Obtenção, requisitos e aprendizado

- pipeline geral de scrolls/spellbooks;
- rotas específicas `NÃO VERIFICADO`;
- requisitos adicionais `NÃO VERIFICADO`;
- itens/focus/rituais específicos `NÃO VERIFICADO`.

## Integrações / QA / fail-closed

- **Effect authority:** `FROSTBITTEN_STRIKES`/`FrostbiteEffect` no source 3.16.3.
- **Bridge específica:** `NÃO VERIFICADO`.
- assets/áudio completos e QA client/modpack real `NÃO VERIFICADO`.
- Não observar mortes congeladas por fora para spawnar um segundo Ice Shadow sem causalidade provider comprovada.

## Deduplicação

Já cobre self-buff Ice que converte kills de alvos fully-frozen em decoys/shatter entities.

## Matriz obrigatória de verificação

- **Status/provider/mod ID/JAR/spell ID/escola/tipo:** confirmados; tipo funcional = self-buff/proc Ice.
- **Descrição funcional:** confirmada pelo catálogo; proc fino fica sob `FrostbiteEffect`.
- **Níveis/raridade:** 1–5 / Epic → Legendary.
- **Cast type / cast time / channel:** `INSTANT` / 0 ticks / não channel.
- **Recurso/custo:** mana / 80–120; fórmula fina de custo `NÃO VERIFICADO` nesta ficha.
- **Cooldown:** 60 s.
- **Dano/cura/tipo de dano:** shatter 6–10; cura não aplicável; tipo/tag do shatter `NÃO VERIFICADO`.
- **Alcance/raio/área/duração:** self target; duração 30 s; raio/área do shatter/Ice Shadow `NÃO VERIFICADO`.
- **Scaling/fórmulas/caps:** amplifier `level + 4`; shatter via `FrostbiteEffect.getDamageForAmplifier`; caps adicionais além de nível 5 `NÃO VERIFICADO`.
- **Targets/PvP/bosses/summons:** proc eligibility `NÃO VERIFICADO` conforme seção.
- **Condições/requisitos:** kill de criatura fully frozen é condição pública; condições internas adicionais `NÃO VERIFICADO`.
- **Obtenção/fabricação/ganho/aprendizado:** pipeline geral; rotas específicas `NÃO VERIFICADO`.
- **Itens/focus/rituais:** específicos `NÃO VERIFICADO`.
- **VFX/partículas/textura/animação/áudio:** `SNOW_DUST`, swirling snowflake e `SELF_CAST_ANIMATION` confirmados; textura/áudio final `NÃO VERIFICADO`.
- **Integrações/bridges:** effect provider-native; bridge específica `NÃO VERIFICADO`.
- **Deduplicação/sobreposição:** conclusão baseada em source 3.16.3 pinado.
- **Bugs/QA/fail-closed:** QA real `NÃO VERIFICADO`; não inferir kill causal por HP delta nem duplicar Ice Shadow.
- **Fonte/evidência/estado:** catálogo + changelog + source pinado.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/` — consulta 2026-09-06.
- Changelog oficial 3.16.2.
- Source 3.16.3 `e4056af...`: `FrostbiteSpell.java` + `gradle.properties`.
