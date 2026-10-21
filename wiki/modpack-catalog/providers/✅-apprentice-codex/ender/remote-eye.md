# Remote Eye

- **Provider:** Apprentice's Codex
- **Mod ID:** `apprenticecodex`
- **Installed JAR:** `apprentice_codex-0.9.7.1+mc1.21.1.jar`
- **Registry ID:** `apprenticecodex:remote_eye`
- **Iron's school:** Ender
- **Levels:** 1–3
- **Minimum rarity:** Epic
- **Cast type:** Instant
- **Cooldown:** 30 s
- **Resource:** Iron's mana
- **Source pin:** `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`

## Exact source coefficients

- `baseSpellPower = 100`
- `spellPowerPerLevel = 30`
- `baseManaCost = 80`
- `manaCostPerLevel = 25`
- `castTime = 0`

Duration:

`40 + round(40 * spellPower / 100)` ticks.

At default unmodified spell power this is approximately **80 / 92 / 104 ticks** for levels 1–3, but actual duration responds to spell-power modifiers.

Persisted-state repair uses an explicit maximum active repair window of `20 * 30 = 600 ticks` for old state lacking active-duration metadata.

## Server-owned observation state

The server rejects dimensions not allowed by the provider config, then stores:

- active-until game time;
- active duration;
- anchor XYZ;
- anchor yaw/pitch.

For a `ServerPlayer`, that state is synchronized to the client. The provider guide describes a detached/free-look observation mode in which the physical caster remains vulnerable and the view cannot simply pass through walls.

The gameplay observation/camera experience is therefore a provider-owned remote-view system, not a Black Arcana `Borrowed Sight` session.

## Divination overlap

This is a direct semantic overlap with Black Arcana Familiars & Divination. A Black Arcana remote-observation spell needs a demonstrable distinction—such as target ownership/privacy semantics or a different noetic contract—rather than reproducing Remote Eye with different VFX.

Black Arcana must not consume client camera state as provider authority. Any future cross-provider progression integration would require a server-observable causal boundary.

## Acquisition

Registered through Iron's spell registry. Exact survival acquisition remains provider-wide audit work.

## Deduplication

Occupies the **temporary detached remote-eye/free-look observation** niche.

## Confidence

`SOURCE-PINNED SPELL / EXACT SERVER STATE+DURATION FORMULA+DIMENSION GATE / CLIENT CAMERA COLLISION+INPUT UX+FULL-PACK QA PENDING`

## Localizadores para Codex — source exato

- **Registry + identidade:** `apprenticecodex:remote_eye` → `SpellRegistry.reg("remote_eye", RemoteEye::new)` no source 0.9.7.1.
- **Classe Java verificável:** [`jp.aquafactory.apprenticecodex.spell.remoteeye.RemoteEye`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/remoteeye/RemoteEye.java) (`hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`).
- **Leitura para perks:** consultar os coeficientes, fórmulas, condições de alvo e relações causa→efeito já registrados nesta ficha; rastrear métodos da classe e classes auxiliares antes de afirmar que qualquer área, alvo, número de entidades ou duração é modificável externamente.
- **Contrato:** host Iron's controla casting e mana; Apprentice's Codex controla o efeito; RPG Skill Tree controla perks/Mastery/gates; Black Arcana só integra via boundary real, sem segunda liquidação de custo/efeito. Sem hook comprovado para a mutação: **⚠️ condicionado/fail-closed**.
- **Pendências:** classificar hooks com signature e validar entidades/efeitos secundários, QA no JAR físico e Survival. O link é prova de localização estática, não de interoperabilidade implementada.

---

## Engenharia causal aprofundada — 0.9.7.1 (audit de source, 2026-10-13)

**Prova rastreável:** [`remoteeye/RemoteEye.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/remoteeye/RemoteEye.java) · [`remoteeye/RemoteEyeBodyControlEvent.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/remoteeye/RemoteEyeBodyControlEvent.java) · [`remoteeye/RemoteEyeSync.java`](https://github.com/hexqua/apprentice_codex/blob/305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e/src/main/java/jp/aquafactory/apprenticecodex/spell/remoteeye/RemoteEyeSync.java). Source `hexqua/apprentice_codex@305ea6aef7bb9642a9d1fc2b9042f3dfb2ce5b2e`, mod ID `apprenticecodex`. Identidade e versão do JAR são da modlist física; **não há prova de equivalência de cada corpo de método com o JAR compilado**.

### Sessão de observação e imobilização do corpo

- **Estado server-owned:** `RemoteEye.onCast` inicia sessão com game time de expiração, duração e anchor de coordenadas/rotação, sincronizando `RemoteEyeState`. O limite de recuperação para save antigo sem duração é `PERSISTED_STATE_REPAIR_MAX_ACTIVE_TICKS=600`; trata-se de **sanitização de tempos persistidos**, não extensão normal da duração da spell.
- **Tick da sessão:** `RemoteEyeBodyControlEvent.onPlayerTick(PlayerTickEvent.Post)` recupera `REMOTE_EYE_STATE`; primeiro chama `PersistentGameTimeSanitizer.repairPersistedFutureUntil` com duração registrada ou limite de reparo. Se expirou, perdeu vida ou passou a ser passageiro, `deactivate` limpa o estado e sincroniza.
- **Imobilização:** enquanto ativa, `anchorBody` reposiciona player no XYZ original, restaura yaw/pitch de cabeça e corpo, zera `Vec3` de movimento e `fallDistance`. A rotina executa com estado compartilhado por lados, mas o cliente apenas apresenta visualização; **não** é autoridade de deslocamento remoto.
- **Limpeza:** `LivingDeathEvent`, login, respawn e mudança de dimensão têm handlers de sincronização/desativação. O corpo real permanece no mundo e pode ser alvo de dano; a câmera não representa um teleport.
- **Boundary:** não reconstruir posição do player a partir da câmera nem gerar perks por movimento do olho. Testar colisão, inputs, logout, restauração de save, cross-dimension, dano e privacidade no servidor real antes de integrar um sistema BA de Borrowed Sight.

### Perfil para integração de perks e QA

- **A / stats e rank:** ler apenas os atributos declarados no host Iron's e os state objects que o addon expõe; stat dinâmica e duração efetiva exigem ambiente, item e configuração. Nenhuma alteração de mana/cooldown do Iron's por Black Arcana.
- **B / causalidade:** uma ação primária `apprenticecodex:remote_eye`; filhos, efeitos retardados, limpeza ou automação pertencem à raiz do provider. Sem `cast UUID`/contrato de retorno validado, o BA e RPG não devem inferir reward do resultado observado.
- **C/D / segurança:** ⛔ adapter de Mastery/perks enquanto inexistir contrato seguro. ⚠️ QA: servidor real, replay, NBT/relog, cross-dimension, compat opcional, ordenação e anti-double-processing. Não houve GameTest do provider nesta auditoria.
- **Clean-room:** análise factual e documentação próprias; código upstream não foi incorporado.

[Matriz causal desta etapa](../PERK-ENGINEERING-MATRIX-HIGH-RISK-0.9.7.1.md).
