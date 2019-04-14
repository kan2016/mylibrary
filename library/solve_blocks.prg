' written by Kazutoshi KAN, 2018
'
' Dependency:
' from library/mcontrol.prg import mcontrol
'
' TODO:
' Automatically import library/mcontrol.prg using absolute path.
' Including mcontrol.prg before this prg in another place is needed so far.
'
' The difficulty comes from that @linepath = @runpath at this file outside
' subrounies. Thus, I couldn't get absolute path of mcontrol.prg.

' solve blocked model iteratively
subroutine solve_blocks(string %filepath_b, scalar !EPSILON)
  ' append blocked model to text object
  text _sq_mt
  _sq_mt.append(file) %filepath_b

  ' generate models and mcontrol & solve iteratively
  !_sq_k = 1
  !_sq_sizeB = @val(_sq_mt.@line(!_sq_k))

  for !_sq_b=1 to !_sq_sizeB
    ' set size of target block, endo2exog, exog2endo
    !_sq_k = !_sq_k + 1
    !_sq_sizeN = @val(_sq_mt.@line(!_sq_k))
    !_sq_k = !_sq_k + 1
    %_sq_exog2endo = @replace(_sq_mt.@line(!_sq_k), "exog2endo =", "")
    !_sq_k = !_sq_k + 1
    %_sq_endo2exog = @replace(_sq_mt.@line(!_sq_k), "endo2exog =", "")

    ' check feasibility
    if (!_sq_b = 1 or !_sq_b = !_sq_sizeB) and !_sq_sizeN > 0 then
      @uiprompt("*** INSOLVABLE PROBLEM! ***")
    endif

    ' make model object
    model _sq_m
    for !_sq_n=1 to !_sq_sizeN
      !_sq_k = !_sq_k + 1
      %_sq_eq = _sq_mt.@line(!_sq_k)
      !_sq_c =  @instr(%_sq_eq, ":")
      %_sq_eq = @right(%_sq_eq, @len(%_sq_eq)-!_sq_c)
      _sq_m.append {%_sq_eq}
    next

    ' make target trajectory
    %_sq_trajectory = ""
    if @len(@trim(%_sq_exog2endo)) <> 0 then
      for %v {%_sq_endo2exog}
        series _sq_{%v} = {%v}
        %_sq_trajectory = %_sq_trajectory+"_sq_"+%v+" "
      next
    endif

    ' mcontrol and solve
    call mcontrol(_sq_m, %_sq_exog2endo, %_sq_endo2exog, %_sq_trajectory, !EPSILON)
  next

  ' cleaning
  delete(noerr) _sq_*
endsub
