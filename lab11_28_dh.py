def cipher(a, n, ka, kb):
    a = int(a)
    n = int(n)
    ka = int(ka)
    Ya = a**ka % n
    print("Ваш Ya = ", Ya)
    kb = int(kb)
    Yb = a**kb % n
    print("Ваш Yb = ", Yb)
    Ka = (Yb**ka) % n
    Kb = (Ya**kb) % n
    print("Первый получившийся ключ = ", Ka)
    print("Второй получившийся ключ = ", Kb)
    if Ka == Kb:
        K = Ka
        print("Ваш общий ключ", K)
    else:
        print("Ключи не сошлись")
