# Ypsilon — 13 Principles como sistemas integráveis, 22/10/2026

Base Black Arcana `4dce7a11d88aab9b18d45c7a80d78c956b64bc4e` (Paladin #874 já integrado). RPG/modlist `ffd1f1ede5bf46ce3425a5c17bc5d279d8c572dc`, Enshrouded `a41dbb51aacb94b7b5db6517f1514b0b7aee3e83`, Factory `518278ae9c0d264a537cc1bc6ee4974e01270fdf`. Source oficial `ypsilonM/FundamentalPrinciples-1.21.1@a9b8f8222fb2a800edece8c1568984bd2a764fc2` consultado no pin; inventário físico versionado mantém #575/JAR `ypfundamentals-1.1.7.1.jar`, SHA-1 `a2855c253202a8fcc2925fcf5b1bf86d64fbe4da`.

## Entrega e escopo

[13 fichas individuais](../../wiki/modpack-catalog/providers/✅-ypsilons-fundamentalism/principles/README.md), índice e correções nos agregados do provider. As fichas registram parâmetros/defaults, consumidores, fase, gates, mutabilidade e roteiro de QA. Elas representam categorias/passivas, não 13 registros de spell. **+0 magias**; 15 spells existentes ficam fora do recorte desta barra. Mínimos mágicos, campanha binária 38/39, 164 providers do painel e denominador global aberto permanecem separados.

Achados úteis para perks:

- Perceptio recalcula `8+D/5+trunc(1,5l)` em vez de apenas somar ao alcance original; Locus pode multiplicar depois, exige `bbInflation>0` e o default pode reduzir o alcance.
- Expansio altera raio uma vez por entidade elegível, exige owner ServerPlayer e exclui EchoingStrikeEntity; não confundir raio com volume ou escala visual.
- Potentia rotaciona e normaliza o vetor no ramo accuracy<1; não amplia hitbox e pode afetar magnitude codificada no vetor.
- Vitale exige `usesSummon` e recast count literal 2. Repetitio exige totalRecasts>2 e não modifica recast já ativo.
- Pertinacia usa nível do destinatário ServerPlayer e somente MagicMobEffect; Remedium usa nível do caster, mas debita food do receptor, com ramo próprio quando insuficiente.
- Primeiro threshold de XP é 46, pois a progressão consulta nível de destino; prática por evento não prova dano/efeito entregue. Power compartilhado, fatigue e ownership permanecem provider-native.

Nenhum runtime, adapter, perk ou arquivo de dependência/lockfile foi alterado. Source depende Iron’s 3.16.2, enquanto o pack usa 3.16.3: declarar mixins no source não comprova que os injection targets sejam compatíveis no pack. Metadata MIT versus licença de template MDK não autoriza importar implementação/assets do addon; esta entrega usa resumos e referências.

## Validação

- Conferência estrutural/source: **13 fichas**, **73 links locais**, **136 referências pinadas/âncoras válidas**, **8 mixins declarados**.
- Revisão independente de fórmulas, gates, recipients/owners, XP, oito mixins, helpers, eventos e attachments sem erro factual bloqueante. Âncora de setLevel corrigida para a declaração L88.
- `PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/global_magic_catalog_test.py`: **52/52 PASS**.
- `PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/catalog_physical_ledger_test.py`: **5/5 PASS**.
- `PYTHONDONTWRITEBYTECODE=1 python3 docs/qa/magic_pendency_tracker_test.py`: **26/26 PASS**.
- Painel JSON/Markdown conferido: 13/13 somente Principles; barra global indeterminada. `git diff --check` sem erro.

O ambiente Black Arcana também passou build/919 testes JUnit (2 adicionais ignorados), isolamento dos JARs e 108 GameTests obrigatórios. Servidor headless respondeu status Minecraft 1.21.1/protocolo767 e salvou todas as dimensões no encerramento intencional. Esses checks validam desenvolvimento do Black Arcana sem Ypsilon carregado: **não** são aceite funcional dos Principles.

Runtime com o JAR Ypsilon, configuração implantada, Survival, cliente, multiplayer e modpack continuam **PENDING**; nenhum Stage é promovido. Instalação/startup reutilizáveis estão no draft do ambiente; snapshot publicado e restauração em nova tarefa são fatos separados ainda não verificados. Resultado de PR/CI/merge deve ser registrado pelo handoff real, sem fabricar SHA futuro neste arquivo.
