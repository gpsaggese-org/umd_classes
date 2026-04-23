/usr/bin/osascript << EOF
set theFile to POSIX file "msml610/lectures/Lesson08.4.pdf" as alias
tell application "Skim"
activate
set theDocs to get documents whose path is (get POSIX path of theFile)
if (count of theDocs) > 0 then revert theDocs
open theFile
end tell
EOF
