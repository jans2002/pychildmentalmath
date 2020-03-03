import os
import random
from wcwidth import wcswidth as ww
import docx
from docx.shared import Pt



def rpad(s, n, c=' '):
    # rpad('你好', 6) => '\u4f60\u597d  '
    return s + (n-ww(s)) * c

def get_mul_expr():
    expr=random.choice("23456789")
    expr+="*"
    expr+=random.choice("23456789")
    return expr

def get_div_expr():
    expr=random.randint(1,99)
    expr+="*"
    expr+=random.choice("123456789")
    return expr

def get_ps_expr():
    while True:
        n1=str(random.randint(1,99))
        n1tail=int(n1[-1:])
        operator=random.choice("+-")
        n2=str(random.randint(1,99))
        n2tail=int(n2[-1:])
        expr = n1+operator+n2
        if operator=='-' and n1tail>=n2tail:
            continue
        elif operator=='+' and n1tail+n2tail<10 :
            continue
        result = eval(expr)
        if result>=0 and result<=100:
            return expr

def get_comb_expr():
    while True:
        expr_final=""
        mode=random.choice("+*")
        if mode=='+':
            while True:
                expr_final = get_ps_expr()
                operator=random.choice("+-")
                n2=str(random.randint(1,99))
                n1 = eval(expr_final)
                #print("got mode +/-:"+expr_final)
                n1tail=int(str(n1)[-1:])
                n2tail=int(n2[-1:])
                if operator=='-' and n1tail>=n2tail:
                    continue
                elif operator=='+' and n1tail+n2tail<10 :
                    continue
                expr_final += operator+n2
                result =  eval(expr_final)

                #add difficult level
                if random.random()>0.5 and result>=0 and result<=100:
                    return expr_final
                elif random.random()<0.5 and result>10 and result<=110:
                    return expr_final

        elif mode=='*' :
            while True:
                position=random.choice("fb")
                expr_final = get_mul_expr()
                if position=='f':
                    n1 = str(eval(expr_final))
                    n1tail=int(str(n1)[-1:])
                    n2=str(random.randint(2,99))
                    n2tail=int(n2[-1:])
                    operator=random.choice("+-")
                    if operator=='-' and n1tail>=n2tail:
                        continue
                    elif operator=='+' and n1tail+n2tail<10 :
                        continue
                    expr_final=expr_final+operator+n2
                else:
                    n1=str(random.randint(2,99))
                    n1tail=int(n1[-1:])
                    n2 = str(eval(expr_final))
                    n2tail=int(str(n2)[-1:])
                    operator=random.choice("+-")
                    if operator=='-' and n1tail>=n2tail:
                        continue
                    elif operator=='+' and n1tail+n2tail<10 :
                        continue
                    expr_final=n1+operator+expr_final
                result =  eval(expr_final)
                #add difficult level
                if random.random()>0.5 and result>=0 and result<=100:
                    return expr_final
                elif random.random()<0.5 and result>10 and result<=110:
                    return expr_final

def write_docx_file(filename,content):
    doc = docx.Document()
    para_obj = doc.add_paragraph(content)
    para_obj.style.paragraph_format.line_spacing=Pt(24)
    doc.save(filename)

#main entry
lines =""
TOTAL_PAGES=10
for i in range(1,TOTAL_PAGES*100+1):
    expr = get_comb_expr()
    expr = expr.replace("*","×")+"="
    expr = rpad(expr,15)
    if i>1 and i % 4 ==0:
        print(expr)
        lines+=expr+"\n"
    else:
        print(expr,end="\t")
        lines+=expr+"\t\t"
    if i>1 and i % 100==0 and i<TOTAL_PAGES*100:
        lines+="\r\n"

write_docx_file(r"test.docx",lines)
