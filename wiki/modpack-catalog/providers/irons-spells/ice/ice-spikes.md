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

## Source audit 3.16.3 — commit `e4056af...`

- count = `7 + 3 * level / 2` (aritmética inteira), produzindo 8–22;
- spell power base 12, +1/level;
- pequenos spikes recebem `damage * 0.5`; final recebe dano integral;
- usa `TargetEntityCastData` para ajustar a distância/final spike em direção a target móvel;
- cada `IceSpikeEntity` recebe tamanho interpolado, wait time por índice e orientação variável;
- só spawna quando o bloco abaixo tem face superior sturdy;
- pre-cast target helper escala aproximadamente com `count * 1.25`.

## Targets / PvP / bosses / summons

- **Targeting:** linha à frente com otimização para target válido no source.
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

## Matriz obrigatória de verificação

- **Status/provider/mod ID/JAR/spell ID/escola/tipo:** confirmados; tipo funcional = sequência de ground spikes Ice.
- **Descrição funcional:** confirmada.
- **Níveis/raridade:** 1–10 / Common → Legendary.
- **Cast type / cast time / channel:** `INSTANT` / 0 ticks / não channel.
- **Recurso/custo:** mana / 30–120; fórmula fina de custo `NÃO VERIFICADO`.
- **Cooldown:** 15 s.
- **Dano/cura/tipo de dano:** 12–21 nominal; spikes intermediários 50%, final 100%; cura não aplicável; tipo/tag exato `NÃO VERIFICADO`.
- **Alcance/raio/área/duração:** área linear; helper ≈ `count*1.25`; delay por spike = índice; hitbox/radius/lifetime exatos da entidade `NÃO VERIFICADO`.
- **Scaling/fórmulas/caps:** count `7+3*level/2`; damage spell power base12 +1/level; size interpolation source-auditada; caps além de nível10 `NÃO VERIFICADO`.
- **Targets/PvP/bosses/summons:** target móvel suportado; policy de entidade `NÃO VERIFICADO`.
- **Condições/requisitos:** superfície sturdy confirmada; outros requisitos `NÃO VERIFICADO`.
- **Obtenção/fabricação/ganho/aprendizado:** pipeline geral; rotas específicas `NÃO VERIFICADO`.
- **Itens/focus/rituais:** específicos `NÃO VERIFICADO`.
- **VFX/partículas/textura/animação/áudio:** entity visual existe; detalhes de VFX/partículas/textura/animação/áudio `NÃO VERIFICADO` nesta ficha.
- **Integrações/bridges:** `IceSpikeEntity` authority; bridge específica `NÃO VERIFICADO`.
- **Deduplicação/sobreposição:** conclusão baseada no source pinado.
- **Bugs/QA/fail-closed:** QA real `NÃO VERIFICADO`; falhar fechado em terrain inválido; não duplicar sequência/dano.
- **Fonte/evidência/estado:** catálogo + source 3.16.3.

## Fonte / evidência

- Catálogo oficial atual: `https://iron.wiki/spells/` — consulta 2026-09-06.
- Source 3.16.3 `e4056af...`: `IceSpikesSpell.java` + `gradle.properties`.
