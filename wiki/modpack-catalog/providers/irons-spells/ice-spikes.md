# Ice Spikes

- **Status no modpack:** PRESENTE — ativo no catálogo atual
- **Provider:** Iron's Spells 'n Spellbooks
- **Mod ID:** `irons_spellbooks`
- **Spell ID:** `irons_spellbooks:ice_spikes`
- **JAR/versão instalada:** `irons_spellbooks-1.21.1-3.16.3.jar` / `1.21.1-3.16.3`
- **Escola:** Ice
- **Níveis:** 1–10
- **Raridade:** Common → Legendary
- **Cast:** Instant
- **Mana:** 30–120
- **Cooldown:** 15 s
- **Dano atual:** 12–21
- **Quantidade atual:** 8–22 spikes

## O que faz

Cria uma linha crescente de ice spikes pelo chão. O spike final causa dano completo; os anteriores causam dano reduzido. Com criatura válida no alcance, o final pode emergir antecipadamente junto ao target.

## Snapshot upstream `e4056af...` — NÃO tratado como tag 3.16.3

- count = `7 + 3 * level / 2` (aritmética inteira), produzindo 8–22;
- spell power base 12, +1/level;
- pequenos spikes recebem `damage * 0.5`; final recebe dano integral;
- usa `TargetEntityCastData` para ajustar a distância/final spike em direção a target móvel;
- cada `IceSpikeEntity` recebe tamanho interpolado, wait time por índice e orientação variável;
- só spawna quando o bloco abaixo tem face superior sturdy;
- pre-cast target helper escala aproximadamente com `count * 1.25`.

## Targets / PvP / bosses / summons

- **Targeting:** linha à frente com otimização para target válido no snapshot.
- **Players em PvP, bosses e summons:** eligibility/damage policy da `IceSpikeEntity` `NÃO VERIFICADO`.
- **Terrain:** requer superfície adequada; não há autorização para uma bridge forçar spikes em superfície inválida.

## Obtenção, requisitos e aprendizado

- pipeline geral de scrolls/spellbooks;
- rotas específicas `NÃO VERIFICADO`;
- requisitos adicionais `NÃO VERIFICADO`;
- itens/focus/rituais específicos `NÃO VERIFICADO`.

## Integrações / QA / fail-closed

- **Entity authority:** `IceSpikeEntity`.
- bridge específica `NÃO VERIFICADO`.
- hitbox/VFX/áudio finais e QA client-real `NÃO VERIFICADO`.
- Não criar segunda linha de spikes nem duplicar o dano final/half-damage.

## Deduplicação

Já cobre cascading ground spikes Ice com final spike fortalecido/antecipável por target.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/` — consulta 2026-09-06.
- Snapshot upstream `e4056af...`: `IceSpikesSpell.java`.
