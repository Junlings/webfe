from import_marc_t16 import post_t16
##
p1 = post_t16("small_dia_job1.t16")


input1 = ['time',2]
input2 = ['ns','Displacement X',1,2]
print p1.postset_str(*input2)
print 1