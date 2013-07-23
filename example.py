from YMR import *
new = YMReader("12345678","123456ABCDEFGHIJKLMNOPRQSTUVWXYZ") # This is not correct data, of course
print new.GetCounters()

print new.GetSummary(new.GetCounters()[0]["ID"])
