; For use with ARMIPS
; 2021/07/18
; For Explorers of Sky All Versions
; ------------------------------------------------------------------------------
; Useless Thing
; ------------------------------------------------------------------------------

.org HookInterrupt1
.area 0x4
	blt CheckDungeonInterrupt
EndExecution:
.endarea

.org HookInterrupt2
.area 0x4
	bl CheckEndDungeon
.endarea

.org HookInterrupt3
.area 0x4
	bl FillIfNotInterrupted
.endarea

