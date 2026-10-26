"""Session 2 - T568A / T568B pin maps and a simulated cable wire-map tester.

A real cable tester sends a signal down each of the 8 wires and reports where it
arrives. Here we describe a cable as "end A standard" + "end B standard" (or a
custom pin map with faults) and classify it like a tester would.
Run:  python session-02_wiremap.py
"""

T568A = ["white/green", "green", "white/orange", "blue",
         "white/blue", "orange", "white/brown", "brown"]
T568B = ["white/orange", "orange", "white/green", "blue",
         "white/blue", "green", "white/brown", "brown"]


def pin_map(end_a: list[str], end_b: list[str]) -> list[int | None]:
    """For each pin 1-8 on end A, which pin on end B carries the same wire colour?"""
    result = []
    for colour in end_a:
        result.append(end_b.index(colour) + 1 if colour in end_b else None)
    return result


def classify(mapping: list[int | None]) -> str:
    straight = list(range(1, 9))
    crossover = [3, 6, 1, 4, 5, 2, 7, 8]       # 1<->3 and 2<->6 swapped
    rollover = list(range(8, 0, -1))           # console cable: 1<->8, 2<->7 ...
    if None in mapping:
        return "OPEN: pin(s) " + ", ".join(str(i + 1) for i, m in enumerate(mapping) if m is None)
    if mapping == straight:
        return "straight-through (PC to switch)"
    if mapping == crossover:
        return "crossover (switch to switch, PC to PC on old gear)"
    if mapping == rollover:
        return "rollover (console cable)"
    # pairs 1-2, 3-6, 4-5, 7-8 must stay together or the twist is lost
    pairs = [(1, 2), (3, 6), (4, 5), (7, 8)]
    for a, b in pairs:
        if {mapping[a - 1], mapping[b - 1]} not in [{a, b}, {1, 2}, {3, 6}, {4, 5}, {7, 8}]:
            return f"SPLIT PAIR or mis-wire around pins {a}/{b}"
    return "REVERSED/CROSSED pair: " + str(mapping)


if __name__ == "__main__":
    print("Pin  T568A           T568B")
    for i, (a, b) in enumerate(zip(T568A, T568B), 1):
        mark = "  <- differs" if a != b else ""
        print(f" {i}   {a:<15} {b:<15}{mark}")

    print("\nTesting cables:")
    tests = {
        "B to B": (T568B, T568B),
        "A to A": (T568A, T568A),
        "A to B": (T568A, T568B),
        "B to reversed B": (T568B, list(reversed(T568B))),
    }
    broken = T568B.copy()
    broken[5] = "cut"                         # green conductor broken at pin 6
    tests["B with cut green wire"] = (T568B, broken)
    swapped = T568B.copy()
    swapped[2], swapped[3] = swapped[3], swapped[2]   # installer swapped pins 3 and 4
    tests["B with pins 3/4 swapped"] = (T568B, swapped)

    for name, (a, b) in tests.items():
        m = pin_map(a, b)
        print(f"  {name:<24} map={m}  -> {classify(m)}")
