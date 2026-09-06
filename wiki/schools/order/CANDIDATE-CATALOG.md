# Arcana da Ordem — Catálogo candidato

## Estado

`CONCEITO / PESQUISA — NOMES E NÚMEROS AINDA NÃO FECHADOS`

| Codinome de design | Categoria | Conceito |
|---|---|---|
| Selo de Passagem | Seal | Bloqueia teleport/displacement dentro de uma área bounded para entidades/casts autorizadamente reconhecidos. |
| Mandala de Guarda | Ward | Barreira orientada que bloqueia ou reduz uma categoria explícita de impacto/projétil/spell. Pode possuir tier reativo/auto-ward como evolução, sem virar um segundo spell semanticamente idêntico. |
| Prisão Poliédrica | Containment | Contém entidade elegível em volume bounded, sem mover block entities ou criar dimensão. |
| Limiar Gêmeo | Portal | Variante/host de Threshold Gate com geometria ritual própria e apresentação via Immersive Portals quando o adapter instalado for validado. |
| Transposição Simétrica | Space | Variante/host de Reciprocal Transposition. |
| Âncora de Lei | Stabilization | Impede displacement/knockback/teleport não autorizado por curto tempo quando hooks permitem. |
| Dissipação Ordenada | Countermagic | Remove/suprime efeito mágico explicitamente classificado e dispellable pelo provider. |
| Geometria de Retorno | Defense | Redireciona projétil/impulso autorizado segundo vetores determinísticos. |
| Olho da Convergência | Divination / Fate Sight | Read-only prediction/telemetry de trajetória, perigo, janela provável ou futuro autorizado; nunca client authority e nunca lê RNG secreto global. Absorve o nicho de `fate sight` identificado em Doctor Fate. |
| Campo Axiomático | Law Field | Stage 07.06 domain que impõe uma pequena lista de leis locais server-authoritative. |
| Julgamento de Simetria | Control | Equaliza/redistribui uma grandeza autorizada entre endpoints sob caps e sem gerar recurso. |
| Círculo de Banimento | Banishment | Remove temporariamente summon/entidade elegível da interação por mecanismo seguro sem delete arbitrário. |
| Arquitetura Imutável | Endgame Ward | Domain/ward de alto custo que estabiliza uma área contra categorias explícitas de mutação/magia. |
| Desdobramento Astral | Astral Projection | Projeta uma presença astral bounded enquanto o corpo real permanece server-authoritative e vulnerável. A projeção não carrega inventário, não duplica player state, não força chunks e tem distância/duração/dimensão limitadas. Só permanece se Asterism/Ars/Eidolon/Iron's/addons não fornecerem mecânica equivalente. |
| Ruptura de Fonte | Countermagic / Link Sever | Interrompe temporariamente a ligação causal de um efeito/cast com **uma fonte reconhecida** (resource/channel/reservoir/link), sem zerar recursos nem silenciar providers desconhecidos. Inspirado também em práticas ocultistas transversais; só existe com adapter explícito. |
| Exorcismo Axiomático | Banishment/Exorcism | Expulsa possessão, entidade vinculada ou influência extradimensional apenas quando o provider expõe identidade e relação causal. Não é kill spell. |
| Prisma de Retorno | Counterspell/Reflection | Captura uma magia elegível e a devolve/redistribui conforme provenance verificável. Se o spell não expõe receipt/owner, degrada para block/deny em vez de refletir. |
| Selo de Transmutação | Transformation | Petrifica, estabiliza ou remove transformação mágica registrada por curta duração. Não altera entidades arbitrárias por NBT. |
| Caminho Ordenado | Portal/Route | Abre rota segura entre dois limiares autorizados, preferencialmente usando Immersive Portals para render/traversal e Stage 07.04 para safety/authority. |

## Feats adicionados pelo corpus Strange/Fate

- Strange reforça counterspell, shields, bindings, banishment/exorcism, astral projection, teleport/portals, transmutation, route stabilization e siphon/redirection de magia.
- Fate reforça teleport/portals, conjuração de armamentos/escudos/laços, bindings, luz anti-sobrenatural, petrificação e remoção de magia.
- Efeitos de 'auto-shield' entram como evolução/passiva de `Mandala de Guarda`, não como um segundo escudo redundante.
- Manipulação temporal de HQ não vira stop-time global. Qualquer adaptação futura fica restrita a cooldown windows, local tick-independent state ou efeitos locais seguros.

## Constantine como fonte transversal

Os seguintes feats não criam escola Constantine; são roteados para Ordem quando o delta é estrutural:

- `turnabout charm`/spell reversal → `Prisma de Retorno`;
- escapar/quebrar snares mágicos → possível evolução de `Dissipação Ordenada`/`Ruptura de Fonte`;
- cages/bindings contra entidades sobrenaturais → `Prisão Poliédrica`/`Círculo de Banimento`;
- teleportes de curta distância/objetos → usar provider já existente antes de novo spell.

Wards de ocultação, contratos, ingredientes e sigilos pragmáticos ficam em Bruxaria/Occult, não Ordem.

## Notas de deduplicação da pesquisa 2026-09-06

- Auto-shields e wards rápidos de Strange/Fate entram como tier/comportamento de `Mandala de Guarda`, não como outro escudo por nome.
- Fate sight entra em `Olho da Convergência`; não criar `Visão do Destino` separado sem delta mecânico.
- Containment em amuleto/vaso/espaço místico é representado por `Prisão Poliédrica`/Binding quando seguro; não criar dimensões temporárias ou serializar entidades arbitrariamente.
- Proteção/resgate de alma deve deduplicar contra `Soul Anchor`, `Spirit Sight`, Malum e Eidolon. Nenhum novo spell de alma é aprovado por esta pesquisa isoladamente.
- Portais de Strange/Fate entram em `Limiar Gêmeo`/`Caminho Ordenado` + Stage 07.04 + Immersive Portals; não criar motores de portal paralelos.
- Transmutação/petrificação permanece candidato apenas se não for duplicata de providers existentes e passar World Safety/target policy.
- Holy light de Fate não vira automaticamente Order; ofensiva sagrada/consagração pertence à escola Divine/Holy quando a semântica for essa.

## Regras

- Ordem não significa imunidade universal;
- selos funcionam somente em hooks reconhecidos;
- barrier/containment respeitam claims/protection/PvP;
- portais reutilizam Stage 07.04;
- law fields reutilizam Stage 07.06;
- divination é read-only;
- dispel não remove effects indiscriminadamente por registry scan sem semântica provider-backed;
- projeção astral não duplica inventário/capabilities, não cria segundo player e não vira câmera com authority;
- reflection exige provenance verificável;
- Iron's é o host pretendido para spell school/UI/progressão.
