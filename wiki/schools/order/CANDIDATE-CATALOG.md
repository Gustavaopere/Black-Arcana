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

## Notas de deduplicação da pesquisa 2026-09-06

- Auto-shields e wards rápidos de Strange/Fate entram como tier/comportamento de `Mandala de Guarda`, não como outro escudo por nome.
- Fate sight entra em `Olho da Convergência`; não criar `Visão do Destino` separado sem delta mecânico.
- Containment em amuleto/vaso/espaço místico é representado por `Prisão Poliédrica`/Binding quando seguro; não criar dimensões temporárias ou serializar entidades arbitrariamente.
- Proteção/resgate de alma deve deduplicar contra `Soul Anchor`, `Spirit Sight`, Malum e Eidolon. Nenhum novo spell de alma é aprovado por esta pesquisa isoladamente.
- Portais de Strange/Fate entram em `Limiar Gêmeo` + Stage 07.04 + Immersive Portals; não criar motores de portal paralelos.
- Transmutação/petrificação permanece candidato apenas se não for duplicata de providers existentes e passar World Safety/target policy.

## Regras

- Ordem não significa imunidade universal;
- selos funcionam somente em hooks reconhecidos;
- barrier/containment respeitam claims/protection/PvP;
- portais reutilizam Stage 07.04;
- law fields reutilizam Stage 07.06;
- divination é read-only;
- dispel não remove effects indiscriminadamente por registry scan sem semântica provider-backed;
- projeção astral não duplica inventário/capabilities, não cria segundo player e não vira câmera com authority;
- Iron's é o host pretendido para spell school/UI/progressão.
