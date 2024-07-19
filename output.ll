; ModuleID = "S:\Hackatones\Primer Hackaton Código Facilito\CoCody-Compiler\codegen.py"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

define void @"main"()
{
entry:
  store i32 10, i32* @"n"
  store i32 7, i32* @"clave"
  store i32 0, i32* @"inicio"
  %".5" = load i32, i32* @"n"
  store i32 %".5", i32* @"fin"
  store i32 0, i32* @"encontrado"
  br label %"cond_block"
cond_block:
  %".9" = load i32, i32* @"inicio"
  %".10" = load i32, i32* @"fin"
  %".11" = icmp slt i32 %".9", %".10"
  br i1 %".11", label %"loop", label %"afterloop"
loop:
  %".13" = load i32, i32* @"encontrado"
  %".14" = icmp eq i32 %".13", 0
  br i1 %".14", label %"then", label %"endif"
afterloop:
  %".58" = load i32, i32* @"encontrado"
  %".59" = icmp eq i32 %".58", 1
  br i1 %".59", label %"then.6", label %"endif.6"
then:
  %".16" = load i32, i32* @"inicio"
  %".17" = load i32, i32* @"fin"
  %".18" = add i32 %".16", %".17"
  %".19" = sdiv i32 %".18", 2
  store i32 %".19", i32* @"mid"
  %".21" = load i32, i32* @"mid"
  %".22" = getelementptr [10 x i32], [10 x i32]* @"lista", i32 0, i32 %".21"
  %".23" = load i32, i32* %".22"
  %".24" = load i32, i32* @"clave"
  %".25" = icmp eq i32 %".23", %".24"
  br i1 %".25", label %"then.1", label %"endif.1"
endif:
  br label %"cond_block"
then.1:
  store i32 1, i32* @"encontrado"
  br label %"endif.1"
endif.1:
  %".29" = load i32, i32* @"mid"
  %".30" = getelementptr [10 x i32], [10 x i32]* @"lista", i32 0, i32 %".29"
  %".31" = load i32, i32* %".30"
  %".32" = load i32, i32* @"clave"
  %".33" = icmp slt i32 %".31", %".32"
  br i1 %".33", label %"then.2", label %"endif.2"
then.2:
  %".35" = load i32, i32* @"encontrado"
  %".36" = icmp eq i32 %".35", 0
  br i1 %".36", label %"then.3", label %"endif.3"
endif.2:
  %".43" = load i32, i32* @"mid"
  %".44" = getelementptr [10 x i32], [10 x i32]* @"lista", i32 0, i32 %".43"
  %".45" = load i32, i32* %".44"
  %".46" = load i32, i32* @"clave"
  %".47" = icmp sgt i32 %".45", %".46"
  br i1 %".47", label %"then.4", label %"endif.4"
then.3:
  %".38" = load i32, i32* @"mid"
  %".39" = add i32 %".38", 1
  store i32 %".39", i32* @"inicio"
  br label %"endif.3"
endif.3:
  br label %"endif.2"
then.4:
  %".49" = load i32, i32* @"encontrado"
  %".50" = icmp eq i32 %".49", 0
  br i1 %".50", label %"then.5", label %"endif.5"
endif.4:
  br label %"endif"
then.5:
  %".52" = load i32, i32* @"mid"
  store i32 %".52", i32* @"fin"
  br label %"endif.5"
endif.5:
  br label %"endif.4"
then.6:
  %".61" = bitcast [20 x i8]* @"str0" to i8*
  %".62" = bitcast [5 x i8]* @"fstr1" to i8*
  %".63" = call i32 (i8*, ...) @"printf"(i8* %".62", i8* %".61")
  br label %"endif.6"
endif.6:
  ret void
}

declare i32 @"printf"(i8* %".1", ...)

@"lista" = internal global [10 x i32] [i32 1, i32 2, i32 3, i32 4, i32 5, i32 6, i32 7, i32 8, i32 9, i32 10]
@"n" = internal global i32 0
@"clave" = internal global i32 0
@"inicio" = internal global i32 0
@"fin" = internal global i32 0
@"encontrado" = internal global i32 0
@"mid" = internal global i32 0
@"str0" = internal constant [20 x i8] c"Elemento encontrado\00"
@"fstr1" = internal constant [5 x i8] c"%s \0a\00"