# Charge Leyline

Status: `COUNTED_EXACT / IDENTIDADE DO REGISTRY 1.0.3 / MECÂNICA ESPECÍFICA NÃO VERIFICADA`

## Registro exato da versão instalada

- **Registry:** `LeySpellRegistry`, campo `CHARGE_LEYLINE`.
- **Registry ID:** `leylines:charge_leyline`.
- **Classe exata:** `ChargeLeylineSpell`.
- **Confiança:** `COUNTED_EXACT` para identidade de registry/artefato; não implica execução física verificada em Survival.
- **Escola:** `leylines:ley`; todas as 14 classes fornecem configuração padrão para esta escola no JAR exato.
- **Autoridade:** Leyline Spellbooks mantém o efeito e o estado específico; Iron's Spells 'n Spellbooks mantém casting/mana/cooldown genéricos. Black Arcana não intercepta nem duplica esse pipeline.
- **Gate documentado:** registro incondicional, sem trava provider-native observada; elegibilidade genérica Iron's com `requiresLearning=false`, `allowLooting=true` e spell enabled por padrão. Configuração implantada no modpack e RNG de loot continuam não verificados.
- **Mecânica numérica, custo, cooldown, level, targeting exato, filtros PvP/boss, persistência e balance:** `NÃO VERIFICADO` individualmente, salvo descrição editorial pública explicitada na ficha; nenhum valor presumido.

## Mecânica e aquisição comprováveis

O JAR exato injeta scrolls de nível 1 de `leylines:charge_leyline` em tabelas de loot selecionadas do Iron's. Isso é uma rota de aquisição documentada, não probabilidade de drop ou confirmação em Survival.

## Deduplicação, segurança e procedência

Contado **uma vez** como registro provider-owned do Leyline 1.0.3, já incluído no total histórico de +14. Não contar escola Ley, scrolls, efeitos, mobs, itens ou nomes alternativos como feitiços adicionais. Não desenvolver hook de magia, world effect, charge ledger ou cooldown próprio do provider sem API e validação exatas.

Fontes: [registry da versão exata](../EXACT-1.0.3-SPELL-INVENTORY.md), [auditoria binária 1.0.3](../EXACT-1.0.3-ARTIFACT-AUDIT.md), [autoridade e reachability](../README.md). A inspeção clean-room retém apenas fatos do registry, metadados de artefato e relações limitadas de elegibilidade; nenhum código nem recurso proprietário é reproduzido.
