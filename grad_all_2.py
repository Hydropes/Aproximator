import math
import numpy as np
import seaborn as sbn
import matplotlib.pyplot as plt
import time
import sympy as sy
import string
import re
from typing import List, Dict

class Aproximator:
    def __init__(self, func:str):
        self.strfunc=self.__unique_params(func)#уникальные имена гиперпараметров
        self.func = sy.simplify(self.strfunc)#функция Симпай
        self.__params  ={k:np.random.randint(1, 3)
                         for k in self.__define_params()}#словарь параметров со значениями
        self.x, self.y = sy.symbols('x y')
    def __str__(self):
        return str(self.func)
    def __eq__(self, other):
        return self.func == other.func
    def __add__(self, other):
        return Aproximator(self.strfunc+'+'+other.strfunc)

    @property
    def params(self):
        return self.__params
    @params.setter
    def params(self, kwargs: Dict):
        #print(kwargs)
        for k, v in kwargs.items():
            self.__params[k] = v

    def __unique_params(self, strng):
        """Возвращает строку формулы с уникальными именами параметров"""
        str_search = re.sub(r'sin|cos|log|tan', '', strng)
        symbs = re.findall(r'[a-wz]', str_search)
        alphabet = list(string.ascii_lowercase)
        list_strng = list(strng)
        for idx, el in enumerate(list_strng):
            if el in symbs:
                symbs.remove(el)
                list_strng[idx]=alphabet.pop(0)
        return ''.join(list_strng)

    def __define_params(self)->List:
        """Возвращает список уникальных имён параметров"""
        str_search = re.sub(r'sin|cos|log|tan', '', self.strfunc)
        symbs = re.findall(r'[a-wz]', str_search)
        # alphabet = list(string.ascii_lowercase)
        # for idx in range(len(symbs)):
        #     symbs[idx] = alphabet.pop(0)
        return symbs

    def eloss(self):
        """Выдает выражение функции потерь
            в формате Симпай для дальнейшей обработки"""
        return (self.func - self.y) ** 2
    def deriv_eloss(self, el:sy.core.add.Add):
        """Выдает выражение производной функции потерь
                    в формате Симпай для дальнейшей обработки"""
        #print('el = ', el)
        return self.eloss().diff(sy.simplify(el))
    @classmethod
    def answer(cls, f, xc = 0, yc = 0)->float:
        """Вовзращает числовое значение текущей функции"""
        expr=f.func
        for k, v in f.params.items():
            expr = expr.evalf(subs={sy.simplify(k): float(v)})
        x, y = sy.symbols('x y')
        expr=expr.evalf(subs={x: xc,y: yc})
        return expr
    @classmethod
    def function_x_nums(cls, f, params=None):
        """Возвращает выражение с числовыми параметрами для переданной функции"""
        f = Aproximator(str(f))
        if not params:
            params = f.params
        expr=f.func
        for k, v in params.items():
            expr = expr.evalf(subs={sy.simplify(k): round(float(v), 3)})
        return expr


class ML_module:

    def __init__(self, func, expr:Aproximator, lambdas:Dict):
        self.expr= expr
        self.xs =np.array([el/2 for el in range(-100, 100)])
        self.ys = np.array([func.subs({sy.symbols('x'):xc})+np.random.randint(-10, 10)
                            for xc in self.xs])
        self.lambdas = lambdas
        self.__drawing()

    def __drawing(self):
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(min(self.xs) - 5, max(self.xs) + 5)
        self.ax.grid(True)
        self.ax.scatter(self.xs, self.ys)
        self.ax.set_title('aproxy')
        self.line, = self.ax.plot(self.xs, self.ys, c='red')

    def learning(self, epochs = 100):
        for e in range(epochs):

            batch_size = len(self.xs) // 50
            rand_pt = np.random.randint(0, len(self.xs) - batch_size)
            for xc, yc in zip(self.xs[rand_pt:rand_pt + batch_size],
                              self.ys[rand_pt:rand_pt + batch_size]):

                for k, v in self.expr.params.items():
                    deriv_loss = Aproximator(str(self.expr.deriv_eloss(k)))
                    deriv_loss.params = self.expr.params
                    delta =Aproximator.answer(deriv_loss, xc, yc)
                    new_val = v-self.lambdas[k]*delta
                    self.expr.params = {k:new_val}
                    #print('params = ', self.expr.params)
            self.line.set_ydata([Aproximator.answer(self.expr, xc=xx)
                                 for xx in self.xs  ])# обновить данные линии
            if e%2==0:
                self.ax.set_title(Aproximator.function_x_nums(self.expr, self.expr.params))
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            time.sleep(0.002)
    def visualization(self):
        pass


# expr = Aproximator('ax+b+sin(x)')
# print(expr.define_params())
# print(expr.params)
# expr.params = {'a':3}
# print(expr.params)

# print(re.search(r'\w', 'a*x+b').group())
#
# expr1 = Aproximator('a*x+d')
# print(expr1)
# expr2 =Aproximator('a*x**2+b*sin(x)')
# expr3 = expr1+expr2
# print(expr3)
# print(expr3.define_params())
# expr3.params = {'a':3}
# print(expr3.params)

# expr1 = Aproximator('a*x+d')
# expr2 =Aproximator('a*x**2+b*sin(x)')
# expr3 = expr1+expr2

# print(expr3)
# print(expr3.eloss())
# for el in expr3.params.keys():
#     print('deriv({}) = '.format(el)+str(expr3.deriv_eloss(el)))
#
# a = expr3.deriv_eloss(sy.symbols('a'))
# print(Aproximator.answer(expr3, 1))
# print(expr3.params)
# func = Aproximator.function_x_nums(a, {'a': 10, 'b': 10, 'c': 10, 'd': 10})
# print('func = ', func)
# print(Aproximator.answer(Aproximator(str(func)), 1, 1))

func1 = sy.simplify('2*x**2+15')
lambdas1 = {'a':0.000001, 'b':0.0001, 'c':0.01}
#Expression_2, rand = 500
func2 = sy.simplify('10*x**3*sin(x)+x**4+5*x**2*tan(x)')
expr2 = Aproximator('a*x**4 + b*x**2+c*x+d')
lambdas2 = {'a':0.00000000000001, 'b':0.0000000001, 'c':0.0000001, 'd':0.000001}
#Expression3, rand = 50
func3 = sy.simplify('x*log(x+110, 2)+x**(2)/30')
expr3 = Aproximator('a*x**2+b*x+c')
lambdas3 ={'a':0.00000001, 'b':0.0001, 'c':0.001}

ml = ML_module(func3, expr3,  lambdas3)
ml.learning(100000)