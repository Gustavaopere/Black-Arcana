# Leyline Spellbooks 1.0.3 — catálogo público source-bounded

## Estado

- JAR instalado: `leylines-1.0.3.jar`
- Mod ID runtime: `leylines`
- Versão runtime: `1.0.3`
- Minecraft: `1.21.1`
- Loader: NeoForge
- Provider base obrigatório: Iron's Spells 'n Spellbooks
- CurseForge Project ID: `1636676`
- CurseForge File ID: `8565076`
- SHA-1 do artefato: `dfa6908731f432905caaaa1e53b4aedeaa26ed59`
- Source público exato: **não localizado**
- JAR exato: **identificado e CDN-resolvido; bytecode ainda não extraído neste ambiente**
- Inventário completo de spells: **NÃO VERIFICADO**
- Estado: `EXACT-ARTIFACT-PINNED / PUBLIC SEMANTIC CATALOG PARTIAL / BYTECODE PENDING / FAIL-CLOSED`

A modlist e o Notion apontam para o mesmo `leylines-1.0.3.jar`. A publicação oficial confirma File ID 8565076 para NeoForge 1.21.1. Um índice externo do mesmo artefato associa esse File ID ao SHA-1 acima, coincidente com a modlist. A URL CDN do artefato exato também foi resolvida, mas os bytes do JAR ainda não puderam ser inspecionados localmente.

## O que a fonte oficial realmente prova

O projeto se apresenta como addon de Iron's que acrescenta uma escola nova chamada **Leyline**. O loop de mundo inclui correntes/leylines subterrâneas, pilares noturnos carregáveis, Leyline Rifts com encontros em ondas, loot temático, experiência e chance de Ley Crystal. A progressão pública também cita **Leyline Codex** e **Ley Staff**.

A página oficial lista como `Signature Spells`:

1. [Blink Step](spells/blink-step.md)
2. [Rift Gate](spells/rift-gate.md)
3. [Chrono Tether](spells/chrono-tether.md)
4. [Temporal Stutter](spells/temporal-stutter.md)
5. [Fissure](spells/fissure.md)
6. [Anchor Recall](spells/anchor-recall.md)
7. [Beam](spells/beam.md)
8. [Ley Blast](spells/ley-blast.md)
9. [Eclipse](spells/eclipse.md)

**Importante:** a publicação diz `and more`. Portanto estes nove nomes são um subconjunto público, não um registry inventory. Este provider não recebe `9/9 COMPLETO`.

## Mundo e progressão

- [Rift encounters e regras 1.0.3](RIFT-ENCOUNTERS.md)
- [Progressão pública e itens](PROGRESSION.md)
- [Auditoria técnica/provenance](TECHNICAL-AUDIT.md)

## Authority / deduplicação

Enquanto o bytecode exato não for auditado:

- não assumir IDs de registry a partir do nome inglês;
- não inventar níveis, raridade, mana, cooldown, cast time, dano, alcance, duração, caps, targeting ou aquisição;
- não recriar portais, time manipulation, charges, rift state, wave lifecycle ou rewards no Black Arcana;
- qualquer bridge que dependa de hook/API específico deve permanecer fail-closed;
- descrições públicas servem para identidade semântica e detecção de sobreposição, não como prova de assinatura de API.

## Próximo gate

Extrair/auditar o JAR `8565076`, verificar hashes, listar registries/resources/classes e então substituir cada `NÃO VERIFICADO` por evidência do artefato instalado. Só após isso o inventário pode ser fechado numericamente.
