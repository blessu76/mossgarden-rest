---
title: "Por que guardamos duas cópias do salvamento"
description: "Perder um jardim que você cultivou é o pior, então o salvamento é dividido em um arquivo principal e um backup."
---
Moss Garden, um jogo idle para iOS, protege seu jardim com duas salvaguardas: uma soma de verificação que detecta um salvamento danificado e um backup separado do qual ele restaura, com um aviso. Voltar o relógio do aparelho para coletar recompensas também é detectado, e esse intervalo não é contabilizado.

## Duas salvaguardas para o salvamento

Em um jogo idle, o mais frustrante é perder o jardim que você vem cultivando. Por isso, o salvamento tem duas salvaguardas.

A primeira é a soma de verificação: um valor de conferência é gravado junto com o salvamento e, se ele não bater ao carregar, o arquivo é tratado como danificado. A segunda é o backup: o arquivo principal e o backup ficam separados, então, se o principal quebrar, restauramos a partir do backup e avisamos você. Também cuidamos da ordem, para que um arquivo principal quebrado nunca sobrescreva um backup saudável.

## Relógio voltado para trás

Também precisávamos barrar o truque de voltar o relógio do aparelho para coletar recompensas. Quando uma volta do relógio é detectada, esse intervalo não é contabilizado, e o app avisa você.

## Mantendo salvamentos antigos funcionando

Ao adicionar recursos, mantemos o formato do salvamento e só acrescentamos novos campos, para que salvamentos antigos continuem abrindo em versões mais novas.

## Perguntas frequentes

### O que acontece se o arquivo de salvamento de Moss Garden quebrar?
A soma de verificação percebe a divergência, o jogo restaura a partir do backup separado e avisa você de que fez isso.

### Posso ganhar recompensas mudando o relógio do aparelho?
Não. Quando uma volta do relógio é detectada, esse intervalo não é contabilizado, e o app avisa você.
