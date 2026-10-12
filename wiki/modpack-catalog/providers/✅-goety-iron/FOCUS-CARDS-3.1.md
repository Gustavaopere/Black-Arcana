# Goety Iron 3.1 — 2 fichas exatas de Focus

Status: **✅ 2/2 Focuses `COUNTED_EXACT` individualizados** · **✅ 12/12 rituais não-Focus com paths e outcomes individualizados** · **⚠️ runtime físico/Survival pendente**.

## Autoridade física e semântica

- `goetyiron`, JAR `GoetyIron-1.21.1-NeoForge-3.1.jar`, SHA-1 físico = publisher `c8529867e798661ed01fb2948abda23735888fc6`, CurseForge `1367643 / 8662179`.
- A [auditoria hash-matched 3.1](EXACT-3.1-ARTIFACT-AUDIT.md) confirma **2 Focus holders** — `FIERY_FOCUS` e `TARNISHED_FOCUS` — apoiados por duas spell surfaces de summon do addon. Ambos possuem ritual de aquisição no pacote.
- Há **14 recipes `goety:ritual`**: 2 são somente aquisição de Focus e não geram novas identidades; as **12 restantes** são rituais não-Focus com outcomes distintos e sem `mod_loaded` condition, já contabilizados.
- A [matriz exata 14/14](RITUAL-INVENTORY-EXACT-3.1.md) obtida por **reauditoria do mesmo SHA-1**, agora vincula individualmente os 12 rituais não-Focus aos paths, subtipos e outcomes, incluindo `goetyiron:hemolytic_ring`, `irons_spellbooks:rotten_spell_book` e `goety:heretic_servant`. [Fichas 12/12](RITUAL-CARDS-3.1.md). `goety:jei_dummy/none` é somente marcador placeholder.
- O estado `COUNTED_EXACT` significa **2 Focuses + 12 rituais não-Focus = 14 identidades já incluídas** no mínimo semântico. Criar as fichas adiciona **+0 novas identidades**, mantendo mínimos **1.851 global / 1.849 no escopo**, com denominador final aberto.
- O initializer tem zero branches de registro e zero config references, mas isso **não** prova execução física, custos, aquisição Survival nem hooks de integração.
- Sem copiar fontes 1.20.1 ou presumir equivalência estrutural Forge ↔ NeoForge. A ausência de source oficial exato e a divergência de licença impõem clean-room estrito. Goety/Iron's/Goety Iron mantêm ownership e liquidação próprios.

## Índice dos 2 Focuses

| # | Focus holder factual | Ficha | Status |
|---:|---|---|---|
| 1 | `FIERY_FOCUS` | [Abrir](focuses/fiery-focus.md) | `COUNTED_EXACT` |
| 2 | `TARNISHED_FOCUS` | [Abrir](focuses/tarnished-focus.md) | `COUNTED_EXACT` |

## Gate dos 12 rituais — evidência agora preservada

**✅ 12/12 rituais semanticamente contabilizados e 12/12 fichas nominais.** A [matriz path→outcome→subtype→top-level conditions](RITUAL-INVENTORY-EXACT-3.1.md) foi preservada após [auditoria independente do JAR SHA-matched #38186445480](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38186445480). Os **14** arquivos incluem 2 recipes de aquisição de Focus deduplicadas. **+0 novas identidades** e sem promoção da execução física/Survival. Não transformar nomes públicos de servants em outros IDs não comprovados.

## Limite de execução

Não há teste físico em modpack Survival nem contrato público de cast/ritual settlement/servant lifecycle comprovado nesta individualização. Nada altera o runtime Black Arcana, seus Stages, Soul Energy, Mastery, Arcane Danger, Corruption ou Strain. Integração técnica permanece **⛔ fail-closed** até API/hook seguro identificado.
