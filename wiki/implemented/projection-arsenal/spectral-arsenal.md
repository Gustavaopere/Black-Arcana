# Spectral Arsenal

## Estado

`IMPLEMENTADO / CANÔNICO — REAL-MODPACK HOST ACCEPTANCE DEFERRED`

## Identidade

- **Domínio:** Projection & Arsenal
- **Authority:** Black Arcana
- **Função:** sessão bounded de arsenal projetado

## Descrição

Cria e gerencia uma sessão de arsenal espectral baseada em handles efêmeros. O arsenal não é um inventário paralelo e não materializa cópias persistentes dos itens reais do jogador.

## Obtenção/aprendizado

`TBD — Stage 08 / provider/RPG`

## Custo e casting

- **Custo:** `TBD`
- **Cooldown:** `TBD`
- **Cast/channel:** `TBD`

## Mecânica

A sessão possui owner/lifecycle e consome budget de projeção. Cada término libera corretamente o budget.

## Hard ceilings

O domínio limita projeções/echoes ativos a `48`. Registry de profiles limitado a `64` entradas.

## Segurança

- sem persistent item duplication;
- sem client-authoritative arsenal;
- handles bounded;
- cleanup em término/lifecycle;
- provider-specific materialization só quando hook verificado.

## VFX

Direção: armas orbitais/projetadas com material espectral e entrada/saída por formação arcana. Número visual pode ser reduzido por LOD sem alterar o número real de handles server-side.

## Testes/evidência

O Stage 07.03 registrou RED→GREEN específico para Spectral Arsenal e pipeline completo com GameTests/dedicated-server smoke antes do merge canônico.
