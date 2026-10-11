# Relics 0.12.8 — ring_of_the_seven_deadly_sins / lust

Status: **✅ CATALOGADO / `COUNTED_EXACT`** na identidade owner-scoped · **⚠️ runtime, configuração e QA de Survival condicionados**.

## Identidade e evidência

- **Provider:** Relics, mod ID `relics`.
- **Tipo:** Habilidade independente do provider, **não** spell de Ars Nouveau/Iron's.
- **Relíquia proprietária:** `ring_of_the_seven_deadly_sins`.
- **ID local da habilidade no artefato:** `lust`.
- **Chave semântica inequívoca:** `ring_of_the_seven_deadly_sins|lust`.
- **Ordinal da seção factual:** 32/39; apenas posição documental, nunca registry ID.
- **Versão e hash exatos:** `relics-1.21.1-0.12.8.jar` (NeoForge 1.21.1), SHA-1 físico/publisher `1fe7d57ebfa56ebd0aeecfed01075f8b55b94ef7`, SHA-256 publisher `db6f436053fe717413389e55390a5f98103ccd91cca5fe469e090bdfaef70717`, CurseForge 445274/8158315.
- **Fonte de contagem:** [inventário de habilidades/sinergias hash-matched](../../EXACT-0.12.8-ABILITY-INVENTORY.md) e [auditoria geral do provider](../../README.md).
- **Estado de evidência:** `COUNTED_EXACT` da identidade composta **já incluída** entre 39 habilidades + duas sinergias; **+0 novas identidades** nesta individualização.
- **ResourceLocation executável, classe Java/método de invocação, configuração e efeito concreto:** **NÃO VERIFICADO** nesta ficha; o ID local não vira automaticamente namespace de registry.

## Semântica permitida e limites

Esta identidade provém da **raiz factual de localização da descrição de habilidade** no artefato exato e é escopada ao item proprietário. O ID local `lust` isolado não basta para identificação global: por exemplo `slots` também existe em outro item. O nome do ID não certifica alcance, dano, cooldown, gatilho, ativação, nivelamento nem efeito exato.

- **Ativação, alvo, custo, XP/rank, modos, cooldowns, buffs, salvamento, persistência, duração, entidades, world mutation e interação entre addons:** **⚠️ NÃO VERIFICADOS** para esta identidade no pack implantado.
- **Deduplicação:** modos/qualidades/ranks/switches e o item da relíquia não geram objetos mágicos extras. O mesmo identificador local em outro owner não é automaticamente o mesmo objeto.
- **Autoridade:** Relics controla abilities, sinergias, XP, levels, cooldowns, estado, progressão e targeting. Curios controla equip slots. Black Arcana não cria segundo cast/estado/recurso, não aplica efeitos duas vezes nem substitui o servidor Relics; RPG Skill Tree não assume o runtime do Relics.
- **Interop:** sem boundary/API provider-native causal comprovada, qualquer integração permanece **⛔ fail-closed**; a CI documental não é teste de execução física do item.

**Clean-room:** somente IDs, metadados e fatos estruturais da auditoria própria; nenhum bytecode, tradução, tooltip, textura, asset ou implementação do provider foi copiado.
