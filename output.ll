; ModuleID = "S:\Hackatones\Primer Hackaton Código Facilito\CoCody-Compiler\codegen.py"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

define void @"main"()
{
entry:
  store i32 5, i32* @"n"
  store i32 0, i32* @"top"
  %".4" = load i32, i32* @"top"
  %".5" = getelementptr [20 x i32], [20 x i32]* @"pila", i32 0, i32 %".4"
  store i32 0, i32* %".5"
  %".7" = load i32, i32* @"top"
  %".8" = add i32 %".7", 1
  store i32 %".8", i32* @"top"
  %".10" = load i32, i32* @"top"
  %".11" = load i32, i32* @"n"
  %".12" = sub i32 %".11", 1
  %".13" = getelementptr [20 x i32], [20 x i32]* @"pila", i32 0, i32 %".10"
  store i32 %".12", i32* %".13"
  %".15" = load i32, i32* @"top"
  %".16" = add i32 %".15", 1
  store i32 %".16", i32* @"top"
  br label %"cond_block"
cond_block:
  %".19" = load i32, i32* @"top"
  %".20" = icmp sgt i32 %".19", 0
  br i1 %".20", label %"loop", label %"afterloop"
loop:
  %".22" = load i32, i32* @"top"
  %".23" = sub i32 %".22", 1
  store i32 %".23", i32* @"top"
  %".25" = load i32, i32* @"top"
  %".26" = getelementptr [20 x i32], [20 x i32]* @"pila", i32 0, i32 %".25"
  %".27" = load i32, i32* %".26"
  store i32 %".27", i32* @"high"
  %".29" = load i32, i32* @"top"
  %".30" = sub i32 %".29", 1
  store i32 %".30", i32* @"top"
  %".32" = load i32, i32* @"top"
  %".33" = getelementptr [20 x i32], [20 x i32]* @"pila", i32 0, i32 %".32"
  %".34" = load i32, i32* %".33"
  store i32 %".34", i32* @"low"
  %".36" = load i32, i32* @"high"
  %".37" = getelementptr [5 x i32], [5 x i32]* @"lista", i32 0, i32 %".36"
  %".38" = load i32, i32* %".37"
  store i32 %".38", i32* @"pivote"
  %".40" = load i32, i32* @"low"
  %".41" = sub i32 %".40", 1
  store i32 %".41", i32* @"i"
  %".43" = load i32, i32* @"low"
  %".44" = load i32, i32* @"high"
  %".45" = sub i32 %".44", 1
  store i32 %".43", i32* @"j"
  br label %"cond"
afterloop:
  %".140" = load i32, i32* @"n"
  %".141" = sub i32 %".140", 1
  store i32 0, i32* @"k"
  br label %"cond.1"
cond:
  %".48" = load i32, i32* @"j"
  %".49" = icmp sle i32 %".48", %".45"
  br i1 %".49", label %"loop.1", label %"afterloop.1"
loop.1:
  %".51" = load i32, i32* @"j"
  %".52" = getelementptr [5 x i32], [5 x i32]* @"lista", i32 0, i32 %".51"
  %".53" = load i32, i32* %".52"
  %".54" = load i32, i32* @"pivote"
  %".55" = icmp slt i32 %".53", %".54"
  br i1 %".55", label %"then", label %"ifcont"
afterloop.1:
  %".78" = load i32, i32* @"i"
  %".79" = add i32 %".78", 1
  %".80" = getelementptr [5 x i32], [5 x i32]* @"lista", i32 0, i32 %".79"
  %".81" = load i32, i32* %".80"
  store i32 %".81", i32* @"temp2"
  %".83" = load i32, i32* @"i"
  %".84" = add i32 %".83", 1
  %".85" = load i32, i32* @"high"
  %".86" = getelementptr [5 x i32], [5 x i32]* @"lista", i32 0, i32 %".85"
  %".87" = load i32, i32* %".86"
  %".88" = getelementptr [5 x i32], [5 x i32]* @"lista", i32 0, i32 %".84"
  store i32 %".87", i32* %".88"
  %".90" = load i32, i32* @"high"
  %".91" = load i32, i32* @"temp2"
  %".92" = getelementptr [5 x i32], [5 x i32]* @"lista", i32 0, i32 %".90"
  store i32 %".91", i32* %".92"
  %".94" = load i32, i32* @"i"
  %".95" = add i32 %".94", 1
  store i32 %".95", i32* @"pivote_idx"
  %".97" = load i32, i32* @"pivote_idx"
  %".98" = load i32, i32* @"low"
  %".99" = add i32 %".98", 1
  %".100" = icmp sgt i32 %".97", %".99"
  br i1 %".100", label %"then.1", label %"ifcont.1"
then:
  %".57" = load i32, i32* @"i"
  %".58" = add i32 %".57", 1
  store i32 %".58", i32* @"i"
  %".60" = load i32, i32* @"i"
  %".61" = getelementptr [5 x i32], [5 x i32]* @"lista", i32 0, i32 %".60"
  %".62" = load i32, i32* %".61"
  store i32 %".62", i32* @"temp1"
  %".64" = load i32, i32* @"i"
  %".65" = load i32, i32* @"j"
  %".66" = getelementptr [5 x i32], [5 x i32]* @"lista", i32 0, i32 %".65"
  %".67" = load i32, i32* %".66"
  %".68" = getelementptr [5 x i32], [5 x i32]* @"lista", i32 0, i32 %".64"
  store i32 %".67", i32* %".68"
  %".70" = load i32, i32* @"j"
  %".71" = load i32, i32* @"temp1"
  %".72" = getelementptr [5 x i32], [5 x i32]* @"lista", i32 0, i32 %".70"
  store i32 %".71", i32* %".72"
  br label %"ifcont"
ifcont:
  %".75" = add i32 %".48", 1
  store i32 %".75", i32* @"j"
  br label %"cond"
then.1:
  %".102" = load i32, i32* @"top"
  %".103" = load i32, i32* @"low"
  %".104" = getelementptr [20 x i32], [20 x i32]* @"pila", i32 0, i32 %".102"
  store i32 %".103", i32* %".104"
  %".106" = load i32, i32* @"top"
  %".107" = add i32 %".106", 1
  store i32 %".107", i32* @"top"
  %".109" = load i32, i32* @"top"
  %".110" = load i32, i32* @"pivote_idx"
  %".111" = sub i32 %".110", 1
  %".112" = getelementptr [20 x i32], [20 x i32]* @"pila", i32 0, i32 %".109"
  store i32 %".111", i32* %".112"
  %".114" = load i32, i32* @"top"
  %".115" = add i32 %".114", 1
  store i32 %".115", i32* @"top"
  br label %"ifcont.1"
ifcont.1:
  %".118" = load i32, i32* @"pivote_idx"
  %".119" = add i32 %".118", 1
  %".120" = load i32, i32* @"high"
  %".121" = icmp slt i32 %".119", %".120"
  br i1 %".121", label %"then.2", label %"ifcont.2"
then.2:
  %".123" = load i32, i32* @"top"
  %".124" = load i32, i32* @"pivote_idx"
  %".125" = add i32 %".124", 1
  %".126" = getelementptr [20 x i32], [20 x i32]* @"pila", i32 0, i32 %".123"
  store i32 %".125", i32* %".126"
  %".128" = load i32, i32* @"top"
  %".129" = add i32 %".128", 1
  store i32 %".129", i32* @"top"
  %".131" = load i32, i32* @"top"
  %".132" = load i32, i32* @"high"
  %".133" = getelementptr [20 x i32], [20 x i32]* @"pila", i32 0, i32 %".131"
  store i32 %".132", i32* %".133"
  %".135" = load i32, i32* @"top"
  %".136" = add i32 %".135", 1
  store i32 %".136", i32* @"top"
  br label %"ifcont.2"
ifcont.2:
  br label %"cond_block"
cond.1:
  %".144" = load i32, i32* @"k"
  %".145" = icmp sle i32 %".144", %".141"
  br i1 %".145", label %"loop.2", label %"afterloop.2"
loop.2:
  %".147" = load i32, i32* @"k"
  %".148" = getelementptr [5 x i32], [5 x i32]* @"lista", i32 0, i32 %".147"
  %".149" = load i32, i32* %".148"
  %".150" = bitcast [4 x i8]* @"fstr0" to i8*
  %".151" = call i32 (i8*, ...) @"printf"(i8* %".150", i32 %".149")
  %".152" = add i32 %".144", 1
  store i32 %".152", i32* @"k"
  br label %"cond.1"
afterloop.2:
  ret void
}

declare i32 @"printf"(i8* %".1", ...)

@"lista" = internal global [5 x i32] [i32 5, i32 3, i32 8, i32 4, i32 2]
@"n" = internal global i32 0
@"pila" = internal global [20 x i32] [i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0]
@"top" = internal global i32 0
@"high" = internal global i32 0
@"low" = internal global i32 0
@"pivote" = internal global i32 0
@"i" = internal global i32 0
@"j" = global i32 0
@"temp1" = internal global i32 0
@"temp2" = internal global i32 0
@"pivote_idx" = internal global i32 0
@"k" = global i32 0
@"fstr0" = internal constant [4 x i8] c"%i\0a\00"