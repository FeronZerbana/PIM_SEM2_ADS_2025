Projeto Integrado Multidisciplinar

2° Semestre de 2025

Projeto de pesquisa que faz parte do método de avaliação da Instituição de ensino superior UNIP.

#INSTALAÇÃO#
    Para o funcionamento desse sistema, é necessária a instalação de alguns componentes:

    -Python 3.14
        -> customtkinter 
    -gcc 

#COMPILAÇÃO#
    Caso o sistema não funcione na primeira tentativa, talvez seja necessário recompilar as bibliotecas dinâmicas, de acordo com o seu Sistema Operacional.

    Terminal  ././PIM_SEM2_ADS_2025

    (windows) -> gcc -shared -o process.dll process.c 
    (Linux) -> gcc -shared -o libprocess.so -fPIC process.c
    (MacOS) -> gcc -dynamiclib -o libprocess.dylib process.c

#DESCRIÇÃO#
    Software de organização e cadastro voltado ao professor. Permite cadastrar alunos, turmas e atividades em um único sistema, assim como gerenciar notas e organizar espaços.

#EXECUÇÃO#

    Terminal ././PIM_SEM2_ADS_2025

    mainf.py

#INSTALL#
    For this system to work, it's necessary to install some components:

    -Python 3.14
        -> customtkinter 
    -gcc

#COMPILATION#
    In case where this system doesn't work on first try, you may need to recompile the dynamic library, based on your operational system:

    Terminal ././PIM_SEM2_ADS_2025

    
    With GCC installed:
    
    (windows) -> gcc -shared -o process.dll process.c 
    (Linux) -> gcc -shared -o libprocess.so -fPIC process.c
    (MacOS) -> gcc -dynamiclib -o libprocess.dylib process.c

#DESCRIPTION#
    Organization and registration software aimed at teachers. It allows registering students, classes, and activities in a single system, as well as managing grades and organizing spaces.

#RUN#

    Terminal ././PIM_SEM2_ADS_2025

    with PYTHON installed:
    
    python mainf.py
