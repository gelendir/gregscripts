#!/usr/bin/env ruby
pre = false
#Skip zim header
4.times { STDIN.readline }
STDIN.readlines.each do |l| 
    #Preformat block
    if pre
      l = '}}}' and pre = false if l.strip =~ /^'''$/
    #End of preformat block
    elsif l.strip =~ /^'''$/
      l = '{{{'
      pre = true
    #If line isn't in a preformat block and isn't empty, transform it
    elsif l.strip != ""
      #Heading
      l = l.gsub(/(=+)\s*([^=]+)\s*=+/) { |m| "#{'='*(7-$1.length)} #{$2.strip} #{'='*(7-$1.length)}" }
      #Images : Haven't found out ow to put images in moinmoin yet
      #l = l.gsub(/\{\{(\S+)\}\}/, "[[Image:\\1]]")
      #Links
      l = l.gsub(/\[\[(.+)(|(.+))\]\]/, "[\\1|\\2]")
      #Bold
      l = l.gsub(/\*\*(.+)\*\*/, "'''\\1'''")
      #Italic
      l = l.gsub(/\/\/(.+)\/\//, "''\\1''")
      #Bullets
      l = l.gsub(/^(\s*)\*(?=.+)/) { |m| " "*($1.length+1) + "* " }
    end
  puts l
end

