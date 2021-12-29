#вывод результатов работы программы
def main():
    a = int(input("Введите число а: "))
    n = int(input("Введите число n, n должно быть больше a: "))
    ka = int(input("Введите число ka: "))
    Ya = a**ka % n
    print ("Ваш Ya = ", Ya)
    Yb = int(input("Введите число Yb, которое прислал собеседник: "))
    K = (a**(Ya*Yb))%n
    print ("Ваш общий ключ: ", K)

if __name__ == "__main__":
    main()

