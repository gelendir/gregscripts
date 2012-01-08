#!/usr/bin/ruby

STDIN.readlines.each do |l| 
  puts l.gsub(/(=+)\s*([^=]+)\s*=+/, "\\1 \\2 \\1").
  gsub(/<br *\/>/, "[[BR]]").gsub("<pre>", "{{{\n").
  gsub(/< *\/pre>/, "}}}\n").
  gsub(/^\s?\*(\**)\s*/) { |m| " *"+" "*($1.length+1) }.
  gsub(/\[\[Image:(\S+)\]\]/, "[[Image(\\1)]]") }
end

