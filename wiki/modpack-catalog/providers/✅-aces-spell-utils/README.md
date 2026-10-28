# Ace's Spell Utils 1.2.7.2 — catálogo técnico

Ace's é uma biblioteca com runtime compartilhado para addons de Iron's. **0 registered standalone spells.** A fonte registra atributos, escolas e exemplos reais; também fornece bases de entidades, armas, summons, domínio, rendering e efeitos visuais. Esses contratos precisam de fichas próprias mesmo sem constituírem magias registradas.

## Identidade e limite da evidência

- Release: `1.2.7.2-1.21.1`; mod ID `aces_spell_utils`; Minecraft `1.21.1` / NeoForge.
- Artefato: `aces_spell_utils-1.2.7.2-1.21.1.jar`; CurseForge projeto/file `1299492 / 8789930`.
- SHA-1: `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca`.
- Fonte oficial: `AceTheEldritchKing/Aces_Spell_Utils@a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`.

O publisher baixado corresponde ao hash registrado do artefato. Os **132 nomes de classes externas** correspondem aos **132 arquivos Java** da fonte; há 150 classfiles incluindo classes internas. Essa comparação estabelece o inventário de nomes, sem demonstrar equivalência de métodos, constantes ou fluxo entre fonte e JAR. [Proveniência detalhada](EVIDENCE-AND-PROVENANCE.md).

O build efetivo da fonte usa NeoForge `21.1.230` e Iron's `3.16.2`; a propriedade Iron's `3.11.0` é antiga e não alimenta essa dependência. O desenvolvimento do Black Arcana usa NeoForge `21.1.248`; o ledger físico de referência registra `21.1.250` e Iron's `3.16.3`. Nenhuma dessas declarações prova compatibilidade em execução.

## Conteúdo individual e consumidores

| Superfície | Fichas / referência |
|---|---|
| 19 atributos, com fórmulas e fases de evento | [Atributos](attributes/INDEX.md) |
| 3 escolas: `ritual` (display Occult), `hydro` (supplier Java `ABYSSAL`), `technomancy` | [Escolas](schools/INDEX.md) |
| 3 tipos de dano e 14 tags | [Dano](damage-types/INDEX.md) · [Tags](tags/INDEX.md) |
| 1 attachment, 1 partícula, 8 raridades, 5 configurações | [Attachment](attachments/INDEX.md) · [Partícula](particles/INDEX.md) · [Raridades](rarities/INDEX.md) · [Config](config/INDEX.md) |
| 27 itens de exemplo registrados em produção e 1 material de armadura | [Exemplos reais](examples/INDEX.md) |
| 8 payloads S2C, 2 mixins e 5 contratos de ciclo de vida visual | [Payloads](payloads/INDEX.md) · [Mixins](mixins/INDEX.md) · [VFX](vfx-runtime/INDEX.md) |
| Helpers, entidades, itens, comandos, animações e exemplo de summon não registrado | [Sistemas](systems/INDEX.md) |

Os exemplos são registrados independentemente de dev mode; apenas a aba criativa é condicionada ao ambiente de desenvolvimento. Dois handlers de spellbooks e um handler de sheath executam procs próprios; chamar um objeto de exemplo não o torna código morto. Os 27 `AnimationHolder` também não são 27 magias.

## Fechamento e progresso

O [manifesto da versão-fonte](SOURCE-CATALOG-MANIFEST-1.2.7.2.json) associa cada arquivo rastreado da fonte a fichas ou a uma disposição de suporte justificada, e fixa os hashes das fichas. A [prova de fechamento](SOURCE-CATALOG-CLOSURE-1.2.7.2.md) define o escopo e as exclusões. O [índice](INDEX.md) apresenta as barras de documentação e certificação separadamente.

Esse fechamento é `CATALOG_SOURCE_SCOPE_ONLY`. **`mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`.** Não homologa o provider para perks nem transforma pendências físicas em conclusão. Alterações no conjunto ou conteúdo das fichas exigem renovar e revisar o manifesto antes de regenerar os índices.

Ace's mantém autoridade sobre seus atributos, eventos, procs e helpers. Iron's controla casting, mana e cooldown nativos. Black Arcana mantém seu runtime, Corruption, Strain, Arcane Danger e `WorldEffectPolicy`; RPG Skill Tree só deve aplicar progressão por contrato comprovado. Não duplicar consumidores de dano, cast, inventário ou proc.

Complementos: [registros](REGISTRIES-AND-ATTRIBUTES.md), [famílias da API](API-AND-RUNTIME-SURFACES.md), [rede e exemplos](NETWORK-MIXINS-AND-EXAMPLES.md) e [causalidade dos eventos](SOURCE-1.2.7.2-COMBAT-CAUSALITY-AND-DOUBLE-SETTLEMENT-20261027.md).
