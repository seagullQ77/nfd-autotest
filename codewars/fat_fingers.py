def fat_fingers(string):
    for i in string:
        if i == 'a':
            string.replace(i, '')

        if i == 'A':
            string.replace(i, '')

    return  # broken string