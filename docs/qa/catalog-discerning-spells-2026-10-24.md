# Discerning The Eldritch — parâmetros e consumidores de 22 spells, 24/10/2026

Base Black Arcana `0c347bfa534259773bcb59b50e3ceb0010e9d7e4` (#884), já incorporando as provas Wind’s Spellbooks das PRs880–884; os arquivos e a entrada de progresso desse provider foram preservados. RPG/modlist `ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc`, Enshrouded `a41dbb51aacb94b7b5db6517f1514b0b7aee3e83`, Factory `518278ae9c0d264a537cc1bc6ee4974e01270fdf`.

## Entrega e proveniência

[22 fichas existentes e contratos comuns](../../wiki/modpack-catalog/providers/✅-discerning-the-eldritch/SPELL-PERK-BOUNDARIES-1.4.4-1.21.md) aprofundados com valores/fórmulas/unidades, classes/métodos consumidores, ingresso e aquisição, targeting/área, dano/tipo, projéteis/hitbox, tempos/custos/recasts, summons, estados e limites de alteração por perks. Índices/auditoria e barras atualizados. **22/22 mede esse recorte documental, +0 identidades/+0 strict**; não encerra todo sistema/item do mod ou aceite físico.

Source oficial `AceTheEldritchKing/Discerning_The_Eldritch@7bbd81f902c65a4452f47656ebd948cae8cd5833`, versão declarada 1.4.4-1.21, MC1.21/range[1.21,1.21.2), build NeoForge21.1.244/Iron’s3.16.2/Azure3.1.0/Ace’s1.2.7.2. Pack MC1.21.1/NeoForge21.1.250/Iron’s3.16.3/Azure3.1.11/Ace’s1.2.7.2; dev BA NeoForge21.1.248. Host Iron’s consultado `e4056af90302d37eb1739f5ff05020b020e6e252`. `mod_license=MIT`/metadata versus TEMPLATE_LICENSE PolyForm Shield1.0.0 são sinais distintos, sem LICENSE MIT na árvore auditada; consulta factual/paráfrases/referências, sem importar corpos ou assets.

Publisher [CF8816497](https://www.curseforge.com/minecraft/mc-mods/discerning-the-eldritch/files/8816497), medido nesta sessão: **22098930 bytes**, SHA-1 `cf35c225aced23b705d1e0fd1bc5c62d96540e0c`, SHA-256 `77e53df3fe020572626593ca9f6b955abce1dd4b49697084c2226019dcf2ef14`. Coincide com ledger físico histórico #220 de `discerning_the_eldritch-1.4.4-1.21.jar`; o perfil instalado original não está nesta sessão. Não se declarou nova medição dele ou igualdade integral source/classfiles.

Os 22 registrations ativos do source foram reconciliados com IDs/classes/referências do registrar no publisher. O JAR contém também **AbstractRitualSpell**, classe-base abstrata, excluída das identidades; são 22 classes concretas registradas. Nomes alternativos de Glacial Edge e Zealous Harbinger não criam raízes extras.

## Provas estreitas e limites

- Inspeção estática JDK21 `javap -c -p` no publisher: ForsakenAid#spawnForsakenAid usa getCreature offset189 seguido de CHECKCAST AbstractSpellCastingMob192; Gaoler#spawnGaoler usa getCreature121 seguido de CHECKCAST GaolerEntity124. Replacement não aceita LivingEntity arbitrária por esse caminho. Gaoler addFreshEntity133 tem resultado descartado136, initSummon145 precede removeSummon do original155 no ramo feral. Essa observação não equipara os métodos inteiros ao source nem prova cleanup em jogo.
- Reprodução isolada no JDK21: compilar **MasteryLaneCatalog** do pin RPG, sem Minecraft/modloader, e chamar ironsDiscipline confirmou `eldritch→irons:eldritch`; `discerning_the_eldritch/ritual` lançou IllegalArgumentException. No source, normalizeSchool produz esse token custom e forIron o entrega ao método; a regex MEMBER proíbe `/`. Prova do contrato do método, sem alegar crash reproduzido no pack ou corrigir runtime. Os cinco Ritual mantêm integração Mastery condicionada.
- [Sources.jar oficial Prometheus1.2.5](https://maven.crystalnest.it/it/crystalnest/prometheus-neoforge/1.21-1.2.5/prometheus-neoforge-1.21-1.2.5-sources.jar): **1016902 bytes**, SHA-256 `436aaa809e4162ca813e6c5bf7cce4a7ed1209ddb43b65ffcd9b3bf89006cb2a`. `it/crystalnest/prometheus/api/FireManager.java`, linhas 943–965, documenta segundos e encaminha setOnFire(Entity,float,ResourceLocation) a Entity::igniteForSeconds; overload interno chama o consumer e define fireType. Assim10/25 são segundos **pedidos nessa fonte consultada**, não ticks nem duração final garantida. DTE build declara1.1.2 versus pack1.2.5, Soul Fire’d6.0.2 versus6.1.0; não foi provada igualdade desse sources.jar com todos os métodos do binário instalado ou da composição montada.

## Achados úteis para perks

- Silence/Metaphysical são vetos em fases específicas. O handler pode incrementar Insanity após seu próprio cancelamento; o veto incoming Metaphysical foi localizado. Pre-cast, contador ou anúncio não confirmam efeito entregue.
- SpellHealEvent é observer. Mend Flesh tem cura do cast, cura fixa por evento Post e cura por XP; nenhum setter desse evento altera os três caminhos.
- Otherworldly/Rift preservam efeitos após tentativa de teleporte vetada; Boogie usa duas chamadas teleportTo diretas. Snapshot de pre-cast, nível do evento, destino real e rollback são contratos diferentes.
- Esoteric Edge faz duas tentativas de helper em Living, com ledger de tentativas. Rift tem corpo não protegido pelo if observado; a query AABB não vira esfera/LOS pelo comentário.
- SoulEruption/RitualBurn guardam fonte estática do primeiro owner; hurt direto com SpellDamageSource ainda pode acionar listeners host, embora pule o helper/SpellDamageEvent. Fonte plain Blood Rot é outra situação. Carver tem estado singleton, fases de CastType, attachments e finisher próprios.
- Summons controlados, feral e Ascended boss não partilham automaticamente ownership/timers/AI. Aquisição por itens, loot, cauldron, presets e AffinityData é rastreada sem inferir Survival PASS ou creative-only por exclusão.

São achados source-causais e provas binárias limitadas; não são correções ou bugs reproduzidos no modpack. Custos, efeitos, autoria, estados e cleanup continuam com os providers.

## Validação

- Nas 22 fichas e no dossiê comum: **554 referências pinadas**, **129 arquivos source distintos**, **89 links locais** e **43 tabelas** conferidos. Referências não são 554 hooks únicos; a prova Prometheus version-bounded foi verificada separadamente.
- Nos **35 Markdown** alterados, incluindo este relatório: **529 links locais** resolvidos e **46 tabelas** com colunas válidas, sem referências indefinidas. `git diff --check` limpo.
- Revisão independente das 22 fichas, dossiê comum, metadata, índices e relatório concluída sem bloqueantes; precisões de owner/castData, consumer de SUMMON_DAMAGE e callbacks de recast registradas. Nenhum aceite físico inferido.
- `PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/global_magic_catalog_test.py`: **52/52 PASS**.
- `PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/catalog_physical_ledger_test.py`: **5/5 PASS**.
- `PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/magic_pendency_tracker_test.py`: **26/26 PASS**.
- Após incorporar a nova base, seis suites sintéticas Wind preservadas: **47/47 PASS** (7 formula contract,9 caller edges,10 getter formulas,8 mobility contract,7 mobility getters,6 metadata). Isso não é nova execução dos nove getters no JAR físico Wind.
- Painel:164 providers únicos, mínimos1856/1854, campanha38/39 e universo global aberto/null preservados; `runtime_acceptance=NOT_INFERRED`. Entrada Wind inalterada, apenas DTE e base/date atualizados.

Nenhum runtime, adapter, perk, dependência ou lockfile alterado. Config/datapacks implantados, métodos/JAR/hosts, Survival/cliente/multiplayer/PvP/claims, budgets, chunks/dimensões, persistência/sync/cleanup/morte/reload/restart continuam **PENDING**. CI/headless BA sem DTE não homologa estas spells; nenhum Stage promovido. Resultados de PR/CI/merge devem ser comunicados após execução real.
