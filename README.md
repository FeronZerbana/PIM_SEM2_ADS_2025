Projeto Integrado Multidisciplinar

2° Semestre 2025

Projeto de pesquisa que faz parte do método de avaliação da Instituição de ensino superior UNIP.

#INSTALAÇÃO#
    Para o funcionamento desse sistema, é necessária a instalação de alguns componentes:

    -Python 3.14
        -> customtkinter 
    -gcc 

#COMPILAÇÃO#
    Caso o sistema não funcione na primeira tentativa, talvez seja necessário recompilar as bibliotecas dinâmicas, de acordo com o seu Sistema Operacional.

    No terminal, dentro da pasta PIM_FINAL:

    (windows) -> gcc -shared -o process.dll process.c 
    (Linux) -> gcc -shared -o libprocess.so -fPIC process.c
    (MacOS) -> gcc -dynamiclib -o libprocess.dylib process.c

#DESCRIÇÃO#
    Software de organização e cadastro voltado ao professor. Permite cadastrar alunos, turmas e atividades em um único sistema, assim como gerenciar notas e organizar espaços.

#INSTALL#
    For this system to work, it's necessary to install some components:

    -Python 3.14
        -> customtkinter 
    -gcc

#COMPILATION#
    In case where this system doesn't work on first try, you may need to recompile the dynamic library, based on your operational system:

    Terminal, inside PIM_FINAL directory:

    (windows) -> gcc -shared -o process.dll process.c 
    (Linux) -> gcc -shared -o libprocess.so -fPIC process.c
    (MacOS) -> gcc -dynamiclib -o libprocess.dylib process.c

#DESCRIPTION#
    Organization and registration software aimed at teachers. It allows registering students, classes, and activities in a single system, as well as managing grades and organizing spaces.
