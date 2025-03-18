def approximate(n: int):
    num_inside_unit_circle = 0

    for i in range(n):
        for j in range(n):
            x = i*2 + 1
            y = j*2 + 1
            d2 = x**2 + y**2
            if d2 <= 4*(n**2):
                num_inside_unit_circle += 1

    return 4*num_inside_unit_circle, n**2


if __name__ == "__main__":
    num, denom = approximate(5000)
    print(f"{num}/{denom} ~= {num/denom:.5f}")
