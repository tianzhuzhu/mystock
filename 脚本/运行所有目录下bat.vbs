set fso=CreateObject("Scripting.FileSystemObject")
set fs=fso.getfolder("C:\project\my").files
for each f in fs
Set shell = Wscript.createobject("wscript.shell")
a = shell.run (f,0)
next