# 🛡️ Simulação de Malwares para Estudo de Segurança Cibernética

> **⚠️ AVISO IMPORTANTE**  
> Este projeto tem **exclusivamente fins educacionais e éticos**. Os códigos aqui presentes são simulacros de ransomwares e keyloggers, desenvolvidos para demonstrar seu funcionamento interno com o objetivo de **ensinar defesas e boas práticas**.  
> **Nunca execute estes scripts em sistemas sem autorização explícita do proprietário.** O autor não se responsabiliza pelo uso indevido.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Purpose](https://img.shields.io/badge/purpose-educational-orange)

## 📌 Índice

- [Sobre o Desafio](#sobre-o-desafio)
- [Estrutura do Repositório](#estrutura-do-repositório)
- [Pré‑requisitos](#pré‑requisitos)
- [Configuração do Ambiente Seguro](#configuração-do-ambiente-seguro)
- [Ransomware Simulado](#ransomware-simulado)
  - [Como funciona](#como-funciona-ransomware)
  - [Execução passo a passo](#execução-ransomware)
- [Keylogger Simulado](#keylogger-simulado)
  - [Como funciona](#como-funciona-keylogger)
  - [Execução passo a passo](#execução-keylogger)
  - [Envio automático por e-mail](#envio-de-e-mail)
- [Reflexão sobre Defesa em Camadas](#reflexão-sobre-defesa-em-camadas)
- [Principais Aprendizados](#principais-aprendizados)
- [Próximos Passos](#próximos-passos)
- [Licença](#licença)

---

## Sobre o Desafio

Este repositório foi criado como parte de um desafio prático de segurança cibernética. O objetivo foi:

- Implementar um **ransomware simulado** que criptografa arquivos de teste com AES (via `cryptography.fernet`) e exibe uma nota de resgate.
- Implementar um **keylogger simulado** que captura teclas, salva em arquivo discreto e pode enviar os logs por e‑mail.
- Documentar **medidas de prevenção e defesa** (antivírus, firewall, sandboxing, conscientização do usuário, backups).

Tudo foi desenvolvido em **Python puro** e testado exclusivamente em ambiente isolado (máquina virtual sem rede, ou container Docker).

---

## Estrutura do Repositório
