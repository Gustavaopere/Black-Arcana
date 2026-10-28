# Alshanex's Familiars — divergência entre wiki pública e JAR 4.0.3 (2026-10-28)

> Escopo: documento de **interoperabilidade e catalogação clean-room**, sem código/asset do fornecedor, sem novo spell/ritual contabilizado e sem certificação `COMPLETE_PERK_READY`. Consulta à wiki pública em 2026-10-28; a página não fornece aqui um pin verificável para a release 4.0.3. Este documento não substitui a autoridade do JAR instalado nem prova comportamento no modpack.

## Autoridade fixada neste repositório

O [dossiê do artifact 4.0.3](EXACT-4.0.3-ARTIFACT-AUDIT.md) informa identidade por SHA-1 **`e5051c2385a426d05bf203ba8081a23d891f6686`** para `alshanex_familiars-1.21.1_v4.0.3.jar` e inspeção estrutural restrita: **7** registros de `AbstractSpell`, **11** recursos `alshanex_familiars:ritual_recipe`, com os respectivos resultados. O [README canônico](README.md) e as 18 fichas individuais registram esse universo **identity-only**. Foi feita inspeção dos relatórios versionados no GitHub, **não** nova abertura do JAR nesta contribuição.

A [wiki pública do fornecedor](https://wiki.pixeldreamstudios.net/mods/alshanex-familiars) é fonte para **comportamento descrito publicamente** e sugestões de datapack, porém não está explicitamente vinculada ao SHA-1 nem à revisão de 4.0.3. Os exemplos atuais da página podem refletir documentação mais recente ou configurações diversas. Não transferir os defaults da página para o ledger de 4.0.3 sem confronto exato.

## Divergências concretas

| Assunto | Prova de artefato/ledger de 4.0.3 | Wiki pública consultada | Disposição segura |
|---|---|---|---|
| `archmage_shard.json`, `druid_shard.json` e outros nomes `*_shard` | Paths tipados `ritual_recipe`; cartões vinculam resultados a IDs próprios de shard | A página afirma que receitas de ovos usam os nomes legados de arquivos `*_shard.json`, mas o resultado agora é `familiarslib:familiar_egg` com componente de tipo | **Conflito de resultado**, não de nome do arquivo; validar JSON do JAR exato antes de qualquer alteração de cards |
| Total de rituais | 11 recursos `ritual_recipe` enumerados no artefato publicado 4.0.3 | A tabela de receitas padrão da página descreve **19 linhas** de resultados (ovos, vessel, essências, estações e outros) | Não alterar 11/11 nem criar +8 identidades: contar somente receitas presentes no JAR exato e verificar overrides de datapack se necessário |
| Spell de raio | ID exato `alshanex_familiars:megido`, classe `MegidoSpell` | Página apresenta **Electric Rain** entre os spells próprios | Não presumir que `Electric Rain` é alias/novo registro de `megido` sem tradução/registro exatos |
| Spell de sombras | ID exato `alshanex_familiars:summon_shadows` | Página chama **Call the Shadows** | Apelido descritivo plausível, mas só o ID do JAR é canônico |
| Aquisição dos sete spells | Fichas de identidade não certificam meios de aquisição em 4.0.3 | Wiki afirma distribuição exclusiva via Scroll Reroll Station para lista editorial de sete spells | Tratar como hipótese de alcance operacional a validar em `4.0.3` e datapacks efetivos |
| Fluxo Sound / Bard | README de 4.0.3 atribui spells Sound/Melodic a Tunes n' Tomes | Wiki também indica dependência opcional de Tunes n' Tomes para Bard e itens | Compatível em termos de ownership; não duplicar spells Sound em Alshanex |

## Regras para os catálogos e perks

1. Os números **7 spells + 11 rituais = 18 identidades** permanecem inalterados até evidência do artefato ou pack efetivo. A comparação documental não constitui prova adicional de resultado, custo, targeting ou hooks.
2. A configuração de `familiarslib:familiar_egg` por componente `familiarslib:familiar_type` publicada na wiki pode orientar testes futuros, **não** substituir as receitas de 4.0.3 por presunção.
3. IDs/paths estáticos de receitas não são prova de que o ritual foi completado pelo servidor, nem comprovam tempo, consumo, proteção de claims ou transação completa. A wiki menciona aproximadamente cinco segundos para um ritual, mas **esse número não está auditado no JAR 4.0.3**.
4. Não registrar `Megido` e `Electric Rain` como duas magias sem confirmação de ID independente. Mesmo cuidado com *Call the Shadows* versus `summon_shadows`.
5. Black Arcana conserva sua autoridade sobre rituais/casting próprios; o provedor e FamiliarsLib mantêm seus efeitos e estado; RPG Skill Tree só integra atributos/perks mediante boundary verificada.

## Evidência adicional necessária para a convergência

Confrontar os **11 JSONs** efetivos de `data/alshanex_familiars/recipe/ritual_recipes/` no JAR exato e nos datapacks do pack, incluindo `result.id` e `result.components`; confirmar os registros `PetSpellRegistry` e traduções `en_us` de `megido`; verificar versão publicada da wiki com release/tag ou changelog; validar servidor dedicado + comportamento JEI no conjunto FamiliarsLib/Iron's/Tunes instalado. Se houver divergência real, registrar como diferença de configuração/versão, sem apagar a prova anterior.

**Estados:** catalogação de identidade `COUNTED_EXACT` do artefato de 4.0.3; correspondência dos defaults atuais da wiki com 4.0.3 **NOT_VERIFIED**; mutating hooks **NOT_VERIFIED**; QA física no modpack **NOT_TESTED**.

Fontes: [Wiki do fornecedor](https://wiki.pixeldreamstudios.net/mods/alshanex-familiars) — seções *Rituals*, *Familiar Eggs*, *Datapacks*, *Scroll rerolls* e *Tunes integration*; [audit 4.0.3](EXACT-4.0.3-ARTIFACT-AUDIT.md), [índice de cards](INDEX.md).
