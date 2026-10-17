# Starbuncle — Ars Morph 2.0.0 / Identity2 ability

**Status: ✅ fonte por habilidade documentada · ⚠️ runtime e JAR físico pendentes · ⛔ perks sem contrato homologado.** Habilidade provider-native Identity2; NÃO constitui novo glifo, cast root Black Arcana ou forma independente de mana. `ars_morph-1.21.1-2.0.0.jar` SHA-1 físico documentado `68ff47cc58c0ffe9570bb907f65c2910311ed45f`; release-aligned source `Alexthw46/Ars-Morph@4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58`. Fatos abaixo **SOURCE_CAUSALITY**, não comparação de bytecode do JAR.

## Registro e valores do pack source-pinned

- **Identidade da habilidade/forma:** `ars_nouveau:starbuncle` (ID de Ars ou Ars Elemental/Identity2, **não** `ars_morph:*` spell).
- **Config de Identity2 no arquivo de atribuição:** `cooldown=100`, `use_duration=20`. São **inteiros brutos nos JSONs upstream**; a interpretação da unidade (ticks, segundos), consumo no cancelamento, skill gates e sincronização são do Identity2 **2.2.4**, ainda não medidos no runtime do pack.
- **Admissão:** Registro no `ModEntities.STARBUNCLE_TYPE`, wrapper por classe `Starbuncle`.

## Matriz causal para perks

| Eixo | Observação fixa em source | Status de adaptação |
|---|---|---|
| Entrada | `MorphBoundAbility.execute(Entity host)` exige que host seja `Player`, `IdentityApi.getCurrentMorph(player)` não-null e seja instância da classe esperada; exceptions em `use` são capturadas/logadas. | `⛔` Não transpor gate de morph ou duplicar os eventos do Identity2. |
| Efeito ativo | Em `use`, o jogador recebe `MobEffects.MOVEMENT_SPEED` por **3000 ticks**, amplifier **1**, ambient=false, showParticles=false, showIcon=false. Não faz resolver Ars adicional, não cria projétil e não altera AABB/target. | `⚠️` Runtime/settlement efetivo do host não foi testado. |
| Target / geometria | Self-buff, sem ataque/AOE/DamageSource nesta classe. | `⛔` Sem hook provado para alterar tipo de alvo, AOE, range, dano ou hitbox. |
| Passivo e tempo | Não há callback passivo próprio. | Efeito contínuo/callback passivo não corresponde a casts adicionais. |
| Causalidade | Tempo e amplifier do efeito são distintos de `cooldown`/`use_duration` do Identity2: não substituí-los por 3000 ticks no sistema de cooldown ou vice-versa. | Uma ativação Identity2 pode originar spell Ars, projétil, potion ou status: não criar segunda cobrança/cooldown/XP. |
| Bounds | Identidade depende da forma atual, servidor/cliente e dependências. Qualquer número de entities/hits ou change de bloqueio só é efetivo se o pipeline host o aceitar. | `⚠️` Testar cancelamento, persistência e resolução de efeito com versões atuais. |

## Evidência de código e arquivo de atribuição

- [java](https://github.com/Alexthw46/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/java/com/alexthw/ars_morph/identity/ability/StarbuncleAbility.java#L8-L17)
- [registry](https://github.com/Alexthw46/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/java/com/alexthw/ars_morph/identity/IdentityReg.java#L56-L67)
- [Identity2 `starbuncle.json`](https://github.com/Alexthw46/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/resources/data/ars_nouveau/identity2/identity_ability/starbuncle.json)
- [Base MorphBoundAbility](https://github.com/Alexthw46/Ars-Morph/blob/4a5a2c706fe5a316fc9ad03ac37a3ac1d1dc3c58/src/main/java/com/alexthw/ars_morph/identity/ability/MorphBoundAbility.java#L15-L62 ).

**QA requerido:** Validar efeito persistindo após troca de forma, reativação antes de expirar, client HUD oculto, logout, atributos da velocidade e evento de cooldown Identity2. Versões físicas usadas como alvo: Ars Nouveau 5.13.1, Identity2 2.2.4, Ars Elemental 0.7.10.1 quando presente, Gabou's Libs 1.8.7. **+0 novas raízes mágicas; 0 adapters implementados.**

## Semântica dos contadores Identity2 — verificação upstream 17/10/2026

**Evidência cruzada do código oficial `xGabou/Identity2`, ramo 1.21.1:** um snapshot anterior (27/05/2026, `847202234ae89a1596c6039b473566e34231c213`) e outro posterior (02/10/2026, `c634278ee637e8b94949a685072c94d67c9b3d4a`, versão fonte 2.2.4.1) mantêm `ModPackets.resolvePrimaryAbilityCooldown=max(0,cooldown+useduration)`; `EntityMixin.baseTick` decrementa contador 1/tick, e o servidor registra o cooldown **antes** de chamar `execute`. Para starbuncle: JSON `cooldown=100` + `use_duration=20` → **120 ticks** para o contador primário, não 100 ticks. Valor usado pelo secundário comum: 100 ticks (sujeito às exceções próprias de outras formas). Um efeito ou resolver Ars derivado pode durar mais/menos e deve ser medido separadamente.

[Protocolo completo de prova e links de código](../IDENTITY2-ABILITY-COOLDOWN-SOURCE-BRACKET-2.2.4.md). **⚠️ SOURCE_BRACKET**, sem prova de equivalência binária da versão instalada Identity2 2.2.4 ou de execução real; **⛔ nenhum hook de cooldown per-player homologado**.

