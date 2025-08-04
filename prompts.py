'''
This file contains the key prompts to generate our training examples. There are two key prompts:
Prompt 1:
    Generates the list of C++ functionalities. This prompt should be roughly 50 lines long and utilize
    few-shot learning. 
Prompt 2:
    This prompt is ran once with each of the functionalities generated from Prompt 1. It needs to be
    specific and guarantee that the LLM will only respond with a valid single C++ file.
'''

CPP_STD = '''
ctype.h: isalnum(), isalpha(), iscntrl(), isdigit(), isgraph(), islower(), isprint(), ispunct(), isspace(), isupper(), isxdigit(), tolower(), toupper()
locale.h: localeconv(), setlocale()
math.h: acos(), asin(), atan2(), atan(), ceil(), cos(), cosh(), exp(), fabs(), floor(), fmod(), frexp(), ldexp(), log10(), log(), modf(), pow(), sin(), sinh(), sqrt(), tan(), tanh()
setjmp.h: longjmp()
signal.h: raise(), signal()
stdio.h: clearerr(), fclose(), feof(), ferror(), fflush(), fgetc(), fgetpos(), fgets(), fopen(), fprintf(), fputc(), fputs(), fread(), freopen(), fscanf(), fseek(), fsetpos(), ftell(), fwrite(), getc(), getchar(), gets(), perror(), printf(), putc(), putchar(), puts(), remove(), rename(), rewind(), scanf(), setbuf(), setvbuf(), sprintf(), sscanf(), tmpfile(), tmpnam(), ungetc(), vfprintf(), vprintf(), vsprintf()
stdlib.h: abort(), abs(), atexit(), atof(), atoi(), atol(), bsearch(), calloc(), div(), exit(), free(), getenv(), labs(), ldiv(), malloc(), mblen(), qsort(), rand(), realloc(), srand(), strtod(), strtol(), strtoul(), system()
string.h: memchr(), memcmp(), memcpy(), memmove(), memset(), memset(), strcat(), strchr(), strcmp(), strcoll(), strcpy(), strcspn(), strerror(), strlen(), strncat(), strncmp(), strncpy(), strpbrk(), strrchr(), strspn(), strstr(), strtok(), strxfrm()
time.h: asctime(), clock(), ctime(), difftime(), mktime(), strftime(), time()
'''

MISSING_FEATURES = '''
Wide character: Not a separate type. wchar_t is an implicit typedef for unsigned short. Characters are 8-bits wide.
Namespaces: Not supported. All top-level items are in the global namespace.
Unimplemented Features: Support for functions for unimplemented features, class, bad_cast for example, are unlikely to be functional.
locale: The locale message facet is not supported.
Timezone: Not supported. The ARM C library does not support it.
Complex default template arguments: Not supported. Complex default template argument definitions are where a type parameter has a default instantiation involving an earlier type parameter. When you request a template that the standard says is defined with a complex default (such as instantiating class queue), you must always supply a value for each template parameter. No defaults are present.
Exceptions: Not supported.
typeinfo: Limited support. typeinfo is supported in a basic way by the ARM C++ library additions.
'''

# Prompt 1: Generate list of C++ functionalities
PROMPT_1 = """
You are an expert C++ developer.
Your task is to generate a list of C++ functionalities that can be used to create training examples for an assembly-to-C++ converter for an esoteric compiler.
You must conform to the ISO/IEC 14822 :1998 International Standard for C++.
NEVER use "std", as it will always cause compilations errors.
NEVER use namespaces.

Here is a list of all available libraries:
"""+ CPP_STD + """

Here is a list of some of the missing features:
"""+ MISSING_FEATURES + """

Each functionality should be distinct and cover a wide range of C++ features, including but not limited to:

- Control structures (if-else, loops)
- Functions and recursion
- Classes and objects
- Templates and generic programming
- Memory management (pointers)
- Virtual functions

Provide at least 1000 distinct functionalities, each described in a single sentence.
Slight rephrasings are acceptable.
Ensure that the functionalities are diverse and cover both simple and complex C++ features.
Your only response should be each of these functionalities, no preamble or closing statements.
Ensure that the features are reasonably complex, they should generate a function that is at least 7 lines long.

Example:
Implement a function that calculates the factorial of a number using recursion.
Create a class that represents a stack using an array and implement push, pop, and peek operations.
Write a program that reads a file and counts the number of words in it.
Implement a template function that sorts an array of any type using the bubble sort algorithm.
Create a program that demonstrates the use of smart pointers to manage dynamic memory.
"""

# Prompt 2: Generate a single C++ file for a given functionality
PROMPT_2 = """
You are an expert C++ developer. Your task is to generate a single C++ file that implements the following functionality:

{}

The C++ file should be complete, compilable, and should only contain the code necessary to implement the given functionality.
Do not include any additional explanations, comments, or unrelated code.
Include a very basic main function that uses the generated function.
Do not print anything.
You must conform to the ISO/IEC 14822 :1998 International Standard for C++.
Usage of "std" is forbidden.
Printf is acceptable.

Here is a list of all available libraries:
"""+ CPP_STD + """

Here is a list of some of the missing features:
"""+ MISSING_FEATURES + """

Example:
If the functionality is "Implement a function that calculates the factorial of a number using recursion", the C++ file should look like this:

int factorial(int n) {{
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}}

Ensure that the code is well-formatted, follows best practices, and is free of errors.
"""