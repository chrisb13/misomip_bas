import cf
import numpy as np

f=cf.read("nple3.nc")
g=cf.read("isf_draft_meter.nc")

isf=g.select('ncvar%isf_draft').array
melt=f.select('ncvar%sowflisf').array[0]

oops=np.where( (melt.mask == False) & (isf < 5) )

#print melt[oops]
melt[oops]=1e-9
f.select('ncvar%sowflisf').insert_data(cf.Data(melt))

#melt=f.select('ncvar%sowflisf').array[0]
#print melt[oops]

cf.write(f, "nple3.nc")
