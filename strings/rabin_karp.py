"""
Rabin-Karp string search algorithm.

Uses rolling hash to find all occurrences of a pattern in a text in O(n + m)
average time, compared to O(n * m) for naive search.

Reference: https://en.wikipedia.org/wiki/Rabin%E2%80%93Karp_algorithm
"""

from __future__ import annotations

BASE = 256   # number of characters in the input alphabet
MOD = 101    # a prime number to reduce hash collisions


def rabin_karp(text: str, pattern: str) -> list[int]:
    """
    Return all starting indices where pattern occurs in text.

    >>> rabin_karp("AABAACAADAABAABA", "AABA")
    [0, 9, 12]
    >>> rabin_karp("hello world", "world")
    [6]
    >>> rabin_karp("aaaaaa", "aaa")
    [0, 1, 2, 3]
    >>> rabin_karp("abc", "xyz")
    []
    >>> rabin_karp("", "a")
    []
    >>> rabin_karp("a", "")
    []
    """
    n = len(text)
    m = len(pattern)
    results: list[int] = []

    if m == 0 or n == 0 or m > n:
        return results

    # h = BASE^(m-1) % MOD
    h = pow(BASE, m - 1, MOD)

    pattern_hash = 0
    window_hash = 0

    for i in range(m):
        pattern_hash = (BASE * pattern_hash + ord(pattern[i])) % MOD
        window_hash = (BASE * window_hash + ord(text[i])) % MOD

    for i in range(n - m + 1):
        if pattern_hash == window_hash:
            # Hash match — verify character by character to rule out collision
            if text[i : i + m] == pattern:
                results.append(i)

        if i < n - m:
            # Roll the hash: remove leading character, add next character
            window_hash = (
                BASE * (window_hash - ord(text[i]) * h) + ord(text[i + m])
            ) % MOD
            if window_hash < 0:
                window_hash += MOD

    return results


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    text = "AABAACAADAABAABA"
    pattern = "AABA"
    matches = rabin_karp(text, pattern)
    print(f"Text:    {text}")
    print(f"Pattern: {pattern}")
    print(f"Found at indices: {matches}")
