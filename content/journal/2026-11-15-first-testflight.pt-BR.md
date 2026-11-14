---
title: "Como o primeiro build do TestFlight foi ao ar"
description: "Depois de concluir o MVP, o primeiro build interno foi enviado, mas o script de deploy nos parou uma vez no caminho."
copy_review: iris 2026-11-14
---
O primeiro MVP de Moss Garden, um jogo idle para iOS, foi enviado ao TestFlight como 1.0.0 (1) para testes internos depois que um script de deploy interrompeu a primeira tentativa. O processamento levou cerca de três minutos, e o build não foi enviado para análise nem aberto a testadores externos.

## O que havia no MVP

O primeiro MVP reuniu oito plantas, cálculo offline, estações do ano, um livro de coleção, salvamento e configurações. Em seguida, o enviamos ao TestFlight como 1.0.0 (1) para testes internos. O processamento levou cerca de três minutos, e não o enviamos para análise nem o abrimos a testadores externos.

## A primeira tentativa falhou

Quando o script de deploy executou o green gate, uma variável de ambiente que significa "não aumente o número do build" vazou para os testes e os quebrou, e o script parou ali mesmo. Graças a essa parada, nenhum build com problema foi enviado. Corrigimos para que os processos filhos não herdem mais o ambiente externo e enviamos de novo.

Fazer deploy pode dar trabalho, mas mantemos a regra: se os testes não estão verdes, nada é publicado.

## Perguntas frequentes

### O que havia no primeiro build de TestFlight de Moss Garden?
Oito plantas, cálculo offline, estações do ano, um livro de coleção, salvamento e configurações, enviados como 1.0.0 (1) para testes internos.

### Moss Garden foi enviado para análise da App Store?
Não. Este build foi enviado apenas para testes internos, e não o submetemos à análise.
