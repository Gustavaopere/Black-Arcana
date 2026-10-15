# Eidolon: Repraised 0.5.0.2 — historical pre-proof checklist

**Static data package identity gate now closed:** [Java21 #38669010587](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38669010587) verified 18/18 normal chants, 24/24 ritual recipes and 4/4 dependent conversions on installed SHA-matched 0.5.0.2. [Exact dossier](../../wiki/modpack-catalog/providers/✅-eidolon-repraised/EXACT-PACKAGED-CHANT-RITUAL-RECIPES-0.5.0.2.md). Pre-proof SOURCE-PINNED statements below are historical only. Compiled Spells.init and loaded RecipeManager/Survival remain unproven; Stage06.05 🟡, Stage09 PENDING.


**🟡 Auditoria física iniciada; 42 IDs ainda SOURCE-PINNED. Não promover até CI real PASS.**

A modlist atual do sibling `neoforge-rpg-skilltree@9e6436edb0049a8dcc4e47165db0f6850e5efa68`, posição **#246**, fixa `eidolon_repraised-1.21.1-0.5.0.2.jar`, mod ID `eidolon_repraised`, SHA-1 **`1f05ffd2f9fa672dc2ecff3c32de092cdbcde989`**. Publisher oficial CurseForge project 870250, file **8064602**, release 1.21.1 NeoForge de 09/05/2026; Modrinth projeto `eWX2m1eM`, version ID `e82la8yu`. 0.5.0.4/0.5.0.5 são posteriores, mas **não instalados**. Fonte exata `Alexthw46/Eidolon-Repraised@696a47333e43970be7f697790eac0af76b6a04b8`.

Escopo: **18 official `eidolon_repraised:chant` recipes** (de 20 objetos de registry Spells: `undead_lure` sem efeito demonstrado, `basic_incense` dummy, ambos excluídos), **24 official ritual recipe identities** (10 generic, 11 summon, 2 brazier craft, 1 location) e **4 conversões dependentes de Dark/Holy Touch**, sem criar novas raízes independentes. Source-version JSON `data/eidolon_repraised/recipe/rituals/*.json` prova ID de receita, não registry carregado em jogo. O inventário de fonte original tem 42 ações semanticamente já contadas.

O script read-only valida o JAR **somente** se SHA-1 publicado corresponder ao sibling, metadata `modId`, presença de todas as identidades e tipos JSON no resource pack, exclusão de duplicatas/extra, signos ordenados por chant, identidade de summons, generic ritual IDs, health gates de brazier crafting e structure id. Publica apenas JSON. Nenhum byte de JAR será incorporado ao Black Arcana.

Fail-closed: não prova `Spells.init()` compilado (20 técnicos), serializers registrados, `RecipeManager` e datapacks customizados carregados, pesquisa/devotion, spell settlement ou consumo de health/ingredientes, spawn ownership, save/relog, client/server dedicado ou Survival. Black Arcana não assume mana/soul/devotion ou ritual runtime do Eidolon e sibling RPG Skill Tree só opera sob contrato real.

Até prova exata na branch+ledger+CI, campanha permanece **31/39 COUNTED_EXACT e 8/39 condicionais**, mínimos **1856 global / 1854 escopo**, Stage 06.05 🟡 e Stage09 PENDING.
