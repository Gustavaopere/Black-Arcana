# Taxing Bellow 1.0.10 — prova reproduzível do Conch e da reputação

**Escopo certificado:** `alexscaves:taxing_bellow`, `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`, sem mutação. Hook mutador `NOT_VERIFIED`, QA física `NOT_TESTED`. [Ficha individual](enchantments/taxing-bellow.md) e [manifesto binário](EXACT-TAXING-BELLOW-STATIC-1.0.10.json).

## Artefato e vinculação à modlist

JAR físico publisher `alexscaves-1.0.10-neoforge+1.21.1.jar` (CurseForge `8856293`), 75.279.314 bytes; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Minecraft 1.21.1 / NeoForge / Java 21, presença na linha #019 da modlist do RPG Skill Tree. Nenhum código-fonte 1.1.1 foi elevado a autoridade 1.0.10.

**Recursos publisher:**

| Recurso | SHA-256 / valor |
|---|---|
| `data/alexscaves/enchantment/taxing_bellow.json` | `275b7ef42207724ae8ee2048097d3f16dbdfc60796f06a98eb77356ddb744df1` · 443 bytes |
| `data/alexscaves/tags/item/enchantable/magic_conch.json` | `730151144ab45cb149cf6adfdf5d9cfb69b450238ff126f7f1ac33a0406d2cd8` |
| `assets/alexscaves/lang/en_us.json` | `a2a3fab567b07ec10b3d946d4e4ce3e65417b6f9348bd49478d8a253a4232d1f` |

A definição possui `max_level=1`, `weight=2`, `anvil_cost=4`, custo mínimo base 1/incremento 19, máximo base 41/incremento 10, slot mainhand e `exclusive_set=[minecraft:unbreaking,minecraft:mending]`. A tag física inclui `alexscaves:magic_conch`. Censo completo de **1.555 classfiles** contém referência direta a `TAXING_BELLOW` apenas em `ACEnchantmentRegistry.class` e `MagicConchItem.class`; isto não descarta reflexão/mixins/transformações externas.

## Métodos e hashes do JAR exato

Prefixo de classe: `com/github/alexmodguy/alexscaves/`.

| Classe | SHA-256 do classfile |
|---|---|
| `server/item/MagicConchItem.class` | `4cfad894baabc9540b09de8df8eaf263952292e9c7cc06f86d288cecfb833ce2` |
| `server/entity/living/DeepOneBaseEntity.class` | `185df23946292e403300849222018480a3cc1397ee6d6d60e0b28abc40e97470` |
| `server/level/storage/ACWorldData.class` | `ddb140795a4a38e077575effb858c2f7664780f11046475335ca132200b031f5` |
| `server/enchantment/ACEnchantmentRegistry.class` | `60006fab1b3b29f5f93c8365416815a12770cf8877a059298cb4ee82f7a92f32` |

| Método e assinatura JVM | Instruções | SHA-256 do método parseado |
|---|---:|---|
| `MagicConchItem.releaseUsing(ItemStack,Level,LivingEntity,int)V` | 211 | `f8a7f97d8a15e513a06cf81e0c4cb2fde5fad9a100b1a3187a9ab4f4f9dd7894` |
| `MagicConchItem.summonDeepOne(EntityType,LivingEntity,int)DeepOneBaseEntity` | 134 | `c355ab39634de12bb46dd45a2286aca99dcacd1843c98c80d4fe6723fbdf6d25` |
| `DeepOneBaseEntity.addReputation(UUID,int)V` | 48 | `e3d32551f26215b7656be6eceefc58def1bbf56e954ef6205165959023079054` |
| `DeepOneBaseEntity.getReputationOf(UUID)I` | 18 | `ea5cf310a6760f138c4faca6f9839426a5b2076ec9d5b1e97c2dd7a2f98efa4a` |
| `DeepOneBaseEntity.setReputationOf(UUID,int)V` | 15 | `7895787ccf834312f55df189ab36f76e62b9bf6a8966755aae5fb1875ce5a35b` |
| `ACWorldData.getDeepOneReputation(UUID)I` | 13 | `d9f33377e874c412a7e9a751e8c743643800a7fb7d140053649e820b3a23923d` |
| `ACWorldData.setDeepOneReputation(UUID,int)V` | 11 | `17caf9eb177f1a8d53077d6715a562b0e11d125bc0e33e3e30e84520e608e4c0` |

A sonda também sela `use`, `getUseDuration`, `setSummonedBy`, `copyTarget` e NBT `addAdditionalSaveData/readAdditionalSaveData` de DeepOne, total **13 métodos selecionados**. Todos os method descriptors reais, digests e janelas bounded ficam no manifesto.

## Condições, CFG e limites

**Magic Conch release:** `@20` som (antes do guard); `@26–32` carga `getUseDuration−timeLeft`; `@39/41` exige >25 ticks para prosseguir. `TAXING_BELLOW@45` e `ACCompat.enchantLevel@48`; `ifle74@51` seleciona desgaste normal quando nível não positivo; `getDamageValue@57` → `iconst_1/isub@60–61` → `Math.min(0,...)@62` → `ItemStack.setDamageValue@65` para positivo, marca flag no local 6 `@68–69` e salta para `@80`. O outro ramo `@74–77` solicita desgaste `1` via helper. `LASTING_MORALE@90` e `@93/96/101` geram `1200+400×L`. `Level.isClientSide/ifne418@104–107` separa invocação/reputação do bloco final de estatística/cooldown.

**Penalidade única após laços:** `iload 6/ifeq418@397–399`, `aload 10/ifnull418@402–404` e `user.getUUID@410`, literal `bipush -2@413`, `DeepOneBaseEntity.addReputation(UUID,int)@415`. Se os loops não retornarem um summon não nulo, o débito não é solicitado. `user instanceof Player@418–422` e `ACCompat.addCooldown@448` seguem após essa região; `Level.addFreshEntity` não garante aceitação pois seu retorno é descartado em `summonDeepOne@290–293`.

**Reputação e clamp:** `DeepOneBaseEntity.addReputation@2` lê valor antigo, soma o delta em `@8`, classifica `DeepOneReaction@9` e chama `setReputationOf@19`. Reações extras exigem alteração da categoria e jogador resolvido; podem produzir advancement/mensagem, sem QA física. `getReputationOf/setReputationOf` leem/escrevem via `ACWorldData` somente no servidor e quando world data existe. O getter de WorldData usa `Map.getOrDefault(UUID,0)@17`. O setter fornece limites **−100/100** a `Mth.clamp@6–10` e faz `Map.put@16`. Não há chamada explícita `setDirty` nesse método: persistência final após save/reload **não está comprovada**.

**Pontos importantes para QA:** `Math.min(0,0−1)` passa **−1** ao setter do ItemStack; não prova valor final de `DAMAGE`. Também não prova conservação da reputação ao carregar mundo, aceitação de summons, execução completa com `Charting Call`, cooldown se houver exceção, hooks, manipulação permitida de reputação nem deduplicação de Mastery. Quando `Charting Call` introduz um `nextInt(0)` no ramo nativo (níveis I–III), isso é risco estático e não crash observado.

## Reprodução (somente leitura)

```sh
python3 docs/qa/alexscaves_1010_taxing_bellow_static_probe_test.py -v
python3 docs/qa/alexscaves_1010_taxing_bellow_static_probe.py \
  --jar '/caminho/alexscaves-1.0.10-neoforge+1.21.1.jar' \
  --javap "$JAVA_HOME/bin/javap" \
  --seal 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-TAXING-BELLOW-STATIC-1.0.10.json'
python3 scripts/catalog/check_perk_ready_indexes.py
python3 scripts/catalog/generate_perk_ready_indexes.py --check
```

O workflow `alexscaves-1010-taxing-bellow-static.yml` usa Java 21 e baixa o artefato do publisher; verifica hash, recursos, classfiles, method digests, branch targets do custo e da reputação, clamp do WorldData e manifesto selado. O relatório contém apenas dados de interoperabilidade, não JAR nem implementação copiada.

**Conclusão delimitada:** este enchantment tem contrato técnico **estático individual**; toda mutação por perk e QA física permanece `NOT_VERIFIED`/`NOT_TESTED`, `NO_MUTATION`; o universo global de mod e as integrações runtime não foram encerrados.
