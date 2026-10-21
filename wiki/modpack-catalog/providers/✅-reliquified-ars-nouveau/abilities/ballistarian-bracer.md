# Spectral Volley — Ballistarian Bracer

- **Provider:** Reliquified Ars Nouveau (`reliquified_ars_nouveau`), versão física `0.8.1`.
- **Status:** ✅ `COUNTED_EXACT` para identidade estática de uma habilidade de relíquia; runtime/Survival ⚠️.
- **Item registrado:** `reliquified_ars_nouveau:ballistarian_bracer`.
- **Classe física:** `it.hurts.shatterbyte.reliquified_ars_nouveau.items.bracelet.BallistarianBracerItem`.
- **ID primário `AbilityTemplate.builder`:** `ballistary`.
- **Nome da habilidade:** Spectral Volley (localização source-pinned 0.8.1).
- **Contribuição semântica:** uma raiz provider-native já contabilizada; **+0** no checkpoint desta auditoria.

## Evidência física

[Java21 #38461801129](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38461801129): o JAR físico SHA-1 `4be1f4b0fd7fbec6618596e2e7c3705db88a7579` inclui o item, a classe e exatamente uma chamada compilada a `AbilityTemplate.builder` com o ID primário acima. Ver [dossiê 19/19](../EXACT-BINARY-RELIC-ABILITIES-0.8.1.md) e [catálogo source-pinned](../README.md).

## Causalidade, exclusões e gates

O item é contêiner da habilidade; rank, modificadores, sub-habilidades, partículas, projéteis, efeitos e eventos de progressão não contam como raízes extras sem nova prova independente. Quando a ação usa casting ou glyphs de Ars Nouveau, sua execução e recursos permanecem sob a autoridade do Ars/provider. Não duplicar mana/cooldowns, dano ou recompensas no Black Arcana.

A auditoria **não** certifica valores de custo/cooldown, algoritmo de combate, aquisição em Survival, loot efetivo, persistência, compatibilidade Relics/Ars ou servidor dedicado. Qualquer adapter Black Arcana requer contrato real e QA próprio.

---

## Engenharia causal — source 0.8.1

**Root:** `AbilityTemplate.builder("ballistary")`. **Fonte:** [`bracelet/BallistarianBracerItem.java`](https://github.com/Octo-Studios/reliquified_ars_nouveau/blob/125e1e3a723d8bc7050026e0670f8ac49535c8bc/src/main/java/it/hurts/shatterbyte/reliquified_ars_nouveau/items/bracelet/BallistarianBracerItem.java), commit `125e1e3a723d8bc7050026e0670f8ac49535c8bc` (declarado 0.8.1). A identidade foi auditada no JAR físico, mas **equivalência do corpo de métodos compilado ↔ source não foi demonstrada**.

- `EntityJoinLevelEvent` trata `Projectile` com owner `ServerPlayer`; a tag persistente `ran_ballistarian_processed` impede processar duas vezes o mesmo projétil.
- `MathUtils.multicast(random, clamp(trigger_chance,0,1), max(1,round(projectile_count)))` calcula quantidade de `BallistarianPhantomProjectileEntity`. Acumula dano total `Σ(count * projectile_damage)` e grava `ran_ballistarian_count` e `ran_ballistarian_total_damage` no projétil principal.
- Em `LivingDamageEvent.Post`, consome as duas tags, usa `try/finally` com `ran_ballistarian_duplicating` e tenta `target.hurt` de dano adicional. Modificadores: `absorbing_kills` (absorção se target morreu), `multicast_duplication` (vizinhos vivos não aliados até limite sorteado) e `paralyzing_shots` (efeito `STUN`). Duplicação pode zerar `invulnerableTime` do vizinho.
- **Perks:** não contar o impacto do projétil, ataque bônus e spawn de phantom como três spells; testes de imunidade, PvP, dano aplicado e custo seguem pendentes.

**Estado:** 🟡 comportamento localizado no source; ⚠️ configuração, método binário, Survival e multiplayer pendentes; ⛔ hooks seguros de perks e Mastery não homologados. Sem segunda execução, duplicação de mana ou novas identidades mágicas. Relics/Ars/addon são donos dos recursos e do comportamento; RPG Skill Tree é somente progression provider.

[Matriz 0.8.1](../PERK-ENGINEERING-MATRIX-0.8.1.md).
