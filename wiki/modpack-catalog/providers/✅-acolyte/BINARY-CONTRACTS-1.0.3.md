# Acolyte 1.0.3 — contratos do artefato publisher

## Identidade e evidência reproduzível

| Campo | Valor confirmado |
|---|---|
| Artefato | `acolyte-1.0.3.jar`, mod ID `acolyte`, runtime `1.0.3` |
| CurseForge | projeto `1534642`, [file `8098233`](https://www.curseforge.com/minecraft/mc-mods/acolyte/files/8098233) |
| Modrinth | projeto `S1u5j9dB`, [versão `r0BSsxdc`](https://modrinth.com/mod/acolyte/version/r0BSsxdc), mesmo filename/tamanho/SHA-1 |
| Tamanho comprimido do JAR | **621837 bytes** |
| SHA-1 do publisher | `ad0abc821f3f8a6573ac19a50970fc1bc46b4275` |
| SHA-256 do publisher | `73fe745bbb0016fbc00af9ba14c0ecfe0a1d8a7d72a7892557739182b3486256` |
| Universo ZIP | **469 entradas: 359 arquivos e 110 diretórios** |
| Classes do provider | **93 classfiles: 66 externas e 27 internas/anônimas** |
| Fonte oficial | não identificada nas URLs oficiais de source consultadas; nenhuma revisão de Git inventada |

O [manifesto](ARTIFACT-CATALOG-MANIFEST-1.0.3.json) fixa caminho, bytes e SHA-256 de cada um dos 359 arquivos, sua disposição documental e os hashes das fichas. Os diretórios não são arquivos extras nem objetos de gameplay. O download é reproduzível pelo [CDN do publisher](https://edge.forgecdn.net/files/8098/233/acolyte-1.0.3.jar); o JAR e seus assets não são redistribuídos aqui.

As referências de código nas fichas usam classe, nome/descriptor do método e **PC**, o offset de uma instrução dentro daquele método. Uma verificação local pode usar Java 21:

```sh
javap -classpath acolyte-1.0.3.jar -p -c -s -constants net.raptorzizi.acolyte.entity.goals.SingleUseSpellGoal
```

Anotações e ligações `invokedynamic`/bootstrap exigem também `javap -v -p`. As fichas retêm resumos factuais de fórmulas, identificadores, chamadas e condições; não publicam o disassembly ou implementações completas. PC e descriptor delimitam o fato observado no publisher, sem homologar aquela assinatura como API mutadora estável.

## Presença física e host

O [índice físico sibling pinado](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc/PROJECT-INSTRUCTIONS/modlist/modlist.md#L54) conserva Acolyte na linha `#004`, filename/runtime `1.0.3`. SHA-256 do documento lido: `f5669ec591dc4d1364a9c7f5e583383e3c6b790f3c9e58fcc0d83f238e46bc2b`. Não foi encontrado um JAR instalado ou hash independente dessa cópia no checkout consultado. **Igualdade entre os bytes do publisher e os instalados: `NOT_VERIFIED`.**

O TOML embarcado declara NeoForge obrigatório `[21.1.205,)` e Minecraft obrigatório `[1.21,1.21.1]`, ambos BOTH. Declara um access transformer; não declara mixin ativo nem stanza de dependência Iron's. Os publishers indicam Iron's como dependência obrigatória, sem uma versão fixada; o Modrinth referencia o projeto `s4OWxYQQ`. O bytecode consome suas APIs diretamente. A omissão no TOML não torna o host opcional.

O pack de referência registra NeoForge `21.1.250` e Iron's `1.21.1-3.16.3`; o desenvolvimento do Black Arcana usa NeoForge `21.1.248`. Declarações de versão e referências de API não comprovam boot, compatibilidade binária ou comportamento nesse conjunto.

## Universo e identidades

| Superfície | Universo observado / disposição |
|---|---|
| Entidades | 8 `EntityType`: seis papéis human/demon, Horn Merchant e Lieutenant; bases `HumanEntity`/`DemonEntity` não são dois registros extras |
| Perfis de archetype | seis chaves efetivamente consumidas, 50 entradas ponderadas; `exemple.json` é apoio, sem um sétimo papel registrado |
| Itens | 31 registros diretos: dois horns consumíveis, quatro horns vestíveis, 15 peças de armadura e dez eggs |
| Marcadores | 14 blocos com BlockItems correspondentes; dois tipos compartilhados de BlockEntity |
| Encontros | 13 estruturas configuradas e cinco tavernas de vilarejo; 28 templates NBT incluem apoio/street/house |
| Recursos de dados | 27 loot tables, seis biome modifiers, uma recipe, dez biome tags e 45 JSONs de worldgen |
| Sistemas | IA/casting, recrutamento e payload C2S, menu, archetype/reload, cinco gamerules, config, spawners e comércio |
| Suporte | um material cosmético, uma aba criativa, modelos/renderers/animações, bootstrap, traduções e metadados |

Os seis perfis têm 11 entradas para cada mage e sete para cada warrior/archer: **50**, cada pool com peso total publicado **76**. Os arquivos não apresentam filtros de bioma; as pastas de skin não são pools de magia diferentes. Datapacks podem substituir esses valores. [Perfis](profiles/INDEX.md) e [pipeline de carregamento](systems/archetype-loadout-pipeline.md).

Há **0 spells standalone próprios**. As [31 referências explícitas a magias Iron's](EXACT-1.0.3-HOST-SPELL-REFERENCES.md) continuam sob o host; seleção dinâmica pode usar outros spells habilitados. Registro de mob, perfil, item, goal, efeito visual e estrutura não é nova identidade de spell.

## Limites de integração por eixo

- **Alvo, alcance e geometria:** separar follow range do mob, limiares de distância do goal, offset de movimento e targeting do spell. Trocar a vítima/área de uma magia exige contrato do host, não somente alterar a seleção do NPC.
- **Dano e projétil:** bases de atributos, qualidade/nível de cast e lógica de flecha não são dano final. Tamanho do mob, alcance visual e tracking de rede não são hitbox/range do projétil Iron's.
- **Tempo e custo:** cooldown de IA, contrato em ticks, duração de item, mana do spell e custo em emeralds/horns são consumidores distintos. Não cobrar ou liquidar novamente por perk.
- **Persistência e rede:** NBT de owner/order/profile e validações do payload devem ser lidos nos consumidores. Menu/ícone de spell é apresentação; packet C2S não é autorização automática para uma ação Black Arcana.
- **Equipamento e loot:** modificadores, slots e políticas de drop pertencem ao provider/vanilla/host. Um item cosmético não recebe atributos hipotéticos por seu nome ou textura.

As ausências de guardas locais são observações estáticas, não exploits ou defeitos reproduzidos. As fichas registram casos de QA para ownership, vida/distância/LOS, morte, unload/reload, multiplayer, proteção e respec, conforme aplicável.

## Wiring e suporte que não criam novas habilidades

`AcolyteMod.<init>` PCs 4–146 inicializa gamerules, registra o loader de archetypes, registros de itens/blocos/entidades/material/menu, listener de payload e três specs de config. `commonSetup` e `onServerStarting` locais retornam sem lógica adicional. `AcolyteModClient.<init>` PCs 0–15 registra a factory de tela de configuração; seu `onClientSetup` é vazio. A aba `acolyte:spellbook_materials` é apresentação dos itens existentes, não uma spell/material extra.

`ModClientSetup.onRegisterMenuScreens` PCs 0–18 associa o menu de recrutamento à tela; `rendererRegister` PCs 0–144 associa renderers às oito entidades registradas. Renderers/modelos/animações são associados às fichas de seus consumidores. `ModEntityRegistry` fixa as oito identidades e os tamanhos/tracking citados nas fichas; isso não é alcance de ataque.

O access transformer declara acesso público a `StructureTemplatePool.templates` e público com remoção de final em `rawTemplates`, usados pela [injeção de tavernas](encounters/village-taverns.md). Sua aplicação efetiva no host não foi testada. `MANIFEST.MF`, TOML e traduções são metadados; não criam registros adicionais.

Modelos legados com nomes `archer_helmet`, `black_wizard_*` e `*_quiver`, mais `no_texture.png`, são retidos como suporte de apresentação no manifesto. Esses nomes não são IDs extras do registro de itens. Essa disposição não presume que um resource nunca possa ser referenciado por outro asset ou datapack.

## Licença e estado da validação

Os projetos oficiais consultados indicam **All Rights Reserved**, enquanto `META-INF/neoforge.mods.toml` no JAR declara **MIT**. O conflito de metadados permanece registrado, sem inferir uma permissão de redistribuição. Este catálogo publica fatos de interoperabilidade e não importa código ou assets.

O escopo é `CATALOG_PUBLISHER_ARTIFACT_SCOPE_ONLY`: documentação factual do publisher exato. `installed_artifact_identity=NOT_VERIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`. A [prova de fechamento](ARTIFACT-CATALOG-CLOSURE-1.0.3.md) e o [índice](INDEX.md) separam essa conclusão de certificação para perks. Nenhuma Stage, perk, adapter ou runtime foi promovido.

Iron's mantém autoridade sobre spells/casting/mana; Acolyte mantém NPCs, economia, recrutamento e encontros; RPG Skill Tree mantém progressão por contrato; Black Arcana mantém seu runtime e `WorldEffectPolicy`.
