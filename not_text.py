# while True:
#     inp = input()
    
#     print_text = ''
#     q = 0
    
#     for i in inp:
#         print_text += i.upper() + ' '
#         q += 1 
#         if q % 5 == 0:
#             print_text += '  '
#         if q % 15 == 0:
#             print_text += '\n'
#     print(print_text)

while True:
    inp = input()
    
    print_text = ''
    q = 0
    p = 0
    
    for i in inp:
        p += 1
        q += 1
        print_text += i.upper()
        if p % 2 == 0:
            print_text += ' '
            if q % 10 == 0:
                print_text += '  '
            if q % 30 == 0:
                print_text += '\n'
            continue
   
         
        
    print(print_text)