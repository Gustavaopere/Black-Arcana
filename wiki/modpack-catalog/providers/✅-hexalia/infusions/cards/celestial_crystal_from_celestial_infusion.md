# Hexalia 1.3.7 — Celestial Infusion `hexalia:celestial_crystal_from_celestial_infusion`

Status: **✅ CATALOGADO / `COUNTED_SOURCE_PINNED`** com recipe ID e contrato source-pinned; **⚠️ funcionamento físico/configuração pendentes**.

## Identidade e transformação

- **Recipe ID:** `hexalia:celestial_crystal_from_celestial_infusion`, do tipo `hexalia:celestial_infusion` (não um glyph ou spell registry ID).
- **Entrada no Ritual Brazier:** `minecraft:amethyst_shard`.
- **Saída substitutiva (1x):** `hexalia:celestial_crystal`.
- **Ordinal editorial:** 2/6; não representa ordem de execução.
- **Provider owner:** Hexalia, mod ID `hexalia`, físico `hexalia-neoforge-1.3.7.jar`, SHA-1 `ca90edf1664cf6d44fe7e5318c71069050499c7e` (Minecraft 1.21.1 / NeoForge).
- **Fonte:** release-correlated source pin `AstralyaStudios/Hexalia@98c22aaf70e069c616fed5ad2dc56d2b37fcd283`; posterior manutenção same-version não é projetada para trás. **Não há prova byte-a-byte do build do source contra o JAR físico.**
- **Estado semântico:** `COUNTED_SOURCE_PINNED`, objeto já presente no ledger de **29** ações provider-owned. A ficha acrescenta **+0 novas identidades**.

## Contrato ambiental e transacional

A infusão se inicia com input não vazio no **Ritual Brazier**, `hexalia:hex_focus` em main/offhand, **céu aberto** acima e pelo menos **três** `Celestial Bloom` ou `Withered Celestial Bloom` em raio horizontal **3** no mesmo nível Y. Deve existir receita correspondente. Diferente do Nature's Ritual, **não há exigência `SALTED=true`** para iniciar esta infusão na auditoria 1.3.7.

A fase de channel dura **120 ticks (6 s)**. A cada tick servidor valida input, pending output, luz solar e permanência dos três bloomed positions capturados. Falha cancela o canal e limpa estado pendente. No sucesso, substitui input por **uma cópia** do resultado e degrada cada um dos três blooms capturados por um estágio: `Celestial Bloom → Withered Celestial Bloom → Dead Bush`. São **três recursos ambientais**, não um novo world mutation Black Arcana.

As seis receitas/source e classes do subsistema são blob-idênticas à linha anterior 1.3.6 na auditoria de release, mas isso **não** comprova igualdade byte-a-byte do JAR distribuído. Moonweave produzido por quatro destas receitas participa do bônus provider-owned de **1,5x duração** dos oito brews padrão quando o conjunto completo está vestido; não replicar bônus de duração no Black Arcana.

## Authority e pendências

Hexalia é dono de channel, Source/ingredientes próprios, consumo ambiental, cancelamento, persistência e output. Black Arcana não executa channel paralelo, não re-degrada blooms e não credita output/brew buff novamente. Sem API/hook validado, integração **⛔ fail-closed**. Sky checks efetivos em biomas/dimensões, config/datapacks, casos de chunk unload/relogin e resultado físico em Survival continuam **⚠️ NÃO VERIFICADOS**.

**Fontes:** [matriz de seis infusões e lifecycle](../../infusions/CELESTIAL-INFUSION-CATALOG.md) · [provider](../../README.md). Clean-room: metadados factuais do catálogo próprio, sem código/assets/recipe JSON upstream.
