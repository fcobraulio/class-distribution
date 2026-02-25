# Class Distribution – Distribuição de Turmas

## Descrição

Este projeto realiza a distribuição automática de turmas entre professores com base em:

- Preferências individuais de disciplinas
- Equilíbrio de carga horária
- Minimização da diferença de carga entre docentes

O algoritmo busca respeitar ao máximo a ordem de preferência de cada professor, mantendo a carga horária global o mais equilibrada possível.

---

## Estrutura do Projeto


project/
│
├── main.py
└── data/
├── turmas.csv
├── preferencias.csv
└── results.csv


---

## Formato do Arquivo `turmas.csv`

Arquivo obrigatório em `data/turmas.csv`.

Estrutura:


disciplina,periodo,turma,quantidade,semestre


Exemplo:


Educação em Tecnologias Digitais,1º Ano,INF (Mat),2,1
Programação Orientada a Objetos,2º Ano,INF (Mat),4,1


Campos:

- `disciplina`: nome da disciplina
- `periodo`: ano/período
- `turma`: identificação da turma
- `quantidade`: carga horária atribuída
- `semestre`: 1 ou 2

---

## Formato do Arquivo `preferencias.csv`

Arquivo localizado em `data/preferencias.csv`.

Estrutura:


nome_professor,preferencia,disciplina


Exemplo:


PROFESSOR1,1,Programação Orientada a Objetos
PROFESSOR1,2,Banco de Dados
PROFESSOR2,1,Redes de computadores


Campos:

- `nome_professor`: identificador do docente
- `preferencia`: ordem de preferência (1 = maior prioridade)
- `disciplina`: nome da disciplina

### Importante

Após gerar um arquivo de preferências aleatórias para teste, é necessário editar este arquivo manualmente com as preferências reais dos professores antes do uso em produção.

---

## Execução

### Distribuir turmas usando preferências existentes


python main.py 1


ou


python main.py 2


O argumento indica o semestre letivo.

---

### Gerar preferências aleatórias (modo simulação)


python main.py 1 --gerar-preferencias


Esse comando sobrescreve `preferencias.csv` com dados aleatórios simulados.

---

## Saída

O resultado é salvo em:


data/results.csv


Formato:


disciplina,periodo,turma,quantidade,semestre,professor


---

## Lógica do Algoritmo (Visão Geral)

O problema tratado é uma alocação de turmas com múltiplos critérios:

1. Cada turma deve ser atribuída a exatamente um professor.
2. Professores possuem uma ordenação de preferência sobre disciplinas.
3. A carga horária total deve permanecer o mais equilibrada possível.

### Estratégia adotada

Para cada turma:

1. Simula-se a atribuição para cada professor elegível.
2. Calcula-se um escore composto por:
   - Prioridade da disciplina na lista de preferência.
   - Impacto na diferença máxima de carga horária entre professores.
   - Nova carga acumulada do professor.
3. Seleciona-se o professor com menor escore.
4. Em caso de empate, realiza-se sorteio controlado.

Além disso, as turmas são processadas em ordem decrescente de carga horária para reduzir distorções no equilíbrio global.

O objetivo é:

- Maximizar o atendimento às preferências.
- Minimizar a diferença entre o professor mais e menos carregado.
- Permitir pequenas assimetrias quando necessárias para respeitar prioridades fortes.

---

## Observações

- O algoritmo é heurístico (não é um resolvedor exato de programação inteira).
- Pode produzir resultados ligeiramente diferentes em execuções distintas se houver empates.
- Pode ser estendido para incluir restrições adicionais (carga máxima, disciplinas obrigatórias, impedimentos, etc.).