# Second Wave 1.0.10 — contrato técnico estático individual (JAR publisher)

**Escopo:** `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`. A [ficha individual](enchantments/second-wave.md) documenta identidade, condição de ativação, dois pedidos de onda por iteração, distribuição, duração solicitada, espera, targeting nativo, custo e fronteiras de integração. Não certifica hook, QA física, PvP, claims, spawn aceito ou dano aceito.

## Autoridade e identidade

Modlist `Gustavaopere/neoforge-rpg-skilltree`: `alexscaves-1.0.10-neoforge+1.21.1.jar`, Minecraft 1.21.1/NeoForge/Java 21. Artefato publisher de 75.279.314 bytes; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Enchantment `alexscaves:second_wave`; JSON de 413 bytes SHA-256 `68d843242cc39b33eb952142b168fa8e72a2695bfa8adea6de3e4bba6febb97c`. Peso2, máximoI, mínimos base1 +12/nível, máximos base41 +10/nível, anvil4, mainhand, tag Ortholance, exclusividade declarada de Tsunami. A tradução `en_us` foi conferida no JAR e só é parafraseada na ficha.

## Grafo e prova do consumer

A [sonda](../../../../docs/qa/alexscaves_1010_second_wave_probe.py) inspeciona **1.555** classfiles: apenas `ACEnchantmentRegistry.class` e `OrtholanceItem.class` possuem a referência binária `SECOND_WAVE`; esse censo cobre o token, não calls dinâmicas por outros caminhos. O método `OrtholanceItem.releaseUsing` tem **435 instruções**, digest `00705e7177cb6fe2914531158bd978b64d497ca4c8262f8e7634c1b4ec9ef7ae`, identificado com SHA de classfile e múltiplas janelas auditadas independentemente pelo [manifesto Flinging](EXACT-FLINGING-1.0.10.json). O [manifesto individual de descoberta selado](EXACT-SECOND-WAVE-DISCOVERY-1.0.10.json) contém somente os *pivôs de interoperabilidade* necessários à prova (sem exportar implementação completa de terceiro). Os [testes semânticos](../../../../docs/qa/alexscaves_1010_second_wave_cards_test.py) impedem modificação silenciosa dos pivôs, falsos counts e promoção de estado runtime.

Fluxo verificável: carga `C=clamp(useDuration-remainingUseTicks,0,60)`; `C<=0` retorna; desgaste único solicitado antes do ramo `hurtAndBreakUsedHand(stack,1,usuário)`. `SECOND_WAVE` exige `level>0` (guard `ifle @466`). O laço tem `N=max(1,B-1)`, em que `B` vem do contador nativo primário (normalmente `C/5` inteiro; o ramo Tsunami pode forçar outro valor, apesar da exclusividade de dados). Há dois construtores `WaveEntity(Level,LivingEntity)` por iteração (offsets 535/620) e exatamente dois pedidos `addFreshEntity` (@610/695) com retorno descartado (@613/698). **Quantidade de pedidos:** `2N`. Isso não implica aceitação de spawn.

Cada iteração define `f=i/N`, `T=3+trunc((1-f)×3)` e `setLifespan(T)` em cada par, geometria horizontal derivada da posição/impulso nativos e yaw espelhado `θ±(60−15i)`. As duas ondas recebem `setWaitingTicks(8)`. A geometria, a espera e os pedidos de spawn são parâmetros nativos, não cooldown, distância máxima de cast ou hit garantido.

O consumer `WaveEntity` já possui [manifesto estático separado](EXACT-SEA-SWING-STATIC-1.0.10.json) **dos mesmos hashes de classfile/JAR**: construtor captura owner/UUID; `tick` guarda `attackEntities` no servidor; seleção de `LivingEntity` usa AABB própria inflada `0,5D`, `mobProjectile`, filtros de owner/aliados/Deep One e pedidos de dano/knockback não condicionados à aceitação de `hurt`; NBT próprio grava `Owner` e `Lifespan`, **não** `WAITING_TICKS`. A ficha registra implicações de reload e Mastery sem pressupor autorização mutadora.

## Replicação e limites

```sh
python3 docs/qa/alexscaves_1010_second_wave_probe.py \
  --jar /caminho/para/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --javap javap \
  --seal 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-SECOND-WAVE-DISCOVERY-1.0.10.json'
python3 docs/qa/alexscaves_1010_second_wave_cards_test.py -v
python3 scripts/catalog/check_perk_ready_indexes.py
python3 scripts/catalog/generate_perk_ready_indexes.py --check
```

**Estados independentes:** contrato estático concluído dentro da fronteira delimitada; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. A certificação não cobre execução de proteção de mundo, aceitação de spawn/hurt, alterações de datapack, redes, travessia de chunks, viabilidade de alterar propriedades, implementação de perk, Stage ou fechamento de todo Alex's Caves. A fonte adjacente pública 1.1.1 não fornece os parâmetros acima.
