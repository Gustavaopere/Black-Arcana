# Simply Swords: Cataclysm — quatro habilidades para perks, 23/10/2026

Base Black Arcana `8514ff044d8e96285ff20d00c5e820e4aed837eb` (Ypsilon #876); RPG/modlist `ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc`, Enshrouded `a41dbb51aacb94b7b5db6517f1514b0b7aee3e83`, Factory `518278ae9c0d264a537cc1bc6ee4974e01270fdf`.

## Entrega e evidência

[Quatro fichas existentes](../../wiki/modpack-catalog/providers/✅-simply-swords-cataclysm/IMPLEMENTATION-PERK-BOUNDARIES-1.0.2.md) aprofundadas: Blazing Brand, Accursed Rage, Mecha Pulse e Mecha Smite. Matrizes registram defaults/fórmulas/unidades/ranges, targeting, damage/status/heal, tempo/custos, consumers, ownership e limites de alteração por perk. Dossiê comum e checklist de config corrigem a leitura de chances inclusivas e deixam ativação implantada separada de inventário. **+0 identidades/+0 strict**; estados/partículas/armas não são novas raízes.

Source oficial `Cephelo/SimplyCataclysmMod@a81158e53b2d215ff534fa59732edd08cfd1d4f4`, com 13 arquivos Java e versão declarada 1.0.2+1.21.1+neoforge. A correlação histórica à release/JAR #501 mantém SHA-1 `a2aa0f82ae3a9be2f43a4d47b3cb2201dd4e1469`, sem afirmar igualdade source→classfiles nem novo fingerprint implantado. Dependências do build do addon (Simply Swords 1.61.3/Cataclysm 2.39) diferem do snapshot físico (1.70.2/3.33). Licença upstream All Rights Reserved; consulta factual e referências, sem importar implementação ou assets.

Consultados os sources das versões declaradas dos hosts: Simply Swords `359a8031b1a3243d1a3b013dbaa0cbba70ea8278` e Cataclysm `fe6d06e79d98fcbf22fbd8aee153c65a1d9eb3cd`. O dossiê registra permalinks e limites de prova; isso não homologa seus JARs físicos ou o conjunto.

NeoForge 21.1.250 oficial: sources.jar SHA-256 `a2811d794544ec67dc3fa43b900158f058ea534881ba1c160373554384311a0d` e userdev.jar `deb6dd1e002aa85406e92501f49d5429cc8eaefe32fc353433e67030c32d8372`, conferidos contra checksums publicados. LivingDamageEvent, DamageContainer, LivingHealEvent e MobEffectEvent foram comparados byte a byte com os quatro arquivos correspondentes do pin Git `e0e7ab5d273fdc034f23fee7bf91c61ae39d3019`; igualdade limitada a esses arquivos. CommonHooks/EventHooks e patches inteiros não têm essa prova de identidade. Os patches oficiais do userdev sustentam a fase real de dano e escala do template de atributo.

Achados relevantes:

- Rage/Pulse recompõem originalDamage+bônus no Pre pós-armor/potion, em vez de partir de currentDamage; podem substituir mitigação/alterações anteriores mesmo com bônus 0. Absorption e fases posteriores ainda existem.
- Blazing Brand cura pelo amplificador candidato e attack speed; retorno de addEffect é ignorado. Veto ao efeito não implica veto à cura. O hook genérico de heal não identifica a origem Brand por si.
- Pulse exige transição de amplificador e usa target único: não há dano em área demonstrado pela partícula de onda. Cataclysm pode recusar stun ou removê-lo no Post do próprio golpe; duração pedida não é duração garantida.
- Smite separa harmful e regen, usa limiar estrito de HP e fogo em segundos×20; estado/DoT/regen não têm cast token próprio.
- RNG usa `<=chance`, sem guard geral chance>0; comentários de disable por zero não demonstram exclusão lógica estrita. Cap/threshold0 podem causar null dentro de try/catch antes do RNG. São achados source-causais, sem alegar bug reproduzido no pack.

## Validação

- **4 fichas**, universo das quatro traits reconciliado com localização oficial e tree Java; Fireproof & Unbreakable e quatro efeitos auxiliares excluídos de novas identidades.
- Fichas/dossiê: **76 referências pinadas** em **25 arquivos source distintos**, **24 links locais** e **8 tabelas** conferidos. São referências, não 76 hooks únicos.
- Nos 11 Markdown do lote antes deste relatório: **455 links locais** resolvidos, **12 tabelas** com colunas válidas. Checksums dos dois artefatos NeoForge e identidade dos quatro arquivos source conferidos.
- Revisão independente das quatro fichas e do dossiê comum, sem bloqueantes factuais restantes.
- `PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/global_magic_catalog_test.py`: **52/52 PASS**.
- `PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/catalog_physical_ledger_test.py`: **5/5 PASS**.
- `PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/magic_pendency_tracker_test.py`: **26/26 PASS**.
- Painel: **4/4 documental**, 164 providers, barra geral indeterminada; escopos Ypsilon 15/15 spells e 13/13 Principles preservados. Mínimos/campanha 38/39 inalterados. `git diff --check` limpo.

Nenhum runtime, adapter, perk, dependência ou lockfile foi alterado. STARTUP implantado completo, source/JAR/hosts carregados, multiplayer, Survival/cliente, persistência e QA de combate continuam **PENDING**. O coletor não foi executado numa instância implantada neste lote. Build/headless Black Arcana sem o addon não valida esses procs. Nenhum Stage promovido; resultados de CI/merge devem ser comunicados somente após execução real.
