load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"

; Plot ONLY the NetCDF outputs prepared by CDO/NCO. No anomaly calculations
; or regional means are performed here. Source: EG's shared seminar example.
begin
  if (.not. isvar("input_dir")) then
    input_dir = "outputs/demo/monthly/cdo_nco"
  end if
  if (.not. isvar("output_dir")) then
    output_dir = "outputs/demo/monthly"
  end if

  ; Figure 1: Robinson map, fixed -0.2 to 0.4 degC range as in EG's revision.
  map_file = addfile(input_dir + "/tas_mean_monthly_anomaly_1979_2014.nc", "r")
  field = map_file->tas_anom(0,:,:)
  replace_ieeenan(field, 1.e20, 0)
  field@_FillValue = 1.e20
  wmap = gsn_open_wks("png", output_dir + "/01_mean_anomaly_map")
  mr = True
  mr@gsnMaximize = True
  mr@gsnAddCyclic = True
  mr@mpProjection = "Robinson"
  mr@mpCenterLonF = 0.0
  mr@mpShapeMode = "FixedAspect"
  mr@mpPerimOn = False
  mr@mpFillOn = False
  mr@mpOutlineOn = True
  mr@cnFillOn = True
  mr@cnFillMode = "RasterFill"
  mr@cnFillPalette = "MPL_coolwarm"
  mr@cnLinesOn = False
  mr@cnLineLabelsOn = False
  mr@cnLevelSelectionMode = "ManualLevels"
  mr@cnMinLevelValF = -0.2
  mr@cnMaxLevelValF = 0.4
  mr@cnLevelSpacingF = 0.025
  mr@lbOrientation = "Horizontal"
  mr@tiMainString = "Mean Monthly Temperature Anomaly, 1979-2014"
  mr@gsnLeftString = "Reference: 1981-2010 monthly climatology"
  mr@gsnRightString = "degC"
  map_plot = gsn_csm_contour_map(wmap, field, mr)

  ; Figure 2: unweighted Arctic monthly mean (65-90N), already calculated.
  line_file = addfile(input_dir + "/tas_arctic_monthly_anomaly_1979_2014.nc", "r")
  monthly = tofloat(ndtooned(line_file->tas_anom))
  dates = cd_calendar(line_file->time, 0)
  years = tofloat(dates(:,0)) + (tofloat(dates(:,1))-0.5)/12.0
  wline = gsn_open_wks("png", output_dir + "/02_arctic_monthly_anomaly")
  lr = True
  lr@gsnMaximize = True
  lr@xyLineThicknessF = 1.5
  lr@xyLineColor = "navy"
  lr@trXMinF = 1979.0
  lr@trXMaxF = 2015.0
  lr@gsnYRefLine = 0.0
  lr@tiXAxisString = "Year"
  lr@tiYAxisString = "Temperature anomaly (degC)"
  lr@tiMainString = "Arctic Monthly Temperature Anomalies, 65-90N"
  lr@gsnLeftString = "Unweighted grid-point mean"
  lr@gsnRightString = "1979-2014"
  line_plot = gsn_csm_xy(wline, years, monthly, lr)

  ; Figure 3: one equal-width stripe per year. Blue-white-red, symmetric
  ; +/-max(abs(annual)) normalization, matching matplotlib bwr in EG's code.
  annual_file = addfile(input_dir + "/tas_arctic_annual_anomaly_1979_2014.nc", "r")
  annual = tofloat(ndtooned(annual_file->tas_anom))
  stripe_count = dimsizes(annual)
  limit = max(abs(annual))
  if (limit.eq.0.0) then
    limit = 1.0
  end if
  wstripe = gsn_open_wks("png", output_dir + "/03_arctic_annual_stripes")
  sr = True
  sr@gsnDraw = False
  sr@gsnFrame = False
  sr@vpXF = 0.05
  sr@vpYF = 0.70
  sr@vpWidthF = 0.90
  sr@vpHeightF = 0.35
  sr@trXMinF = 0.0
  sr@trXMaxF = tofloat(stripe_count)
  sr@trYMinF = 0.0
  sr@trYMaxF = 1.0
  sr@tmXBOn = False
  sr@tmXTOn = False
  sr@tmYLOn = False
  sr@tmYROn = False
  sr@tmXBBorderOn = False
  sr@tmXTBorderOn = False
  sr@tmYLBorderOn = False
  sr@tmYRBorderOn = False
  stripes = gsn_blank_plot(wstripe, sr)
  draw(stripes)
  pr = True
  pr@gsEdgesOn = False
  do i = 0, stripe_count-1
    scaled = annual(i)/limit
    if (scaled.le.0.0) then
      pr@gsFillColor = (/1.0+scaled, 1.0+scaled, 1.0/)
    else
      pr@gsFillColor = (/1.0, 1.0-scaled, 1.0-scaled/)
    end if
    left = 0.05 + 0.90*tofloat(i)/tofloat(stripe_count)
    right = 0.05 + 0.90*tofloat(i+1)/tofloat(stripe_count)
    xx = (/left, right, right, left, left/)
    yy = (/0.35, 0.35, 0.70, 0.70, 0.35/)
    gsn_polygon_ndc(wstripe, xx, yy, pr)
  end do
  frame(wstripe)
  print("NCL wrote all three EG figures to " + output_dir)
  print("Arctic annual stripes: " + stripe_count + " years; symmetric limit +/-" + limit + " degC")
end
