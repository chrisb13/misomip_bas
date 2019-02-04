import numpy

from netCDF4 import Dataset

def bisiclesToSTDGeom(inFileName,outFileName,resFactor):
  
  def smoothGeometry(bathy, bathyMask, draft, darftMask, filterSigma):
    import scipy.ndimage.filters as filters
  
    threshold = 0.01 # we won't normalize bathymetry or ice draft where the mask is below this threshold
    
    
    smoothedMask = filters.gaussian_filter(darftMask,filterSigma,mode='constant',cval=0.)
    draft = filters.gaussian_filter(draft*darftMask,filterSigma,mode='constant',cval=0.)
    mask = smoothedMask > threshold
    draft[mask] /= smoothedMask[mask]
  
    smoothedMask = filters.gaussian_filter(bathyMask,filterSigma,mode='constant',cval=0.)
    bathy = filters.gaussian_filter(bathy*bathyMask,filterSigma,mode='constant',cval=0.)
    mask = smoothedMask > threshold
    bathy[mask] /= smoothedMask[mask]
    
    return (bathy,draft)
  
  def mapField(field):
    newField = numpy.zeros((ny,nx))
    for yOffset in range(resFactor):
      for xOffset in range(resFactor):
        newField += field[yOffset::resFactor,xOffset::resFactor]
    newField /= resFactor**2
    return newField
    
  def readField(fieldName,tIndex,initVal):
    field = initVal*numpy.ones((inNy,inNx))
    if(len(t) == 0):
      field[:,0:xCount] = numpy.array(inFile.variables[fieldName])[:,xOffset:]
    else:
      field[:,0:xCount] = numpy.array(inFile.variables[fieldName])[tIndex,:,xOffset:]
    return field

  def createVar(fieldName):
    if(len(t) == 0):
      var = outFile.createVariable(fieldName,'f8',('y','x'))
    else:
      var = outFile.createVariable(fieldName,'f8',('t','y','x'))
    return var

  def writeField(field,var,tIndex):
    if(len(t) == 0):
      var[:,:] = field
    else:
      var[tIndex,:,:] = field

  zMin = -720 #m
  minIceThickness = 100 #m
  
  calvingX = 640 #km
  xMax = 800 #km
  
  densityRatio = 0.9
  
  inNx = 480
  inNy = 80
  
  inFile = Dataset(inFileName,'r')
  x = numpy.array(inFile.variables['x'])[:]
  y = numpy.array(inFile.variables['y'])[:]
  
  try:
    t = numpy.array(inFile.variables['t'])[:]
    nt = len(t)
  except KeyError:
    t = []
    nt = 1
  
  deltaX = x[1]-x[0]
  deltaY = y[1]-y[0]
  
  xOffset = int(xMax/(1e-3*deltaX)-inNx)
  print xOffset
  
  xCount = len(x)-xOffset
  print deltaX
  print x[xOffset]
  inX = x[xOffset] + deltaX*numpy.arange(inNx)
  inY = y[0] + deltaY*(numpy.arange(inNy))

  nx = inNx/resFactor
  ny = inNy/resFactor
  
  deltaX = resFactor*(inX[1]-inX[0])
  deltaY = resFactor*(inY[1]-inY[0])
  
  
  (xIndices,yIndices) = numpy.meshgrid(0.5+numpy.arange(nx),0.5+numpy.arange(ny))
    
  filterSigma = 1.0*resFactor

  x = numpy.zeros((nx))
  for index in range(resFactor):
    x += inX[index::resFactor]
  x /= resFactor
  
  y = numpy.zeros((ny))
  for index in range(resFactor):
    y += inY[index::resFactor]
  y /= resFactor
    
    
  outFile = Dataset(outFileName,'w', format='NETCDF3_CLASSIC')
  outFile.createDimension('x', nx)
  outFile.createDimension('y', ny)
  xVar = outFile.createVariable('x','f8',('x',))
  xVar[:] = x[:]
  xVar.units = 'm'
  yVar = outFile.createVariable('y','f8',('y',))
  yVar[:] = y[:]
  yVar.units = 'm'
  if(len(t) > 0):
    outFile.createDimension('t', len(t))
    tVar = outFile.createVariable('t','f8',('t',))
    tVar[:] = t[:]*365.*24.*60.*60.
    tVar.units = 's'
    tVar.description = 'time from the start of the experiment'

  surfVar = createVar('Z_surface')
  surfVar.units = 'm'
  surfVar.description = 'ice surface elevation'
  draftVar = createVar('Z_bottom')
  draftVar.units = 'm'
  draftVar.description = 'elevation of ice bottom (depth of ice-ocean interface)'
  bathyVar = createVar('Z_base')
  bathyVar.units = 'm'
  bathyVar.description = 'elevation of bedrock (bathymetry)'
  floatVar = createVar('floatingIceFranction')
  floatVar.units = 'unitless'
  floatVar.description = 'fraction of a cell that contains floating ice'
  groundedVar = createVar('groundedIceFraction')
  groundedVar.units = 'unitless'
  groundedVar.description = 'fraction of a cell that contains grounded ice'
  openVar = createVar('openOceanFraction')
  openVar.units = 'unitless'
  openVar.description = 'fraction of a cell that contains open ocean (with no ice)'
      
  
  for tIndex in range(nt):
    print tIndex
  
    inSurf = readField('Z_surface',tIndex,0.)
    inDraft = readField('Z_bottom',tIndex,0.)
    inBathy = readField('Z_base',tIndex,zMin)  
          
    (X,Y) = numpy.meshgrid(inX*1e-3,inY*1e-3)
    
    # take care of calving
    mask = X > calvingX
    inSurf[mask] = 0
    inDraft[mask] = 0
    
    iceThickness = inSurf-inDraft
    
    grounded_mask = densityRatio*iceThickness > -inBathy
    floating_mask = numpy.logical_and(inDraft < 0,numpy.logical_not(grounded_mask))
    
    ##ISOMIP "CALVING" NOT WANTED FOR COUPLED MISOMIP
    ##mask = numpy.logical_and(floating_mask, iceThickness < minIceThickness)
    ##inSurf[mask] = 0
    ##inDraft[mask] = 0
    
    floating_mask = numpy.logical_and(inDraft < 0,numpy.logical_not(grounded_mask))
    
    #open_ocean_mask = numpy.logical_or(floating_mask,grounded_mask)==False
    
    #make bathy no deeper than max depth
    inBathy[inBathy < zMin] = zMin
    
    #oceanMask = grounded_mask==False
    
    inFloatingFraction = numpy.array(floating_mask,float)
    inGroundedFraction = numpy.array(grounded_mask,float)
    
  
    (bathy,draft) = smoothGeometry(inBathy, 1.-inGroundedFraction, inDraft, 
                                   inFloatingFraction, filterSigma)
  
    (groundedBathy,groundedDraft) = smoothGeometry(inBathy, inGroundedFraction, inDraft, 
                                   inGroundedFraction, filterSigma)
    
    threshold = 0.01 # we won't normalize bathymetry or ice draft where the mask is below this threshold
    
    groundedFraction = mapField(grounded_mask)
    floatingFraction = mapField(floating_mask)
    
    # if there's barely any floating ice or open ocean, make it land
    mask = floatingFraction < threshold
    floatingFraction[mask] = 0.
    mask = groundedFraction > 1. - threshold
    groundedFraction[mask] = 1.
    openOceanFraction = 1. - (groundedFraction+floatingFraction)
    oceanFraction = 1. - groundedFraction
    
    
    surf = mapField(inSurf)
    mask = numpy.logical_and(oceanFraction >= threshold,floatingFraction < threshold)
    surf[mask] = 0.
    
    draft = mapField(draft*floating_mask)
    bathy = mapField(bathy*(1.-grounded_mask))
  
    groundedDraft = mapField(groundedDraft*grounded_mask)
    groundedBathy = mapField(groundedBathy*grounded_mask)
    
    mask = floatingFraction >= threshold
    draft[mask] /= floatingFraction[mask]
    mask = oceanFraction < threshold
    draft[mask] = groundedDraft[mask]/groundedFraction[mask]
    mask = numpy.logical_and(oceanFraction >= threshold,floatingFraction < threshold)
    draft[mask] = 0.
    
    mask = oceanFraction >= threshold
    bathy[mask] /= oceanFraction[mask]
    mask = mask==False
    bathy[mask] = groundedBathy[mask]/groundedFraction[mask]
    
    writeField(surf,surfVar,tIndex)
    writeField(draft,draftVar,tIndex)
    writeField(bathy,bathyVar,tIndex)
    writeField(floatingFraction,floatVar,tIndex)
    writeField(groundedFraction,groundedVar,tIndex)
    writeField(openOceanFraction,openVar,tIndex)
    
  
  inFile.close()
  outFile.close()
  
  
inFileName = 'bplex.nc'
outFileName = 'bathy_isfdraft.nc'
resFactor=2
bisiclesToSTDGeom(inFileName,outFileName,resFactor)
