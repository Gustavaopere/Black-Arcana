# Crystal Chronicles 0.1.3-alpha — prova estática de registro binário

**✅ 1/1 magia `COUNTED_EXACT` exclusivamente para identidade estática do registro. ⚠️ Runtime, config e Survival não verificados.**

## Artefato e proveniência

- Snapshot físico certificado do sibling `de80b186357cad20ba5b81892a8682777e96e35a`, posição **#208**, JAR `crystal_chronicles-0.1.3-alpha.jar`, NeoForge 1.21.1, mod ID `crystal_chronicles`, SHA-1 `afdc32ab27661cd52160280dc4273d70a2d4a3d2`.
- [CurseForge file 8346590 / project 1153374](https://www.curseforge.com/minecraft/mc-mods/crystal-chronicles/files/8346590), publicado 2026-06-30, NeoForge 1.21.1.
- [Auditoria isolada, não-merge: run #38298343874](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38298343874), commit `57a4a696137b6922642ba1f88695efe9fba8be50` da branch `audit/crystal-chronicles-013-physical-registry-20261012`: job `binary-identity` **SUCCESS**.
- Download do publicador comparado por `sha1sum --check` ao SHA-1 físico: **match**; tamanho **2192223 bytes**. ZIP validado com `zipfile.testzip()`; `javap -c -p` com Java 21 analisou três classfiles, sem iniciar mod ou jogo. Nenhum JAR/bytecode/asset foi commitado.

## Cardinalidade do registro

| # | Owner | Classe concreta | Registry ID final | Evidência |
|---:|---|---|---|---|
| 1 | `crystal_chronicles` | `PrismaticPortalSpell` | `crystal_chronicles:prismatic_portal` | `EXACT_BINARY_STATIC` |

O log da CI registra:

- `SPELL_CLASS_CANDIDATES=['net/veroxuniverse/crystal_chronicles/spells/PrismaticPortalSpell.class']`
- `STATIC_BINARY_REGISTRATION_INVOCATIONS=1`
- `STATIC_BINARY_NAMESPACE=crystal_chronicles`
- `STATIC_BINARY_PATH=prismatic_portal`
- `BOOTSTRAP_TO_CCSPELLS=present`
- `RESULT=EXACT_REGISTRY_IDENTITY_ONLY`

`CCSpells` tem **uma** chamada `DeferredRegister.register(String,Supplier)` para a classe concreta, e a classe principal contém o bootstrap `CCSpells.register`. A classe de spell inclui o caminho literal `prismatic_portal`; `CrystalChronicles` contém namespace `crystal_chronicles`. Só uma classe top-level terminada em `Spell.class` foi encontrada no pacote próprio de spells. Sem outro spell root provider-owned demonstrado por este caminho.

O inventário estático não adiciona a escola Prismatic, portal Bismuth, dimensão Alpha, armaduras, equipamentos ou spells nativos Iron's embutidos em gear como novas magias. A contagem das classes e inscrições auditadas não substitui leitura dinâmica do registry em instância real.

## Limite da promoção

`COUNTED_SOURCE_PINNED → COUNTED_EXACT` **somente para ID e cardinalidade de registro estático** do arquivo físico publicado. A magia já estava contada: **+0 novas raízes**. Campanha original: **3/39** registries exatos, **36/39** pendentes. Mínimos semânticos **1851 global / 1849 escopo** preservados; denominador real ainda aberto.

O source pin `VeroxUniverse/CrystalChronicles-NeoForge@dff00d5ebbc5c726dad010f0d4cd40201ba4fc17` continua referência de assinatura e semântica; **não** foi demonstrada compilação source↔JAR reproduzível. A correspondência demonstrada é release publicada ↔ SHA-1 do JAR do snapshot físico.

## Pendências e autoridade

**⚠️ Não testado:** boot integral do pack, compatibilidade efetiva das dependências (incluindo Iron's 3.16.3), config e Scroll Forge ativos, aquisição em Survival, ativação e persistência do portal, dimensões, save/restart, multiplayer, proteção e custo aplicado na execução. O provider permanece Alpha/WIP.

Iron's controla casting, mana, cooldown, host registry, Scroll Forge e escola genérica. Crystal Chronicles controla Prismatic Portal, suporte Prismatic, portal Bismuth e Alpha. Black Arcana preserva autoridade do seu runtime e não duplica teleport, efeito ou settlement. RPG Skill Tree continua provider de progressão. **Stage 06.05 não foi promovida.**
