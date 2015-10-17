from __future__ import division

def lcs(str1, str2):
  # If either string is empty, stop
  if len(str1) == 0 or len(str2) == 0:
    return []

  # First property
  if str1[-1] == str2[-1]:
    return lcs(str1[:-1], str2[:-1]).append(str1[-1])

  # Second proprerty
  # Last of str1 not needed:
  t1 = lcs(str1[:-1], str2)
  # Last of str2 is not needed
  t2 = lcs(str1, str2[:-1])
  if len(t1) > len(t2):
    return t1
  else:
    return t2



if __name__ == "__main__":

    r = 'At least 13 sailors have been killed in a mine attack on a convoy in north-western Sri Lanka officials say'.split(' ')

    s1 = 'Tamil Tiger guerrillas have blown up a navy bus in northeastern Sri Lanka killing at least 10 sailors and wounding 17 others'.split(' ')
    s2 = 'Blasts blamed on Tamil Tiger rebels killed 13 people in Wednesday in Sri Lanka \'s northeast and dozens more were injured officials said, raising fears planned peace talks may be cancelled and a civil war could restart'.split(' ')

    print lcs(r,s1)

    r = set(r)
    s1 = set(s1)
    s2 = set(s2)

    s1tp = list(r & s1)
    s2tp = list(r & s2)




    print len(s1tp), len(s1)
    print len(s1tp) / len(s1)

    print len(s2tp), len(s2)
    print len(s2tp)/len(s2)

    s1fn = r - s1
    s2fn = r - s2

    print len(s1tp), len(s1fn)
    print (len(s1tp)) / (len(s1tp)+len(s1fn))

    print len(s2tp), len(s2fn)
    print (len(s2tp)) / (len(s2tp)+len(s2fn))

    print len(s1tp)/ len(r)
    print len(s2tp)/ len(r)
