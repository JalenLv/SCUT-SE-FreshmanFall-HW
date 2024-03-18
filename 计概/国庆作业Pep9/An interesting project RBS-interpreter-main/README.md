# RBS-interpreter

This project is an interpreter for RBS, a programming language which is a subset of Python. Given a RBS program, it will automatically convert it into Pep/9 code.

To use, simply run <code>python translator.py -f py_file_location</code>

![-f flag](https://github.com/quinnha/RBS-interpreter/blob/main/media/f_flag.PNG)

To view the AST, run <code>python translator.py --ast-only -f py_file_location</code>

![--ast-only flag](https://github.com/quinnha/RBS-interpreter/blob/main/media/ast_flag.PNG)


----
Reb-bellied Snakes (RBS) are a non-venomous kind of snake, endemic to North-America. They are quite small, but can be spotted
when hiking in Hamilton, for example.

The RBS language holds the following properties:

• It is a subset of Python. Thus, RBS code can be run by any Python interpreter;

• It only works with integers, and only natively supports binary additions and subtractions;

• Conditional instructions are if, elif and else;

• The only available loop instruction is while;

• It supports global and locals variables. Anonymous computations (e.g., print(1+3)) are not legit (1+3 must be stored in a named variable before being printed).;

• Functions calls are only “by-value” (no side effects on objects outside of a function scope);

• Arrays are of fixed size, decided at initialization. Arrays can be global or local to functions;

• We support basic I/O with input and print functions.


