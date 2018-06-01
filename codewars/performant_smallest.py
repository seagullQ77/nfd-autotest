def performant_smallest(arr, n):
    s = arr[:n]

    for i in range(n, len(arr)):
        maxs = max(s)
        if maxs > arr[i]:
            s.remove(maxs)
            s.append(arr[i])
    return s

