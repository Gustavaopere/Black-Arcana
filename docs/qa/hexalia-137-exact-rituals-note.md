# Hexalia 1.3.7 — auditoria binária de 29 receitas mágicas

**Checkpoint:** 2026-10-14 · Minecraft 1.21.1, NeoForge, Java 21 · Black Arcana `main@98b9a0fe53f0b51c7d371d33355c8c55291e8ddc`. **Estado: 🟡 gate implementado; ⚠️ resultado físico pendente até inspeção do workflow exato.**

## Autoridades e divergência de distribuição

- Modlist atual do sibling `neoforge-rpg-skilltree/main@9e6436edb0049a8dcc4e47165db0f6850e5efa68`: Hexalia `hexalia-neoforge-1.3.7.jar`, mod ID `hexalia`, SHA-1 físico `ca90edf1664cf6d44fe7e5318c71069050499c7e` (#314). NeoForge 21.1.250 no pack.
- Publisher oficial CurseForge `962878` contém **duas publicações 1.3.7 / NeoForge / 1.21.1 com o mesmo filename**, [file 8875587 (13/09/2026)](https://www.curseforge.com/minecraft/mc-mods/hexalia/files/8875587) e [file 8943719 (21/09/2026)](https://www.curseforge.com/minecraft/mc-mods/hexalia/files/8943719). **O número do arquivo instalado não está demonstrado por nome/versão isoladamente**. A automação verifica ambos e aceita apenas o que corresponder ao SHA-1 físico; se nenhum corresponder, bloqueia, sem substituir a identidade instalada por upstream mais recente.
- Fonte publicada e pinada: `AstralyaStudios/Hexalia@98c22aaf70e069c616fed5ad2dc56d2b37fcd283`. O catálogo possui as [23 fichas de Nature's Ritual](../wiki/modpack-catalog/providers/✅-hexalia/NATURES-RITUAL-CARDS-1.3.7.md) e as [6 Celestial Infusions](../wiki/modpack-catalog/providers/✅-hexalia/CELESTIAL-INFUSION-CARDS-1.3.7.md). Source pin ≠ paridade de todos os métodos compilados.

## Auditoria executável

`docs/qa/hexalia_binary_recipes_audit.py` é uma inspeção **read-only** dos arquivos `data/hexalia/recipe/*.json` empacotados. O JAR é aceito apenas se houver:

1. Filename correto, SHA-1 exato da modlist física, arquivo regular, ZIP sem entradas duplicadas e metadados NeoForge cujo `modId` seja `hexalia`.
2. **23/23 IDs** de `hexalia:natures_ritual` e **6/6 IDs** de `hexalia:celestial_infusion`, sem ausência, excesso, duplicação ou identidade indevida. A contagem é de receita com tipo exato, não de todos os JSON em datapacks.
3. Elementos estruturais `center`/`offerings`/`output` coerentes com o tipo; as duas nature rituals `summon_silk_moth` e `summon_cacofey` exigem `requires_soul=true`, resultado tipo `entity`, contagem 1 e entidade respectiva. Esses campos são factos de dados e **não** certificam o tempo de manifestação ou a segurança do ritual.
4. Resultado `PASS` somente quando todos os gates forem satisfeitos; caso contrário, `FAIL_CLOSED`/ `UNPROVEN_OR_MISMATCH`. Relatório JSON contém SHA-1, SHA-256, file size, contagens e desvios; JAR/recursos do publisher não são compartilhados como artefato.

Os testes em `docs/qa/hexalia_binary_recipes_audit_test.py` usam apenas ZIPs sintéticos; green não equivale a resultado físico. A execução real usa `.github/workflows/hexalia-137-binary-recipes.yml` e dois URLs oficiais com hash obrigatório.

## Limites de interpretação

**Mesmo 29/29 `PASS` seria somente prova binária das receitas empacotadas no JAR exato**; não prova que o servidor as carregou após datapack/reload, que a configuração ativa permite crafting, que o Ritual Table consumiu offerings/salt/crops corretamente, que o soul gate foi satisfeito ou que houve proteção de claims. Os nove brews documentados não são somados novamente ao denominador 29. **+0 raízes semânticas** nesta auditoria.

A campanha de 39 providers permanece em **27/39 exatos / 12/39 condicionados** até evidência observada e integração da matriz. **Stage 06.05** continua sem promoção; **Stage 09** preserva QA Survival/dedicated. Sem contrato homologado com RPG Skill Tree, perks/Mastery ficam ⛔ bloqueados. Black Arcana não assume settlement de Hexalia.

**Handoff:** registrar workflow, SHA-256, file ID escolhido e contagens somente depois do run real; não inferir o ID da publicação com base na URL candidata.
