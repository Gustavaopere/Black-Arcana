# Asterism Arcanum — onze fichas com parâmetros e consumidores, 23/10/2026

Base Black Arcana `a93890ed70561176ace0859f76f4e6b63170ff0f` (#877); RPG/modlist `ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc`, Enshrouded `a41dbb51aacb94b7b5db6517f1514b0b7aee3e83`, Factory `518278ae9c0d264a537cc1bc6ee4974e01270fdf`.

## Entrega e proveniência

[11 fichas existentes](../../wiki/modpack-catalog/providers/✅-asterism-arcanum/SPELL-PERK-BOUNDARIES-0.1.0.md) aprofundadas com defaults/fórmulas/unidades, targeting, dano/tipo, geometria/colisão, tempo/custos, procs/estados, summons/movimento, persistência e limites por eixo para perks. Dossiê comum, README/auditoria e painel atualizados. **10 spells normais + Astral Gateway conditional**, fora do strict; não são onze spells Survival homologados. **+0 identidades/+0 strict**; Trailblaze não entra no universo, nem entidades/partes/efeitos filhos viram novas raízes.

Source oficial `BirdieVibes/Asterism-Arcanum@f1738c7813a85d31a6da10e6c9f2dbce18d2b583`, versão declarada 1.21.1-0.1.0, build NeoForge 21.1.215/Iron’s 3.15.6. Host consultado Iron’s 3.16.3 `e4056af90302d37eb1739f5ff05020b020e6e252`; build/dev Black Arcana NeoForge 21.1.248 versus snapshot físico 21.1.250. Licença Polyform Shield não é a licença MIT do template; somente consulta/paráfrases/referências, sem importar implementação ou assets.

Publisher CurseForge 8157080, baixado para inspeção estática e medido nesta data: **987245 bytes**, SHA-1 `4a25ba80116168ddcc812f71467c0598127e774a`, SHA-256 `191422cf3096a79e158d3262b52ea98fb1abc745847d4eb356548a5a5f58eebc`. Coincide com o fingerprint físico histórico #56 do JAR `asterismarcanum-1.21.1-0.1.0.jar`. O perfil instalado original não está nesta sessão; não se declarou nova medição dele nem equivalência integral de métodos source→classfiles.

Os onze registros ativos do source foram reconciliados com os onze nomes de classes Spell no JAR e suas referências no classfile registrar. `TrailblazeSpell` é comentado no bootstrap e ausente desse conjunto binário. A prova histórica de registry continua separada da causalidade source. Inspeção `javap` estreita de SummonLunarMothsSpell confirmou `getCreature` offset122 → **CHECKCAST SummonedLunarMothEntity125**: o replacement não pode ser tratado como LivingEntity arbitrária. Essa observação não equipara o método inteiro ao source nem comprova runtime.

NeoForge: dois arquivos do pin `e0e7ab5d273fdc034f23fee7bf91c61ae39d3019` (EntityTeleportEvent e PlayerRespawnPositionEvent) comparados byte a byte ao sources.jar21.1.250 oficial, cujo SHA-256 é `a2811d794544ec67dc3fa43b900158f058ea534881ba1c160373554384311a0d`. Prova limitada a esses dois arquivos; evento mutável genérico não é adapter testado do spell.

## Achados úteis para perks

- Brightburst chama hurt diretamente; não passa pelo ramo SpellDamageEvent/resist do helper Iron’s. Push não depende de dano aceito.
- PiercingLight distingue constructor caster de factory/load, vetor inicial versus speed e escala visual versus hitbox. Gravidade também depende dos listeners da dimensão Astral Sea.
- Beam/Gate têm cleanup normal via reset de EntityCastData do host. Failsafe401 e budget de Swarm órfão não são duração/budget garantidos por cast; filhos já emitidos têm lifecycle próprio e sourceSpellID PiercingLight.
- Starcutter limita radius a1 e usa raio terminal10r; getDimensions não atesta AABB final sem refresh. NBT não salva damage; Echo começa damage0, porém persistência desse zero não foi demonstrada.
- Echo usa evento/helper no teleporte inicial e setPos direto no retorno anti-magic. Gateway itera alvos mas transporta o caster, pode repetir transições e não representa portal de grupo seguro. Aquisição implantada segue aberta.
- Tether remove no tick após contador negativo; `n+2` é sequência nominal, não cap rígido de eventos. Barbs depende de Luck+tag, sem consumir a tag no primeiro hit; tooltip só lê o radius estático.
- Moth é singular, com ownership iniciado antes do evento de replacement. Ataque herdado seguido de helper são duas tentativas, não duas perdas de HP garantidas; Mana Rend 0.15 não é bônus plano de 15% nem mana drain.

São achados source-causais com limites por campo, sem alegar bugs reproduzidos no modpack ou autorização para substituir settlement/cleanup do provider.

## Validação

- **11 fichas/11 registrations source/11 classes Spell publisher**, com identidades reais e distinção de dez normais/Gateway conditional.
- Nas onze fichas e no dossiê comum: **291 referências pinadas**, **69 arquivos source distintos**, **42 links locais** e **13 tabelas** conferidos. Referências não são 291 hooks únicos.
- Nos 16 Markdown alterados antes deste relatório: **468 links locais** resolvidos e **17 tabelas** com colunas válidas.
- Revisão independente de todas as onze fichas e do dossiê comum concluída sem bloqueantes factuais; conferidos também os offsets estreitos do replacement Moth no publisher.
- `PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/global_magic_catalog_test.py`: **52/52 PASS**.
- `PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/catalog_physical_ledger_test.py`: **5/5 PASS**.
- `PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/magic_pendency_tracker_test.py`: **26/26 PASS**.
- Painel JSON/Markdown: **11/11 documental**, 164 providers únicos, denominador global aberto, `runtime_acceptance=NOT_INFERRED`. Mínimos semânticos, Gateway fora strict e campanha 38/39 preservados. `git diff --check` limpo.

Nenhum runtime, adapter, perk, dependência ou lockfile foi alterado. Config/datapacks implantados, equivalência dos métodos/JAR/hosts, Survival/cliente, multiplayer/PvP/claims, cleanup, sync e persistência/restart continuam **PENDING**. CI/headless Black Arcana sem Asterism não homologa estes spells; nenhum Stage promovido. Resultados de PR/CI/merge devem ser comunicados após execução real.
