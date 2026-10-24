# Fire’s Ender Expansion — onze fichas com parâmetros e consumidores, 24/10/2026

Base Black Arcana `de3ed3ddbc696597bae5e6dd993e04dbef99aa05` (#878); RPG/modlist `ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc`, Enshrouded `a41dbb51aacb94b7b5db6517f1514b0b7aee3e83`, Factory `518278ae9c0d264a537cc1bc6ee4974e01270fdf`.

## Entrega e proveniência

[Onze fichas existentes e dossiê comum](../../wiki/modpack-catalog/providers/✅-fires-ender-expansion/SPELL-PERK-BOUNDARIES-2.4.1.md) aprofundados com defaults/fórmulas/unidades, classes/métodos consumidores, alvo/área, dano/tipo, projétil/hitbox, tempos/custos/recasts, estados, mundo, persistência e limites de alteração por perks. README/auditoria e barras atualizados. **11/11 mede esse recorte documental, +0 identidades/+0 strict**; não homologa todo conteúdo do provider nem onze rotas Survival ou adapters.

Source oficial `FireOfPower/firesenderexpansion-1.21.1@5e4067e8112316f55c9f249530ba1917a7bf6643`, versão declarada2.4.1/MC1.21.1, build NeoForge21.1.215/Iron’s3.15.6/Ace’s1.2.6.1-1.21.1 (dependência efetiva file8079666). Pack registrado NeoForge21.1.250/Iron’s3.16.3/Ace’s1.2.7.2; dev BA NeoForge21.1.248. Host consultado Iron’s `e4056af90302d37eb1739f5ff05020b020e6e252`, Ace’s `a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`. Os métodos source não foram equiparados integralmente aos JARs. Metadata **All Rights Reserved** difere da licença do template; somente fatos/paráfrases/referências, sem importar corpos upstream ou assets.

Publisher CurseForge [8167304](https://www.curseforge.com/minecraft/mc-mods/fires-ender-expansion/files/8167304), baixado em23/10 e revalidado em24/10: **2442013bytes**, SHA-1 `da87a4a0c926dd75236766584cddbae69c6aeff7`, SHA-256 `6a02f54a5ffea0443faf31366649be5ea5cb648f0f2cf55b557b198d93b10519`. Coincide com ledger físico histórico #281 de `firesenderexpansion-2.4.1.jar`. O perfil instalado original não está nesta sessão; não se declarou nova medição dele. Onze registrations source, onze classes Spell no publisher e seus nomes/IDs/referências no registrar binário foram reconciliados; isso não prova equivalência de todos os corpos ou execução em jogo.

`AbstractDomainEntity.java` tem blob `1c830383020f373cc7304703a9fbeb307b70eede` tanto no Ace antigo `0f6110925de4c4c0422095d9ee9ca8ce4009e438` quanto no pin1.2.7.2 consultado. Igualdade limitada a esse arquivo, sem inferir igualdade de JAR/ABI ou da composição inteira.

## Achados úteis para perks

- Arcane Slice aplica o fator de mana apenas ao alvo ServerPlayer com maxMana>0; partículas não são novos hits. Aspect usa incoming antes de HP e gera bullet vanilla, cuja baseline está abaixo. Adaptation tem cache global com reload ausente/parcial/stale, sem setter por jogador.
- Rod tem cadência de tiro distinta da liquidação do canal. Gate também usa nível armazenado do callback; mudar o nível no anúncio de cast não demonstra mudar essa emissão. Portais Gate de delay21 ainda emitem antes do discard; delays≥22 podem perder a emissão normal.
- Binary Stars não executa o slam/AOE comentado e seu contato não tem ledger ativo que garanta um único hit. Nova Burn usa fonte plain própria, sem herdar automaticamente o settlement do helper Iron’s.
- Fury lê a arma uma vez; push é separado do dano. O Earthquake filho com duration20/reapplicationDelay25 não garante seu callback no lifecycle normal consultado. Stride distingue anúncio manual de teleporte, helper e remoção cancelável; retorno em toda expiração não foi comprovado.
- Cage separa dimensões herdadas, radius, tracking e duration sincronizada/local. Hollow Crystal usa contato5³ e sweep terminal35³ com ledger de tentativas; o expiry herdado>300 pode encerrar antes de>600/max1200 locais. AntiMagic não demonstra autorização exclusiva do owner.
- Void separa domínio herdado, sucção/transport, dimensão de sure-hit, mapas de origem/retorno e fonte de dano da própria vítima. O argumento20 de region ticket não demonstra ticket level20. Fallbacks/guardas/rotations e player Survival exigem os casos de QA da ficha.

São conclusões de causalidade source e provas binárias estreitas; não são bugs reproduzidos no modpack nem autorização para substituir efeitos, recursos, ownership ou cleanup do provider.

## Baseline vanilla do Aspect

Prova estática restrita ao Minecraft1.21.1 oficial, consultada nesta sessão sem copiar implementação. O [manifesto imutável](https://piston-meta.mojang.com/v1/packages/1757c8b1fbfc6b638504e1f6cceb05893f7389d5/1.21.1.json) fornece URLs/hash dos artefatos; a reprodução usa JDK21 `javap -c -p`, os mappings oficiais e leitura dos JSON de data no JAR.

- [Client oficial](https://piston-data.mojang.com/v1/objects/30c73b1c5da787909b2f73340419fdf13b9def88/client.jar): **26836906bytes**, SHA-1 `30c73b1c5da787909b2f73340419fdf13b9def88`; [client mappings](https://piston-data.mojang.com/v1/objects/2244b6f072256667bcd9a73df124d6c58de77992/client.txt) SHA-1 `2244b6f072256667bcd9a73df124d6c58de77992`. [Server outer](https://piston-data.mojang.com/v1/objects/59353fb40c36d304f2035d51e7d6e6baa98dc05c/server.jar) SHA-1 `59353fb40c36d304f2035d51e7d6e6baa98dc05c`; server interno extraído conforme versions.list SHA-256 `c301de10f575027d13eac18c7f34409d60648cf56a35d566aa1f530ff617840a`.
- `ShulkerBullet→cns`: classfile idêntico nos client/server verificados, SHA-256 `9645c3441cf8997c61589adbc27c5342d46a8ce78c241229e24bcfc28de797c6`. Mappings nomeiam `EntityType.SHULKER_BULLET→bsx.aL`, `DamageSources#mobProjectile→brl.a(Entity,LivingEntity)`, `DamageTypes.MOB_PROJECTILE→brn.F`, `MobEffects.LEVITATION→bsb.y`.
- O overload `cns(Level,LivingEntity,Entity,Axis)` seleciona `bsx.aL` no offset1, delega ao constructor e grava owner. Registro estático de bsx define largura/altura **0.3125/0.3125** nos offsets4011/4014. Esse caminho não escolhe o registro alternativo FEE1×1.
- No `onHitEntity` mapeado, offsets32–50 criam fonte mobProjectile e tentam **4HP** via hurt. Só no ramo de retorno true é tentado o pós-ataque de enchantments, se ServerLevel; nesse ramo, se a vítima é Living, também tenta Levitation200ticks. O constructor de effect com dois argumentos delega amplifier0; o resultado de addEffect não é consumido. `mob_projectile.json` define o tipo plain vanilla e a tag is_projectile o inclui; não é SpellDamageSource ou fórmula de spellPower.

Esses fatos fecham a **baseline vanilla binária**, não o resultado físico da composição NeoForge21.1.250/FEE/pack. O patch de impacto, demais patches/listeners, mitigação, enchantments, atribuição efetiva, trajetória, lifetime, persistência e sync continuam sujeitos aos seus próprios contratos e QA. Em particular, a fonte plain não satisfaz sozinha o predicado SpellDamageSource do proc Aspect, mas isso não exclui fontes extras produzidas por terceiros.

## Validação

- Onze fichas, onze registrations source e onze classes Spell publisher com IDs reais e parâmetros/consumers por eixo.
- Nas onze fichas e no dossiê comum: **321 referências pinadas**, **107 arquivos source distintos**, **46 links locais** e **22 tabelas** conferidos. Referências não são321 hooks únicos; a prova vanilla estática foi verificada separadamente pelos hashes/mappings/offsets acima.
- Nos **18 Markdown** alterados, incluindo este relatório: **498 links locais** resolvidos e **25 tabelas** com colunas válidas; sem referências indefinidas. `git diff --check` limpo.
- Revisão independente das onze fichas e do dossiê comum/metadata concluída sem bloqueantes de conteúdo; três limites de permalinks corrigidos antes da conferência final.
- `PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/global_magic_catalog_test.py`: **52/52 PASS**.
- `PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/catalog_physical_ledger_test.py`: **5/5 PASS**.
- `PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/magic_pendency_tracker_test.py`: **26/26 PASS**.
- Painel JSON/Markdown: **11/11 documental**, 164 providers únicos, total global aberto/null, mínimos1856/1854 e campanha38/39 preservados, `runtime_acceptance=NOT_INFERRED`.

Nenhum runtime, perk, adapter, dependência ou lockfile foi alterado. Config/datapacks implantados, equivalência de métodos/JAR/hosts, Survival/cliente, multiplayer/PvP/claims, chunks/dimensões, budgets, cleanup/reload/logout/restart, persistência e sync continuam **PENDING**. CI/headless BA sem FEE não homologa estes spells; nenhum Stage promovido. Resultados de PR/CI/merge devem ser comunicados após execução real.
