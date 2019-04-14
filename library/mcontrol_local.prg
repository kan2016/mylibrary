' written by Kazutoshi KAN, Yui KISHABA, 2018
'
' Specification:
'   reverse-calculate exogenous variables listed in %exog2endo (mcontrol)
'   solve the model and calculate endogenous variables (solve)
'
' Note: 
'   Success in multi-variate case depends on the order of variables
'   i.e. the following may occur:
'     %exog2endo="a b", %endo2exog="x y" works well
'     %exog2endo="b a", %endo2exog="x y" fails
'
local subroutine mcontrol(model m, _
                          string %exog2endo , string %endo2exog, _
                          string %trajectory, scalar !EPSILON)
  svector exog2endo  = @wsplit(%exog2endo)
  svector endo2exog  = @wsplit(%endo2exog)
  svector trajectory = @wsplit(%trajectory)

  ' check input format
  if @rows(exog2endo) <> @rows(endo2exog ) or _
     @rows(exog2endo) <> @rows(trajectory) then
    @uiprompt("INCONSISTENT LEN of exog2endo, endo2exog," _
              +" trajectory! @mcontrol")
  endif

  ' set solve option
  m.scenario "actuals"
  m.solveopt(g=n, z=n, c=1e-6)

  ' solve without control
  if @len(@trim(%exog2endo)) = 0 then
    m.solve
    return
  endif

  ' solve with univariate control
  if @rows(exog2endo) = 1 then
    m.control {%exog2endo} {%endo2exog} {%trajectory}
    m.solve
    return
  endif

  ' solve with multivariate control
  scalar counter = 1 'for debug
  !isConverged = 0
  while !isConverged = 0
    ' preserve exog2endo as prev for convergence check
    for !n = 1 to @rows(exog2endo)
      %exog2endo = exog2endo(!n)
      copy {%exog2endo} prev_{%exog2endo}
    next

    ' control and solve
    for !n = 1 to @rows(exog2endo)
      %exog2endo  = exog2endo(!n)
      %endo2exog  = endo2exog(!n)
      %trajectory = trajectory(!n)
      m.control {%exog2endo} {%endo2exog} {%trajectory}
      m.solve
    next

    ' check convergence

    ' count length of current smpl range
    series tmp = 0
    scalar N = @ilast(tmp) - @ifirst(tmp) + 1

    for !n = 1 to @rows(exog2endo)
      ' calc sum of squared diff
      %exog2endo = exog2endo(!n)
      series ds = @abs({%exog2endo} - prev_{%exog2endo})
      stom(ds, dv) ' convert to vector
      scalar err = @sqrt(@inner(dv, dv))

      ' adjust scale
      scalar base = @mean(@abs({%exog2endo})) ' scale of series
      base = @recode(base>1e-5, base, 1e-5)   ' avoid exact 0 scale
      err  = err/(10^@floor(@log10(base)))    ' 1.23 * 10^N -> 1.23

      if err < !EPSILON * N then
        !isConverged = 1
        return
      endif
    next
    counter = counter + 1
  wend
endsub


'' *** sample code ***
'wfcreate a 2000 2005
'series x = -3
'series y = 3
'series z = 0
'series ey = 0
'series ez = 0.00001'1
'series xn = 0.000005 ' -2
'series yn = 0.0000000005 '-3
'
'' make model object
'model m
'm.append x = 0.8*y+0.2*z
'm.append y = 0.5*x-0.5*z+ey
'm.append z = ez
'
'!EPSILON = 1e-5
'smpl 2001 2002
'
'' find ey, ez s.t. x = xn, y = yn
'%exog2endo  = "ey ez"
'%endo2exog  = "x y"
'%trajectory = "xn yn"
'call mcontrol(m, %exog2endo, %endo2exog, %trajectory, !EPSILON)
'
'' find ey s.t. x = xn
'%exog2endo  = "ez"
'%endo2exog  = "x"
'%trajectory = "xn"
'call mcontrol(m, %exog2endo, %endo2exog, %trajectory, !EPSILON)
'
'' just solve
'%exog2endo  = ""
'%endo2exog  = ""
'%trajectory = "  "
'call mcontrol(m, %exog2endo, %endo2exog, %trajectory, !EPSILON)
