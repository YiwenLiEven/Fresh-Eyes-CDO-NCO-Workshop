load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"

begin
  input_file = getenv("STRIPES_INPUT")
  output_base = getenv("STRIPES_OUTPUT_BASE")
  plot_title = getenv("STRIPES_TITLE")

  if (input_file.eq."" .or. output_base.eq."") then
    print("Set STRIPES_INPUT and STRIPES_OUTPUT_BASE before running this script.")
    exit
  end if

  if (.not. isstring(plot_title)) then
    plot_title = "Global Temperature Anomaly Stripes (1850-2014)"
  end if

  source = addfile(input_file, "r")
  anomaly = tofloat(ndtooned(source->tas_anom))
  count = dimsizes(anomaly)

  workstation = gsn_open_wks("png", output_base)
  gsn_define_colormap(workstation, "BlueWhiteOrangeRed")

  plot_resources = True
  plot_resources@gsnDraw = False
  plot_resources@gsnFrame = False
  plot_resources@vpWidthF = 0.90
  plot_resources@vpHeightF = 0.24
  plot_resources@trXMinF = 0.0
  plot_resources@trXMaxF = tofloat(count)
  plot_resources@trYMinF = 0.0
  plot_resources@trYMaxF = 1.0
  plot_resources@tmXBOn = False
  plot_resources@tmXTOn = False
  plot_resources@tmYLOn = False
  plot_resources@tmYROn = False
  plot_resources@tiMainString = plot_title
  plot_resources@tiMainFontHeightF = 0.018

  plot = gsn_blank_plot(workstation, plot_resources)
  draw(plot)
  polygon_resources = True
  polygon_resources@gsEdgesOn = False

  color_count = 252
  color_min = -2.0
  color_max = 2.0

  do index = 0, count - 1
    fraction = (anomaly(index) - color_min) / (color_max - color_min)
    if (fraction.lt.0.0) then
      fraction = 0.0
    end if
    if (fraction.gt.1.0) then
      fraction = 1.0
    end if
    color_index = 2 + toint(fraction * tofloat(color_count - 1))
    polygon_resources@gsFillColor = color_index
    left = 0.05 + 0.90*tofloat(index)/tofloat(count)
    right = 0.05 + 0.90*tofloat(index+1)/tofloat(count)
    x = (/left, right, right, left, left/)
    y = (/0.56, 0.56, 0.80, 0.80, 0.56/)
    gsn_polygon_ndc(workstation, x, y, polygon_resources)
  end do
  frame(workstation)
  print("NCL stripes written to " + output_base + ".png")
end
