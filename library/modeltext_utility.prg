' written by Kazutoshi KAN, 2018
'
' *** model object utility *** 
'append_file       (model m, %filename)
'append_text       (model m, text mt)
'
' *** text object utility *** 
'append_equation   (text mt, %newEquation)
'drop_equation     (text mt, %dropSymbol)
'insert_equation   (text mt, %insertEquation, %afterSymbol)
'
'extract_expression(text mt)
'extract_equation  (text mt)
'
' note: ignore white spaces, empty lines, comments('***)
' note: carefully preserve EOF symbol in the last line of text object
' note: use suffix to avoid duplicate names

'**************************************************************
'                  model object utility
'**************************************************************

' load modeltext file and append to model object
subroutine append_file(model m, string %filename)
  text tmpAFTM
  tmpAFTM.clear
  tmpAFTM.append(file) {%filename}
  call append_text(m, tmpAFTM)
  delete tmpAFTM
endsub

' append text object to model object
subroutine append_text(model m, text mt)
  text tmpATTM
  tmpATTM.clear
  copy mt tmpATTM
  call extract_expression(tmpATTM)
  !sizeATTM = tmpATTM.@linecount-1
    for !idxATTM = 1 to !sizeATTM
      %lineATTM = tmpATTM.@line(!idxATTM)
      m.append {%lineATTM}
      next
  delete tmpATTM
endsub


'**************************************************************
'                text object utility
'**************************************************************

' append equation at the last line or replace existing one
' usage: append_equation(mt, "X:X=X(-1)")
subroutine append_equation(text mt, string %newEquation)
  ' extract target symbol from "symbol:equation"
  %newEquation = @replace(%newEquation, " ","")
  !colonAE     = @instr(%newEquation, ":")
  if !colonAE = 0 then
    @uiprompt("Error: """+%newEquation+""" doesn't" _
              +"contain a colon(:)! @appendEquation")
    stop
  endif
  %targetSymbolAE = @left(%newEquation, !colonAE-1)

  ' copy original equations to empty mt orderly
  ' copy the target equation if symbol matches 
  !isSuccessfullyReplaced = 0
  text tmpAE
  copy mt tmpAE
  mt.clear

  !sizeAE = tmpAE.@linecount-1
  for !idxAE = 1 to !sizeAE
    ' extract symbol
    %lineAE   = tmpAE.@line(!idxAE)          ' X :X = X(-1)+V
    %lineAE   = @replace(%lineAE, " ","")
    !colonAE  = @instr(%lineAE, ":")
    %symbolAE = ""
    if !colonAE > 0 then
      %symbolAE = @left(%lineAE, !colonAE-1) ' X
    endif
    if %symbolAE = %targetSymbolAE then
      ' copy target equation since symbol matches
      mt.append {%newEquation}
      !isSuccessfullyReplaced = 1
    else
      ' copy original equation
      mt.append {%lineAE}
    endif
  next

  ' append target at last
  if !isSuccessfullyReplaced = 0 then
    mt.append {%newEquation}
  endif

  ' preserve last line
  %lastLineAE = tmpAE.@line(!sizeAE+1)
  mt.append {%lastLineAE}

  mt.save mt
  close mt
  delete tmpAE
endsub


' drop equation
' usage: drop_equation(mt, "X")
subroutine drop_equation(text mt, string %dropSymbol)
  ' cleaning
  %dropSymbolDE = @replace( %dropSymbol," ", "")

  ' copy equations to empty mt object orderly
  ' skip if symbol matches the target
  !isSuccessfullyDropped = 0
  text tmpDE
  copy mt tmpDE
  mt.clear

  !sizeDE = tmpDE.@linecount
  for !idxDE = 1 to !sizeDE
    ' extract symbol
    %lineDE   = tmpDE.@line(!idxDE)          ' X :X = X(-1)+V
    %lineDE   = @replace(%lineDE, " ","")
    !colonDE  = @instr(%lineDE, ":")
    %symbolDE = ""
    if !colonDE > 0 then
      %symbolDE = @left(%lineDE, !colonDE-1) ' X
    endif
    ' skip the drop target
    if %symbolDE = %dropSymbolDE then
      !isSuccessfullyDropped = 1
    else
      mt.append {%lineDE}
    endif
  next

  mt.save mt
  close mt

  ' ERROR: invalid drop target
  if !isSuccessfullyDropped = 0 then
    @uiprompt("Error: Cannot find drop target of """_
              +%dropSymbolDE+""" @dropEquation")
    stop
  endif
endsub


' insert equation at indicated location
' usage: insert_equation(mt, "X:X=X(-1)+V", "Y")
subroutine insert_equation(text mt, string %insertEquation, _
                                    string %afterSymbol)
  ' cleaning
  %insertEquation = @replace(%insertEquation, " ", "")
  %afterSymbol = @replace(%afterSymbol, " ", "")

  ' extract target symbol
  !colonIE = @instr(%insertEquation, ":")
  if !colonIE = 0 then
    @uiprompt("Error: """+%insertEquation+""" doesn't"+
              " contain a colon(:)! @insertEquation")
    stop
  endif
  %insertSymbolIE = @left(%insertEquation, !colonIE-1)

  ' copy equations to empty mt object orderly
  ' insert equation if find indicated location
  !isSuccessfullyInserted = 0
  text tmpIE
  tmpIE.clear
  copy mt tmpIE
  mt.clear

  !sizeIE = tmpIE.@linecount-1
  for !idxIE = 1 to !sizeIE
    ' extract symbol
    %lineIE   = tmpIE.@line(!idxIE)          ' X :X = X(-1)+V
    %lineIE   = @replace(%lineIE, " ","")
    !colonIE  = @instr(%lineIE, ":")
    %symbolIE = ""
    if !colonIE > 0 then
      %symbolIE = @left(%lineIE, !colonIE-1) ' X
    endif
    ' ERROR: duplicate equation
    if %insertSymbolIE = %symbolIE then
      @uiprompt("Error: Duplicate equation of """_
                +%insertSymbolIE+"""! @insertEquation")
      stop
    endif
    mt.append {%lineIE}

    ' insert after the afterSymbol
    if %symbolIE = %afterSymbol then         
      mt.append {%insertEquation}
      !isSuccessfullyInserted = 1
    endif
  next

  ' append at the last if afterSymbold is not indicated
  if %afterSymbol = "" then
    !isSuccessfullyInserted = 1
    mt.append {%insertEquation}
  endif

  ' preserve last line
  %lastLineIE = tmpIE.@line(!sizeIE+1)
  mt.append {%lastLineIE}

  mt.save mt
  close mt

  ' ERROR: invalid location of insertion
  if !isSuccessfullyInserted = 0 then
    @uiprompt("Error: Cannot find insert location of """_
              +%afterSymbol+""" @insertEquation")
    stop
  endif
  delete tmpIE
endsub


' extract equation EXCLUDING symbol e.g. "X=Y+V"
' note: mt can be directly loaded by model object
subroutine extract_expression(text mt)
  call extract_model(mt, "expression")
endsub

' extract equation INCLUDING symbol e.g. "X:X=Y+V"
' note: mt share the same format with Q-JEM model text file
subroutine extract_equation(text mt)
  call extract_model(mt, "equation")
endsub

' extract equation EXCLUDING/INCLUDING symbol
' note: delete white spaces, empty lines, comments ('***)
' note: only called by extractExpression or extractEquations
' usage: extract_model(mt, "expression") ->   X=X(-1)+V
'        extract_model(mt, "equation")   -> X:X=X(-1)+V
subroutine extract_model(text mt, string %target)
  text tmpEM
  tmpEM.clear
  copy mt tmpEM
  mt.clear

  !sizeEM = tmpEM.@linecount-1
  for !idxEM = 1 to !sizeEM
    ' cleaning
    %lineEM  = tmpEM.@line(!idxEM)
    %lineEM  = @replace(%lineEM, " ", "")
    ' delete comment e.g. '****
    !sqEM    = @instr(%lineEM, "'")
    if !sqEM > 0 then
      %lineEM  = @left(%lineEM, !sqEM-1)
    endif
    ' copy equation including/excluding symbol
    ' skip empty line
    !colonEM = @instr(%lineEM, ":")
    !isNotEmptyEM   = @len(%lineEM)>0       ' 1 if line is not empty
    !isEquationEM   = !colonEM > 0          ' 1 if line is equation
    if !isNotEmptyEM and !isEquationEM then
      if %target="expression" then
        ' append EXCLUDING symbol e.g. X=X(-1)+V
        %expressionEM = @right(%lineEM, @len(%lineEM) - !colonEM)
        mt.append {%expressionEM}
      else
        ' %target = "equation" by default
        ' append INCLUDING symbol e.g. X:X=X(-1)+V
        mt.append {%lineEM}
      endif
    endif
  next

  ' preserve last line
  %lastLineEM = tmpEM.@line(!sizeEM+1)
  mt.append {%lastLineEM}

  delete tmpEM
endsub
