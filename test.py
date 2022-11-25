lst1 = [46,24,17,36,9,24,35,21,47,45]
lst2 = [93,55,41,94,52,5,87,39,78,8]
lst = []
for i in range(len(lst1)):
    lst.append(lst1[i] / lst2[i])
keydict1 = dict(zip(lst1, lst))
keydict2 = dict(zip(lst2, lst))
lst1.sort(key=keydict1.get)
lst2.sort(key=keydict2.get)


