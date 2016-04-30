#include <iostream>
#include <stdio.h>
using namespace std;
// // // 
// 
//Класс для лексем.
// 
// // // 
class Token {
public:
    char type;        // + - / * ( ) - конструктор №1 и # - числа конструктор 2
    double value;     // числа - конструктор №2
//     конструктор №1
    Token(char ch) :type(ch), value(0) { } 
//     конструктор №2
    Token(char ch, double val) :type(ch), value(val) { }
};
// Token stream
class Token_stream {
public:
    Token_stream() : full(false), buffer(0) {}   // конструктор буфера токен стрима.
    Token get();      // Функция получения токена с ввода.
    void putback(Token t);    // Функция возврата токена.
private:
    bool full;        // Проверка есть ли в буфере данные.
    Token buffer;     // Буфер для токеноввозвращаемых функцией putback()
};
// // // 
// 
// Глобальные переменные.
// 
// // // 

Token_stream ts; //

// // // --------------------------------------
//Объявление нееобходимых функций.
// 
// // // 

//Получение переменных с ввода и составление лексем.
//Выражение сложения и вычитания.
double expression_step3(); // назначет left из term_step2() 
                           // а term из primary_step1()
//Терминирующее выражение умножения и деления.
double term_step2();       // возвращает в expression_step3 left
                           // который берет из primary_step1
//Работа с числами и скобками.
double primary_step1();    // получет left из get() токенстрима

// // //----------------------------------------
// Основная программа.
// // //----------------------------------------
int main ()
{
    double val = 0;
    cout << "Введите выражение заканчивая его знаком '=' :" << endl;
    cout << ">>";
    while (cin)
    {
        Token t = ts.get();
        if (t.type == 'q') break;
        if (t.type == '=')
        {
            cout << "Результат: " << val << endl;
            cout << "Для выхода введите q" << endl;
        }
        else
            ts.putback(t);
        val = expression_step3();
    }
    
}

// // // ---------------------------------------
// Реализация функций
// // // ---------------------------------------


//  Сложениеи вычитание.

double expression_step3()
{
    double left = term_step2();
    Token t = ts.get();
    while (true)
    {
        switch(t.type)
        {
            case '+':
                left += term_step2();
                t = ts.get();
                break;
            case '-':
                left -= term_step2();
                t = ts.get();
                break;
            default:
                ts.putback(t);
                return left;
        }
    }
}

// Деление и умножение.

double term_step2()
{
    double left = primary_step1();
    Token t = ts.get();
    while (true)
    {
        switch(t.type)
        {
            case '*':
                left *= primary_step1();
                t = ts.get();
                break;
            case '/':
            {
                double d = primary_step1();
                if (d == 0) 
                {
                    perror("деление на нуль");
                }
                left /= d;
                t = ts.get();
                break;
            }
            default:
                ts.putback(t);
                return left;
        }
    }
}

// Обработка потока токенов, в том числе и скобок.

double primary_step1()
{
    Token t = ts.get();
    switch (t.type)
    {
        case '(':
        {
            double d = expression_step3();
            t = ts.get();
            if (t.type != ')')
            {
                perror("требуется ')'");
            }
            return d;
        }
        case '#':
            return t.value;
        default:
            perror("требуется первичное выражение");
    }
}



// // //-------------------------------- 
// 
// Функции Token_stream
// 
// // //-------------------------------

//Кладем лексемы в поток

Token Token_stream::get()
{
    if (full)
    {
        full = false;
        return buffer;
    }
    char ch;
    cin >> ch;
    
        switch (ch) {
    case '=':
    case 'q':            
    case '(':
    case ')': 
    case '+': 
    case '-': 
    case '*': 
    case '/': 
        return Token(ch);        // Отправляет в конструктор 1
    case '.':
    case '0': 
    case '1':
    case '2': 
    case '3': 
    case '4':
    case '5': 
    case '6': 
    case '7': 
    case '8': 
    case '9':
        {    
            cin.putback(ch);         
            double val;
            cin >> val;             
            return Token('#',val);   // отправляет в конструктор 2
        }
    default:
        perror("Bad token");
    }
}
// Возврат лексем в поток.

void Token_stream::putback(Token t)
{
    if (full) perror("putback(): буфер заполнен");
    buffer = t;
    full = true;
}
