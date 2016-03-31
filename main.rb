#! /usr/bin/env ruby
def htmlBase64Img(file)
    <<EOS
Content-type: text/html

<!DOCTYPE html>
<img src="data:image/png;base64,#{File.read(file)}">
EOS
end

def inc
  $stdin.readchar
end

begin
  unless "G" == inc && "E" == inc && "T" == inc && " " == inc
    throw "cought"
  end
  
  if "/" == inc && " " == inc
    puts "HTTP/1.0 200 OK"
    puts htmlBase64Img("base64/index")
  else
    puts "HTTP/1.0 404 Not Found"
    puts htmlBase64Img("base64/404")
  end
rescue => e
  puts "HTTP/1.0 400 Bad Request"
  puts htmlBase64Img("base64/400")
end
